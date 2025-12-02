import time
from os.path import isfile, join
from enum import Enum
import sys
import os
import getfunctionalfeatures as funf

'''(Non Trojan = 0, Trojan = 1)'''

file_location_input = 'test_small.bench.txt'
name_of_file = 'test_small.bench.bench'
trojan_nontrojan = 1


def main_function(file_location_input, name_of_file, trojan_notrojan):

    trojan_notrojan = str(trojan_notrojan)
    funf.getFunctionalfeatures(file_location_input,trojan_notrojan, name_of_file)

main_function(file_location_input, name_of_file, trojan_nontrojan)