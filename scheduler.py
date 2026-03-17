from datetime import datetime

def wait_until(target_time):
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        if now >= target_time:
            break
