#!/usr/bin/env python3
"""
linux_clean.py — Tony's Ultimate Linux Clean
For Discord Users & Gamers
Zero-intervention. Run once. Walk away spotless.
Usage: python3 linux_clean.py [--full]
"""

import os
import sys
import re
import shutil
import subprocess
import time
from pathlib import Path
from datetime import datetime

# ── Config ────────────────────────────────────────────────────
HOME        = Path.home()
DESKTOP     = HOME / "Desktop"
DOWNLOADS   = HOME / "Downloads"
SCREENSHOTS = DESKTOP / "Screenshots"
MISC        = DESKTOP / "Misc"
ARCHIVE     = DOWNLOADS / "Archive"
DAYS_OLD    = 30
FULL_MODE   = "--full" in sys.argv

# ── Colours ───────────────────────────────────────────────────
G  = "\033[0;32m"
Y  = "\033[1;33m"
B  = "\033[0;36m"
D  = "\033[2m"
NC = "\033[0m"
BD = "\033[1m"

def header(title): print(f"\n{B}{BD}▸ {title}{NC}\n{D}  {'─'*41}{NC}")
def ok(msg):       print(f"  {G}✔{NC}  {msg}")
def info(msg):     print(f"  {B}→{NC}  {msg}")
def warn(msg):     print(f"  {Y}⚠{NC}  {msg}")
def skip(msg):     print(f"  {D}–  {msg} (skipped){NC}")

def human(b):
    if b >= 1_073_741_824: return f"{b/1_073_741_824:.1f} GB"
    if b >= 1_048_576:     return f"{b/1_048_576:.1f} MB"
    if b >= 1_024:         return f"{b/1_024:.1f} KB"
    return f"{b} B"

def dir_size(p):
    total = 0
    try:
        for f in Path(p).rglob("*"):
            try: total += f.stat().st_size
            except: pass
    except: pass
    return total

def run(cmd, **kw):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, **kw)

def has(cmd):
    return shutil.which(cmd) is not None

report = []
total_freed = 0

def add(emoji, title, detail, freed=0):
    global total_freed
    total_freed += freed
    report.append({"emoji": emoji, "title": title, "detail": detail,
                   "freed": human(freed) if freed > 0 else ""})

start = time.time()

print(f"\n{BD}{B}")
print("  ╔═══════════════════════════════════════╗")
print("  ║   🐧⚡ TONY'S ULTIMATE LINUX CLEAN    ║")
print(f"  ║      {datetime.now():%d %b %Y  %H:%M}                  ║")
print("  ╚═══════════════════════════════════════╝")
print(NC)

# ══════════════════════════════════════════════════════════════
# 1. SCREENSHOTS
# ══════════════════════════════════════════════════════════════
header("📸  Screenshots")

moved = 0
pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")

# Common Linux screenshot locations
sources = [DESKTOP, DOWNLOADS, HOME / "Pictures"]
for source in sources:
    if not source.exists():
        continue
    for f in list(source.iterdir()):
        if not f.is_file():
            continue
        name = f.name.lower()
        if not any(name.startswith(x) for x in ["screenshot", "screen_shot", "scrot", "gnome-screenshot"]):
            continue
        m = pattern.search(f.name)
        dest_dir = SCREENSHOTS / (m.group(1) + "/" + m.group(2)) if m else SCREENSHOTS / "Unsorted"
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f.name
        if dest.exists():
            dest = dest_dir / f"{f.stem}_dup{f.suffix}"
        try:
            shutil.move(str(f), str(dest))
            moved += 1
        except Exception as e:
            warn(f"Could not move {f.name}: {e}")

if moved:
    ok(f"{moved} screenshot(s) sorted → {SCREENSHOTS}")
    add("📸", "Screenshots sorted", f"{moved} files → Desktop/Screenshots/YYYY/MM")
else:
    info("No screenshots found.")
    add("📸", "Screenshots", "Nothing to sort")

# ══════════════════════════════════════════════════════════════
# 2. DESKTOP TIDY
# ══════════════════════════════════════════════════════════════
header("🖥️   Desktop")

misc_count = 0
skip_names = {".DS_Store", "Misc", "Screenshots"}

if DESKTOP.exists():
    for f in list(DESKTOP.iterdir()):
        if f.name in skip_names or f.name.startswith("."):
            continue
        if f.is_file():
            MISC.mkdir(exist_ok=True)
            try:
                shutil.move(str(f), str(MISC / f.name))
                misc_count += 1
            except Exception as e:
                warn(f"Could not move {f.name}: {e}")

if misc_count:
    ok(f"{misc_count} loose file(s) → Desktop/Misc")
    add("🖥️", "Desktop tidied", f"{misc_count} files moved to ~/Desktop/Misc")
else:
    info("Desktop already clean.")
    add("🖥️", "Desktop", "Already tidy")

# ══════════════════════════════════════════════════════════════
# 3. DOWNLOADS ARCHIVE
# ══════════════════════════════════════════════════════════════
header("📥  Downloads")

cutoff = time.time() - (DAYS_OLD * 86400)
old_count = 0

if DOWNLOADS.exists():
    for f in list(DOWNLOADS.iterdir()):
        if f.is_file() and not f.name.startswith("."):
            try:
                if f.stat().st_mtime < cutoff:
                    ARCHIVE.mkdir(exist_ok=True)
                    shutil.move(str(f), str(ARCHIVE / f.name))
                    old_count += 1
            except Exception as e:
                warn(f"Could not archive {f.name}: {e}")

if old_count:
    ok(f"{old_count} file(s) older than {DAYS_OLD} days → Downloads/Archive")
    add("📥", "Old downloads archived", f"{old_count} files moved to ~/Downloads/Archive")
else:
    info("No old downloads to archive.")
    add("📥", "Downloads", f"Nothing older than {DAYS_OLD} days")

# ══════════════════════════════════════════════════════════════
# 4. TRASH
# ══════════════════════════════════════════════════════════════
header("🗑️   Trash")

trash = HOME / ".local/share/Trash"
trash_size = dir_size(trash)

if has("gio"):
    result = run("gio trash --empty")
    if result.returncode == 0:
        ok(f"Trash emptied via gio (~{human(trash_size)} freed)")
        add("🗑️", "Trash emptied", f"{human(trash_size)} freed", trash_size)
    else:
        # fallback
        shutil.rmtree(str(trash / "files"), ignore_errors=True)
        shutil.rmtree(str(trash / "info"), ignore_errors=True)
        ok(f"Trash emptied (~{human(trash_size)} freed)")
        add("🗑️", "Trash emptied", f"{human(trash_size)} freed", trash_size)
else:
    shutil.rmtree(str(trash / "files"), ignore_errors=True)
    shutil.rmtree(str(trash / "info"), ignore_errors=True)
    ok(f"Trash emptied (~{human(trash_size)} freed)")
    add("🗑️", "Trash emptied", f"{human(trash_size)} freed", trash_size)

# ══════════════════════════════════════════════════════════════
# 5. USER CACHE (~/.cache)
# ══════════════════════════════════════════════════════════════
header("🧹  App Caches")

cache_dir = HOME / ".cache"
freed = 0
for item in list(cache_dir.iterdir()) if cache_dir.exists() else []:
    try:
        sz = dir_size(item)
        shutil.rmtree(str(item), ignore_errors=True)
        freed += sz
    except: pass
ok(f"~/.cache cleared (~{human(freed)} freed)")
add("🧹", "App caches cleared", f"{human(freed)} freed from ~/.cache", freed)

# ══════════════════════════════════════════════════════════════
# 6. LOG FILES
# ══════════════════════════════════════════════════════════════
header("🪵  Logs")

log_dir = HOME / ".local/share/xorg"
log_freed = 0
for ld in [HOME / ".local/share/xorg", HOME / ".xsession-errors"]:
    if ld.exists():
        sz = dir_size(ld) if ld.is_dir() else ld.stat().st_size
        shutil.rmtree(str(ld), ignore_errors=True) if ld.is_dir() else ld.unlink(missing_ok=True)
        log_freed += sz

ok(f"User logs cleared (~{human(log_freed)} freed)")
add("🪵", "Log files removed", f"{human(log_freed)} freed", log_freed)

# journald — vacuum logs older than 7 days (needs sudo)
if has("journalctl"):
    result = run("sudo -n journalctl --vacuum-time=7d")
    if result.returncode == 0:
        ok("systemd journal vacuumed (logs older than 7 days removed)")
        add("🪵", "Journal vacuumed", "Logs older than 7 days removed")
    else:
        info("Journal vacuum skipped (needs sudo) — run: sudo journalctl --vacuum-time=7d")

# ══════════════════════════════════════════════════════════════
# 7. THUMBNAIL CACHE
# ══════════════════════════════════════════════════════════════
header("👁️   Thumbnail Cache")

thumb_dir = HOME / ".cache/thumbnails"
thumb_size = dir_size(thumb_dir)
shutil.rmtree(str(thumb_dir), ignore_errors=True)
ok(f"Thumbnail cache cleared (~{human(thumb_size)} freed)")
add("👁️", "Thumbnail cache cleared", f"{human(thumb_size)} freed", thumb_size)

# ══════════════════════════════════════════════════════════════
# 8. BROWSER CACHES
# ══════════════════════════════════════════════════════════════
header("🌍  Browser Caches")

browsers = {
    "Chrome":  HOME / ".cache/google-chrome",
    "Chromium":HOME / ".cache/chromium",
    "Brave":   HOME / ".cache/BraveSoftware",
    "Edge":    HOME / ".cache/microsoft-edge",
    "Opera":   HOME / ".cache/opera",
}
browser_freed = 0
found = []

for name, path in browsers.items():
    if path.exists():
        sz = dir_size(path)
        shutil.rmtree(str(path), ignore_errors=True)
        browser_freed += sz
        found.append(name)

# Firefox
ff_base = HOME / ".cache/mozilla/firefox"
if ff_base.exists():
    for profile in ff_base.iterdir():
        cache = profile / "cache2"
        if cache.exists():
            sz = dir_size(cache)
            shutil.rmtree(str(cache), ignore_errors=True)
            browser_freed += sz
    if "Firefox" not in found:
        found.append("Firefox")

if found:
    ok(f"Browser caches cleared — {human(browser_freed)} freed ({', '.join(found)})")
    add("🌍", "Browser caches cleared", f"{human(browser_freed)} freed — {', '.join(found)}", browser_freed)
else:
    info("No browser caches found.")
    add("🌍", "Browser caches", "None found")

# ══════════════════════════════════════════════════════════════
# 9. PACKAGE MANAGER CLEANUP
# ══════════════════════════════════════════════════════════════
header("📦  Package Managers")

# APT
if has("apt"):
    apt_cache = run("sudo -n du -sb /var/cache/apt/archives 2>/dev/null").stdout.split()[0] if run("sudo -n true").returncode == 0 else "0"
    result = run("sudo -n apt autoremove -y && sudo -n apt autoclean -y")
    if result.returncode == 0:
        ok("apt autoremove + autoclean done")
        add("📦", "apt cleaned", "Unused packages and cache removed")
    else:
        info("apt cleanup skipped (needs sudo) — run: sudo apt autoremove && sudo apt autoclean")

# Snap
if has("snap"):
    # Remove old snap revisions
    result = run("snap list --all 2>/dev/null")
    snaps_removed = 0
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 6 and parts[5] == "disabled":
            run(f"sudo -n snap remove {parts[0]} --revision={parts[2]}")
            snaps_removed += 1
    if snaps_removed:
        ok(f"Removed {snaps_removed} old snap revision(s)")
        add("📦", "Snap cleaned", f"{snaps_removed} old revisions removed")
    else:
        info("No old snap revisions found.")

# Flatpak
if has("flatpak"):
    result = run("flatpak uninstall --unused -y")
    if result.returncode == 0:
        ok("Flatpak unused runtimes removed")
        add("📦", "Flatpak cleaned", "Unused runtimes removed")

# ══════════════════════════════════════════════════════════════
# 10. NPM
# ══════════════════════════════════════════════════════════════
header("📦  npm")

if has("npm"):
    npm_cache = run("npm config get cache").stdout.strip()
    npm_size = dir_size(npm_cache)
    run("npm cache clean --force")
    ok(f"npm cache cleared (~{human(npm_size)} freed)")
    add("📦", "npm cache cleared", f"{human(npm_size)} freed", npm_size)
else:
    skip("npm not installed")

# ══════════════════════════════════════════════════════════════
# 11. PIP
# ══════════════════════════════════════════════════════════════
header("🐍  pip")

for pip in ["pip3", "pip"]:
    if has(pip):
        pip_dir = run(f"{pip} cache dir").stdout.strip()
        pip_size = dir_size(pip_dir)
        run(f"{pip} cache purge")
        ok(f"pip cache cleared (~{human(pip_size)} freed)")
        add("🐍", "pip cache cleared", f"{human(pip_size)} freed", pip_size)
        break
else:
    skip("pip not installed")

# ══════════════════════════════════════════════════════════════
# 12. HOMEBREW (Linux)
# ══════════════════════════════════════════════════════════════
header("🍺  Homebrew")

if has("brew"):
    run("brew update --quiet")
    brew_cache = run("brew --cache").stdout.strip()
    before = dir_size(brew_cache)
    run("brew cleanup --prune=7 -q")
    run("brew autoremove -q")
    freed_b = max(0, before - dir_size(brew_cache))
    ok(f"Homebrew cleaned (~{human(freed_b)} freed)")
    add("🍺", "Homebrew cleaned", f"{human(freed_b)} freed", freed_b)
else:
    skip("Homebrew not installed")

# ══════════════════════════════════════════════════════════════
# 13. DNS FLUSH
# ══════════════════════════════════════════════════════════════
header("🌐  DNS")

if has("resolvectl"):
    result = run("sudo -n resolvectl flush-caches")
    if result.returncode == 0:
        ok("DNS cache flushed (systemd-resolved)")
        add("🌐", "DNS flushed", "systemd-resolved cache cleared")
    else:
        info("DNS flush skipped (needs sudo) — run: sudo resolvectl flush-caches")
        add("🌐", "DNS", "Skipped (needs sudo)")
elif has("nscd"):
    result = run("sudo -n nscd -i hosts")
    if result.returncode == 0:
        ok("DNS cache flushed (nscd)")
        add("🌐", "DNS flushed", "nscd cache cleared")
    else:
        info("DNS flush skipped (needs sudo)")
        add("🌐", "DNS", "Skipped (needs sudo)")
else:
    skip("No DNS cache service found")
    add("🌐", "DNS", "No cache service found")

# ══════════════════════════════════════════════════════════════
# 14. RAM / MEMORY
# ══════════════════════════════════════════════════════════════
header("🧠  Memory")

result = run("sudo -n sh -c 'sync && echo 3 > /proc/sys/vm/drop_caches'")
if result.returncode == 0:
    ok("RAM page cache dropped (memory freed)")
    add("🧠", "RAM purged", "Page cache dropped via /proc/sys/vm/drop_caches")
else:
    info("Memory purge skipped (needs sudo) — run: sudo sh -c 'sync && echo 3 > /proc/sys/vm/drop_caches'")
    add("🧠", "RAM purge", "Skipped (needs sudo)")

# ══════════════════════════════════════════════════════════════
# 15. DOCKER (--full only)
# ══════════════════════════════════════════════════════════════
header("🐳  Docker")

if FULL_MODE and has("docker"):
    if run("docker info").returncode == 0:
        run("docker system prune -af --volumes")
        ok("Docker pruned — unused images, containers, volumes removed")
        add("🐳", "Docker pruned", "All unused resources removed")
    else:
        warn("Docker not running")
        add("🐳", "Docker", "Not running")
elif not FULL_MODE:
    info("Docker skipped — use --full to include")
    add("🐳", "Docker", "Skipped (use --full)")
else:
    skip("Docker not installed")

# ══════════════════════════════════════════════════════════════
# 16. HTML REPORT
# ══════════════════════════════════════════════════════════════
header("📊  Report")

import json
elapsed = int(time.time() - start)
report_path = DESKTOP / f"Linux_Clean_Report_{datetime.now():%Y-%m-%d_%H%M}.html" if DESKTOP.exists() else Path.home() / f"Linux_Clean_Report_{datetime.now():%Y-%m-%d_%H%M}.html"
items_json = json.dumps(report)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Linux Clean Report — {datetime.now():%d %b %Y}</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{ --bg:#0a0a0f; --surface:#13131a; --surface2:#1c1c28; --border:#2a2a3a; --accent:#7c6aff; --text:#e8e8f0; --muted:#6b6b88; }}
  *,*::before,*::after {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--text); font-family:'Syne',sans-serif; min-height:100vh; padding:0 0 80px; }}
  .hero {{ position:relative; padding:80px 40px 60px; text-align:center; overflow:hidden; }}
  .hero::before {{ content:''; position:absolute; inset:0; background:radial-gradient(ellipse 60% 50% at 50% -10%, rgba(124,106,255,.2) 0%, transparent 70%); pointer-events:none; }}
  .eyebrow {{ font-family:'DM Mono',monospace; font-size:.75rem; letter-spacing:.2em; text-transform:uppercase; color:var(--accent); margin-bottom:20px; }}
  h1 {{ font-size:clamp(2.8rem,8vw,6rem); font-weight:800; line-height:1; letter-spacing:-.03em; background:linear-gradient(135deg,#fff 30%,var(--accent) 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:12px; }}
  .sub {{ color:var(--muted); font-size:1rem; font-family:'DM Mono',monospace; }}
  .stats {{ display:flex; max-width:700px; margin:40px auto 0; border:1px solid var(--border); border-radius:16px; overflow:hidden; background:var(--surface); }}
  .stat {{ flex:1; padding:28px 24px; text-align:center; border-right:1px solid var(--border); }}
  .stat:last-child {{ border-right:none; }}
  .stat-val {{ font-size:2rem; font-weight:800; color:var(--accent); }}
  .stat-label {{ font-family:'DM Mono',monospace; font-size:.7rem; letter-spacing:.12em; text-transform:uppercase; color:var(--muted); margin-top:6px; }}
  .wrap {{ max-width:1000px; margin:64px auto 0; padding:0 40px; }}
  .section-label {{ font-family:'DM Mono',monospace; font-size:.7rem; letter-spacing:.18em; text-transform:uppercase; color:var(--muted); margin-bottom:20px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:12px; }}
  .card {{ background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:22px 24px; display:flex; align-items:flex-start; gap:16px; animation:fadeUp .4s ease both; }}
  @keyframes fadeUp {{ from {{ opacity:0; transform:translateY(16px) }} to {{ opacity:1; transform:translateY(0) }} }}
  .emoji {{ font-size:1.6rem; flex-shrink:0; width:42px; height:42px; display:flex; align-items:center; justify-content:center; background:var(--surface2); border-radius:10px; border:1px solid var(--border); }}
  .card-body {{ flex:1; min-width:0; }}
  .card-title {{ font-weight:700; font-size:.95rem; margin-bottom:4px; }}
  .card-detail {{ font-family:'DM Mono',monospace; font-size:.72rem; color:var(--muted); line-height:1.4; }}
  .card-freed {{ font-family:'DM Mono',monospace; font-size:.75rem; color:var(--accent); margin-top:8px; }}
  footer {{ text-align:center; margin-top:80px; font-family:'DM Mono',monospace; font-size:.72rem; color:var(--muted); }}
</style>
</head>
<body>
<div class="hero">
  <p class="eyebrow">🐧 Linux Deep Clean — {datetime.now():%A, %d %B %Y at %H:%M}</p>
  <h1>All<br>Clean.</h1>
  <p class="sub">Your Linux machine has been scrubbed, sorted &amp; optimised.</p>
  <div class="stats">
    <div class="stat"><div class="stat-val">{human(total_freed)}</div><div class="stat-label">Freed</div></div>
    <div class="stat"><div class="stat-val">{len(report)}</div><div class="stat-label">Tasks</div></div>
    <div class="stat"><div class="stat-val">{elapsed}s</div><div class="stat-label">Duration</div></div>
  </div>
</div>
<div class="wrap">
  <p class="section-label">Detailed Results</p>
  <div class="grid" id="grid"></div>
</div>
<footer><p>Generated by linux_clean.py · {datetime.now():%Y-%m-%d %H:%M:%S}</p></footer>
<script>
const items = {items_json};
const grid = document.getElementById('grid');
items.forEach((item, i) => {{
  const c = document.createElement('div');
  c.className = 'card';
  c.style.animationDelay = (i * 40) + 'ms';
  c.innerHTML = `<div class="emoji">${{item.emoji}}</div>
    <div class="card-body">
      <div class="card-title">${{item.title}}</div>
      <div class="card-detail">${{item.detail}}</div>
      ${{item.freed ? `<div class="card-freed">↓ ${{item.freed}} freed</div>` : ''}}
    </div>`;
  grid.appendChild(c);
}});
</script>
</body>
</html>"""

report_path.write_text(html)
ok(f"Report saved → {report_path}")

# Try to open the report
for opener in ["xdg-open", "gnome-open", "kde-open"]:
    if has(opener):
        run(f'{opener} "{report_path}"')
        break

# ══════════════════════════════════════════════════════════════
# DONE
# ══════════════════════════════════════════════════════════════
print(f"\n{BD}{B}")
print("  ╔═══════════════════════════════════════╗")
print("  ║   ✅  DEEP CLEAN COMPLETE             ║")
print(f"  ║   💾  ~{human(total_freed):<32}║")
print(f"  ║   ⏱   Finished in {elapsed} seconds{' '*(21-len(str(elapsed)))}║")
print("  ║   📊  Report saved to Desktop        ║")
print("  ╚═══════════════════════════════════════╝")
print(NC)
print(f"  {D}Tip: run with --full to also clean Docker{NC}\n")
