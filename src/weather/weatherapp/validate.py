import re


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True
    else:
        return False

def validate_password(password):
    pattern = r'^(?=.*[a-zA-Z0-9])(?=.*[!@#$%^&*()-_=+])[a-zA-Z0-9!@#$%^&*()-_=+]{8,}$'
    
    if re.match(pattern, password):
        return True
    else:
        return False
    
def validate_city(city):
    if city.isalpha():
        return True
    else:
        return False