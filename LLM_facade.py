import google.generativeai as genai
import spacy
import wikipedia
from spacy.tokens.doc import Doc
from relation_structure import RelationStructure
SEPERATOR = " SEP "
KEY = "AIzaSyC92XWZEYYG0bAsp5KlfDZrMGdAaKPl9QE"
PROMPT_PREFIX = (
    "Extract triplets from the given text in the format: [Subject SEP Relation SEP Object]. "
    "Follow these rules:\n"
    "- The Subject and Object must be names (proper nouns).\n"
    "- The Relation must be a verb or a verb with a preposition.\n"
    "- Ensure the extracted triplets accurately reflect relationships explicitly stated in the text.\n"
    "Return each triplet on a new line in the specified format."
)


def LLM_respeonse(text: Doc) -> list[str]:
    """send the text to the LLM model and return the response

    Args:
        text (Doc): the given text

    Returns:
        list[str]: LLM response, split between relations
    """
    prompt = PROMPT_PREFIX + text.text
    genai.configure(api_key=KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.split("\n")

def remove_brackets(text: str) -> str:
    """LLM relation is expected to start and end with brackets. This function removes them.

    Args:
        text (str): the LLM relation

    Returns:
        str: text without the brackets, if they exist
    """
    return text.replace("[", "").replace("]", "")

def triplet_to_relation(triplet: str) -> RelationStructure:
    """converts a relation from the LLM response to a RelationStructure object

    Args:
        triplet (str): relation as given by the LLM response

    Returns:
        RelationStructure: relation as extracted from the LLM response
    """
    triplet = remove_brackets(triplet)
    try:
        subject, relation, obj = triplet.split(SEPERATOR)
    except ValueError:
        return
    return RelationStructure(subject, relation, obj)

def LLM_relations(text: Doc) -> list[RelationStructure]:
    """extract relations from the text using LLM

    Args:
        text (Doc): the given text

    Returns:
        list[RelationStructure]: list of relation extracted
    """
    triplets = LLM_respeonse(text)
    relations = []
    for triplet in triplets:
        if triplet:
            relations.append(triplet_to_relation(triplet))
    return relations