"""Conservative HTTP URL scope preflight, not a crawler or network sandbox.

Python 3.11+, standard library. Prints JSON; exit 0 allowed, 2 rejected.
Usage: python url_scope.py --scope https://docs.example/guide/ URL
Recheck each redirect and asset before I/O. DNS/address and robots/license policy
remain the caller's responsibility. This deliberately rejects ambiguous paths.
"""
import argparse
import json
from urllib.parse import unquote, urlsplit, urlunsplit


def _parts(url):
    if not isinstance(url, str) or not url or '\\' in url or any(ord(c) <= 32 or ord(c) == 127 for c in url):
        raise ValueError('Empty URL, whitespace/control character or backslash')
    parsed = urlsplit(url)
    if parsed.scheme.lower() not in ('http', 'https') or not parsed.hostname:
        raise ValueError('Require an absolute HTTP(S) URL')
    if parsed.username is not None or parsed.password is not None:
        raise ValueError('Credentials in URL are not allowed')
    host = parsed.hostname.encode('idna').decode('ascii').lower()
    if '%' in host or host.endswith('.'):
        raise ValueError('Ambiguous hostname spelling')
    port = parsed.port
    scheme = parsed.scheme.lower()
    effective_port = port or (443 if scheme == 'https' else 80)
    if port == 0:
        raise ValueError('Port zero is not allowed')
    path = parsed.path or '/'
    decoded = path
    for _ in range(4):
        next_path = unquote(decoded, errors='strict')
        if next_path == decoded:
            break
        if next_path.count('/') != decoded.count('/'):
            raise ValueError('Encoded path separator')
        decoded = next_path
    if '%' in decoded or '\\' in decoded or any(ord(c) <= 32 or ord(c) == 127 for c in decoded):
        raise ValueError('Ambiguous path encoding')
    if any(segment in ('.', '..') for segment in decoded.split('/')) or '//' in decoded:
        raise ValueError('Dot segments or repeated separators are rejected')
    authority = f'[{host}]' if ':' in host else host
    if effective_port != (443 if scheme == 'https' else 80):
        authority += f':{effective_port}'
    return parsed, (scheme, host, effective_port), decoded, urlunsplit((scheme, authority, path, parsed.query, ''))


def check_url(url, scope):
    try:
        allowed, origin, prefix, _ = _parts(scope)
        if allowed.query or allowed.fragment:
            raise ValueError('Scope must not contain a query or fragment')
        _, candidate_origin, path, normalized = _parts(url)
        prefix = prefix.rstrip('/') or '/'
        if candidate_origin != origin:
            raise ValueError('Origin outside allowed scope')
        if prefix != '/' and path != prefix and not path.startswith(prefix + '/'):
            raise ValueError('Path outside allowed segment prefix')
        return dict(allowed=True, url=normalized)
    except (ValueError, UnicodeError) as exc:
        return dict(allowed=False, reason=str(exc))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', required=True)
    parser.add_argument('url')
    args = parser.parse_args()
    result = check_url(args.url, args.scope)
    print(json.dumps(result))
    raise SystemExit(0 if result['allowed'] else 2)
