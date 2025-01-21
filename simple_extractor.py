"""Simple extractor module
API:
    extract(text: Doc) -> list[RelationStructure]
"""

import spacy
import spacy.tokens
from spacy.tokens.token import Token
from spacy.tokens.doc import Doc
from relation_structure import RelationStructure

PROPN = "PROPN"

def find_proper_noun_spans(text: Doc) -> list[tuple[int, int]]:
    """returns a list of tuples (start, end) that the range in the text in all proper nouns

    Args:
        text (Doc): the given text

    Returns:
        list[tuple[int, int]]: the list of ranges. if (i,j) is in the list it means the tokens in indexes i, i+1, ..., j-1 are PROPN, and the token in j isn't.
    """
    i = 0
    in_propn = False
    spans = []
    for token in text:
        if token.pos_ == PROPN:
            if not in_propn:
                in_propn = True
                start = i
        elif in_propn:
            in_propn = False
            spans.append((start, i))
        i += 1
    if in_propn:
        spans.append((start, i))
    return spans

def merge_proper_nouns(text: Doc) -> Doc:
    """whenever there are a few tokens tagged PROPN one after the other, they are merged to one. This is done in place.

    Args:
        text (Doc): the guven text

    Returns:
        Doc: the resulting text after the merge
    """
    spans = find_proper_noun_spans(text)
    with text.retokenize() as retokenizer:
        attrs = {}
        for start, end in spans:
            retokenizer.merge(text[start:end], attrs=attrs)
    return text            

def extract(text: Doc) -> list[RelationStructure]:
    """extracts relations from the article

    Args:
        text (Doc): given article

    Returns:
        list[RelationStructure]: all relations found
    """
    propn_merged = merge_proper_nouns(text)
    
    
# hekp code to test because im not making another file    
nlp = spacy.load("en_core_web_sm")    
doc = nlp("Dan James really like David Bowie because Marry Jane told him")
print([token.text + " " + token.pos_ for token in doc])
merge_proper_nouns(doc)
print([token.text + " " + token.pos_ for token in doc])