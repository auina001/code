utrykk = input("Utrykk av i: ")
ledd = int(input("Ledd: "))

sum = 0

for i in range(ledd):
    sum += eval(utrykk)

print(sum)
