import hmac 
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet
import base64

data_dir = Path(__file__).parent / "data"
data_dir.mkdir(parents=True, exist_ok=True)

data_file = data_dir / "hash-info.bin"
data_file.touch()

class Encrypt:
    
    def __init__(self, password):
        self.password = password
        
        hash_key = hashlib.sha256(password.encode()).digest()
        prep_key = base64.urlsafe_b64encode(hash_key)
        self.fernet = Fernet(prep_key)
    
    def encoder(self, value):
        self.value = value
 
        encoded_value = self.value.encode()

        encrypted_value = self.fernet.encrypt(encoded_value)

        return(encrypted_value + b"\n")
    
    def decode(self, value):
        try:
            decrypted_value = self.fernet.decrypt(value).decode()
        except:
            decrypted_value = False
        return(decrypted_value)
