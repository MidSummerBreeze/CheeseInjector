# CheeseInjector

A high-performance Minecraft hot-injection cheat tool that manipulates game memory and bytecode in real-time without requiring a game restart.

---

## Overview

CheeseInjector is a runtime cheat injection framework for Minecraft. It attaches to a running game process via JNI and native hooks, enabling live memory patching, bytecode manipulation, and game logic overriding — all without relaunching the client.

## Key Features

- **Hot Injection** – Attach to Minecraft while it's already running. No restart needed.
- **Native & JNI Hooking** – Low-level memory access via platform-specific native code and Java Native Interface.
- **Dynamic Bytecode Manipulation** – Rewrite game classes on the fly using runtime instrumentation.
- **Real-time Memory Patching** – Modify values, flags, and game state instantly.
- **Stealth-oriented Design** – Bypass basic client integrity checks (educational/research purposes).

## Injection Capabilities

| Capability | Description |
|------------|-------------|
| Live Class Redefinition | Replace method bytecode during runtime |
| Field Override | Force-read/write private/protected fields |
| Native Interception | Hook native methods and reroute execution |
| Memory Search & Edit | Scan and modify heap/off-heap data |

### Disclaimer

> This project is intended for **educational and research purposes only**. Use it only on servers you own or have explicit permission to test. Unauthorized use violates Minecraft's EULA and may result in account bans.
