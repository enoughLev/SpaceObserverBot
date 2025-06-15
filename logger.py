from datetime import datetime

def log_dialog(user_id: int, message: str):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}\n"
    with open(f'{user_id}.log', 'a', encoding='utf-8') as f:
        f.write(log_line)
