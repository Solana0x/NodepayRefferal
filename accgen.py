import random
import string

base_email = "enteryouremail@gmail.com" #use only gmail address here 
used_emails = set()
used_usernames = set()
def generate_username():
    while True:
        length = random.randint(8, 15)
        first_letter = random.choice(string.ascii_letters)
        rest = ''.join(random.choices(string.ascii_letters + string.digits, k=length - 1))
        username = first_letter + rest
        if username not in used_usernames:
            used_usernames.add(username)
            return username
def generate_password():
    password_length = random.randint(8, 12)
    special_characters = "!@#$%^&*()-_=+"
    lower = random.choice(string.ascii_lowercase)
    upper = random.choice(string.ascii_uppercase)
    special = random.choice(special_characters)
    rest = ''.join(random.choices(string.ascii_letters + string.digits + special_characters, k=password_length - 3))
    return lower + upper + special + rest
def generate_email():
    while True:
        alias_method = random.choice(['plus', 'dot'])
        if alias_method == 'plus':
            email = base_email.replace('@', f'+{random.randint(1, 9999)}@')
        elif alias_method == 'dot':
            split_email = base_email.split('@')
            name_part = split_email[0]
            if '.' not in name_part:
                insert_pos = random.randint(1, len(name_part) - 1)
                new_name_part = name_part[:insert_pos] + '.' + name_part[insert_pos:]
                email = f"{new_name_part}@{split_email[1]}"
            else:
                email = base_email
        if email not in used_emails:
            used_emails.add(email)
            return email
def save_to_file(email, password, username):
    with open('reg.txt', 'a') as file:
        file.write(f"{email},{password},{username}\n")
def generate_accounts(num_accounts):
    for _ in range(num_accounts):
        username = generate_username()
        password = generate_password()
        email = generate_email()
        save_to_file(email, password, username)
if __name__ == "__main__":
    num_accounts = 1000
    generate_accounts(num_accounts)
