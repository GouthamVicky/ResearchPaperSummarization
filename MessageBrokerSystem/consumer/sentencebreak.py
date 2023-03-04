import stanza

# Set up the Stanza pipeline
stanza.download('en')


nlp = stanza.Pipeline('en')


def process_stanza(paragraphText):
     # Process text using Stanza
    doc = nlp(paragraphText)
    sentences = [' '.join([token.text for token in sentence.tokens]) for sentence in doc.sentences]
    return sentences