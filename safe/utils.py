from cryptography.fernet import Fernet
import base64
def encrypt_password(password,master_key):
    key = base64.b64encode(bytes('0'*(32-len(master_key)) + str(master_key), 'utf-8'))
    fernet = Fernet(key)
    return (fernet.encrypt(password.encode())).decode("utf-8")

def decrypt_password(password,master_key):
    key = base64.b64encode(bytes('0'*(32-len(str(master_key))) + str(master_key), 'utf-8'))
    password = str(password).encode("utf-8")
    fernet = Fernet(key)
    return (fernet.decrypt(password)).decode("utf-8")

print(len(encrypt_password('1111115678934@#$%11111111111111cdcsgvdgsvdjavsvdvsdvhasjvdjvsajvdjvasjdvjsavjddfhfjehfvjevjfvejfvefejjvjsavjdvsavfdhfvdshgfvdghfghfghdsvfhgdv','1233451223343434343434343')))
