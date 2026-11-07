# Disposable PowerShell fixture. Compatible with the available Pester 3.x syntax.
param([Parameter(Mandatory)][string]$FixtureRoot)

function Get-CheckedFile {
    [CmdletBinding()]
    param([Parameter(Mandatory, ValueFromPipeline)][ValidateNotNullOrEmpty()][string]$LiteralPath)
    process {
        $item = Get-Item -LiteralPath $LiteralPath -ErrorAction Stop
        if ($item.PSIsContainer) { throw 'Expected a file' }
        [pscustomobject]@{ Path = $item.FullName; Bytes = $item.Length }
    }
}

Describe 'Reusable automation contracts' {
    It 'preserves literal paths and pipeline result cardinality' {
        $paths = @('space name.txt', 'a&b.txt', '[x].txt') | ForEach-Object { Join-Path $FixtureRoot $_ }
        foreach ($path in $paths) { [IO.File]::WriteAllText($path, 'fixture') }
        $items = @($paths | Get-CheckedFile)
        $items.Count | Should Be 3
        $items[2].Path | Should Be (Get-Item -LiteralPath $paths[2]).FullName
        (Split-Path -Leaf $items[2].Path) | Should Be '[x].txt'
        $items[0].Bytes | Should Be 7
    }
    It 'rejects missing and invalid parameters' {
        # Explicit catches avoid the installed legacy Pester 3 Should Throw
        # mismatch observed with PowerShell 7 parameter binding errors.
        $invalidCaught = $false
        try { Get-CheckedFile -LiteralPath '' -ErrorAction Stop }
        catch { $invalidCaught = $_.FullyQualifiedErrorId -like '*Validation*' }
        $invalidCaught | Should Be $true
        $missingCaught = $false
        try { Get-CheckedFile -LiteralPath (Join-Path $FixtureRoot 'missing.txt') -ErrorAction Stop }
        catch [System.Management.Automation.ItemNotFoundException] { $missingCaught = $true }
        $missingCaught | Should Be $true
    }
    It 'passes exact native argv including quotes and empty strings' {
        $expected = @('space name', 'a&b', '[x]', '', 'a"b', 'trailing\')
        $nativeArgs = @('-c', 'import sys,json; print(json.dumps(sys.argv[1:]))') + $expected
        $actual = & python @nativeArgs | ConvertFrom-Json
        if ($LASTEXITCODE -ne 0) { throw 'argv fixture failed' }
        ($actual | ConvertTo-Json -Compress) | Should Be ($expected | ConvertTo-Json -Compress)
    }
    It 'detects native nonzero exits explicitly' {
        & python -c 'import sys; sys.exit(7)'
        $nativeCode = $LASTEXITCODE
        $nativeCode | Should Be 7
    }
    It 'keeps an idempotent output unchanged on rerun' {
        $path = Join-Path $FixtureRoot 'idempotent.txt'
        $desired = 'stable content'
        foreach ($iteration in 1..2) {
            if (-not (Test-Path -LiteralPath $path) -or [IO.File]::ReadAllText($path) -ne $desired) {
                [IO.File]::WriteAllText($path, $desired)
            }
            if ($iteration -eq 1) { $first = (Get-FileHash -LiteralPath $path).Hash; $mtime = (Get-Item -LiteralPath $path).LastWriteTimeUtc }
        }
        (Get-FileHash -LiteralPath $path).Hash | Should Be $first
        (Get-Item -LiteralPath $path).LastWriteTimeUtc | Should Be $mtime
    }
}
