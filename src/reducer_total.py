#!/usr/bin/env python3

import sys

def reducer():
    totalSales = 0
    totalCount = 0
    
    for line in sys.stdin:
        data = line.strip().split("\t")
        if len(data) == 2:
            thiskey, thissale = data
            totalSales += float(thissale)
            totalCount += 1
    print(f"Total Sales: {totalSales}")
    print(f"Total Count: {totalCount}")
    
if __name__ == "__main__":
    reducer()
