import psutil

def kill_python_workers():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if it's a Python process
            if 'python' in proc.info['name'].lower():
                print(f"Found Python process: {proc.info['pid']} {proc.info['name']} {proc.info['cmdline']}")
                cmdline = proc.info['cmdline']
                # if cmdline and any('kcg' in arg.lower() for arg in cmdline):
                proc.terminate()
                print(f"Terminated process {proc.info['pid']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            print(f"Failed to terminate process {proc.info['pid']}")
            pass

if __name__ == "__main__":
    kill_python_workers()