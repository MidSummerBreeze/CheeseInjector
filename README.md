# Cheese Injector

A modern, lightweight **cheat injector** designed specifically for Minecraft Java Edition. Built with Python and PyQt5, featuring a frameless custom UI with a cyan-themed sidebar layout, used to inject cheat clients into the Minecraft process.

## ✨ Features

- **Modern UI**: Frameless window with a gradient sidebar, animated buttons with color transitions, and clean typography (forced Segoe UI font).
- **Process Scanning**: Multi-threaded scanning to quickly and accurately locate `java.exe` and `javaw.exe` processes.
- **Heuristic Bypass**: Utilizes a dynamically executed PowerShell script to delegate WinAPI calls, effectively avoiding dynamic heuristic detection by antiviruses on the Python interpreter itself.
- **Single File Build**: Easily compiles into a standalone `.exe` executable using Nuitka.

## 📂 Project Structure

```text
CheeseInjector/
├── main.py                 # Application entry point
├── build.bat               # Robust Nuitka build script
├── requirements.txt        # Dependencies list
├── core/                   # Core logic layer
│   ├── scanner.py          # Java process scanner thread
│   ├── injector.py         # PS1 script caller
│   └── injector.ps1        # WinAPI injection script
├── ui/                     # User interface components
│   ├── styles.py           # QSS Stylesheet
│   ├── animated_button.py  # Custom button with color transition
│   ├── main_window.py      # Main application window
│   ├── sidebar.py          # Left sidebar panel
│   ├── content_header.py   # Top draggable header
│   ├── process_table.py    # Process list table
│   └── status_bar.py       # Bottom status indicator
└── utils/                  # Utilities
    ├── admin.py            # Admin privilege check
    ├── dialogs.py          # Native Windows dialogs
    └── window_utils.py     # Window title enumeration
```

## 🚀 Getting Started

### Prerequisites

- Windows OS (Due to the use of underlying WinAPI and PowerShell)
- Python 3.8 or higher

### Installation & Running

1. Clone the repository:
   ```bash
   git clone https://github.com/MidSummerBreeze/CheeseInjector.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application (**Note: Must be run as Administrator**):
   ```bash
   python main.py
   ```

## 🛠️ Building from Source

To compile the project into a standalone `.exe` executable, simply run the provided build script. This script is highly robust: it automatically cleans up previous build artifacts, checks the Python environment and dependencies, and starts the Nuitka compilation process.

```bash
build.bat
```

Once completed, the final executable `CheeseInjector.exe` will be generated in the `dist/` directory.

## ⚠️ Disclaimer

This software is a game cheat injector provided solely for educational purposes, reverse engineering research, and cybersecurity defense studies. The author assumes no legal responsibility for any misuse of this tool. Using cheats disrupts game balance and inherently violates the Terms of Service of most multiplayer online games (including Minecraft), which may result in account bans. All risks and consequences arising from the use of this tool are borne solely by the user.
