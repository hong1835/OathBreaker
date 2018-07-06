#required at least powershell2.0
param
(
        [parameter(Mandatory = $true)][int]$data1,
        [parameter(Mandatory = $true)][int]$data2

)

$data3 = $data1 + $data2

Write-Host $data3
