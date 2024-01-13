import spacy

def remove_nonwords(s):
    return [word for word in s if word.isalpha()]

def extract(doc, diseases_list, drugs_list):
    for ent in doc.ents:
        # Check if ent is a Span object and has a text attribute
        if isinstance(ent, spacy.tokens.Span) and hasattr(ent, 'label_'):
            if ent.label_ == "DISEASE" and ent.text not in diseases_list:
                diseases_list.append(ent.text)
            elif ent.label_ == "CHEMICAL" and ent.text not in drugs_list:
                drugs_list.append(ent.text)

# Load the model
model = spacy.load("en_core_sci_sm")
model.max_length = 21000000
diseases = []
drugs = []

with open('C:/Users/ASUS/Downloads/Assignment 2/text_part_K100.txt', 'r') as file:
    text = file.read().lower().strip()

    print (len(text))
    doc = model(text)

    extract(doc, diseases, drugs)

print(f"Extracted {len(diseases)} diseases: {diseases}")
print(f"Extracted {len(drugs)} drugs: {drugs}")
