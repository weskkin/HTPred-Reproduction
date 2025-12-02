import time
from os.path import isfile, join
from enum import Enum
import sys
import os

import getfunctionalfeatures as funf
import string_processing as sp

'''(Non Trojan = 0, Trojan = 1)'''

file_location_input = 'test_small.bench.txt'
name_of_file = 'test_small.bench.bench'
trojan_nontrojan = 1


def main_function(file_location_input, name_of_file, trojan_notrojan):

    # Turn label to a string
    trojan_notrojan = str(trojan_notrojan)

    # Step 1 - Functional Features Extraction
    print("---------- Starting Functional Features Extraction -----------")
    funf.getFunctionalfeatures(file_location_input,trojan_notrojan, name_of_file)
    print("---------- Functional Features Extraction Done -----------")
    print("---------- Results are in functional_results_x folders -----------")

    # Step 2 - String processing
    start_time = time.time()
    print("---------- Starting String Processing -----------")

    (final_gates_list_2,
     final_gates_list,
     super_list_gates,
     mighty_raju_list,
     final_primary_inputs_list,
     final_primary_outputs_list,
     gate_list_input,
     gate_list_output,
     gate_list_name) = sp.StringProcessing(file_location_input)
     
    end_time = time.time()
    print("---------- String processing Done -----------")

    print("\n---------- String Processing OUTPUT -----------")
    print("final_gates_list_2:", final_gates_list_2)
    print("final_gates_list:", final_gates_list)
    print("super_list_gates:", super_list_gates)
    print("mighty_raju_list:", mighty_raju_list)
    print("final_primary_inputs_list:", final_primary_inputs_list)
    print("final_primary_outputs_list:", final_primary_outputs_list)
    print("gate_list_input:", gate_list_input)
    print("gate_list_output:", gate_list_output)
    print("gate_list_name:", gate_list_name)
    print("-----------------------------------------------")

main_function(file_location_input, name_of_file, trojan_nontrojan)