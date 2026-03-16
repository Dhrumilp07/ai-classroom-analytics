API_KEY = "classroom_secure_key"

def verify(key):
    if key == API_KEY:
        return True
    return False