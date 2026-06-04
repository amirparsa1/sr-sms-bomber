<p align="center">
  <img src="https://img.shields.io/badge/💣-SR ROOT BOMBER-00FF00?style=for-the-badge&logo=discord&logoColor=white&labelColor=000000"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/VERSION-2.0-39FF14?style=flat-square&labelColor=000000"/>
  <img src="https://img.shields.io/badge/PYTHON-3.8+-00FF41?style=flat-square&logo=python&logoColor=white&labelColor=000000"/>
  <img src="https://img.shields.io/badge/LICENSE-MIT-7FFF00?style=flat-square&labelColor=000000"/>
  <img src="https://img.shields.io/badge/TEAM-SR ROOT-00CC00?style=flat-square&labelColor=000000"/>
</p>

---

# 💣》SR-ROOT-BOMBER

<p align="center">
  <b>⚡ Powerful Iranian SMS & Call Bomber Discord Bot</b><br>
  <i>Fast • Secure • 170+ APIs • Proxy Support</i>
</p>

---

## 🔥 About

**SR ROOT BOMBER** is a high-performance Discord bot designed for SMS and Call bombing with **170+ active APIs**. Built with a beautiful cyber-green theme and robust permission system.

💣》SR-ROOT-BOMBER
🔥》Powered by SR ROOT TEAM
⚡》170+ SMS APIs | 50+ Call APIs
text


---

## ✨ Features

💣 SMS & Call Bomber 🔒 Admin + User Role System
📡 Proxy Support (HTTP) ⏱️ Smart Cooldown System
📊 Live Progress Tracking 🎨 Cyber Green Embeds
🔄 Auto API Reload ⚡ Multi-Threaded Attack
📝 Channel Lock System 💀 Fast & Lightweight
text


---

## 🎮 Commands

| Command | Access | Description |
|---------|:------:|-------------|
| `!bomb <type> <phone> <count>` | User+ | 💣 Start bombing |
| `!status` | User+ | 📊 System status |
| `!reload` | Admin | 🔄 Reload APIs |
| `!help` | All | ℹ️ Help menu |

---

📖 Usage

bash
# SMS Bomb - 50 requests
!bomb sms 09123456789 50

# Call Bomb - 30 requests
!bomb call 09123456789 30

# Check system status
!status

# Reload APIs (Admin only)
!reload

# Help menu
!help

🛠️ Installation
Prerequisites

    Python 3.8+

    Discord Bot Token (Get here)

Windows
bash

git clone https://github.com/amirparsa1/sr-sms-bomber.git
cd sr-sms-bomber
pip install -r requirements.txt
# Edit config.py with your info
python main.py

Linux / VPS
bash

git clone https://github.com/amirparsa1/sr-sms-bomber.git
cd sr-sms-bomber

# Option 1: With --break-system-packages
pip install -r requirements.txt --break-system-packages

# Option 2: With virtual environment (Recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Edit config.py
nano config.py

# Run
python3 main.py

⚙️ Configuration

Edit config.py with your information:
python

# Discord Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Role IDs
ADMIN_ROLE_ID = 123456789012345678  # Full access
USER_ROLE_ID = 123456789012345678   # Bomb & Status only

# Channel ID
ALLOWED_CHANNEL_ID = 123456789012345678

# Colors (Cyber Green Theme)
EMBED_COLOR = 0x00FF00      # Matrix Green
SUCCESS_COLOR = 0x00FF41    # Bright Green
ERROR_COLOR = 0x39FF14      # Neon Green
INFO_COLOR = 0x00CC00       # Dark Green
WARNING_COLOR = 0x7FFF00    # Chartreuse

# Settings
MAX_SPAM_COUNT = 100        # Max requests per command
COOLDOWN_SECONDS = 30       # Cooldown between uses

🔒 Permission System
text

👑 ADMIN_ROLE → All commands (including !reload)
👥 USER_ROLE  → !bomb & !status only
📝 Channel Lock → Commands only work in ALLOWED_CHANNEL_ID
⏱️ Cooldown → 30 seconds between each use

📡 Proxy Setup

Create proxies.txt and add HTTP proxies:


http://username:password@ip:port
http://ip:port

Bot auto-detects and uses proxies when the file exists.
📂 Structure
text

sr-sms-bomber/
├── main.py
├── config.py
├── requirements.txt
├── proxies.txt
├── cogs/
│   ├── __init__.py
│   └── bomber.py
├── Plugins/
│   ├── __init__.py
│   ├── api_list.py
│   └── my_handler.py
└── utils/
    └── __init__.py

🎨 Colors
Color	Hex	Usage
🟢 Matrix Green	#00FF00	Primary
💚 Bright Green	#00FF41	Success
⚡ Neon Green	#39FF14	Error
🌿 Dark Green	#00CC00	Info
🍋 Chartreuse	#7FFF00	Warning
🖥️ Preview
text

🔥》ATTACK STARTED
🎯: 09123456789 | 💣: SMS | 📊: 50

📊》Progress: 50/50
✅》Success: 48
❌》Failed: 2
📈》Rate: 96.0%
⏱️》Time: 12.3s

👑 Team
text

╔══════════════════════╗
║                      ║
║   💀 SR ROOT TEAM    ║
║   💣 Cyber Warfare   ║
║   ⚡ Since 2024      ║
║                      ║
╚══════════════════════╝

⚠️ Disclaimer

    Educational Purposes Only

    This tool is intended for educational and research purposes only.
    The developers assume no liability and are not responsible for any misuse or damage caused by this program.

    Use at your own risk.

📜 License
text

MIT License
Copyright (c) 2024 SR ROOT TEAM

⭐ Support

    ⭐ Star this repository

    🍴 Fork and contribute

    📢 Share with friends

<p align="center"> <img src="https://img.shields.io/badge/MADE WITH ❤️ BY-SR ROOT TEAM-00FF00?style=for-the-badge&labelColor=000000"/> </p><p align="center"> <sub>💣》SR-ROOT-BOMBER v2.0 | © 2024 SR ROOT TEAM</sub> </p> ```