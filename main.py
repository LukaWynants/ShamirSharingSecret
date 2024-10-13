from shamirFunctions import *

shamir = ShamirSharingSecret(secret_key=1234, threshold=3, num_of_shares=5)

shamir.generate_polynomials()

print(shamir.coefficients)

shamir.calculate_shares()

print(shamir.shares)