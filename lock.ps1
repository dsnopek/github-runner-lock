
& python "$PSScriptRoot\locker.py" lock
$exitCode = $LASTEXITCODE

if ($exitCode -ne 0) {
    Write-Error "Failed to lock GitHub Actions runner."
    Exit $exitCode
}
