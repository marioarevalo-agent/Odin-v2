
$parents = @()
$ucm = Get-PnpDevice -Class UCM -Status OK -ErrorAction SilentlyContinue
if ($ucm) {
    foreach ($u in $ucm) {
        $p = (Get-PnpDeviceProperty -InstanceId $u.InstanceId -KeyName DEVPKEY_Device_Parent -ErrorAction SilentlyContinue).Data
        if ($p) { $parents += $p }
    }
}
if ($parents.Count -gt 0) { $parents | ConvertTo-Json -Compress } else { Write-Output '[]' }
