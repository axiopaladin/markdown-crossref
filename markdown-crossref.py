#!/usr/bin/python3

import os, sys  # , yaml

def read_inputs(args: list):
    """Return a list of all lines from all input files, concatenated."""
    inputlines = []
    for item in args:
        if os.path.isfile(item):
            with open(item, "r") as file:
                for line in file.readlines():
                    inputlines.append(line)
                inputlines.append("\n")
        else:
            print(f"'{item}' is not a file. Skipping...")
    return inputlines

def find_labels(lines: list):
    """Return a dict of labels and their positions."""
    labels = {}
    N = len(lines)
    for y in range(N): # line by line
        lStart = False
        line = lines[y]
        n = len(line)
        for x in range(1,n): # character by character
            if (not lStart) and (line[(x-1):(x+1)] == "{#"):
                # Searching for the opening `{#` of a label
                lStart = True
                open_position = x+1
            
            if lStart and (line[x] == "}"):
                # Searching for the closing `}` of a label
                lStart = False
                end_position = x-1
                fullslice = line[open_position:end_position]
                if " " in fullslice:
                    # in case it has other attributes, e.g. width=7in
                    label = line[open_position:].split(" ")[0]
                else:
                    label = line[open_position:end_position+1]
                
                if label in labels:
                    # lazy simple error reporter
                    print(f"WARNING! Label {label} was declared multiple times!")
                else:
                    labels[label.lower()] = (y, (open_position-2, end_position+2))
    # example output:
    # {'sec:title1': (0, (33, 46)),
    # 'sec:results': (3, (19, 52))}
    # where each entry is 'label': (line_num, (character_range))
    return labels

def find_refs(lines: list, labels: list):
    """Return a dict of refs and their positions"""
    refs = {}
    N = len(lines)
    for y in range(N): # line by line
        lStart = False
        line = lines[y]
        n = len(line)
        for x in range(1,n): # character by character
            if (not lStart) and (line[(x-1):(x+1)] == "[@"):
                # Searching for the opening `[@` of a ref
                lStart = True
                open_position = x+1
            
            if lStart and (line[x] == "]"):
                # Searching for the closing `]` of a ref
                lStart = False
                end_position = x-1
                label = line[open_position:end_position+1].lower()
                if label in labels:
                    if label in refs.keys():
                        refs[label].append(((y, (open_position-2, end_position+2))))
                    else:
                        refs[label] = [(y, (open_position-2, end_position+2))]
    # example output:
    # {"sec:title1": [(1,  (94, 107)), (4, (123, 136))],
    # "sec:results": [(4, (143, 157)), (4, (293, 307))]}
    return refs


# Debug: print output and results
inlines = read_inputs(sys.argv[1:])

sys.stdout.writelines(inlines)
print("Labels detected:")
outlabels = find_labels(inlines)
print(outlabels)
print("These slices are:")
for item in outlabels.values():
    #the exact parts to replace with `\label{sec:whatever}`
    print(inlines[item[0]][item[1][0]:item[1][1]])

outrefs = find_refs(inlines, outlabels.keys())
print("\nRefs detected:")
print(outrefs)
print("These slices are:")
for entry in outrefs:
    for item in outrefs[entry]:
        #the exact parts to replace with `\ref{sec:whatever}`
        print(inlines[item[0]][item[1][0]:item[1][1]])
