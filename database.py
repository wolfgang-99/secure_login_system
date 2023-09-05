import os
import random
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()


def database_connection():
    # Create a new client and connect to the server
    client = MongoClient(os.getenv("MONGODB_URL"), server_api=ServerApi('1'))
    db = client['ellextraDB']
    collection = db['LOGIN details']

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return collection


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letter = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_char = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letter + password_symbols + password_char
    random.shuffle(password_list)

    password = "".join(password_list)

    return password


def add_password_into_database(database_connection, generate_password):
    collection = database_connection()
    password = generate_password()

    username = input("type in username:")
    submission = {'username': username,
                  'password': password,
                  }
    collection.insert_one(submission)
    print(f"data has been recoreded: username:{username}, password:{password}")


add_password_into_database(database_connection, generate_password)
