# Install Dependancies

    pip install pycryptodome

# Run Script
run:

    1. python main.py

You will be prompted to input 2 values in the beginning:

    a. Number of shares : This is the number of total shares 
    b. Threshold : This is the amount of shares needed to recover the Secret text

You will be led to a menu of choices

    1. Generate Secret -> if you have no secret this option generates one for you                      
    2. Generate Shares -> this option generates diffrent shares from your secret in a (x, y) format                        
    3. Input Your Own Shares -> this option allows you to input your own shares to then calculate the secret            
    4. Reconstruct Secret from Shares -> this option reconstructs the secret from the shares

example: 


sources:

https://mathworld.wolfram.com/LagrangeInterpolatingPolynomial.html