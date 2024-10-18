from shamirFunctions import *

# Input for number of shares and threshold
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
## 3: Encrypt the secret message                   ##
## 4: Input Your Own Shares and reconstruct Secret ##
## 5: Decrypt message                              ##
## 6: Reconstruct Secret key from Shares           ##
## 7: Re-enter Number of shares & threshold        ##
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
        shamir.encrypt_secret_message()

    elif option == 4:
        # Clearing the shares
        shamir.shares = []
        
        print(f"[INFO] Enter {shamir.threshold} shares:")
        for i in range(1, shamir.threshold + 1):  # Include the last share
            x = int(input(f"[INFO] Value x{i}: "))
            y = int(input(f"[INFO] Value y{i}: "))
            shamir.shares.append((x, y))

        shamir.reconstruct_secret()
        shamir.int_to_AES()

    elif option == 5:
        shamir.decrypt_secret_message()


    elif option == 6:
        shamir.reconstruct_secret()
        shamir.int_to_AES()

    elif option == 7:
        num_of_shares = int(input("[INFO] Define the number of shares: "))
        threshold = int(input("[INFO] Define the threshold: "))
        shamir = ShamirSharingSecret(threshold, num_of_shares)

    elif option == 0:
        running = False  # Exit the loop

    else:
        print("[!] Invalid option, please choose again.")