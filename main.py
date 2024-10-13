from shamirFunctions import *  

num_of_shares = input(int("""
[INFO] The Number of shares is the amount of shares you will be creating from the secret
define the Number of shares: """)

threshold = input(int("""
[INFO] The threshold is the amount of shares you need to reconstruct the Key
define the threshold: """)

# Create an instance of the ShamirSharingSecret class
shamir = ShamirSharingSecret(threshold, num_of_shares)

# Generate the AES key and convert it to an integer
shamir.generate_AES_key()
shamir.AES_to_int()

# Generate polynomial coefficients based on the secret key
shamir.generate_polynomials()

# Print coefficients
print("Coefficients:", shamir.coefficients)

# Calculate shares
shamir.calculate_shares()

# Print shares
print("Shares:", shamir.shares)

shamir.reconstruct_secret()