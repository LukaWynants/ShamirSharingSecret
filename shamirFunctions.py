#importing the secrets library to generate randomly secure numbers
import secrets

class ShamirSharingSecret:

    def __init__(self, secret_key, threshold, num_of_shares):
        self.secret_key = secret_key
        self.threshold = threshold
        self.num_of_shares = num_of_shares
        self.coefficients = [secret_key] #the X values of the polinomial
        self.shares = []

    def generate_AES_key(self):
        pass


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

    

            
                





        

    



    