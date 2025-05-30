def get_token():
    with open('get_token/token.txt') as file:
        token = file.readline()
    return token

API_TOKEN = get_token()