
import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()

LOCK_FILE=os.environ['LOCK_FILE']
MARKER_FILE=os.environ['MARKER_FILE']
TIMEOUT=int(os.environ['TIMEOUT'])
INTERVAL=int(os.environ['INTERVAL'])

def lock():
    acquired = False
    wait = 0

    while wait < TIMEOUT:
        if not os.path.exists(MARKER_FILE):
            try:
                fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                try:
                    with open(MARKER_FILE, 'w') as file:
                        file.write("Delete this file when the job is finished.")
                    acquired = True
                    break
                finally:
                    os.close(fd)
                    os.remove(LOCK_FILE)
            except FileExistsError:
                print(f"Another process is acquiring the lock")
            except Exception as e:
                print(f"An error occured: {e}")

        print(f"Another process is running (we've been waiting for {wait} seconds)")
        time.sleep(INTERVAL)
        wait += INTERVAL
    
    return acquired

def unlock():
    os.remove(MARKER_FILE)

def main():
    command = sys.argv[1]
    if command == 'lock':
        if not lock():
            print ("Timed out after {TIMEOUT} seconds waiting for lock.")
            sys.exit(1)
    elif command == 'unlock':
        unlock()
    else:
        raise Exception(f"Unknown command: {command}")

if __name__ == '__main__': main()
