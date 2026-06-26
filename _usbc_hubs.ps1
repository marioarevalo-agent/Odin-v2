
$controllers = Get-CimInstance Win32_PnPEntity -Filter "PNPClass='USB'" | Where-Object { $_.Name -match 'USB 3\.20|USB 3\.2[^0]' }
$hubs = @()
foreach ($c in $controllers) {
    $children = (Get-PnpDeviceProperty -InstanceId $c.PNPDeviceID -KeyName DEVPKEY_Device_Children -ErrorAction SilentlyContinue).Data
    if ($children) { $hubs += $children }
    $hubs += $c.PNPDeviceID
}
if ($hubs.Count -gt 0) { $hubs | ConvertTo-Json -Compress } else { Write-Output '[]' }
