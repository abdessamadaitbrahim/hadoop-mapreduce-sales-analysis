#!/usr/bin/env python3

import sys

def reducer():
    maxSale = 0
    oldkey = None
    
    for line in sys.stdin:
        data = line.strip().split("\t")
        if len(data) == 2:
            thiskey, thissale = data
            if oldkey and oldkey != thiskey:
                print(f"{oldkey}\t{maxSale}")
                maxSale = 0
            oldkey = thiskey
            maxSale = max(maxSale, float(thissale))
    if oldkey != None:
        print(f"{oldkey}\t{maxSale}")
        
if __name__ == "__main__":
    reducer()
