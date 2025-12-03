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
import HTPredBenchCreator
import structural_features_extractor as f2
import lfeaturesextractor
import csv_append as ca
import headers_list as hl

'''(Non Trojan = 0, Trojan = 1)'''


file_location_input = 's35932_T000_bench.txt'
name_of_file = 's35932_T000_bench.bench'

trojan_nontrojan = 1

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

def get_feature_data(input_file):
    r = HTPredBenchCreator.BenchToFeature(input_file)
    final_data = r.getfeatures()
    return final_data

def ensure_headers_and_append(csv_path, header_list, feature_row, force_write_headers=False):
    """
    Ensure header row exists in csv_path (write if missing/empty).
    Then append feature_row using csv_append.Append().
    If file exists and header differs, prints a warning. If force_write_headers=True it will overwrite header.
    """
    write_headers = False

    # decide whether to write headers
    if not os.path.exists(csv_path):
        print(f"[INFO] CSV '{csv_path}' does not exist. Will create and write headers.")
        write_headers = True
    else:
        try:
            if os.stat(csv_path).st_size == 0:
                print(f"[INFO] CSV '{csv_path}' exists but is empty. Will write headers.")
                write_headers = True
            else:
                # read first row to compare
                with open(csv_path, 'r', newline='') as fh:
                    reader = csv.reader(fh)
                    try:
                        existing_header = next(reader)
                    except StopIteration:
                        existing_header = []
                # if header differs, warn (or force rewrite if requested)
                if existing_header != [str(h) for h in header_list]:
                    msg = (f"[WARN] Existing CSV header differs from expected header. "
                           f"Existing cols: {len(existing_header)}, Expected cols: {len(header_list)}.")
                    print(msg)
                    if force_write_headers:
                        print("[INFO] force_write_headers=True — rewriting header (will overwrite first row).")
                        write_headers = True
                    else:
                        print("[INFO] Not rewriting header. Appending row anyway (be careful about column mismatch).")
        except Exception as e:
            print("[WARN] Could not inspect existing CSV header:", e)
            # fall back to writing headers to be safe
            write_headers = True

    # write header if needed
    if write_headers:
        try:
            with open(csv_path, 'w', newline='') as fh:
                writer = csv.writer(fh)
                writer.writerow(header_list)
            print(f"[OK] Wrote header to '{csv_path}' ({len(header_list)} columns).")
        except Exception as e:
            print("[ERROR] Failed to write header:", e)
            return

    # append the feature row using your csv_append module
    try:
        ca.Append(csv_path, header_list, feature_row)
        print(f"[OK] Appended feature row to '{csv_path}'.")
    except Exception as e:
        print("[ERROR] Failed to append feature row via csv_append.Append:", e)

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

    # Step 5 - Structural features

    print("---------- Starting Structural Features (BenchToFeature) -----------")

    # get per-wire primitive structural data (dict: feature_name -> {wire_name: value_or_list})
    structural_data = get_feature_data(file_location_input)

    print("---------- BenchToFeature OUTPUT (primitives) -----------")
    keys = list(structural_data.keys())
    print("Primitive structural keys (features):", keys)
    # find number of wires by checking any key's dict length
    if keys:
        example_key = keys[0]
        wire_names = list(structural_data[example_key].keys())
        print("Number of wires in structural output:", len(wire_names))
        print("\nSample per-wire primitive values (first 8 wires):")
        sample_wires = wire_names[:8]
        for w in sample_wires:
            # collect the value/list for each primitive key for this wire
            vals = []
            for k in keys:
                vals.append(structural_data[k].get(w))
            print(f"{w} ->", vals)
    else:
        print("No structural primitive keys found (empty structural_data).")

    print("---------- BenchToFeature Done -----------\n")

    # Step 6 - Structural expansion (convert primitive BenchToFeature -> expanded structural features) ===

    print("---------- Starting structural_features_extractor.extract_sf (expansion) -----------")

    # Expand primitives into the structural feature vector
    new_list = f2.extract_sf(structural_data)

    print("---------- structural_features_extractor Done -----------")

    # Sanity checks / quick previews
    print("Structural feature vector length:", len(new_list))
    # Small previews
    print("Preview (first 20 structural features):", new_list[:20])
    print("Preview (last 10 structural features):", new_list[-10:])

    # Append structural features to list_of_features (to keep pipeline consistent)
    try:
        list_of_features.extend(new_list)
        print("Structural features appended to list_of_features. Total features now:", len(list_of_features))
    except NameError:
        # if list_of_features doesn't exist (you may be running BenchToFeature-only run), just report
        print("Note: list_of_features not found in scope; structural features computed but not appended.")

    # Step 7 - L-features (from CO list)
    print("---------- Starting L-features extraction (lfeaturesextractor.getLfeatures) -----------")
    try:
        Lfeatures = lfeaturesextractor.getLfeatures(CO_list)
        print("---------- L-features extraction Done -----------")
        print("Number of L-features returned:", len(Lfeatures))
        print("Preview L-features (first 10):", Lfeatures[:10])
    except Exception as e:
        print("[ERROR] Failed to compute L-features:", e)
        Lfeatures = []

    # Append L-features to feature vector (if list_of_features exists)
    try:
        list_of_features.extend(Lfeatures)
        print("L-features appended. Total features now:", len(list_of_features))
    except NameError:
        print("Note: list_of_features not in scope; L-features computed but not appended.")

    # Step 8 - Append label (trojan / non-trojan)
    print("---------- Starting label append -----------")
    try:
        label_value = trojan_notrojan
        try:
            list_of_features.append(label_value)
            print("Label appended to feature vector:", label_value)
            print("Final feature vector length (after label):", len(list_of_features))
        except NameError:
            print("Note: list_of_features not in scope; label computed but not appended.")
    except Exception as e:
        print("[ERROR] Failed to append label:", e)

    # Final sanity checks
    print("---------- Final checks before append -----------")
    try:
        header_list = hl.Headers()
        print("Header count:", len(header_list))
        # list_of_features may not exist if you ran only BenchToFeature; guard it
        if 'list_of_features' in locals():
            print("Feature vector length:", len(list_of_features))
            if len(header_list) != len(list_of_features):
                print(f"[WARN] header length ({len(header_list)}) != feature vector length ({len(list_of_features)}).")
                print("Mismatch = ", len(list_of_features) - len(header_list))
            else:
                print("[OK] header and feature-vector length match. Ready to append to CSV.")
        else:
            print("Note: list_of_features not available in locals(); cannot compare header vs features.")
    except Exception as e:
        print("[WARN] Could not load headers_list to compare lengths:", e)
        header_list = None

    # Only proceed if header_list is available and list_of_features exists
    if header_list is not None and 'list_of_features' in locals():
        csv_path = 'data.csv'   # change path here if you want a different file
        # If you want to force rewrite header when it mismatches, pass force_write_headers=True
        ensure_headers_and_append(csv_path, header_list, list_of_features, force_write_headers=False)
    else:
        print("[INFO] Skipping CSV write: header_list or list_of_features not available.")

    

main_function(file_location_input, name_of_file, trojan_nontrojan)