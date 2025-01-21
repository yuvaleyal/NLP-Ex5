import wikipedia, spacy

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    page = wikipedia.page('Brad Pitt').content
    analyzed_page = nlp(page)

    # Get POS tags
    pos_tags = {}
    for token in analyzed_page:
        pos_tags[token.text] = token.pos_
    
    
