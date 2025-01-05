import spacy
import random
from collections import Counter
from collections import OrderedDict
from sense2vec import Sense2Vec

# load sense2vec vectors
s2v = Sense2Vec().from_disk(r'C:\Users\Administrator\Downloads\Ccoder\.vscode\mcq_app\s2v_old')
nlp=spacy.load('en_core_web_sm')

#generate distractors for the mcq using sense2vec
def sense2vec_get_words(word,s2v):
    output = []
    word = word.lower()
    word = word.replace(" ", "_")

    sense = s2v.get_best_sense(word)
    most_similar = s2v.most_similar(sense, n=20)

    # print ("most_similar ",most_similar)

    for each_word in most_similar:
        append_word = each_word[0].split("|")[0].replace("_", " ").lower()
        if append_word.lower() != word:
            output.append(append_word.title())

    out = list(OrderedDict.fromkeys(output))
    return out



def is_number(string):
    """Check if a string is a number (integer or float)."""
    try:
        float(string.replace(',', ''))  # Handle numbers like '1,000'
        return True
    except ValueError:
        return False

def generate_number_distractors(correct):
    """Generate random distractors for numbers close to the correct value."""
    correct_num = float(correct.replace(',', ''))  # Handle commas in numbers
    distractors = set()
    while len(distractors) < 3:
        variation = random.uniform(-10, 10)  # Small random variations
        option = round(correct_num + variation, 2)  # Round to two decimals
        if option != correct_num and option > 0:  # Valid and not the same
            distractors.add(f"{option:,}")  # Add commas for formatting
    return list(distractors)


def mcq(text,n):
    
    doc=nlp(text)
    #Extract the sentences from the text..
    sentences=[sent.text for sent in doc.sents]
    
    #Generate random sentences..
    selected_sent=random.sample(sentences,min(n,len(sentences)))
    
    #generate the mcqs by extracting keywords and replacing them with a blank..
    ques = []

    for i in selected_sent:
        i = i.lower()  # Convert to lowercase
        sent_doc = nlp(i)  # Process the sentence with Spacy

        # Step 1: Look for dates, numbers, and years first
        date_tokens = [ent.text for ent in sent_doc.ents if ent.label_ in ["DATE", "TIME"]]
        number_tokens = [token.text for token in sent_doc if token.pos_ == "NUM"]

        # Combine date and number tokens for prioritization
        prioritized_tokens = date_tokens + number_tokens

        # Step 2: Look for adjectives, proper nouns if no prioritized tokens
        blanks = {
            "ADJ": [],  # Adjectives
            "PROPN": [],  # Proper nouns
        }

        for token in sent_doc:
            if token.pos_ in blanks:
                blanks[token.pos_].append(token.text)

        # Step 3: Select the most appropriate blank
        subject = None
        if prioritized_tokens:  # Prioritize dates, numbers, and years
            subject = prioritized_tokens[0]
        else:
            for key in ["ADJ", "PROPN"]:  # Check for adjectives and proper nouns
                if blanks[key]:
                    subject = blanks[key][0]
                    break

        # Step 4: Fall back to nouns if no other tokens are found
        if not subject:
            nouns = [token.text for token in sent_doc if token.pos_ == 'NOUN']
            noun_count = Counter(nouns)
            if noun_count:
                subject = noun_count.most_common(1)[0][0]

        # Step 5: Generate MCQ if a subject is identified
        if subject:
            stem = i.replace(subject, '_____')  # Replace the selected word with a blank
            #print(f"Stem: {stem}")

            # Step 6: Generate distractors using Sense2Vec
            distractors = None
            try:
                distractors = sense2vec_get_words(subject, s2v)
                if not distractors:  # If no distractors were found, use random numbers or words
                    raise ValueError("No distractors found for subject.")
            except Exception as e:
                print(f"Error generating distractors for '{subject}': {e}")
                # Fallback: randomly generate distractors (if it's a number or date)
                if is_number(subject):  # If subject is a number, generate number-based distractors
                    distractors = generate_number_distractors(subject)
                else:  # Randomly generate options (for cases when Sense2Vec fails)
                    distractors = random.sample([subject, 'Option1', 'Option2', 'Option3', 'Option4'], 4)

            # Ensure we have enough distractors
            if len(distractors) < 3:
                distractors += ["Option1", "Option2", "Option3"][:3 - len(distractors)]

            choices = distractors[:3] + [subject]  # Add correct answer
            random.shuffle(choices)  # Shuffle the options

            # Determine the correct answer index
            correct_answer = chr(65 + choices.index(subject))  # A, B, C, D, ...

            ques.append([stem, choices, correct_answer])
    return ques
