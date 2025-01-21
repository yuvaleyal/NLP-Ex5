"""Simple extractor module
API:
    extract(text: Doc) -> list[RelationStructure]
"""

import spacy
import spacy.tokens
from spacy.tokens.token import Token
from spacy.tokens.doc import Doc

from relation_structure import RelationStructure
from utils import *

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

def has_a_verb(tokens: list[Token]) -> bool:
    """checks if there is a verb in the given list of tokens

    Args:
        tokens (list[Token]): the given list of tokens

    Returns:
        bool: True if there is a verb, False otherwise
    """
    for token in tokens:
        if token.pos_ == VERB:
            return True
    return False

def realtion_caniadates(text: Doc) -> list[list[Token]]:
    """returns a list of all the subsections of the text that might become a relation.
    A subsection that might become a relation is a consecutive pair of proper nouns such that all the tokens between them are nonpunctuation and at least one of the tokens between them is a verb.

    Args:
        text (Doc): the given text

    Returns:
        list[list[Token]]: the list of potential relations
    """
    all_canidates = []
    cur_canidate = []
    for token in text:
        if cur_canidate == []:
            if token.pos_ == PROPN:
                cur_canidate.append(token)
        else:
            if token.pos_ == PROPN:
                if has_a_verb(cur_canidate):
                    cur_canidate.append(token)
                    all_canidates.append(cur_canidate)
                cur_canidate = [token]
            elif token.pos_ == PUNCT:
                cur_canidate = []
            else:
                cur_canidate.append(token)
    return all_canidates
                        
def make_relation(tokens: list[Token]) -> RelationStructure:
    relation = [token.text for token in tokens if token.pos_ in {VERB, ADP}]
    if relation == []:
        return
    return RelationStructure(tokens[0].text, " ".join(relation), tokens[-1].text)

def extract(text: Doc) -> list[RelationStructure]:
    """extracts relations from the article

    Args:
        text (Doc): given article

    Returns:
        list[RelationStructure]: all relations found
    """
    propn_merged = merge_proper_nouns(text)
    potentials_relations = realtion_caniadates(propn_merged)
    relations = []
    for rel in potentials_relations:
        relations.append(make_relation(rel))
    return relations
    
    
# hekp code to test because im not making another file    
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")    
    doc = nlp("Dan and James really likes David Bowie because Marry Jane likes David")
    print([token.text + " " + token.pos_ for token in doc])
    merge_proper_nouns(doc)
    print([token.text + " " + token.pos_ for token in doc])
    l = realtion_caniadates(doc)
    print (l)
    for n in l:
        print(make_relation(n))