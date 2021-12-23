#!/usr/bin/env python3

import timeit

start = timeit.default_timer()

l = [1,2,3,5555,5456,54654151,554654,2,16,1866,31,6,161,51,554,10556]

for i in range(100000000):
    if i in l:
        print('pog')

end = timeit.default_timer()

print(end - start)
