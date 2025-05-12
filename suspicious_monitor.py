import psutil

# Define suspicious indicators
suspicious = ['bash', 'python', 'curl', 'sh']
abnormal_parents = ['WINWORD.EXE', 'EXCEL.EXE', 'Teams.exe', 'chrome.exe']

print("\n--- Suspicious Process Monitor ---\n")

for proc in psutil.process_iter(['pid', 'name', 'ppid', 'cmdline']):
    try:
        name = proc.info['name'] or ''
        pid = proc.info['pid']
        ppid = proc.info['ppid']
        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''

        # Match suspicious process names or command line content
        if any(s in name.lower() for s in suspicious) or any(s in cmdline.lower() for s in suspicious):
            try:
                parent = psutil.Process(ppid) if ppid else None
                parent_name = parent.name() if parent else 'N/A'
            except:
                parent_name = 'N/A'

            alert = f"[!] SUSPICIOUS: {name} | PID: {pid} | Parent: {parent_name} | PPID: {ppid}\n    CMD: {cmdline}"
            if parent_name.upper() in abnormal_parents:
                alert += " [!! ABNORMAL PARENT PROCESS DETECTED]"

            print(alert)
    except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
        continue
