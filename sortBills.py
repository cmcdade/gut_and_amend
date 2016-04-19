f1 = open('billScores.txt', 'r')
f2 = open('sortedScores', 'a+')

sorts = []

for line in f1:
    split = line.split(',')
    num = split[1]
    num = num.split()
    try:
        x = float(num[0])
    except ValueError:
        pass
    sorts.append((split[0], x))

sorted_by_second = sorted(sorts, reverse=True,key=lambda tup: tup[1])
for x in sorted_by_second:
    f2.write(x[0]+", "+str(x[1])+"\n")
