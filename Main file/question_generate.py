from transformers import T5ForConditionalGeneration,T5Tokenizer
import spacy
import nltk
from nltk.corpus import stopwords
import string


# Load spaCy's English NLP model
nlp = spacy.load('en_core_web_sm')
# Load stop words from NLTK
stop_words = set(stopwords.words('english')) | set(string.punctuation)


#Load the pretrained model for question generation
question_model = T5ForConditionalGeneration.from_pretrained('ramsrigouthamg/t5_squad_v1')
question_tokenizer = T5Tokenizer.from_pretrained('ramsrigouthamg/t5_squad_v1')


#extract keywords from the text..
def extract_keywords(text):
    # Use spaCy's NLP pipeline
    doc = nlp(text)
    keywords = []

    # Step 1: Prioritize dates, numbers, and years
    date_tokens = [ent.text for ent in doc.ents if ent.label_ in ['DATE', 'TIME', 'CARDINAL', 'ORDINAL']]
    keywords.extend(date_tokens)

    # Step 2: Collect multi-word noun phrases (noun chunks)
    noun_chunk_texts = set()
    for chunk in doc.noun_chunks:
        # Exclude chunks containing stopwords and keep only meaningful phrases
        if not any(token.text.lower() in stop_words for token in chunk) and len(chunk) > 1:
            noun_chunk_texts.add(chunk.text)
    keywords.extend(noun_chunk_texts)

    # Step 3: Collect individual nouns and proper nouns
    for token in doc:
        if token.text.lower() not in stop_words and token.pos_ in ['NOUN', 'PROPN']:
            keywords.append(token.text)

    # Step 4: Add any additional entities (e.g., money, quantity, etc.)
    for ent in doc.ents:
        if ent.label_ in ['MONEY', 'QUANTITY', 'PERCENT']:
            keywords.append(ent.text)

    # Step 5: Remove individual keywords that are part of a noun chunk
    filtered_keywords = []
    for keyword in keywords:
        if all(keyword.lower() not in chunk.lower() for chunk in noun_chunk_texts) or keyword in noun_chunk_texts:
            filtered_keywords.append(keyword)

    # Remove duplicates and return the list of keywords
    return list(set(filtered_keywords))  # Removing duplicates




#get the questions 
def get_question(sentence,answer):
  mdl=question_model
  tknizer=question_tokenizer
  text = "context: {} answer: {}".format(sentence,answer)
  #print (text)
  max_len = 256
  encoding = tknizer.encode_plus(text,max_length=max_len, pad_to_max_length=False,truncation=True, return_tensors="pt")

  input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

  outs = mdl.generate(input_ids=input_ids,
                                  attention_mask=attention_mask,
                                  early_stopping=True,
                                  num_beams=5,
                                  num_return_sequences=1,
                                  no_repeat_ngram_size=2,
                                  max_length=300)


  dec = [tknizer.decode(ids,skip_special_tokens=True) for ids in outs]


  Question = dec[0].replace("question:","")
  Question= Question.strip()
  return Question

