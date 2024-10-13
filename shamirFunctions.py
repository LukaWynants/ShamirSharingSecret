#importing the secrets library to generate randomly secure numbers
import secrets
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class ShamirSharingSecret:

    def __init__(self, threshold, num_of_shares):
        self.AES_key = 0
        self.secret_key = 0
        self.threshold = threshold
        self.num_of_shares = num_of_shares
        self.coefficients = [] #the X values of the polinomial
        self.shares = []

    def generate_AES_key(self):
        """
        A method to generate an AES key for encryption
        """
        # generate random AES key
        print("[INFO] Generating AES key...")
        
        self.AES_key = get_random_bytes(4)
        print(f"[INFO] KEY: {self.AES_key}")
        

    def AES_to_int(self):
        print("[INFO] Converting AES bytes to integer...")
        self.secret_key = int.from_bytes(self.AES_key, 'big')
        print(f"[INFO] KEY: {self.secret_key}")

        # adding the secret key as the first coefficient
        self.coefficients.append(self.secret_key)

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
            Reconstruct the secret from the given shares using Lagrange interpolation
            """
            #set the secret key at 0
            secret = 0

            k = len(self.shares)

            for n in range(k):
                x_n, y_n = self.shares[n]
                L_n = 1

                for m in range(k):
                    if m != n:
                        x_m, _ = self.shares[m]
                        L_n *= (0 - x_m) / (x_n - x_m)  # Use 0 to evaluate L_j at x=0

                secret += y_n * L_n

            print(f"[INFO] SECRET KEY calculated: {int(secret)}")

            #self.secret_key = secret

    

    

            
                





        

    



    