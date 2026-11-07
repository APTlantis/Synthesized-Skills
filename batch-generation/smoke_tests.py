"""Disposable local tool fixtures, separate from unexecuted agent trials.

Python 3.11+; Pillow needed for pixel assertions. Optional tools skip when absent.
Writes small evidence files under batch-generation/evidence; temporary inputs are
owned by TemporaryDirectory. Never installs tools, signs, publishes or touches a
production app/database. Run: python batch-generation/smoke_tests.py
"""
from pathlib import Path
import argparse
import base64
import csv
import hashlib
import http.server
import importlib.util
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
import tomllib
import urllib.error
import urllib.request
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
EVIDENCE = ROOT / 'batch-generation/evidence'
RESULTS = []
STEPS = []


class Missing(Exception):
    pass


def run(argv, cwd, ok=True, timeout=60):
    executable = shutil.which(str(argv[0]))
    if executable is None:
        raise Missing(f'{argv[0]} not on PATH')
    start = time.perf_counter()
    process = subprocess.run([executable, *map(str, argv[1:])], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
    STEPS.append(dict(argv=list(map(str, argv)), exit=process.returncode, seconds=round(time.perf_counter()-start, 3), stdout=process.stdout[-5000:], stderr=process.stderr[-5000:]))
    if ok and process.returncode:
        raise AssertionError(f'{argv[0]} exit {process.returncode}: {process.stderr[-1200:]}')
    return process


def case(name, skill, function, work):
    start_step = len(STEPS)
    start = time.perf_counter()
    folder = work / name
    folder.mkdir()
    try:
        detail = function(folder)
        result = dict(name=name, skill=skill, status='pass', detail=detail)
    except Missing as exc:
        result = dict(name=name, skill=skill, status='skip', reason=str(exc))
    except Exception as exc:
        result = dict(name=name, skill=skill, status='fail', reason=f'{type(exc).__name__}: {exc}')
    result.update(seconds=round(time.perf_counter()-start, 3), steps=STEPS[start_step:])
    RESULTS.append(result)
    print(f'{name}: {result["status"]}', flush=True)


def probe(path, work):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', path], work).stdout)


def media(work):
    source = work / 'source [x] & space.mkv'
    run(['ffmpeg', '-n', '-v', 'error', '-f', 'lavfi', '-i', 'testsrc2=size=160x120:rate=10', '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000', '-t', '1', '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'ffv1', '-c:a', 'pcm_s16le', '-metadata', 'title=Skill Fixture', source], work)
    before = probe(source, work)
    copied = work / 'copy.mkv'
    run(['ffmpeg', '-n', '-v', 'error', '-i', source, '-map', '0:v:0', '-map', '0:a?', '-c', 'copy', '-map_metadata', '0', copied], work)
    after = probe(copied, work)
    assert [s['codec_name'] for s in before['streams']] == [s['codec_name'] for s in after['streams']]
    assert after['format']['tags']['title'] == 'Skill Fixture'
    assert abs(float(after['format']['duration']) - 1) < 0.15
    video = work / 'scaled.mp4'
    run(['ffmpeg', '-n', '-v', 'error', '-i', source, '-filter_complex', '[0:v:0]scale=80:60[v]', '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', video], work)
    info = probe(video, work)
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    assert (v['width'], v['height'], v['codec_name']) == (80, 60, 'h264')
    assert next(s for s in info['streams'] if s['codec_type'] == 'audio')['codec_name'] == 'aac'
    run(['ffmpeg', '-v', 'error', '-i', video, '-map', '0:v?', '-map', '0:a?', '-f', 'null', '-'], work)
    run(['ffmpeg', '-n', '-v', 'error', '-i', source, '-vn', '-c:a', 'flac', work/'audio.flac'], work)
    assert probe(work/'audio.flac', work)['streams'][0]['codec_name'] == 'flac'
    failure = run(['ffmpeg', '-n', '-v', 'error', '-i', source, '-an', '-c:v', 'no_such_encoder_fixture', work/'bad.mkv'], work, ok=False)
    assert failure.returncode != 0 and 'encoder' in failure.stderr.lower()
    run(['ffmpeg', '-hide_banner', '-h', 'filter=scale'], work)
    run(['ffprobe', '-h'], work)
    return dict(streams=2, metadata=after['format']['tags']['title'], scaled=[80,60], decoded=True, unsupported_encoder_rejected=True, hardware='not exercised', perceptual_review='not performed')


def documents(work):
    from PIL import Image
    Image.new('RGB', (8, 8), 'green').save(work/'pixel.png')
    md = '''---\ntitle: Fixture Title\nlang: en\n---\n\n# Sample Heading\n\nA paragraph with **bold**.\n\n| Key | Value |\n|---|---|\n| ID | 0007 |\n\n```python\nprint("a&b")\n```\n\n![Green square](pixel.png)\n'''
    (work/'source.md').write_text(md, encoding='utf-8')
    run(['pandoc', 'source.md', '-f', 'markdown', '-t', 'html5', '-s', '-o', 'page.html'], work)
    html = (work/'page.html').read_text()
    assert '<title>Fixture Title</title>' in html and '<table>' in html and 'pixel.png' in html and '0007' in html
    run(['pandoc', 'source.md', '-f', 'markdown', '-t', 'docx', '-o', 'document.docx'], work)
    with zipfile.ZipFile(work/'document.docx') as archive:
        xml = archive.read('word/document.xml')
        ET.fromstring(xml)
        assert b'Sample Heading' in xml and b'0007' in xml and b'<w:tbl>' in xml
        assert any(n.startswith('word/media/') for n in archive.namelist())
    run(['pandoc', 'document.docx', '-f', 'docx', '-t', 'markdown', '--extract-media=extracted', '-o', 'roundtrip.md'], work)
    text = (work/'roundtrip.md').read_text()
    assert 'Sample Heading' in text and '0007' in text and 'print(' in text and list((work/'extracted').rglob('*.png'))
    (work/'heading.lua').write_text('function Header(el) el.content:insert(1, pandoc.Str("Section: ")); return el end\n')
    (work/'template.html').write_text('<!doctype html><html><head><title>$title$</title></head><body>$body$</body></html>')
    run(['pandoc', 'source.md', '-s', '--template=template.html', '--lua-filter=heading.lua', '-o', 'filtered.html'], work)
    filtered = (work/'filtered.html').read_text()
    assert 'Section: Sample Heading' in filtered and '<title>Fixture Title</title>' in filtered
    inputs = run(['pandoc', '--list-input-formats'], work).stdout.split()
    outputs = run(['pandoc', '--list-output-formats'], work).stdout.split()
    if 'asciidoc' in inputs:
        (work/'source.adoc').write_text('= AsciiDoc fixture\n\n== Native heading\n\nA paragraph.\n')
        run(['pandoc','source.adoc','-f','asciidoc','-t','html5','-o','asciidoc.html'],work)
        assert 'Native heading' in (work/'asciidoc.html').read_text()
    return dict(html=True, docx_structure_and_image=True, roundtrip=True, lua_template=True, asciidoc_reader='asciidoc' in inputs, native_asciidoc_conversion='asciidoc' in inputs, asciidoc_writer='asciidoc' in outputs, visual_docx_review='not performed')


def pdf_route(work):
    if not shutil.which('xelatex'):
        raise Missing('XeLaTeX missing')
    (work/'source.md').write_text('# PDF fixture\n\nUnicode: café.\n')
    run(['pandoc', 'source.md', '--pdf-engine=xelatex', '-o', 'output.pdf'], work)
    assert (work/'output.pdf').read_bytes().startswith(b'%PDF-')
    return 'PDF file header checked; layout/rendering not inspected'


def images(work):
    from PIL import Image
    run(['magick', '-size', '40x20', 'xc:blue', 'base.png'], work)
    run(['magick', 'base.png', '-resize', '16x16>', 'fit.png'], work)
    run(['magick', 'base.png', '-crop', '10x8+2+3', '+repage', 'crop.png'], work)
    assert Image.open(work/'fit.png').size == (16,8)
    assert Image.open(work/'crop.png').size == (10,8)
    run(['magick', '-size', '40x20', 'xc:rgba(255,0,0,0.5)', 'overlay.png'], work)
    run(['magick', 'base.png', 'overlay.png', '-compose', 'Over', '-composite', 'composite.png'], work)
    px = Image.open(work/'composite.png').convert('RGB').getpixel((0,0))
    assert abs(px[0]-128) <= 1 and px[1] == 0 and abs(px[2]-127) <= 1, px
    run(['magick', 'base.png', '-colorspace', 'Gray', 'gray.png'], work)
    gray = run(['magick', 'identify', '-format', '%[colorspace]', 'gray.png'], work).stdout
    assert 'gray' in gray.lower()
    run(['magick', '-size', '40x20', 'gradient:red-blue', '-colors', '8', 'palette.png'], work)
    palette = Image.open(work/'palette.png').convert('RGB')
    assert len(palette.getcolors(1000)) <= 8
    hist = run(['magick', 'palette.png', '-format', '%c', 'histogram:info:'], work).stdout
    assert sum(int(n) for n in re.findall(r'^\s*(\d+):', hist, re.M)) == 800
    hashes = []
    for number in (1,2):
        dest = f'repeat-{number}.png'
        run(['magick', 'base.png', '-resize', '20x10', '-strip', '-define', 'png:exclude-chunks=date,time', dest], work)
        hashes.append(hashlib.sha256((work/dest).read_bytes()).hexdigest())
    assert hashes[0] == hashes[1], hashes
    Image.open(work/'composite.png').save(EVIDENCE/'alpha-composite.png')
    return dict(fit=[16,8], crop=[10,8], composite_rgb=px, gray=gray, palette_colors=len(palette.getcolors(1000)), repeated_file_hash=hashes[0], icc='not exercised')


def powershell(work):
    script = ROOT/'batch-generation/automation.Tests.ps1'
    invocation = "param($testFile,$fixture) Import-Module Pester -RequiredVersion 3.4.0 -ErrorAction Stop; $r = Invoke-Pester -Script @{Path=$testFile;Parameters=@{FixtureRoot=$fixture}} -PassThru; if ($r.FailedCount -gt 0 -or $r.PassedCount -ne 5) { exit 1 }"
    # File wrapper avoids Windows command string interpolation of paths.
    wrapper = work/'run.ps1'
    wrapper.write_text(invocation, encoding='utf-8')
    result = run(['pwsh', '-NoProfile', '-File', wrapper, script, work], work)
    assert '5' in result.stdout
    return '5 Pester 3.4 tests passed on PowerShell 7; ScriptAnalyzer and Linux untested'


def graph(work):
    source = 'digraph delivery { rankdir=LR; source [label="Editable source"]; render [label="Render and inspect"]; source -> render -> artifact; }'
    (work/'workflow.dot').write_text(source)
    run(['dot', '-Tsvg', 'workflow.dot', '-o', 'workflow.svg'], work)
    tree = ET.parse(work/'workflow.svg')
    ns = {'s':'http://www.w3.org/2000/svg'}
    nodes = [g for g in tree.findall('.//s:g', ns) if g.attrib.get('class') == 'node']
    edges = [g for g in tree.findall('.//s:g', ns) if g.attrib.get('class') == 'edge']
    assert len(nodes) == 3 and len(edges) == 2
    run(['dot', '-Tpng', 'workflow.dot', '-o', EVIDENCE/'graph.png'], work)
    shutil.copyfile(work/'workflow.dot', EVIDENCE/'workflow.dot')
    shutil.copyfile(work/'workflow.svg', EVIDENCE/'workflow.svg')
    (EVIDENCE/'graph-description.txt').write_text('Editable source flows to Render and inspect, which produces artifact. Three nodes and two directed edges.\n')
    return 'DOT rendered to SVG/PNG; 3 nodes, 2 edges asserted; visual inspection recorded separately'


def site(work):
    p = run(['python', '-m', 'mkdocs', '--version'], work, ok=False)
    if p.returncode:
        raise Missing('MkDocs Python module unavailable; no site production build executed')
    (work/'docs/assets').mkdir(parents=True)
    from PIL import Image
    Image.new('RGB',(8,8),'blue').save(work/'docs/assets/pixel.png')
    (work/'mkdocs.yml').write_text('site_name: Fixture Docs\nnav:\n  - Home: index.md\n  - Guide: guide.md\nplugins:\n  - search\n')
    (work/'docs/index.md').write_text('# Home\n\n[Guide](guide.md)\n\n![pixel](assets/pixel.png)\n')
    (work/'docs/guide.md').write_text('# Guide\n\n```python\nprint("hello")\n```\n\n[Home](index.md)\n')
    run(['python','-m','mkdocs','build','--strict'],work)
    assert (work/'site/guide/index.html').exists() and (work/'site/search/search_index.json').exists()
    return 'MkDocs production fixture built; browser behavior not tested'


def sqlite_case(work):
    db = sqlite3.connect(work/'fixture.sqlite')
    db.execute('PRAGMA foreign_keys=ON')
    db.executescript("CREATE TABLE parent(id INTEGER PRIMARY KEY); CREATE TABLE item(id INTEGER PRIMARY KEY, code TEXT UNIQUE NOT NULL, amount INTEGER NOT NULL, parent INTEGER REFERENCES parent(id)); INSERT INTO parent VALUES(1); INSERT INTO item VALUES(1,'0007',12,1);")
    db.commit()
    try:
        db.execute("INSERT INTO item VALUES(2,'bad',1,99)")
    except sqlite3.IntegrityError:
        db.rollback()
    else:
        raise AssertionError('Foreign key not enforced')
    db.execute('BEGIN')
    db.execute("INSERT INTO item VALUES(2,'0008',3,1)")
    db.rollback()
    assert db.execute('SELECT COUNT(*) FROM item').fetchone()[0] == 1
    plan = db.execute("EXPLAIN QUERY PLAN SELECT * FROM item WHERE code='0007'").fetchall()
    assert any('INDEX' in row[-1] for row in plan)
    db.execute('ALTER TABLE item ADD COLUMN note TEXT')
    db.execute('PRAGMA user_version=1')
    db.commit()
    db.execute("INSERT INTO item(id,code,amount,parent) VALUES(1,'0007',12,1) ON CONFLICT(code) DO UPDATE SET amount=excluded.amount")
    db.commit()
    assert db.execute('SELECT COUNT(*) FROM item').fetchone()[0] == 1
    backup = sqlite3.connect(work/'backup.sqlite')
    db.backup(backup)
    assert backup.execute('SELECT code,amount FROM item').fetchall() == [('0007',12)]
    assert backup.execute('PRAGMA user_version').fetchone()[0] == 1
    assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    assert not db.execute('PRAGMA foreign_key_check').fetchall()
    with (work/'export.csv').open('w',newline='') as f:
        csv.writer(f).writerows(db.execute('SELECT code,amount FROM item'))
    with (work/'export.csv').open(newline='') as f:
        assert list(csv.reader(f)) == [['0007','12']]
    backup.close(); db.close()
    return dict(sqlite=sqlite3.sqlite_version, foreign_keys=True, rollback=True, indexed_lookup=True, migration=True, idempotent_upsert=True, backup_restore=True, csv=True)


def duckdb_case(work):
    (work/'fixture.csv').write_text('code,amount\n0007,12\n0008,3\n0007,12\n')
    sql = """CREATE TABLE staged AS SELECT * FROM read_csv('fixture.csv', header=true, all_varchar=true);
CREATE TABLE clean AS SELECT DISTINCT code, CAST(amount AS INTEGER) amount FROM staged;
BEGIN; INSERT INTO clean VALUES('rollback', 99); ROLLBACK;
COPY (SELECT * FROM clean ORDER BY code) TO 'roundtrip.parquet' (FORMAT PARQUET);
SELECT count(*) AS row_count, sum(amount) AS total, min(code) AS first_code FROM read_parquet('roundtrip.parquet');"""
    result = run(['duckdb','fixture.duckdb','-json','-c',sql],work)
    rows = json.loads(result.stdout)
    assert len(rows)==1 and rows[0]['row_count']==2 and int(rows[0]['total'])==15 and rows[0]['first_code']=='0007',rows
    reopen = run(['duckdb','fixture.duckdb','-json','-c','SELECT COUNT(*) AS n FROM clean;'],work)
    assert json.loads(reopen.stdout) == [{'n':2}]
    return dict(rows=2,total=15,first_code='0007', rollback=True, dedup='exact row fixture only', parquet_roundtrip=True,reopen=True)


def archaeology(work):
    (work/'src').mkdir()
    (work/'package.json').write_text('{"scripts":{"start":"node src/main.js"}}')
    (work/'README.md').write_text('Entry point: legacy.js\n')
    (work/'src/main.js').write_text("const service = require('./service'); console.log(service.read());\n")
    (work/'src/service.js').write_text("exports.read = () => require('../data.json').value;\n")
    (work/'data.json').write_text('{"value":7}')
    run(['git','init','-q'],work)
    before = {str(p.relative_to(work)):hashlib.sha256(p.read_bytes()).hexdigest() for p in work.rglob('*') if p.is_file() and '.git' not in p.parts}
    run(['git','status','--short'],work)
    files = run(['rg','--files','-g','!.git'],work).stdout
    hits = run(['rg','-n','service|legacy|src/main','src','README.md','package.json'],work).stdout
    assert 'src/main.js' in hits and 'legacy.js' in hits and 'service' in hits
    assert 'data.json' in files
    after = {str(p.relative_to(work)):hashlib.sha256(p.read_bytes()).hexdigest() for p in work.rglob('*') if p.is_file() and '.git' not in p.parts}
    assert before == after
    return 'Fixture inventory/import chain/stale README exposed by read-only searches; source hashes unchanged. Agent reconstruction not evaluated.'


def receipt(work):
    payload = work/'fixture.bin'
    payload.write_bytes(b'disposable receipt fixture; not an installer')
    digest = hashlib.sha256(payload.read_bytes()).hexdigest()
    text = f'version = "1.2.3"\n[[artifacts]]\npath = "fixture.bin"\nsha256 = "{digest}"\nsigning = "unsigned"\ninstallation_test = "not-run"\n'
    (work/'receipt.toml').write_text(text)
    data = tomllib.loads(text)
    assert hashlib.sha256((work/data['artifacts'][0]['path']).read_bytes()).hexdigest() == data['artifacts'][0]['sha256']
    payload.write_bytes(b'changed')
    assert hashlib.sha256(payload.read_bytes()).hexdigest() != digest
    return 'Receipt TOML roundtrip and checksum mismatch detection only; no installer built, signed or installed'


def retrieval(work):
    db = sqlite3.connect(':memory:')
    db.execute('CREATE VIRTUAL TABLE passage USING fts5(id UNINDEXED, body)')
    db.executemany('INSERT INTO passage VALUES(?,?)',[('a','Aster stores backups locally.'),('b','Birch displays charts.'),('c','Cedar runs an unrelated service.')])
    ranked = db.execute("SELECT id FROM passage WHERE passage MATCH ? ORDER BY rank",('backups',)).fetchall()
    ids = [x[0] for x in ranked]
    assert ids[0] == 'a'
    recall = len(set(ids[:3]) & {'a'}) / 1
    mrr = 1/(ids.index('a')+1)
    assert recall == 1 and mrr == 1
    assert db.execute("SELECT id FROM passage WHERE passage MATCH ?",('unknownterm',)).fetchall() == []
    db.execute("UPDATE passage SET body='Aster stores encrypted snapshots.' WHERE id='a'")
    assert not db.execute("SELECT id FROM passage WHERE passage MATCH 'backups'").fetchall()
    db.execute("DELETE FROM passage WHERE id='a'")
    assert not db.execute("SELECT id FROM passage WHERE passage MATCH 'snapshots'").fetchall()
    contract = dict(model='fixture-v1', dimension=3)
    incoming = dict(model='fixture-v2', dimension=3)
    assert contract != incoming  # equal dimensions do not establish compatibility
    assert len([0.1,0.2]) != contract['dimension']
    db.close()
    return dict(baseline='SQLite FTS5; no embeddings or generation',recall_at_3=recall,mrr=mrr,corpus_passages=3,judged_queries=1,no_match=True,update_delete=True,dimension_contract_fixture=True,citations_and_model_abstention='not evaluated')


def ollama_probe(work):
    try:
        with urllib.request.urlopen('http://127.0.0.1:11434/api/tags', timeout=3) as response:
            data=json.load(response)
        return dict(models=len(data.get('models',[])), inference='not requested')
    except urllib.error.URLError as exc:
        raise Missing(f'Local Ollama server unavailable: {exc.reason}; no download or inference attempted')


def ingestion(work):
    spec = importlib.util.spec_from_file_location('url_scope', ROOT/'documentation-ingestion-mirroring/scripts/url_scope.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    scope = 'https://docs.example.test/guide/'
    allowed = ['https://docs.example.test/guide/', 'https://DOCS.example.test:443/guide/a?q=1#part', 'https://docs.example.test/guide']
    rejected = ['https://docs.example.test.evil/guide/a','https://docs.example.test/guidebook/a','http://docs.example.test/guide/a','https://user@docs.example.test/guide/a','https://docs.example.test/guide/../secret','https://docs.example.test/guide/%2e%2e/secret','https://docs.example.test/guide/a%2fb','https://docs.example.test/guide/%252e%252e/secret','https://docs.example.test/guide/a\\b']
    assert all(module.check_url(x,scope)['allowed'] for x in allowed)
    assert all(not module.check_url(x,scope)['allowed'] for x in rejected)
    hits=[]
    body=b'# Home\n\n[Next](next.md#part)\n\n![pixel](assets/pixel.png)\n\n```text\nhttps://outside.invalid/leave\n```\n'
    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self,*args):
            pass
        def do_GET(self):
            hits.append(self.path)
            if self.path == '/guide/redirect':
                self.send_response(302); self.send_header('Location','/outside'); self.end_headers(); return
            if self.path == '/guide/index.md' and self.headers.get('If-None-Match') == '"v1"':
                self.send_response(304); self.end_headers(); return
            content = {'/guide/index.md':body,'/guide/next.md':b'# Part\n\n[Home](index.md)\n','/guide/assets/pixel.png':base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=')}.get(self.path)
            if content is None:
                self.send_response(404); self.end_headers(); return
            self.send_response(200); self.send_header('ETag','"v1"'); self.end_headers(); self.wfile.write(content)
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
    origin=f'http://127.0.0.1:{server.server_port}'
    local_scope=origin+'/guide/'
    class ScopedRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,req,fp,code,msg,headers,newurl):
            if not module.check_url(newurl,local_scope)['allowed']:
                raise ValueError('Redirect escaped scope')
            return super().redirect_request(req,fp,code,msg,headers,newurl)
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),ScopedRedirect())
    try:
        url=origin+'/guide/index.md'
        with opener.open(url,timeout=3) as response:
            captured=response.read(); etag=response.headers['ETag']
        try:
            opener.open(urllib.request.Request(url,headers={'If-None-Match':etag}),timeout=3)
        except urllib.error.HTTPError as exc:
            assert exc.code==304
            reused=captured
        else:
            raise AssertionError('Expected 304')
        assert reused==body
        try:
            opener.open(origin+'/guide/redirect',timeout=3)
        except ValueError:
            pass
        else:
            raise AssertionError('Redirect escape allowed')
        assert '/outside' not in hits
        (work/'source.md').write_bytes(captured)
        astfile=work/'ast.json'
        run(['pandoc','source.md','-f','commonmark','-t','json','-o',astfile],work)
        ast=json.loads(astfile.read_text())
        seen=[]
        def walk(value):
            if isinstance(value,dict):
                if value.get('t') in ('Link','Image'):
                    target=value['c'][-1][0]
                    destination=urljoin(url,target)
                    assert module.check_url(destination,local_scope)['allowed']
                    seen.append(target)
                for v in value.values(): walk(v)
            elif isinstance(value,list):
                for v in value: walk(v)
        walk(ast)
        assert seen==['next.md#part','assets/pixel.png']
        for path in ('next.md','assets/pixel.png'):
            destination=work/path; destination.parent.mkdir(exist_ok=True)
            with opener.open(urljoin(url,path),timeout=3) as response: destination.write_bytes(response.read())
        run(['pandoc',astfile,'-f','json','-t','commonmark','-o','local.md'],work)
        local=(work/'local.md').read_text()
        assert 'https://outside.invalid/leave' in local and (work/'next.md').exists() and (work/'assets/pixel.png').exists()
        frontmatter='title: "Fixture: Home"\nsource: '+json.dumps(url)+'\n'
        import yaml
        assert yaml.safe_load(frontmatter)['title']=='Fixture: Home'
        return dict(scope_allowed=len(allowed),scope_rejected=len(rejected),redirect_escape_blocked=True,etag_304_reuse=True,relative_page_asset=True,code_preserved=True,frontmatter=True,full_crawler='not evaluated',siyuan_import='not performed')
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=3)


def live_embeddings(work):
    endpoint='http://127.0.0.1:11434'
    try:
        with urllib.request.urlopen(endpoint+'/api/tags',timeout=3) as response:
            models=json.load(response)['models']
    except urllib.error.URLError as exc:
        raise Missing(f'Ollama unavailable: {exc.reason}')
    model=next((m for m in models if m['name']=='embeddinggemma:latest'),None)
    if model is None:
        raise Missing('Small embedding fixture model is not already installed; no download attempted')
    texts=['Aster stores backups locally.','Birch draws colorful charts.','Cedar manages calendar appointments.','Where does Aster store backups?']
    request=urllib.request.Request(endpoint+'/api/embed',data=json.dumps(dict(model=model['name'],input=texts,truncate=False,keep_alive=0)).encode(),headers={'Content-Type':'application/json'})
    start=time.perf_counter()
    with urllib.request.urlopen(request,timeout=60) as response:
        result=json.load(response)
    elapsed=time.perf_counter()-start
    vectors=result['embeddings']
    import math
    assert len(vectors)==len(texts)
    dims={len(v) for v in vectors}
    assert len(dims)==1 and next(iter(dims))>0
    assert all(math.isfinite(x) for v in vectors for x in v)
    def cosine(a,b):
        return sum(x*y for x,y in zip(a,b))/(math.sqrt(sum(x*x for x in a))*math.sqrt(sum(x*x for x in b)))
    scores=[cosine(v,vectors[-1]) for v in vectors[:-1]]
    assert max(range(3),key=lambda i:scores[i])==0,scores
    return dict(model=model['name'],digest=model.get('digest'),dimension=next(iter(dims)),passages=3,queries=1,top1='Aster',seconds=round(elapsed,3),scores=scores,scope='One synthetic query; no generation, citation entailment, memory benchmark or general relevance claim')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only',nargs='+',help='Rerun named fixtures and merge their evidence with the prior report')
    args=parser.parse_args()
    EVIDENCE.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='agent-skill-fixtures-') as temp:
        work=Path(temp)
        tests=[('media','ffmpeg-media-engineer',media),('documents','pandoc-document-engineer',documents),('pdf-route','pandoc-document-engineer',pdf_route),('images','imagemagick-imaging-engineer',images),('powershell','powershell-automation-engineer',powershell),('graph','visual-engineering-architect',graph),('site','documentation-site-engineer',site),('ingestion','documentation-ingestion-mirroring',ingestion),('sqlite','duckdb-sqlite-data-engineer',sqlite_case),('duckdb','duckdb-sqlite-data-engineer',duckdb_case),('archaeology','repository-archaeologist',archaeology),('receipt','desktop-release-installer-engineer',receipt),('retrieval','local-ai-retrieval-engineer',retrieval),('ollama-probe','local-ai-retrieval-engineer',ollama_probe),('live-embeddings','local-ai-retrieval-engineer',live_embeddings)]
        for name,skill,function in tests:
            if args.only and name not in args.only:
                continue
            case(name,skill,function,work)
    if args.only:
        unknown=set(args.only)-{t[0] for t in tests}
        if unknown:
            parser.error('Unknown fixtures: '+','.join(sorted(unknown)))
        previous=EVIDENCE/'smoke-results.json'
        if previous.exists():
            old=json.loads(previous.read_text())['results']
            replaced={r['name'] for r in RESULTS}
            RESULTS[:]=[r for r in old if r['name'] not in replaced]+RESULTS
    report=dict(scope='Local tool smoke tests; not agent behavior evaluation',results=RESULTS)
    (EVIDENCE/'smoke-results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    summary={s:sum(r['status']==s for r in RESULTS) for s in ('pass','fail','skip')}
    print(json.dumps(summary),flush=True)
    raise SystemExit(summary['fail']>0)


if __name__=='__main__':
    main()
