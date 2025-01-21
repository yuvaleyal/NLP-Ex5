"""Simple extractor module
API:
    extract(text: Doc) -> list[RelationStructure]
"""

import spacy
from spacy.tokens.doc import Doc
from relation_structure import RelationStructure

def extract(text: Doc) -> list[RelationStructure]:
    """extracts relations from the article

    Args:
        text (Doc): given article

    Returns:
        list[RelationStructure]: all relations found
    """
    