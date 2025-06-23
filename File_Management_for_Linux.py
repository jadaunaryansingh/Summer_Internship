import subprocess

command_map = {
    "cal": "gnome-calendar",  # GNOME Calendar or replace with 'korganizer' etc.
    "calendar": "gnome-calendar",
    "notepad": "gedit",  # Replace with 'kate', 'mousepad', etc., based on your editor
    "editor": "gedit",
    "calculator": "gnome-calculator",
    "calc": "gnome-calculator",
    "explorer": "nautilus",  # File manager (GNOME)
    "file": "nautilus",
    "browser": "xdg-open https://www.google.com",  # Opens default browser
    "terminal": "gnome-terminal",  # or 'x-terminal-emulator' or 'konsole'
    "cmd": "gnome-terminal",
    "task manager": "gnome-system-monitor",
    "taskmgr": "gnome-system-monitor",
    "control": "gnome-control-center",
    "system info": "gnome-system-monitor",  # Not exact equivalent
    "device manager": "lshw -short",
    "settings": "gnome-control-center",
    "shutdown": "shutdown now",
    "restart": "reboot",
    "lock": "gnome-screensaver-command -l",  # Or 'loginctl lock-session'
    "paint": "pinta",  # Or 'gimp', 'kolourpaint', etc.
    "snipping": "gnome-screenshot",
    "exit": None
}

print("🐧 Welcome to Python OS Command Launcher (Linux Edition)")
print("👉 Type commands like: cal, notepad, browser, terminal, shutdown, etc.")
print("🔚 Type 'exit' to quit\n")

while True:
    cmd = input("Enter command: ").strip().lower()
    if cmd == "exit":
        print("Exiting launcher...")
        break
    elif cmd in command_map:
        action = command_map[cmd]
        if action:
            try:
                if " " in action:
                    subprocess.Popen(action, shell=True)
                else:
                    subprocess.Popen([action])
            except FileNotFoundError:
                print(f"⚠️ Command not found or not installed: {action}")
        else:
            print("⚠️ This command is not mapped to any action.")
    else:
        print("⚠️ Unknown command. Try again.")
