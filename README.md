# 🐧⚡ Tony's Ultimate Linux Clean

[![Stars](https://img.shields.io/github/stars/hardlygospel/tonys-ultimate-linux-clean?style=for-the-badge&color=yellow)](https://github.com/hardlygospel/tonys-ultimate-linux-clean/stargazers) [![Forks](https://img.shields.io/github/forks/hardlygospel/tonys-ultimate-linux-clean?style=for-the-badge&color=blue)](https://github.com/hardlygospel/tonys-ultimate-linux-clean/network/members) [![Issues](https://img.shields.io/github/issues/hardlygospel/tonys-ultimate-linux-clean?style=for-the-badge&color=red)](https://github.com/hardlygospel/tonys-ultimate-linux-clean/issues) [![Last Commit](https://img.shields.io/github/last-commit/hardlygospel/tonys-ultimate-linux-clean?style=for-the-badge&color=green)](https://github.com/hardlygospel/tonys-ultimate-linux-clean/commits) [![License](https://img.shields.io/badge/License-GPL_v3-blue?style=for-the-badge)](https://github.com/hardlygospel/tonys-ultimate-linux-clean/blob/main/LICENSE) [![macOS](https://img.shields.io/badge/macOS-supported-brightgreen?style=for-the-badge&logo=apple)](https://github.com/hardlygospel/tonys-ultimate-linux-clean) [![Linux](https://img.shields.io/badge/Linux-supported-brightgreen?style=for-the-badge&logo=linux)](https://github.com/hardlygospel/tonys-ultimate-linux-clean) [![Shell](https://img.shields.io/badge/Shell-Bash-4EAA25?style=for-the-badge&logo=gnubash)](https://github.com/hardlygospel/tonys-ultimate-linux-clean) [![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=for-the-badge&logo=docker)](https://github.com/hardlygospel/tonys-ultimate-linux-clean) [![Maintained](https://img.shields.io/badge/Maintained-yes-brightgreen?style=for-the-badge)](https://github.com/hardlygospel/tonys-ultimate-linux-clean) [![Repo Size](https://img.shields.io/github/repo-size/hardlygospel/tonys-ultimate-linux-clean?style=for-the-badge)](https://github.com/hardlygospel/tonys-ultimate-linux-clean) [![Code Size](https://img.shields.io/github/languages/code-size/hardlygospel/tonys-ultimate-linux-clean?style=for-the-badge)](https://github.com/hardlygospel/tonys-ultimate-linux-clean)
### *For Discord Users & Gamers*

> One command. No intervention. Walk away with a faster, cleaner Linux machine.

---

## ⚡ Quick Start

```bash
python3 linux_clean.py
```

```bash
# Nuclear mode — also cleans Docker
python3 linux_clean.py --full
```

> Some steps (DNS flush, RAM purge, apt cleanup) need sudo. Run with `sudo python3 linux_clean.py` for a full deep clean.

---

## 🧹 What Gets Cleaned

| | What | Result |
|---|---|---|
| 📸 | **Screenshots** | Sorted into `Desktop/Screenshots/YYYY/MM` |
| 🖥️ | **Desktop** | Loose files moved to `Desktop/Misc` |
| 📥 | **Downloads** | Files 30+ days old archived automatically |
| 🗑️ | **Trash** | Emptied |
| 🧹 | **App Caches** | All of `~/.cache` cleared |
| 🪵 | **Log Files** | User logs + systemd journal vacuumed |
| 👁️ | **Thumbnails** | `~/.cache/thumbnails` cleared |
| 🌍 | **Browsers** | Chrome, Chromium, Firefox, Brave, Edge, Opera caches cleared |
| 📦 | **apt** | autoremove + autoclean |
| 📦 | **Snap** | Old revisions removed |
| 📦 | **Flatpak** | Unused runtimes removed |
| 📦 | **npm** | Cache purged |
| 🐍 | **pip** | Cache purged |
| 🍺 | **Homebrew** | Updated + cleaned (if installed) |
| 🌐 | **DNS** | Cache flushed (systemd-resolved or nscd) |
| 🧠 | **RAM** | Page cache dropped |
| 📊 | **HTML Report** | Report saved to Desktop |

**With `--full` also cleans:**

| | What | Result |
|---|---|---|
| 🐳 | **Docker** | All unused images, containers & volumes |

---

## 📊 Report

After every run a slick dark-mode HTML report opens showing total space freed, every task result, and how long it took.

---

## 🎮 Why This Exists

Discord and games chew through cache, logs and temp files fast. Linux doesn't clean these up automatically. This script fixes all of that in one go.

Works on Ubuntu, Debian, Fedora, Arch, Pop!\_OS, Linux Mint and most other distros. Falls back gracefully if a tool isn't installed.

---

## 🔒 Safe by Default

- Files are **moved**, not deleted (Desktop → Misc, Downloads → Archive)
- Browser **passwords and history are never touched** — only cache
- `--full` Docker cleanup is **opt-in only**
- Steps needing sudo are **skipped gracefully** if not available

---

## 💻 Requirements

- Python 3 (ships with all major distros)
- Everything else (apt, snap, flatpak, npm, pip etc.) is optional — skipped if not installed

---

## 📄 Licence


---

*Made with ☕ and too many hours in Discord.*
