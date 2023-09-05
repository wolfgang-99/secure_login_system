import socket
import threading
import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

server.listen()


def handle_connection(c):
    c.send("Username:".encode())
    username = c.recv(1024).decode()
    c.send("password:".encode())
    password = c.recv(1024).decode()

    # Create a new client and connect to the server
    client = MongoClient(os.getenv("MONGODB_URL"), server_api=ServerApi('1'))
    db = client['ellextraDB']
    collection = db['LOGIN details']

    # Define the criteria for the username and password
    input_username = username
    input_password = password

    try:
        # Find the user by username
        user_document = collection.find_one({"username": input_username})
        if user_document:
            stored_password = user_document["password"]

            # Check if the provided password matches the stored hash
            if stored_password == input_password:
                c.send("Login Successful".encode())
            else:
                c.send("Login Failed: Incorrect Password".encode())
        else:
            c.send("Login Failed: User not found".encode())
    except Exception as e:
        print("An error occurred:", str(e))


while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()

