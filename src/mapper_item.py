#!/usr/bin/env python3

import sys

def mapper():
    for line in sys.stdin:
        data = line.strip().split("\t")
        if len(data) == 6:
            date, temps, store, item, cost, payment = data
            print(f"{item}\t{float(cost)}")

if __name__ == "__main__":
    mapper()
