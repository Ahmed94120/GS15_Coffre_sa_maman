R = '0001011011100100010001100100111010111000101110011100110111110001'
blocks = [R[i:i+8] for i in range(0, len(R), 8)]

inv_blocks = []
for bloc in blocks:
    inv_blocks += [bloc[::-1]]

R_blocks = [R[i:i + 8] for i in range(0, 128, 8)][::-1]
print(inv_blocks)
print(R_blocks)

X = [36, 20, 5, 56, 50, 59, 0, 52, 30, 14, 9, 21, 27, 54, 38, 6, 37, 24, 25, 41, 47, 19, 32, 46, 57, 15, 34, 1, 39, 40, 44, 61, 12, 35, 48, 63, 31, 18, 28, 4, 11, 13, 53, 7, 23, 55, 33, 10, 62, 3, 49, 26, 2, 58, 51, 22, 17, 42, 60, 8, 43, 45, 29, 16]
Y = [0] * len(X)
for i, p in enumerate(X):
    Y[p] = i

print(Y)