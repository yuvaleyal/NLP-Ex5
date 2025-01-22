import wikipedia, spacy
from simple_extractor import extract as simple_extract
from complex_extractor import extract as complex_extract

def output_list_to_file(items: list, path: str):
    with open(path, "w") as f:
        for item in items:
            f.write(item.__str__())
            f.write("\n")

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    page = wikipedia.page(title="Bradley Pitt").content
    analyzed_page = nlp(page)
    # relations = simple_extract(analyzed_page)
    # print(relations[0])
    # output_list_to_file(relations, "output.txt")
    relations = complex_extract(analyzed_page)
    output_list_to_file(relations, "output_complex.txt")

    
    
