"""
Author: Chukwunazaekpere Emmanuel Obioma
Written for: Group 3
Nationality: Biafran
Email-1: chukwunazaekpere.obioma@ue-germany.de 
Email-2: ceo.naza.tech@gmail.com
************************************************
Course: Software Optimisation
Written: June 15th 2024
Due: June 30th 2024
"""

from datetime import datetime
import math
from .base_class import BaseClass


class ElGamalEncryptionAlgorithm(BaseClass):
    def __init__(self, private_key: int, plain_message_file_name:str):
        super().__init__()
        self.private_key = private_key
        self.public_key_file_name = "./files/public_keys.txt"
        self.encoded_message_file_name = "./files/encoded_message.txt"
        self.encrypted_message_file = "./files/encrypted_message.txt"
        self.plain_message = plain_message_file_name
        self.secret_key_file_name = "./files/secret_key.txt" 
        self.secret_key = "" 
        self.primitive_root = ""
        self.public_key = "" 
        self.large_prime = "" 
        self.encryption_dictionary = {} #dictionary where plain-character is key & encrypted character is the value. This is to reduce the extra time taken for excrypting plain characters that have been encrypted already

    
    
    def _secret_key_generator(self):
        """Generate secret key for encryption"""
        self.log_info("\n\t ElGamalEncryptionAlgorithm is generating a secret key for encryption...")
        public_key_content = self._file_helper(file_mode="rl",file_name=self.public_key_file_name)# get content written to the public key file
        large_prime = self._get_line_prop(public_key_content, "prime")
        public_key = self._get_line_prop(public_key_content, "generator")#public key generated during key generation
        primitive_root = self._get_line_prop(public_key_content, "primitive")
        pub_key_int = int(public_key)
        large_prime_int = int(large_prime)
        primitive_root_int = int(primitive_root)

        public_key_power = math.pow(pub_key_int, self.private_key)
        secret_key = int(public_key_power) % large_prime_int
        # secret_key_int = int(secret_key)
        self._file_helper(file_mode="w", file_name=self.secret_key_file_name, content="")
        self._file_helper(file_name=self.secret_key_file_name, file_mode="a+", content=f"\n\t Secret Key During Encryption:\n {str(secret_key)}",)
        self.secret_key = secret_key
        self.public_key = pub_key_int
        self.large_prime = large_prime_int
        self.primitive_root = primitive_root_int
        self.log_info("\n\t Secret key has been successfully generated...")

    def _generate_encrypter_public_key(self):
        self._secret_key_generator()
        primitive_power = math.pow(self.primitive_root, self.private_key)
        public_key = int(primitive_power) % self.large_prime 
        self._file_helper(file_mode="a+", file_name=self.public_key_file_name, content=f"\n\t Encrypter Public Key:\n {str(public_key)}")
        return public_key

    def required_char(self, char:str, char_to_write: str):
        req_char = ""
        if char == '.':
            req_char = f"{char_to_write} \n"
        else:
            req_char = char_to_write
        return f"{req_char}-"

    def encrypt_message(self):
        start_time = datetime.now()
        self.log_info(f"\n\t Encryption started: {start_time.ctime()}")
        self._generate_encrypter_public_key()
        plain_text = self._file_helper(file_mode="r", file_name=self.plain_message)
        self._file_helper(file_mode="w", file_name=self.encrypted_message_file, content="")
        for char in plain_text:
            char_to_write = str(char)
            if char != " ":
                encrypted_char = ""
                try:
                    encrypted_char = self.encryption_dictionary[char]
                    char_to_write = encrypted_char
                except:
                    char_to_write = ord(char)
                    encrypted_char = self.secret_key*char_to_write % self.large_prime
                    char_to_write = encrypted_char
                    self.encryption_dictionary[char] = char_to_write
            self._file_helper(file_mode="a+", file_name=self.encrypted_message_file, content=self.required_char(char=char, char_to_write=char_to_write))
        self.log_info(f"\n\t Encryption finished: {datetime.now()}")