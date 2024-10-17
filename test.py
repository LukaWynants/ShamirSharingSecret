from sympy import mod_inverse
import secrets
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class ShamirSharingSecret:

    def __init__(self, threshold, num_of_shares, prime=257):  # Adding prime field
        self.AES_key = 0
        self.secret_key = 0
        self.threshold = threshold
        self.num_of_shares = num_of_shares
        self.coefficients = []  # the X values of the polynomial
        self.shares = []
        self.prime = prime  # A prime for modular arithmetic

    def generate_AES_key(self):
        """A method to generate an AES key for encryption."""
        print("[INFO] Generating secret key...")
        self.AES_key = get_random_bytes(4)
        print(f"[INFO] KEY: {self.AES_key}")

    def AES_to_int(self):
        """Converting secret bytes to integer."""
        print("[INFO] Converting secret bytes to integer...")
        self.secret_key = int.from_bytes(self.AES_key, 'big')
        print(f"[INFO] KEY: {self.secret_key}")

        # Adding the secret key as the first coefficient
        self.coefficients.append(self.secret_key)

    def generate_polynomials(self):
        """Generates random values for coefficients of a polynomial."""
        if self.secret_key == 0:
            print("[!] AES secret key not set/generated...")
            print("[INFO] Generate your AES key before calculating your shares")
        else:
            # Generate k-1 coefficients
            for i in range(self.threshold - 1):
                self.coefficients.append(secrets.randbelow(256))

    def calculate_shares(self):
        """Calculates the shares as (x, y) coordinates on a polynomial."""
        # Create the number of shares based on num_of_shares
        for x in range(1, self.num_of_shares + 1):
            y = 0

            # Looping over the coefficients and calculating the y-values
            for degree, coefficient in enumerate(self.coefficients):
                y += (coefficient * (x**degree)) % self.prime

            # Storing the (x, y) values as a tuple in the shares list
            self.shares.append((x, y))

    def reconstruct_secret(self):
        """Reconstructs the secret from the given shares using Lagrange interpolation."""
        if len(self.shares) < self.threshold:
            print("[!] Not enough shares provided to reconstruct the secret.")
            return None

        print(f"[INFO] Reconstructing secret key using Lagrange interpolation...")
        
        x_values, y_values = zip(*self.shares)  # Split shares into x and y values
        secret = lagrange_interpolation(0, x_values, y_values, self.prime)

        print(f"[INFO] SECRET KEY calculated: {int(secret)}")
        self.secret_key = secret
        return secret


def lagrange_interpolation(x, x_values, y_values, prime):
    """Lagrange interpolation to reconstruct the secret."""
    total = 0
    k = len(x_values)
    
    for i in range(k):
        xi, yi = x_values[i], y_values[i]
        li = yi
        
        for j in range(k):
            if i != j:
                xj = x_values[j]
                li *= (x - xj) * mod_inverse(xi - xj, prime)
                li %= prime
                
        total += li
        total %= prime
        
    return total

if __name__ == "__main__":
    num_of_shares = int(input("[INFO] Define the number of shares: "))
    threshold = int(input("[INFO] Define the threshold: "))

    # Create an instance of the ShamirSharingSecret class
    shamir = ShamirSharingSecret(threshold, num_of_shares)

    running = True

    while running:
        print("""
#####################################################
##                      MENU                       ##
##                                                 ##
## 1: Generate Secret                              ##
## 2: Generate Shares                              ##
## 3: Input Your Own Shares and reconstruct Secret ##
## 4: Reconstruct Secret from Shares               ##
## 5: Re-enter Number of shares & threshold        ##
## 0: Exit                                         ##
##                                                 ##
#####################################################
""")
        option = int(input("[INFO] Choose an option: "))

        if option == 1:
            # Generate the AES key and convert it to an integer
            shamir.generate_AES_key()
            shamir.AES_to_int()

        elif option == 2:
            # Generate polynomial coefficients based on the secret key
            shamir.generate_polynomials()

            # Print coefficients
            print("[INFO] Coefficients:", shamir.coefficients)

            # Calculate shares
            shamir.calculate_shares()

            # Print shares
            print("[INFO] Shares:", shamir.shares)

        elif option == 3:
            # Clearing the shares
            shamir.shares = []
            
            print(f"[INFO] Enter {shamir.threshold} shares:")
            for i in range(1, shamir.threshold + 1):  # Include the last share
                x = int(input(f"[INFO] Value x{i}: "))
                y = int(input(f"[INFO] Value y{i}: "))
                shamir.shares.append((x, y))

            reconstructed_secret = shamir.reconstruct_secret()

        elif option == 4:
            reconstructed_secret = shamir.reconstruct_secret()

        elif option == 5:
            num_of_shares = int(input("[INFO] Define the number of shares: "))
            threshold = int(input("[INFO] Define the threshold: "))
            shamir = ShamirSharingSecret(threshold, num_of_shares)

        elif option == 0:
            running = False  # Exit the loop

        else:
            print("[!] Invalid option, please choose again.")