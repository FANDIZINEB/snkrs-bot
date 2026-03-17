import datetime

def log(message):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {message}")
