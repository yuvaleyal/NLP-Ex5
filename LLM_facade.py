import google.generativeai as genai
import spacy
import wikipedia
from spacy.tokens.doc import Doc
from relation_structure import RelationStructure
KEY = "AIzaSyC92XWZEYYG0bAsp5KlfDZrMGdAaKPl9QE"
PROMPT_PERFIX = "read the following text end extracts triplets of (Subject, Relation,Object), where each of them is a span of text. The Subject and Object slot fillers are names (proper nouns), and the Relation slot filler is a verb or a verb along with a preposition. Return only the relations you find, each in a seperate line and formatted as follows: [Subject, Relation, Object]. The text is: "

def LLM_respeonse(text: Doc):
    prompt = PROMPT_PERFIX + text.text
    genai.configure(api_key=KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.split("\n")

def triplet_to_relation(triplet: str) -> RelationStructure:
    triplet = triplet[1:-1]
    subject, relation, obj = triplet.split(", ")
    return RelationStructure(subject, relation, obj)

def LLM_relations(text: Doc) -> list[RelationStructure]:
    triplets = LLM_respeonse(text)
    relations = []
    for triplet in triplets:
        if triplet:
            relations.append(triplet_to_relation(triplet))
    return relations