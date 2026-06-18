import bcrypt 

# hashed using bcrypt
def generate_hash(psw):
 # UTF-8 encoding converts the string characters into binary byte formatting.
    byte_psw = psw.encode('utf-8')
    # Cryptographic Salt: Generates a random sequence of characters.
    # This ensures two users with identical passwords (e.g.'Password123$)
    # will generate completely distinct hashes, successfully mitigating Rainbow Table attacks.
    salt = bcrypt.gensalt()
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
import re
def is_strong_password(password):
    """Checks if the password meets security requirements."""
    if len(password) < 12:
        return False, "Password must be at least 12 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
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

def register_user():
    name = input('Enter your name: > ')
   
    is_name_valid, name_message = is_valid_username(name)
    if not is_name_valid:
        print(f"Registration Failed: {name_message}")
        return
   
    password = input('Enter your password: > ')

    is_valid, message = is_strong_password(password)
    if not is_valid:
        print(f"Registration Failed: {message}")
        return


    hash_password = generate_hash(password)
    with open('CW2_demo/DATA/DATA/users.txt', 'a') as f:
        f.write(f'{name},{hash_password}\n')
    print('User successfully registered!')

def login_user():
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    
    # Exception Handling Safeguard: If no users have registered yet, the file won't exist.
    # Wrapping with try-except avoids an application crash.
    try:
        
        with open('CW2_demo/DATA/DATA/users.txt', 'r') as f:
            users = f.readlines()
    except FileNotFoundError:
        print("Database system is empty. Please register an account first.")
        return False
    
    # Validation Loop: Linear scanning search across all registered records.
    for user in users:
        # Formatting Cleanup: .strip() eliminates hidden trailing whitespace and newline symbols (\n).
        # .split(',') breaks the comma-separated row string into discrete index components.
        user_name, user_hash = user.strip().split(',')
        
        if name == user_name and is_valid_hash(password, user_hash):
            return True         
    return False

def main():
    while True:
        print('1. To Register\n2. To Log in\n3. To Exit')
        choice = input(': > ')
        if choice == '1':
            register_user()
        elif choice == '2':
              if login_user():
               print('Login successful!' )
              else :
               print('Incorrect login.')
        elif choice == '3':
            print('Goodbye!');break
        
    

if __name__ == '__main__': 
     main()