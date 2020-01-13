#!/usr/bin/python3
import os
import glob
from colorama import Fore, Back, Style

inputs = glob.glob("in*")
inputs.sort()

TASK = "EXECUTABLE" # change it manually

compiled = os.system("g++ -std=c++14 -Wall -Wshadow -Wextra -DDK -g -fsanitize=address -fsanitize=undefined -D__GLIBCXX_DEBUG -o {} {}.cpp".format(TASK, TASK))

if compiled == 0:
    sample = 0
    for inp in inputs:
        print("Sample #{}:".format(str(sample)))
        os.system("./{} < in{} > my_out{}".format(TASK, str(sample), str(sample)))
        if open("out{}".format(str(sample)), "r").read() != open("my_out{}".format(str(sample)), "r").read().strip():
            print(Fore.RED + "Wrong answer!")
            print(Fore.WHITE + "Expected: ")
            print(open("out{}".format(str(sample)), "r").read())
            print("Output:")
            print(open("my_out{}".format(str(sample)), "r").read())
        else:
            print(Fore.GREEN + "Accepted!")
        print(Style.RESET_ALL)
        sample += 1

