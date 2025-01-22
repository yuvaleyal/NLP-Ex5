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

# Implement an extractor based on the dependency trees of the sentences in the document
def extract(text: Doc) -> list[RelationStructure]:
    """extracts relations from the article

    Args:
        text (Doc): given article

    Returns:
        list[RelationStructure]: all relations found
    """