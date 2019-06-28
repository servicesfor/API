import hashlib


def make_password(passwd_str):
    return hashlib.md5(("9@^"+passwd_str+'$&').encode()).hexdigest()


def check_password(passwd_str, encrypted_str):
    print(make_password(passwd_str))
    return make_password(passwd_str) == encrypted_str

if __name__ == '__main__':
    print(make_password('123456'))
