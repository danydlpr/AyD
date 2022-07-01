from entropymdlp.mdlp import MDLP
mdlp = MDLP()

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]

print(mdlp.find_cut_index(x, y))


