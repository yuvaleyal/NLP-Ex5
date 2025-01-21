import wikipedia, spacy

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    page = wikipedia.page('Brad Pitt').content
    analyzed_page = nlp(page)
