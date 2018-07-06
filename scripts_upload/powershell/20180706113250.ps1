#required at least powershell2.0
Get-Service | ? { $_.status -eq "running" }