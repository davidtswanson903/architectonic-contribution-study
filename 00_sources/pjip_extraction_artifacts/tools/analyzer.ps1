$payloadPath = Join-Path $PSScriptRoot "..\payloads\z_en_Philosophy.json"
$jsonText = Get-Content $payloadPath -Raw
$jsonObj = ConvertFrom-Json $jsonText
$encoded = $jsonObj.encoded.Replace("4jri23jru283rf", "")
$bytes = [System.Convert]::FromBase64String($encoded)
$rawString = [System.Text.Encoding]::UTF8.GetString($bytes)
$decoded = ConvertFrom-Json $rawString

Write-Host "1. Top-level keys:"
$topKeys = $decoded | Get-Member -MemberType NoteProperty | Select-Object -ExpandProperty Name
$topKeys -join ", "

$philosophy = $decoded.Philosophy
Write-Host "`n2. Field names on representative record:"
$fields = $philosophy[0] | Get-Member -MemberType NoteProperty | Select-Object -ExpandProperty Name
$fields -join ", "

Write-Host "`n3. Language counts:"
$philosophy | Group-Object Language | Select-Object Name, Count | Format-Table -AutoSize

Write-Host "`n4. Link investigation:"
$philosophy[0] | Select-Object JournalPageTitle, eISSN, *URL*, *Link*, *Home*, *Guide* | Format-List