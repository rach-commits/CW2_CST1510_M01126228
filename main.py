import bcrypt 

# hashed using bcrypt
def generate_hash(psw):
 # UTF-8 encoding converts the string characters into binary byte formatting.
    byte_psw = psw.encode('utf-8')
    # Cryptographic Salt: Generates a random sequence of characters.
    # This ensures two users with identical passwords (e.g.'Password123')
    # will generate completely distinct hashes, successfully mitigating Rainbow Table attacks.
    salt = bcrypt.gensalt()
    # Hashing Process: Combines the byte-string password and the unique salt.
    hash= bcrypt.hashpw(byte_psw, salt)
    return hash.decode('utf-8')

# validating hash vs pwd
psw = "HelloWorld123"

def is_valid_hash(psw, hash):
    # Format Conversion: Converts the stored plaintext database string hash 
    # back into its original binary byte format so it can be parsed by bcrypt.
    hash = hash.encode('utf-8')
    byte_psw = psw.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, hash)
    return is_valid

# user registration
import re
def is_strong_password(password):
    """Checks if the password meets security requirements."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    return True, "Strong password."

def register_user():
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')

    is_valid, message = is_strong_password(password)
    if not is_valid:
        print(f"Registration Failed: {message}")
        return

    # Hashing Layer: Never record passwords in plaintext format.
    # Passes credentials into the bcrypt function to secure data before it hits disk storage.
    hash_password = generate_hash(password)
    with open('users.txt', 'a') as f:
        f.write(f'{name},{hash_password}\n')
    print('User successfully registered!')

def login_user():
    name = input('Enter your name: > ')
    password = input('Enter your password: > ')
    
    # Exception Handling Safeguard: If no users have registered yet, the file won't exist.
    # Wrapping with try-except avoids an application crash.
    try:
        
        with open('users.txt', 'r') as f:
            # Data Parsing: readlines() imports all file rows into an indexable Python list.
            users = f.readlines()
    except FileNotFoundError:
        print("Database system is empty. Please register an account first.")
        return False
    
    # Validation Loop: Linear scanning search across all registered records.
    for user in users:
        # Formatting Cleanup: .strip() eliminates hidden trailing whitespace and newline symbols (\n).
        # .split(',') breaks the comma-separated row string into discrete index components.
        user_name, user_hash = user.strip().split(',')
        
        # Identity Validation: Compares target usernames and executes cryptographically 
        # safe password hash verification. If both match, the user is granted access.
        if name == user_name and is_valid_hash(password, user_hash):
            return True  # Authorization Granted immediately upon a match.        
    return False

def main():
    while True:
        print('1. To Register\n2. To Log in\n3. To Exit')
        choice = input(': > ')
        if choice == '1':
            register_user()
        elif choice == '2':
            print('Login successful!' if login_user() else 
'Incorrect login.')
        elif choice == '3':
            print('Goodbye!'); break
if __name__ == '__ main__':
    main()
    
