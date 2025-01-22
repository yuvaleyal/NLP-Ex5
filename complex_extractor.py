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
from compound_propn import CompoundPROPN
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

def get_compound_proper_nouns(text: Doc) -> list[CompoundPROPN]:
    """returns all proper nouns in the text

    Args:
        text (Doc): the given text

    Returns:
        list[CompoundPROPN]: the list of compound proper nouns
    """
    proper_noun_heads = get_proper_noun_heads(text)
    proper_nouns: list[CompoundPROPN] = []
    for head in proper_noun_heads:
        children = set()
        for child in head.children:
            if child.dep_ == COMPOUND_RELATION:
                children.add(child)
        proper_nouns.append(CompoundPROPN(head, children))
    return proper_nouns

def conditional_relation(h1: Token, h2: Token) -> None | tuple[Token]:
    """Checks if the pair relation should be extracted, and if so, returns the relation

    Args:
        h1 (Token): The first proper noun head
        h2 (Token): The second proper noun head

    Returns:
        None | tuple[Token]: None if the relation shouldn't be extracted, otherwise the relation
    
    Notes:
        Condition 1: h1 and h2 have the same head token h, the edge (h, h1) is labeled nsubj
        (nominal subject), and the edge (h, h2) is labeled dobj (direct object).

        Condition 2: h1’s parent in the dependency tree (denoted with h)
        is the same as h2’s grandparent (denote h2’s parent with h'),
        the edge (h, h1) is labeled nsubj (nominal subject),
        the edge (h, h') is labeled prep (preposition),
        and the edge (h', h2) is labeled pobj (prepositional object).
    """
    # In the case condition #1 holds, the Relation is defined to be h.
    # In the case condition #2 holds, the Relation is defined to be the concatenation of h and h'.

    # Condition 1
    if h1.head == h2.head and h1.dep_ == NSUBJ_RELATION and h2.dep_ == DOBJ_RELATION:
        return (h1.head,)
    # Condition 2
    if h1.head == h2.head.head and h1.dep_ == NSUBJ_RELATION \
        and h1.head.dep_ == PREP_RELATION and h2.dep_ == POBJ_RELATION:
        print("Preposition detected:", h1.head, h2.head)
        return (h1.head, h2.head)


def extract_relations(text: Doc, proper_nouns: list[CompoundPROPN]) -> list[RelationStructure]:
    """Extracts relations between PROPNs in the text if they follow the conditions

    Args:
        text (Doc): the given text
        proper_nouns (list[set[Token]]): the list of compound proper nouns

    Returns:
        list[RelationStructure]: the list of relations as RelationStructure
    """
    pnoun_relations: list[RelationStructure] = []
    for i, h1 in enumerate(proper_nouns):
        for j, h2 in enumerate(proper_nouns):
            if relation := conditional_relation(h1.get_head(), h2.get_head()):
                relation = " ".join([token.text for token in relation])
                pnoun_relations.append(RelationStructure(str(h1), relation, str(h2)))
    
    return pnoun_relations


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
    return extract_relations(text, proper_nouns)
