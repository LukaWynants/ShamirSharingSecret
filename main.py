from shamirFunctions import *  

# Create an instance of the ShamirSharingSecret class
shamir = ShamirSharingSecret(threshold=3, num_of_shares=5)

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