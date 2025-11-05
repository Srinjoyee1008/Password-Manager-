from cryptography.fernet import Fernet
import os
import sys

def write_key():
    """Generates a key and saves it to a file."""
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """Loads the key from the current directory named 'key.key'."""
    try:
        with open("key.key", "rb") as f:
            key = f.read()
        return key
    except FileNotFoundError:
        print("Error: 'key.key' not found. Generating a new key.")
        write_key()
        # Try loading again after writing
        try:
            with open("key.key", "rb") as f:
                return f.read()
        except Exception as e:
            print(f"Critical Error: Could not generate or load key file: {e}")
            sys.exit(1) # Exit if key cannot be managed

# Check if key file exists, if not create one
if not os.path.exists("key.key"):
    write_key()
    print("New key file 'key.key' generated.")

# Load the key and initialize Fernet
try:
    key = load_key()
    fer = Fernet(key)
except Exception as e:
    print(f"Failed to initialize Fernet: {e}")
    sys.exit(1)

# Ensure passwords file exists to avoid read errors on first run
if not os.path.exists('passwords.txt'):
    open('passwords.txt', 'a').close()


def view():
    """Reads and decrypts stored usernames and passwords."""
    print("-" * 20)
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            if not data: # Skip empty lines
                continue
            try:
                user, passw = data.split("|")
                # Decrypt the password part
                decrypted_pass = fer.decrypt(passw.encode()).decode()
                print(f"User: {user}, Password: {decrypted_pass}")
            except Exception as e:
                print(f"Error reading line: {line.strip()}. Possible corruption.")
    print("-" * 20)

def add():
    """Prompts for a new account name and password, encrypts, and appends to file."""
    name = input("Account Name: ")
    # Mask input for the password for basic security on screen
    import getpass
    pwd = getpass.getpass("Password: ")

    # Encrypt the password and store the byte string representation
    encrypted_pwd = fer.encrypt(pwd.encode()).decode()
    
    with open('passwords.txt', 'a') as f:
        f.write(f"{name}|{encrypted_pwd}\n")
    print(f"Added password for account: {name}")

while True:
    mode = input("Would you like to add a new password, view existing ones, or quit? (add/view/quit): ").lower()
    
    if mode == "quit":
        break
    elif mode == "view":
        view() 
    elif mode == "add":
        add()
    else:
        print("Invalid mode.")
        continue

print("Goodbye!")
