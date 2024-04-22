"""
fifi_inference.py

Uses a pretrained model to reclassify service requests submitted to the city of Seattle
using the FindItFixIt application.
"""

import os, argparse, sys
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import tensorflow as tf
import numpy as np

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
    
    inputs = tokenizer(texts, truncation=True, padding=True, max_length=512, return_tensors="tf")
    
    # Load the retrained model and predict the classification of the test text
    model = TFAutoModelForSequenceClassification.from_pretrained("mjbeattie/fifi_classification")
    logits = model(**inputs).logits
    
    # Get predicted labels
    predicted_labels = tf.math.argmax(logits, 1).numpy().tolist()
    
    # Print the predicted labels
    for i, text in enumerate(texts):
        f.write(f"Text: {text} | Predicted Label: {predicted_labels[i]}")

    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--fileout", type=str, required=False, help="Enter name of output file", default='fifi_inference_output.txt')

    args = parser.parse_args()
    print('Running classification with fileout = ', args.fileout)
    main(args.fileout)
