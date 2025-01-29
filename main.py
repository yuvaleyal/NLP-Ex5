import spacy.lang
import spacy.tokens
import wikipedia, spacy
from simple_extractor import extract as simple_extract
from complex_extractor import extract as complex_extract
from LLM_facade import LLM_relations as LLM_extract
import numpy as np
from typing import Callable

def output_list_to_file(items: list, path: str):
    with open(path, "w") as f:
        for item in items:
            f.write(item.__str__())
            f.write("\n")


def extract_relations(nlp: spacy.language.Language,
                         extractor_functions: list[Callable[[spacy.tokens.Doc], list[str]]],
                         extractor_names: list[str],
                         num_samples: int = 5,
                         wikipedia_titles: list[str] = ("Bradley Pitt", "Donald Trump", "J.K. Rowling")):
    """Evaluate the extractors by:
    Sampling `num_samples` relations from each page, and manually checking if they are correct.

    Args:
        nlp (spacy.language.Language): the spacy language object
        extractor_functions (list[Callable]): list of extractor functions, accepting a spacy doc and returning a list of relations
        extractor_names (list[str]): list of extractor names
        num_samples (int, optional): number of relations samples. Defaults to 5.
        wikipedia_titles (list[str], optional): wikipedia pages to use. Defaults to ("Bradley Pitt", "Donald Trump", "J.K. Rowling").
    """
    if len(extractor_functions) != len(extractor_names):
        raise ValueError("extractor_functions and extractor_names must have the same length.")

    pages = wikipedia_titles
    for page in pages:
        print(f"Page: {page}")
        page_content = wikipedia.page(title=page).content
        analyzed_page = nlp(page_content)
        for extractor, extractor_name in zip(extractor_functions, extractor_names):
            print(f"\n{extractor_name}:")
            relations = extractor(analyzed_page)
            sample = np.random.choice(relations, num_samples, replace=False)
            for relation in sample:
                print(relation)
        print("\n")


def evaluate_extractors(nlp: spacy.language.Language):
    """For each extractor (simple, complex, LLM),
    evaluate the extractor on the wikipedia page of:
    1. Bradley Pitt
    2. Donald Trump
    3. J.K. Rowling

    Evaluate the extractors by:
    Sampling 5 relations from each page, and manually checking if they are correct.

    Args:
        nlp: spacy Language object
    """
    extractors = [simple_extract, complex_extract, LLM_extract]
    extractor_names = ["Simple Extractor", "Complex Extractor", "LLM Extractor"]
    extract_relations(nlp, extractors, extractor_names)


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

    
    
