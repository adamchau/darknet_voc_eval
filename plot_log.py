#!/usr/bin/env python
import argparse
import sys
import matplotlib.pyplot as plt
def plot_log():
    f = open("./train.log",'r')
    lines  = [line.rstrip("\n") for line in f.readlines()]
    # skip the first 3 lines
    lines = lines[3:]
    numbers = {'1','2','3','4','5','6','7','8','9','0'}
    iters = []
    loss_train = []
    loss_val=[]
    for line in lines:
        if line[0] in numbers:
            args = line.split(" ")
            if len(args) >3:
                iters.append(int(args[0][:-1]))
                loss_train.append(float(args[2]))
#                loss_val.append(float(args[1][:-1]))
    plt.plot(iters,loss_train)
#    plt.plot(iters,loss_val)
    plt.xlabel('iters')
    plt.ylabel('loss')
    plt.grid()
    plt.show()

if __name__ == "__main__":
    plot_log()
