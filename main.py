import wikipedia, spacy

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    page = wikipedia.page(title="Bradley Pitt").content
    analyzed_page = nlp(page)
    for s in analyzed_page.sents:
        print(s)
        for token in s:
            print(token.text, token.pos_)
        break

    # Get POS tags
    pos_tags = {}
    for token in analyzed_page:
        pos_tags[token.text] = token.pos_
    
    
