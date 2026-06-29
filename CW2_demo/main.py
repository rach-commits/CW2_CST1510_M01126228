import bcrypt
import sqlite3
import pandas as pd
import re

from app_model.db import conn
from app_model.users import add_user, get_user

# hashed using bcrypt
def generate_hash(psw):
 # UTF-8 encoding converts the string characters into binary byte formatting.
    byte_psw = psw.encode('utf-8')
    # Cryptographic Salt: Generates a random sequence of characters.
    # This ensures two users with identical passwords (e.g.'Password123$)
    # will generate completely distinct hashes, successfully mitigating Rainbow Table attacks.
    salt = bcrypt.gensalt(rounds=12)
    # Hashing Process: Combines the byte-string password and the unique salt.
    hash= bcrypt.hashpw(byte_psw, salt)
    return hash.decode('utf-8')


def is_valid_hash(psw, hash):
    """
    Format Conversion: Converts the stored plaintext database string hash 
    back into its original binary byte format so it can be parsed by bcrypt.
    """
    hash = hash.encode('utf-8')
    byte_psw = psw.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, hash)
    return is_valid

# user registration
def is_strong_password(password):
    """Checks if the password meets security requirements."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, "Strong password."

def is_valid_username(username):
    """Validates that the username is clean and not purely numeric."""
    # Strip whitespace to see if anything is actually written
    username = username.strip()
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
        
    # Check if the username consists entirely of numbers
    if username.isdigit():
        return False, "Username cannot contain only numbers. It must include letters."
        
    return True, "Valid username."

def register_user(conn):
    name = input('Enter your name: > ').strip()
    
   
    is_name_valid, name_message = is_valid_username(name)
    if not is_name_valid:
        print(f"Registration Failed: {name_message}")
        return False
   
    password = input('Enter your password: > ')
    
    role = input('Enter your role: ')

    is_valid, message = is_strong_password(password)
    if not is_valid:
        print(f"Registration Failed: {message}")
        return False

    hash_password = generate_hash(password)
    add_user(conn,name,hash_password,role)
    return True

# user log in
def login_user(conn):
    name = input('Enter your name: > ').strip()
    password = input('Enter your password: > ')

    #Check if user exists 
    user_data = get_user(conn,name)
    if not user_data:
        return False

    id, username,hash, role = user_data

      
    if name == username and is_valid_hash(password,hash):
        print(f'Welcome back {username}!')
        return True         
    return False

def main():
    while True:
        print('\nWelcome to the system!')
        print('Choose from the following options:')
        print('1. To Register\n2. To Log in\n3. To Exit')

        choice = input(': > ')

        if choice == '1':
             if  register_user(conn):
              print('Registration successful!')
        elif choice == '2':
            if login_user(conn):
               print('Login successful!' )
            else :
               print('Incorrect login details.')
        elif choice == '3':
            print('Goodbye!');break
        
 
if __name__ == '__main__':
    main()
       
       
























