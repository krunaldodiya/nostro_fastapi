import random

class ManagerHelper:
  @classmethod
  def generate_temp_password(cls, length:int=12):
    if length < 4:
        raise ValueError("Password length must be at least 4 characters")

    valid_chars = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    password = ["M", "t", "5", "*"]
    
    for _ in range(4, length):
        password.append(random.choice(valid_chars))  

    return "".join(password)