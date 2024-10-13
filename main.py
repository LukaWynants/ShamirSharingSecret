from shamirFunctions import *

# Input for number of shares and threshold
num_of_shares = int(input("[INFO] Define the number of shares: "))
threshold = int(input("[INFO] Define the threshold: "))

# Create an instance of the ShamirSharingSecret class
shamir = ShamirSharingSecret(threshold, num_of_shares)

running = True

while running:
    print("""
###################################################
##                     MENU                      ##
##                                               ##
## 1: Generate Secret                            ##
## 2: Generate Shares                            ##
## 3: Input Your Own Shares                      ##
## 4: Reconstruct Secret from Shares             ##
## 5: Exit                                       ##
##                                               ##
####################################################
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

    elif option == 4:
        reconstructed_secret = shamir.reconstruct_secret()
        print(f"[INFO] Reconstructed Secret: {reconstructed_secret}")

    elif option == 5:
        running = False  # Exit the loop

    else:
        print("[ERROR] Invalid option, please choose again.")