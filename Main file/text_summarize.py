#to summarize text (both extractive and abstractive)..
import re
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from transformers import T5ForConditionalGeneration,T5Tokenizer
import spacy
import nltk
import pandas as pd
from nltk.corpus import stopwords
import string
import random
from collections import Counter 
import spacy
from string import punctuation
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest

nlp=spacy.load('en_core_web_sm')
stop_words = set(stopwords.words('english')) | set(string.punctuation)
# load the Pegasus model for text summarization
model_name = "google/pegasus-cnn_dailymail" 
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

#Extractive Summarization

def extractive_summary(text, num_sentences):
    doc = nlp(text)
    # Store the tokens and remove stop words
    tokens = [token.text.lower() for token in doc 
              if not token.is_stop and 
              not token.is_punct and token.text != '\n']
    
    # Count the number of tokens
    count = Counter(tokens)
    max_freq = max(count.values())
    
    # Normalize the frequency
    for i in count:
        count[i] = count[i] / max_freq
        
    sent_token = [sent.text for sent in doc.sents]
    sent_score = {}
    for sent in sent_token:
        for word in sent.split():
            if word.lower() in count.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = count[word]
                else:
                    sent_score[sent] += count[word]
                    
    # Get the top 'num_sentences' sentences
    selected_sentences = nlargest(num_sentences, sent_score, key=sent_score.get)
    # Join the selected sentences into a paragraph
    summary = " ".join(selected_sentences)
    return summary

#Abstractive Summarization
def abstractive_summary(text):
   
    tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
    # Generate summary with controlled parameters
    summary_ids = model.generate(
        tokens['input_ids'],
        max_length=400,          # Set an appropriate max length for your summary
        min_length=150,           # Minimum length can vary based on your needs
        length_penalty=2.0,      # Penalize overly lengthy summaries
        num_beams=4,             # Beam search for better quality
        early_stopping=True
    )

    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
