import random

from decimal import Decimal,getcontext

# Set higher precision for Decimal calculations
getcontext().prec = 1000  # Increase precision
 
# it denotes the end value of coeff
FIELD_SIZE = 10**5
 
def polynom_value(x, coefficients):
    # Generates the value of y from x and coeff given
    point = 0
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        point += x ** coefficient_index * coefficient_value
    return point
 
 
def coeff(t, secret):
    # Get random coeff for the equation
    coeff = [random.randrange(0, FIELD_SIZE) for _ in range(t - 1)]
    coeff.append(secret)
    return coeff
 
 
def generate_shares(n, m, secret):
    # here n is total split, m is threshold
    coefficients = coeff(m, secret) # We get random coeff
    shares = []
    
    for _ in range(1, n+1):
        x = random.randrange(1, FIELD_SIZE) 
        shares.append((x, polynom_value(x, coefficients))) # all the points
 
    return shares
 
def reconstruct_secret(shares):
    sums = 0

    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)

        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                # Convert to Decimal before division to maintain precision
                prod *= Decimal(xi)/Decimal(xi-xj)

        prod *= Decimal(yj)
        sums += prod

    return int(round(sums))

def ShamirSecret(secret,total_shares,threshold):
    shares = generate_shares(total_shares, threshold, secret) 
    return shares

 
# Driver code
if __name__ == '__main__':
 
    # (3,5) sharing scheme
    threshold, total_shares = 3, 5
    secret = 1234
    print(f'Original Secret: {secret}')
 
    # Phase I: Generation of shares
    shares = generate_shares(total_shares, threshold, secret) 
    print(shares)
    print(f'Shares: {", ".join(str(share) for share in shares)}')
 
    # Phase II: Secret Reconstruction
    pool = random.sample(shares, threshold) # Nothing but takes random 3 shares from total
    print(f'Combining shares: {", ".join(str(share) for share in pool)}')
    print(f'Reconstructed secret: {reconstruct_secret(pool)}')

    # shares = [[41995, 88005544978243525395867303165512797245133915281764755685631547528387408949851], [96683, 88005544978243525395867303165512797245133915281764755685631547697012089061179], [17867, 88005544978243525395867303165512797245133915281764755685631547496273050914715], [80207, 88005544978243525395867303165512797245133915281764755685631547632211978771015], [72527, 88005544978243525395867303165512797245133915281764755685631547606131346694215]]
    # value = reconstruct_secret(shares)
    # print(value)
    # print(value.to_bytes((value.bit_length() + 7) // 8, byteorder='big'))