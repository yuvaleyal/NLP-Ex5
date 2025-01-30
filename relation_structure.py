from dataclasses import dataclass
@dataclass
class RelationStructure:
    subject: str
    relation: str
    relative: str
    
    def __str__(self):
        return f"({self.subject}, {self.relation}, {self.relative})"