"""
fifi_reclass_torch.py

Reclassifies FindItFixIt service requests using the retrained model.

TORCH VERSION

"""

import os, argparse, sys, pandas as pd, time
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def append_line_to_file(file_path, line):
    # Open the file in append mode ('a+')
    with open(file_path, 'a+') as file:
        # Move the cursor to the end of the file
        file.seek(0, 2)
        # If the file is not empty, add a newline before appending
        if file.tell() > 0:
            file.write('\n')
        # Append the line to the file
        file.write(line)

def main(blocknum, startrow, endrow):

    # Try to manage memory
    device_map="auto"
    torch_dtype=torch.float16

    # Set parallelism explicitly to avoid warning
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    
    # Check for GPU
    print("GPU available?", torch.cuda.is_available())
    devices = [i for i in range(torch.cuda.device_count())]
    device_names = [torch.cuda.get_device_name(d) for d in devices]
    print(f"Available GPUs: {device_names}")

    # Record the run times to a log file
    logf = 'fifi_torch_running_times.txt'
    start_time = time.time()
    
    file_path = ''
    unlabelledf = 'shuffled_unlabelled.csv'
    
    unldf = pd.read_csv(file_path + unlabelledf)
    
    # Run the routine on blocks of 500 -- memory can't handle more
#    blocknum = 6
#    startrow = 35000
#    endrow = 40000
    samplesize = endrow - startrow
    unlsubset = unldf.iloc[startrow:endrow]
    
    texts = unlsubset['text'].tolist()
    servreqids = unlsubset['servreqid'].tolist()
    
    # Get tokenizer from pre-trained model and tokenize texts
    tokenizer = AutoTokenizer.from_pretrained("mjbeattie/fifi_classification")
    print("Tokenizing input texts")
    inputs = tokenizer(texts, truncation=True, padding=True, max_length=512, return_tensors="pt")

    # Get model for reclassification
    print("Loading model")
    model = AutoModelForSequenceClassification.from_pretrained("mjbeattie/fifi_classification")

    # Predict the classification of the test text
    print("Reclassifying texts")
    with torch.no_grad():
        logits = model(**inputs).logits
    
    # Record the end time
    end_time = time.time()
    
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    runtime_entry = "Blocknum: " + str(blocknum) + " Startrow: " + str(startrow) + " Endrow: " + str(endrow) + " Classified texts: " + str(samplesize) + " Elapsed time: " + str(elapsed_time)
    append_line_to_file(logf, runtime_entry)
    
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
    
    # Get predicted labels
    predicted_labels = torch.argmax(logits, dim=1)
    predicted_labels = predicted_labels.tolist()
    
    # Join new labels to original dataset
    relabelleddf = pd.DataFrame({'servreqid': servreqids, 'newlabel': predicted_labels})
    unlsubset = pd.merge(unlsubset, relabelleddf, on='servreqid', how='inner')

    # Add the new labels and IDs back to the sample and save
    label2id = {
        'SPU-Graffiti Report': 0,
        'SEA-Unauthorized Encampment': 1,
        'SDOT-Abandoned Vehicle': 2,
        'SPU-Illegal Dumping Report': 3,
        'SPD-Parking Enforcement': 4,
        'SPU-Clogged Drains': 5,
        'SPR-Maintenance': 6,
        'CSB-General Inquiry': 7,
        'SDOT-Sign and Signal Maintenance': 8,
        'SPU-Public Litter Cans': 9,
        'SDOT-Shared Micromobility': 10,
        'SDOT-Pothole': 11,
        'SEA-Overgrown Vegetation': 12,
        'SCL-Streetlight Report': 13,
        'FAS-SAS-Dead Animal': 14
    }
    
    label2iddf = pd.DataFrame(label2id.items(), columns=['newid', 'newlabel'])
    
    # Add new IDs to original dataset and save to a file
    unlsubset = pd.merge(unlsubset, label2iddf, on='newlabel', how='inner')
    savef = 'reclassified_fifi_reqs_' + str(blocknum) + '.csv'
    unlsubset.to_csv(file_path + savef, index=False)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--blocknum", type=int, required=True, help="Enter the block number", default=999)
    parser.add_argument("--startrow", type=int, required=True, help="Enter the startrow", default=40000)
    parser.add_argument("--endrow", type=int, required=True, help="Enter the endrow", default=45000)
    args = parser.parse_args()
    print('Running classification with blocknum=', args.blocknum, "startrow=", args.startrow, "endrow=", args.endrow)
    main(args.blocknum, args.startrow, args.endrow)
