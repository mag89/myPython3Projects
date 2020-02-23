def cost(b):
    return (b - 4) ** 2

print(cost(4))

# numerical
def num_slope(b):
    h = 0.0001
    return (cost(b +h) - cost(b)) / h

print(num_slope(5))

def slope(b):
    return 2 * (b - 4) * 1 ** 1

print(slope(5))

b = 6


for i in range(100):
    print(b)
    b -= 0.1 * slope(b)