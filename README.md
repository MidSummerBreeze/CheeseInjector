# Cheese Injector

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-AGPL--3.0-red.svg" alt="License: AGPL-3.0"></a>
  <a href="https://github.com/MidSummerBreeze/CheeseInjector/stargazers"><img src="https://img.shields.io/github/stars/MidSummerBreeze/CheeseInjector?style=social" alt="Stars"></a>
  <a href="https://github.com/MidSummerBreeze/CheeseInjector/network/members"><img src="https://img.shields.io/github/forks/MidSummerBreeze/CheeseInjector?style=social" alt="Forks"></a>
</p>

A next-gen Minecraft cheat injector. Dominates the game with stealthy payload execution, multi-threaded process targeting, and a stunning native Windows 11 Acrylic UI. Built with Python and PyQt5.

## ✨ Features

### 💉 Injector Capabilities
- **Stealthy Execution**: Delegates critical API calls to avoid dynamic heuristic detection, ensuring silent background delivery.
- **Multi-threaded Targeting**: Instantly locates `java.exe` and `javaw.exe` processes with accurate window title enumeration.
- **Undetected Payload Delivery**: Advanced execution techniques ensure your payload runs without triggering anti-cheat alarms.

### 🎨 Premium UI / UX (Perfect for Forking)
- **Native Windows 11 Acrylic**: True `SetWindowCompositionAttribute` implementation for a flawless frosted-glass effect. Automatically falls back to a flat design on Windows 10.
- **Smooth Custom Scrollbars**: Handcrafted `AnimatedScrollBar` replacing native Qt scrollbars to eliminate jumping bugs and provide macOS-like smooth pixel scrolling.
- **Animated Toast Notifications**: Non-intrusive, modern notification system with sliding animations and progress bars.
- **Fully Frameless**: Custom dragable title bar with animated minimize/close buttons.

## 📂 Project Structure

```text
CheeseInjector/
├── main.py                 # Application entry point
├── build.bat               # Robust Nuitka build script
├── requirements.txt        # Dependencies list
├── core/                   # Core logic layer
│   ├── scanner.py          # Multi-threaded Java process scanner
│   ├── injector.py         # Execution delegator
│   └── injector.ps1        # Stealthy WinAPI execution script
├── ui/                     # User interface components
│   ├── styles.py           # QSS Stylesheet (Easy to theme)
│   ├── animated_button.py  # Buttons with smooth color transitions
│   ├── animated_scrollbar.py # Bug-free custom scrollbar
│   ├── main_window.py      # Main application window
│   ├── sidebar.py          # Left sidebar panel
│   ├── content_header.py   # Top draggable header
│   ├── process_table.py    # Process list table
│   └── toast.py            # Toast notification system
└── utils/                  # Utilities
    ├── admin.py            # Admin privilege check
    ├── dialogs.py          # Native Windows dialogs
    ├── acrylic.py          # Win11 Acrylic blur enabler
    └── window_utils.py     # Window title enumeration
```

## 🚀 Quick Start

### Prerequisites
- Windows 10/11 OS
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

3. Run the application (**Must be run as Administrator**):
   ```bash
   python main.py
   ```

## 🛠️ Customization (For Forks)

This project is designed to be highly modular. If you fork this as a UI template, customizing it is easy:

- **Change Theme Color**: Open `ui/styles.py` and change the cyan values (e.g., `#06B6D4`) to your preferred color.
- **Change Target Process**: Open `core/scanner.py` and modify the `JAVA_PROCESS_NAMES` set.
- **Change Injected Payload**: Open `core/injector.ps1` and replace the `$shellcode` array with your own bytes.

## 📦 Building from Source

To compile the project into a standalone `.exe` executable, simply run the provided robust build script. It automatically cleans up previous artifacts, checks dependencies, and starts the Nuitka compilation process.

```bash
build.bat
```

Once completed, the final executable `CheeseInjector.exe` will be generated in the `dist/` directory.

## ⚠️ Disclaimer

This software is provided for educational purposes, reverse engineering research, and UI/UX design studies only. The author assumes no legal responsibility for any misuse of this tool. Using cheats disrupts game balance and inherently violates the Terms of Service of most multiplayer online games. All risks and consequences arising from the use of this tool are borne solely by the user.
