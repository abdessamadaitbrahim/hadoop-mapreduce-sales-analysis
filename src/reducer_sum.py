#!/usr/bin/env python3

import sys

def reducer():
    salesTotal = 0
    oldkey = None
    
    for line in sys.stdin:
        data = line.strip().split("\t")
        if len(data) == 2:
            thiskey, thissale = data
            if oldkey and oldkey != thiskey:
                print(f"{oldkey}\t{salesTotal}")
                salesTotal = 0
            oldkey = thiskey
            salesTotal += float(thissale)
    if oldkey is not None:
        print(f"{oldkey}\t{salesTotal}")

if __name__ == "__main__":
    reducer()
