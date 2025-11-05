from cryptography.fernet import Fernet
import os
import sys

def write_key():
    
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    try:
        with open("key.key", "rb") as f:
            key = f.read()
        return key
    except FileNotFoundError:
        print("Error: 'key.key' not found. Generating a new key.")
        write_key()
        try:
            with open("key.key", "rb") as f:
                return f.read()
        except Exception as e:
            print(f"Critical Error: Could not generate or load key file: {e}")
            sys.exit(1) 


if not os.path.exists("key.key"):
    write_key()
    print("New key file 'key.key' generated.")


try:
    key = load_key()
    fer = Fernet(key)
except Exception as e:
    print(f"Failed to initialize Fernet: {e}")
    sys.exit(1)


if not os.path.exists('passwords.txt'):
    open('passwords.txt', 'a').close()


def view():
    """Reads and decrypts stored usernames and passwords."""
    print("-" * 20)
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            if not data: 
                continue
            try:
                user, passw = data.split("|")
                
                decrypted_pass = fer.decrypt(passw.encode()).decode()
                print(f"User: {user}, Password: {decrypted_pass}")
            except Exception as e:
                print(f"Error reading line: {line.strip()}. Possible corruption.")
    print("-" * 20)

def add():
   name = input("Account Name: ")
   
    import getpass
    pwd = getpass.getpass("Password: ")

    
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

