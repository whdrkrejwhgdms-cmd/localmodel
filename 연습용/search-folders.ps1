param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Name,

    [string]$Path = (Get-Location).Path
)

if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
    Write-Error "검색할 폴더를 찾을 수 없습니다: $Path"
    exit 1
}

Get-ChildItem -LiteralPath $Path -Directory -Recurse -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -like "*$Name*" } |
    Select-Object -ExpandProperty FullName
