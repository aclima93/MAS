import itertools

def test_me(lista):
    num_comb = 0
    iterable = range(len(lista))
    for s in range(len(iterable)+1):
        for comb in itertools.combinations(iterable, s):
            num_comb += 1
            print(comb)
            for index in comb:
                print(lista[index])
    print(num_comb)

if __name__ == '__main__':
    test_me([1, 2, 3, 4, 5])