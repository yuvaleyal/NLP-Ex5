import spacy.lang
import wikipedia, spacy
from simple_extractor import extract as simple_extract
from complex_extractor import extract as complex_extract
import numpy as np

def output_list_to_file(items: list, path: str):
    with open(path, "w") as f:
        for item in items:
            f.write(item.__str__())
            f.write("\n")

def evaluate_extractors(nlp: spacy.language.Language):
    """For each extractor (simple and complex),
    evaluate the extractor on the wikipedia page of:
    1. Bradley Pitt
    2. Donald Trump
    3. J.K. Rowling

    Evaluate the extractors by:
    Sampling 5 relations from each page, and manually checking if they are correct.

    Args:
        nlp: spacy Language object
    """
    pages = ["Bradley Pitt", "Donald Trump", "J.K. Rowling"]
    num_samples = 5

    for page in pages:
        print(f"Page: {page}")
        page_content = wikipedia.page(title=page).content
        analyzed_page = nlp(page_content)
        simple_relations = simple_extract(analyzed_page)
        complex_relations = complex_extract(analyzed_page)
        print("Simple Extractor:")
        simple_sample = np.random.choice(simple_relations, num_samples, replace=False)
        for relation in simple_sample:
            print(relation)
        print("\nComplex Extractor:")
        complex_sample = np.random.choice(complex_relations, num_samples, replace=False)
        for relation in complex_sample:
            print(relation)
        print("\n")


if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    # page = wikipedia.page(title="Bradley Pitt").content
    # page = wikipedia.page(title="Donald Trump").content
    # analyzed_page = nlp(page)
    # # relations = simple_extract(analyzed_page)
    # # print(relations[0])
    # # output_list_to_file(relations, "output.txt")
    # relations = complex_extract(analyzed_page)
    # output_list_to_file(relations, "output_complex_trump.txt")
    evaluate_extractors(nlp)

    
    
