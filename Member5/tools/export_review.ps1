# Export the reviewed presentation and new preparation companion using Office.
$ErrorActionPreference = 'Stop'
$submission = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../submission'))
if (-not (Test-Path -LiteralPath $submission -PathType Container)) { throw 'Submission directory missing' }
$powerpoint = $null
$deck = $null
try {
    $powerpoint = New-Object -ComObject PowerPoint.Application
    $deck = $powerpoint.Presentations.Open((Join-Path $submission 'MAIN_PRESENTATION.pptx'), -1, 0, 0)
    $deck.SaveAs((Join-Path $submission 'MAIN_PRESENTATION.pdf'), 32)
    'Exported MAIN_PRESENTATION.pdf'
} finally {
    if ($null -ne $deck) { $deck.Close() }
    if ($null -ne $powerpoint) { $powerpoint.Quit() }
}
$word = $null
$document = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $document = $word.Documents.Open((Join-Path $submission 'LIVE_PREPARATION.docx'), $false, $true)
    $document.ExportAsFixedFormat((Join-Path $submission 'LIVE_PREPARATION.pdf'), 17)
    'Exported LIVE_PREPARATION.pdf'
} finally {
    if ($null -ne $document) { $document.Close(0) }
    if ($null -ne $word) { $word.Quit() }
}
