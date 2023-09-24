#variables
$NETMASK = "255.255.255.0"
$InterfaceNames = @("VirtualBox Host-Only Ethernet Adapter", "VirtualBox Host-Only Ethernet Adapter #2", "VirtualBox Host-Only Ethernet Adapter #3")
$IPAddresses = @("192.168.71.100", "192.168.72.100", "192.168.12.100")
$VBoxManagePath = $null

# Get available drives/partitions
$drives = Get-WmiObject -Class Win32_LogicalDisk | Where-Object { $_.DriveType -eq 3 } | ForEach-Object { $_.DeviceID }

# Search each drive for VBoxManage.exe
foreach ($drive in $drives) {
    $filePath = "$drive\Program Files\Oracle\VirtualBox\VBoxManage.exe"
    
    Write-Output "Checking path: $filePath"
    
    if (Test-Path $filePath) {
        $VBoxManagePath = $filePath
        Write-Output "VBoxManage.exe found at $VBoxManagePath"
        # Get existing host-only interfaces
        $existingInterfaces = & $VBoxManagePath list hostonlyifs | Where-Object {$_ -match "Name: (.+)"} | ForEach-Object {($_ -split ":")[1].Trim()}

        for ($i=0; $i -lt $InterfaceNames.Length; $i++) {
            $INTERFACE_NAME = $InterfaceNames[$i]
            Write-Output $INTERFACE_NAME
            $TARGET_IP = $IPAddresses[$i]
            Write-Output $TARGET_IP

            # Create a new "host-only" network interfaces
            if ($existingInterfaces -notcontains $INTERFACE_NAME) {
                $creationOutput = & $VBoxManagePath hostonlyif create 2>&1
                $INTERFACE = ($creationOutput | Where-Object {$_ -match "Interface '(.+?)' was successfully created"} | ForEach-Object {($_ -split "'")[1]}).Trim()
            } else {
                $INTERFACE = $INTERFACE_NAME
            }

            if (-not $INTERFACE) {
                Write-Error "Failed to create $INTERFACE."
                continue
            }

            # Configure the network interface with the desired IP address
            & $VBoxManagePath hostonlyif ipconfig "$INTERFACE" --ip $TARGET_IP --netmask $NETMASK

            # Check if there's a DHCP server for this interface
            $dhcpExist = & $VBoxManagePath list dhcpservers | Where-Object {$_ -match $INTERFACE}

            if ($dhcpExist) {
                # Disable the DHCP server for this interface
                & $VBoxManagePath dhcpserver remove --ifname $INTERFACE
            }

            Write-Output "Network interface $INTERFACE has been configured with IP address $TARGET_IP."
        }
    } else {
        Write-Error "VBoxManage.exe not found on $drive"
    }
}






