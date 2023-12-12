from dataclasses import dataclass, field
import json

@dataclass
class BookEntry:
    entryNumber: str = ""
    author: str = ""
    authorc: str = ""
    authorp: str = ""
    title: str = ""
    titlec: str = ""
    titlep: str = ""
    publication: str = ""
    pageCount: str = ""
    ISBN: str = ""
    seriesTitle: str = ""
    note: str = ""
    resource: str = ""
    languageCode: list[str] = field(default_factory=list)
    subjects: list[str] = field(default_factory=list)
    seriesTitle: str = ""
    seriesTitlec: str = ""
    missingFields: list[str] = field(default_factory=list)
    
    def toDict(self):
        return vars(self)
    
    def assignMissingFields(self):
        for key, value in vars(self).items():
            if value == '':
                self.missingFields.append(key)