import pandas as pd
import os
import re
import numpy as np
from collections import Counter

# user to input file name for analysis, and designate output file name
# please make sure the file is in the same directory with this script
file_input = input("Please enter your file name: ") + ".csv"
file_path = os.path.dirname(__file__)
input_file = os.path.join(file_path, file_input)

output_name = input('Output file name: ') + ".csv"
output_file = os.path.join(file_path, output_name)

dataset = pd.read_csv(file_input, header=None)
dataset_sequences = dataset.iloc[:, 2] #exported sequencing data should be in third column of Excel spreadsheet; change accordingly

#Search for barcodes flanking between two sequences
barcodes_list = []
for item in dataset_sequences:
    try:
        barcode_results = re.search('AAAAGCATAA(.*)GGAAAGGGGC', item).group(1)
        barcodes_list.append(barcode_results)
    except AttributeError:
        barcode_results = re.search('AAAAGCATAA(.*)GGAAAGGGGC', item)

#Counts number of unique barcodes from dataset
total_barcodes_count = len(dataset_sequences.index)
unique_barcodes_count = len(np.unique(np.array(barcodes_list)))

#Counts the number of counts per unique barcode
counts_per_unique_barcodes = Counter(barcodes_list) #dictionary

#save list of barcodes and export to Excel
# for barcode, count in counts_per_unique_barcodes.most_common():
col_1_title = "Barcodes"
col_2_title = "Number of Occurrences"
col_3_title = "Result Summary"

output_message = "The number of unique barcodes in this library is " + str(unique_barcodes_count)\
                 + ", out of the total reads of " + str(total_barcodes_count)
data = pd.DataFrame(list(counts_per_unique_barcodes.items()), columns=[col_1_title, col_2_title])
data.rename(columns={'3': 'Number of unique barcodes'}, inplace=True)

data[col_3_title] = pd.Series(dtype='str')
data.iloc[0, 2] = output_message

data.to_csv(output_file, index=False)

