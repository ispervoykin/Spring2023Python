import time

db = [
    {
        "time": time.time(),
        "name": "Jack",
        "text": "Привет всем!"
    },
    {
        "time": time.time(),
        "name": "Mary",
        "text": "Привет, Jack!"
    }
]

def send_message(name, text):
    message = {
        'time': time.time(),
        'name': name,
        'text': text
    }
    db.append(message)

send_message('me', 'hi')
send_message('me', 'anybody here?')

def get_messages(after):
    """messages from db after given timestamp"""
    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
    return result

print(db)
t1 = db[-1]['time']
print(get_messages(t1))
send_message('123', 'yo')
print(get_messages(t1))