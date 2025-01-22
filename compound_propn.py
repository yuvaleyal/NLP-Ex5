
from spacy.tokens import Token

class CompoundPROPN:
    """Represents a compound proper noun, with a head PROPN and PROPN children.
    """
    def __init__(self, head: Token, children: set[Token]):
        """Initializes a new CompoundPROPN object with a proper noun head
        and its proper noun children.

        Args:
            head (Token): The compound proper noun head.
            children (set[Token]): The compound proper noun children,\
                which are related to head with the 'compound' relation.
        """
        self.head = head
        self.children = children
    
    def __str__(self):
        # Get original text
        all_propns = set({self.head}.union(self.children))
        ordered_propns = sorted(all_propns, key=lambda x: x.i)
        return " ".join([token.text for token in ordered_propns])

    def get_head(self) -> Token:
        """Returns the head of the compound proper noun.

        Returns:
            Token: The head of the compound proper noun.
        """
        return self.head
    
    def get_children(self) -> set[Token]:
        """Returns the children of the compound proper noun.

        Returns:
            set[Token]: The children of the compound proper noun.
        """
        return self.children