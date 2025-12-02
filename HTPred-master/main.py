import time
from os.path import isfile, join
from enum import Enum
import sys
import os
import csv
from collections import defaultdict

import getfunctionalfeatures as funf
import string_processing as sp
import features_extractor as f1

'''(Non Trojan = 0, Trojan = 1)'''

file_location_input = 'medium_test.bench.txt'
name_of_file = 'medium_test.bench.bench'
trojan_nontrojan = 0

def get_raw_list_features(name_of_file):

    columns = defaultdict(list)  # each value in each column is appended to a list

    with open(name_of_file) as f:
        reader = csv.DictReader(f)  # read rows into a dictionary format
        for row in reader:  # read a row as {column1: value1, column2: value2,...}
            for (k, v) in row.items():
                if(k=="Wire"):
                    continue
                columns[k].append(float(v))  # append the value into the appropriate list
                # based on column name k

    super_list = []

    super_list.append(columns['Controllability0'])
    super_list.append(columns['Controllability1'])
    super_list.append(columns['Observability'])
    super_list.append(columns['Prob0'])
    super_list.append(columns['Prob1'])

    return super_list

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
    time_elapsed = end_time - start_time
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

    # Step 3 - Get Raw List Features
    print("---------- Starting Getting Raw List Features -----------")

    if(trojan_notrojan=="0"): # Non Trojan
        path = "../functional_results_non_trojan/"
    else:
        path = "../functional_results_trojan/"

    files = os.listdir(path)
    raw_feature_list = []
    for f in files:
        if(name_of_file in f):
            new_path = join(path, f)
            raw_feature_list = get_raw_list_features(new_path)
            break

    if(raw_feature_list == []):
        raise Exception('File Functional Feature not found ! ')

    CC0_list = raw_feature_list[0]
    CC1_list = raw_feature_list[1]
    CO_list = raw_feature_list[2]
    P0_list = raw_feature_list[3]
    P1_list = raw_feature_list[4]

    print("---------- Getting Raw List Features Done -----------")

    print("\n---------- RAW FUNCTIONAL FEATURES OUTPUT -----------")

    print(f"Matched functional CSV file: {new_path}\n")

    print(f"Number of wires detected in functional features: {len(CC0_list)}")

    print("\n--- Controllability 0 (CC0) ---")
    print("First 10 values:", CC0_list[:10])
    print("Min:", min(CC0_list), "Max:", max(CC0_list))

    print("\n--- Controllability 1 (CC1) ---")
    print("First 10 values:", CC1_list[:10])
    print("Min:", min(CC1_list), "Max:", max(CC1_list))

    print("\n--- Observability (CO) ---")
    print("First 10 values:", CO_list[:10])
    print("Min:", min(CO_list), "Max:", max(CO_list))

    print("\n--- Probability 0 (P0) ---")
    print("First 10 values:", P0_list[:10])
    print("Min:", min(P0_list), "Max:", max(P0_list))

    print("\n--- Probability 1 (P1) ---")
    print("First 10 values:", P1_list[:10])
    print("Min:", min(P1_list), "Max:", max(P1_list))

    print("----------------------------------------------------\n")

    # Step 4 - Extract Features
    print("---------- Starting Features Extraction -----------")
    list_of_features = f1.FeatureExtractor(final_primary_inputs_list,
                                            final_primary_outputs_list, 
                                            final_gates_list,
                                            gate_list_input,
                                            gate_list_output,
                                            gate_list_name,
                                            time_elapsed,
                                            name_of_file,
                                            CC0_list,
                                            CC1_list,
                                            CO_list,
                                            P0_list,
                                            P1_list)
    print("---------- Features Extraction Done -----------")

    print("\n---------- FEATURE EXTRACTOR OUTPUT (246 features) -----------")
    print(f"Number of features returned: {len(list_of_features)}")

    # Print first 20 features for preview
    # print("\nFirst 20 features:")
    # print(list_of_features[:20])

    # # Print last 10 features for preview
    # print("\nLast 10 features:")
    # print(list_of_features[-10:])

    # FULL PRINT (optional – uncomment if you want everything)
    print("\nFull feature list:")
    print(list_of_features)

    print("--------------------------------------------------------------\n")

main_function(file_location_input, name_of_file, trojan_nontrojan)