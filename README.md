# ⚡ Soda Optimizer

**Soda Optimizer** is a powerful Windows-based performance optimizer built for gamers, power users, and enthusiasts. It applies deep system-level tweaks, aggressively manages background processes, and ensures complete restoration after gameplay or heavy tasks. Designed with precision and safety in mind, Soda Optimizer improves real-time system responsiveness while monitoring critical performance metrics.

## 🚀 Core Optimization Features
### 🔋 Power Management
- Switches to the **High Performance** power plan.
- Command used:
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c

- Automatically restores the original power plan post-optimization.

---

### 🎮 GPU Optimization

#### NVIDIA
- Enables persistence mode.
- Increases power limit to **125W**.

#### AMD
- Sets GPU to high-performance profile.
- Increases engine clock to **1200MHz**.

> ✅ GPU settings are fully restored after optimization ends.

---

### 🧠 Process Management

An advanced, intelligent system for real-time background process control.

#### Key Features
- Selective termination of unnecessary background processes.
- Multi-layer protection for critical system components including:
- `explorer.exe`
- `System`, `svchost.exe`, `lsass.exe`, etc.
- Hardware communication and core Windows services.

#### Whitelist Management (via `whitelist.json`)
```json
[
"System",
"smss.exe",
"csrss.exe",
"wininit.exe",
"services.exe",
"lsass.exe",
"svchost.exe",
"dwm.exe",
"TrustedInstaller.exe"
]
```
Includes **30+ pre-configured Windows core services** for protection.

### 🔁 State-Aware Restoration
- Tracks all terminated process states and their original arguments.
- Automatically relaunches protected processes if terminated.
- Restores `explorer.exe` without user input if missing.

### 🛡 Built-In Safety Measures
- Performs system stability checks before terminating any process.
- Analyzes process dependencies to prevent chain failures.
- Guarantees that **at least 2 critical core processes** remain running.
- Includes a fallback restoration mechanism in case of unexpected failure.

### 📉 Performance Overhead
- **CPU usage:** <1% during active monitoring.
- **Memory footprint:** ~15MB RAM.

### 🧼 Memory Management
- Clears standby memory to free up cached RAM and reduce clutter.
- Utilizes `EmptyStandbyList.exe` (must be present in system `PATH`).
- Helps reduce memory pressure for high-performance tasks.

---

### 💽 Disk Optimization
- Disables built-in Windows defragmentation to reduce background I/O:
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Dfrg\BootOptimizeFunction

- Adjusts virtual memory (pagefile) for optimized memory handling:
- **Initial size:** 1.5 × RAM
- **Maximum size:** 3 × RAM
- All virtual memory settings are automatically reverted post-session.

---

### 🌐 Network Optimization

Applies advanced TCP/IP stack optimizations for better connection stability and reduced latency:

- Enables:
  - **Direct Cache Access (DCA)** – Improves memory throughput for network transfers.
  - **Receive Side Scaling (RSS)** – Distributes network load across CPU cores.
  - **CTCP Congestion Control Provider** – Enhances TCP performance in high-latency environments.

> 🔁 All network changes are fully reverted during system restoration.

---

### 🪟 Windows Tweaks

- Disables **GameDVR** to prevent background recording overhead.
- Disables **Fullscreen Optimizations** to reduce input lag and improve game responsiveness.
- Registry modified:

HKEY_CURRENT_USER\System\GameConfigStore


---

## 📊 Real-Time Monitoring Features

Track key performance indicators in real-time for better situational awareness:

- **CPU usage**
- **RAM usage**
- **GPU usage / temperature** (if supported)
- **Network latency**

### 🎯 Game Process Tracking

- Monitors active game executables based on a defined whitelist.
- Applies optimizations only while games are running.
- Automatically restores system to original state once all games exit.
- Operates silently in the background without user interference.

## 🛡️ Safety & Fail-Safes

Soda Optimizer prioritizes system stability with robust recovery mechanisms:

- Creates a **full system state backup** before applying any optimization.
- Automatically restores all settings and processes when:
  - A game or monitored process exits.
  - The user manually triggers a restore.
  - The script encounters an error or unexpected crash.

> ⚠️ You’re always just one step away from full restoration.

---

## 🧰 Requirements

To run Soda Optimizer smoothly, make sure your environment meets the following:

- **Operating System:** Windows 10 or Windows 11
- **Privileges:** Administrator access (required for system-level changes)
- **Python Version:** Python 3.9 or higher
- **Python Dependencies:**
psutil tkinter pywin32
- **Additional Tools:**
- `EmptyStandbyList.exe` (must be available in system PATH for memory clearing)
