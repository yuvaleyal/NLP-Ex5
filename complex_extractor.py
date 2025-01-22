"""
Complex extractor module
# API:
    extract(text: Doc) -> list[RelationStructure]

"""

import spacy
import spacy.tokens
from spacy.tokens.token import Token
from spacy.tokens.doc import Doc

from relation_structure import RelationStructure
from pos import *
from relations import *


def get_proper_noun_heads(text: Doc) -> list[Token]:
    """returns the heads of all proper nouns in the text

    Args:
        text (Doc): the given text

    Returns:
        list[Token]: the list of heads
    """
    return [token for token in text if token.pos_ == PROPN and token.dep_ != COMPOUND_RELATION]

def get_compound_proper_nouns(text: Doc) -> list[set[Token]]:
    """returns all proper nouns in the text

    Args:
        text (Doc): the given text

    Returns:
        list[set]: the list of proper nouns sets
    """
    proper_noun_heads = get_proper_noun_heads(text)
    proper_nouns: list[set] = []
    for head in proper_noun_heads:
        proper_noun = {head}
        for child in head.children:
            if child.dep_ == COMPOUND_RELATION:
                proper_noun.add(child)
        proper_nouns.append(proper_noun)
    return proper_nouns

def should_be_extracted(h1: Token, h2: Token) -> bool:
    """returns if the given pair of proper noun heads should be
    extracted as a relation, based on whether they follow the conditions

    Args:
        h1 (Token): The first proper noun head
        h2 (Token): The second proper noun head

    Returns:
        bool: if the pair relation should be extracted
    """
    # Condition 1
    if h1.head == h2.head and h1.dep_ == NSUBJ_RELATION and h2.dep_ == DOBJ_RELATION:
        return True
    # Condition 2
    if h1.head == h2.head.head and h1.dep_ == NSUBJ_RELATION \
        and h1.head.dep_ == PREP_RELATION and h2.dep_ == POBJ_RELATION:
        return True
    return False


def extract_relations(text: Doc, proper_nouns: list[set[Token]]) -> list[RelationStructure]:
    """Extracts relations between PROPNs in the text if they follow the conditions

    Args:
        text (Doc): the given text
        proper_nouns (list[set[Token]]): the list of proper nouns

    Returns:
        list[RelationStructure]: the list of relations as RelationStructure
    
    Notes:
        Condition 1: h1 and h2 have the same head token h, the edge (h, h1) is labeled nsubj
        (nominal subject), and the edge (h, h2) is labeled dobj (direct object).

        Condition 2: h1’s parent in the dependency tree (denoted with h)
        is the same as h2’s grandparent (denote h2’s parent with h'),
        the edge (h, h1) is labeled nsubj (nominal subject),
        the edge (h, h0) is labeled prep (preposition),
        and the edge (h', h2) is labeled pobj (prepositional object).
    """


# Implement an extractor based on the dependency trees of the sentences in the document
def extract(text: Doc) -> list[RelationStructure]:
    """extracts relations from the article

    Args:
        text (Doc): given article

    Returns:
        list[RelationStructure]: all relations found
    """
    # Find all tokens that serve as heads of proper nouns in the corpus (henceforth, proper noun heads).
    # Do so by locating all tokens with the POS PROPN that do not have the dependency label compound
    # (i.e., the edge from them to their headword is not labeled compound)

    # For each proper noun head t, define the corresponding proper noun as a set including t along with
    # all its children tokens that have a dependency label compound (i.e., the edge from them to t is
    # labeled compound)
    proper_nouns = get_compound_proper_nouns(text)

    # For each pair of proper noun heads h1 and h2, extract a (Subject, Relation, Object) triplet if one
    # of the following conditions hold:
        # 1. h1 and h2 have the same head token h, the edge (h, h1) is labeled nsubj
        # (nominal subject), and the edge (h, h2) is labeled dobj (direct object).

        # 2. h1’s parent in the dependency tree (denoted with h)
        # is the same as h2’s grandparent (denote h2’s parent with h'),
        # the edge (h, h1) is labeled nsubj (nominal subject),
        # the edge (h, h0) is labeled prep (preposition),
        # and the edge (h', h2) is labeled pobj (prepositional object).
    
