#importing the secrets library to generate randomly secure numbers
import secrets
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from sympy import mod_inverse
import hashlib

class ShamirSharingSecret:

    def __init__(self, threshold, num_of_shares):
        self.AES_key = 0
        self.secret_key = 0
        self.ciphertext = ""
        self.cipher = ""
        self.tag = ""
        self.threshold = threshold
        self.num_of_shares = num_of_shares
        self.coefficients = [] #the X values of the polinomial
        self.shares = []
        self.secret_message = ""
        self.decrypted_secret_message = ""

    def generate_AES_key(self):
        """
        A method to generate an AES key for encryption
        """
        # generate random AES key
        print("[INFO] Generating secret key...")
        
        self.AES_key = get_random_bytes(16)
        
        print(f"[INFO] KEY: {self.AES_key}")

    def AES_to_int(self):
        print("[INFO] Converting secret bytes to integer...")
        self.secret_key = int.from_bytes(self.AES_key, 'big')
        print(f"[INFO] KEY: {self.secret_key}")

        # adding the secret key as the first coefficient
        self.coefficients.append(self.secret_key)

    def int_to_AES(self):
        """ 
        A method which converts a AES key back to bytes
        """
        print("[INFO] Reversing integer back to AES secret bytes...")
 
        self.AES_key = self.secret_key.to_bytes(16, 'big')
        print(f"[INFO] Reversed KEY: {self.AES_key}")

    def encrypt_secret_message(self):
        """
        A method which encrypts the secret message to a cipher text
        """
        self.secret_message = input("[INFO] Input a secret message: ")
        print(f"[NOTE] Encrypting secret message: {self.secret_message}")
        # create a fixed nonce from the private key
        nonce = hashlib.sha256(self.AES_key).digest()[:16]
        print(f"[NOTE] nonce generated: {nonce}")
        self.cipher = AES.new(self.AES_key, AES.MODE_EAX, nonce=nonce)
        self.ciphertext, self.tag = self.cipher.encrypt_and_digest(str.encode(self.secret_message))

        tag = self.tag.hex()
        encrypted_message = self.ciphertext.hex()

        print(f"[NOTE] tag: {tag}")
        print(f"[NOTE] encrypted message: {encrypted_message}")

    def decrypt_secret_message(self):
        """
        A method to decrypt the secret message
        """
        set_encrypted_message = input("[NOTE] Do you wish to input your own encrypted message? (Y/N)")
        
        if set_encrypted_message.lower() == "y":

            encrypted_message = input("[INFO] Input an encrypted message (in HEX): ")
            self.ciphertext = bytes.fromhex(encrypted_message)
            tag = input("[NOTE] input tag (in HEX): ")
            self.tag = bytes.fromhex(tag)

        print(f"[NOTE] Decrypting Encrypted message: {self.ciphertext}")
        nonce = hashlib.sha256(self.AES_key).digest()[:16]
        print(f"[NOTE] nonce generated: {nonce}")

        self.cipher = AES.new(self.AES_key, AES.MODE_EAX, nonce=nonce)
        self.decrypted_secret_message = self.cipher.decrypt_and_verify(self.ciphertext, self.tag)
        print(f"[NOTE] decrypted message: {self.decrypted_secret_message}")


    def generate_polynomials(self):
        """
        A method which generates random values for coefficients of a polynomial
        
        Threshold: int = the threshold value determines how many shares are needed to recover the secret_key
        The polynomial used in Shamir's Secret Sharing has a degree of:

            k - 1
        
        where k is the minimum number of shares required to reconstruct the secret also called the threshold.
        For example, if you need 3 shares to reconstruct the secret, the polynomial will be of degree 2 and will take the shape:

            f(x) = ax^2 + bx + c
        
            to find the value of c (secret) you will need atleast 3 coordinates of the curve

        """
        if self.secret_key == 0:
            print("[!] AES secret key not set/generated...")
            print("[INFO] generate your AES key before calculating your shares")

        else:
            # generate k-1 coefficients
            for i in range(self.threshold - 1):
                self.coefficients.append(secrets.randbelow(256))

    def calculate_shares(self):
        """
        A method which calculates the shares in as a coordinate on a polynomial -> (x,y) format

        """
        # create the amount of shares based on num_of_shares
        for x in range(1, self.num_of_shares + 1):

            y = 0

            # looping over the coeficcients and mapping them with an index: (degree, coeff) eg. (1, coeff1), (2, coeff2) ... (n, coeffn)
            for degree, coefficient in enumerate(self.coefficients):
                
                # calculating the y values for the polynomial using the X values
                y += (coefficient * (x**degree))

            # storing the x,y valuies as a tuple in the shares list
            self.shares.append((x,y))

    def reconstruct_secret(self):
        """
        A method which Reconstructs the secret from the given shares using Lagrange interpolation.
        """
        # Set the prime modulus to a large prime number greater than the secret key
        prime_modulus = 2**257 - 1  # Example of a large prime

        secret = 0
        k = len(self.shares)

        print(f"[INFO] Calculating secret key with modulus {prime_modulus}...")

        for n in range(k):
            x_n, y_n = self.shares[n]
            L_n = 1

            for m in range(k):
                if m != n:
                    x_m, _ = self.shares[m]
                    # Calculate Lagrange basis polynomial in modular arithmetic
                    L_n *= (0 - x_m) * mod_inverse(x_n - x_m, prime_modulus)
                    L_n %= prime_modulus

            # Add contribution of current share to the secret
            secret += y_n * L_n
            secret %= prime_modulus

        print(f"[INFO] SECRET KEY calculated: {secret}")
        self.secret_key = secret

    

    

            
                





        

    



    