import psutil


def detect_csgo_path():
    # Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            # Check if the process name matches 'csgo.exe'
            if proc.info['name'] == 'csgo.exe':
                # Return the path of the executable
                return proc.info['exe']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None
