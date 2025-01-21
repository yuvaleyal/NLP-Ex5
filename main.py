import wikipedia, spacy
from simple_extractor import extract as simple_extract

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    page = wikipedia.page(title="Bradley Pitt").content
    analyzed_page = nlp(page)
    relations = simple_extract(analyzed_page)
    print(relations[0])
    with open("output.txt", "w") as f:
        for relation in relations:
            f.write(relation.__str__())
            f.write("\n")
    
    
