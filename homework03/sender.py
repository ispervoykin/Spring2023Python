<<<<<<< HEAD
import requests

name = input("Введите имя: ")

while True:
    text = input("Введите текст: ")

    response = requests.post(
        'http://127.0.0.1:5000/send',
        json = {
            "name": name,
            "text": text
        }
    )

=======
import requests

name = input("Введите имя: ")

while True:
    text = input("Введите текст: ")

    response = requests.post(
        'http://127.0.0.1:5000/send',
        json = {
            "name": name,
            "text": text
        }
    )

>>>>>>> 9da9ad5897043b2dc2b400e92df224257804c46f
print(response.text)