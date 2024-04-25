"""
fifi_inference_torch.py

Uses a pretrained model to reclassify service requests submitted to the city of Seattle
using the FindItFixIt application.

TORCH VERSION

"""

import os, argparse, sys
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def main(fileout):

    # Set parallelism explicitly to avoid warning
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    
    f = open(fileout, 'w', encoding='utf8')
    f.write("Starting routine")
    print("Starting routine")
    texts = ["There is a dead dog.", "Somebody tagged the wall of my store", "There are tents blocking the sidewalk of my business",
             "The streetlight in front of my house is out"]
    
    # Load the retrained tokenizer and tokenize the input
    tokenizer = AutoTokenizer.from_pretrained("mjbeattie/fifi_classification")
    
    inputs = tokenizer(texts, truncation=True, padding=True, max_length=512, return_tensors="pt")
    
    # Load the retrained model and predict the classification of the test text
    model = AutoModelForSequenceClassification.from_pretrained("mjbeattie/fifi_classification")
    with torch.no_grad():
        logits = model(**inputs).logits
    
    # Get predicted labels
    predicted_labels = torch.argmax(logits, dim=1)
    
    # Print the predicted labels
    for i, text in enumerate(texts):
        f.write(f"Text: {text} | Predicted Label: {predicted_labels[i]}\n")

    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--fileout", type=str, required=False, help="Enter name of output file", default='fifi_inference_torch_output.txt')

    args = parser.parse_args()
    print('Running classification with fileout = ', args.fileout)
    main(args.fileout)
