"""Hold character-related classes and functions"""


class classproperty(property):
    """Helper decorator to combine @classmethod and @property"""
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class Character:
    """A Trail of Cthulu character."""

    OCCUPATIONS = [{
        "name": "antiquarian",
        "credit": {"min": 2, "max": 5},
        "abilities": ["architecture", "art history", "bargain", "history",
                      "languages", "law", "library use"],
    }, {
        "name": "author",
        "credit": {"min": 1, "max": 3},
        "abilities": ["art", "history", "languages", "library use",
                      "oral history", "bullshit detector"],
    }]

    CATEGORIES = {
        "academic": ["accounting", "anthropology", "archaeology",
                     "architecture", "art history", "biology",
                     "correspondance", "cthulu mythos", "cryptography",
                     "district knowledges", "geology", "history", "law",
                     "library use", "languages", "medicine", "occult",
                     "physics", "theology"],
        "interpersonal": ["bullshit detector", "bargain", "bureaucracy",
                          "cop talk", "credit rating",
                          "flattery", "interrogation", "intimidation",
                          "oral history", "reassurance", "streetwise"],
        "technical": ["art", "astronomy", "chemistry", "craft", "dreaming",
                      "evidence collection", "forgery", "forensics",
                      "locksmith", "outdoorsman", "pharmacy", "photography"]
    }

    DISTRICTS = ["university", "old arkham"]

    GENERAL = ["athletics", "conceal", "disguise", "driving",
               "electrical repair", "explosives", "filch", "firearms",
               "first aid", "fleeing", "hypnosis", "magic",
               "mechanical repair", "piloting", "preparedness",
               "psychoanalysis", "riding", "scuffling", "sense trouble",
               "shadowing", "stealth", "weapons"]

    GENERAL_INVESTIGATIVE = ["disguise", "electrical repair", "explosives",
                             "mechanical repair"]

    @classmethod
    def new(cls):
        """Return a new trail of cthulu character dict."""
        return {
            "player": "",
            "name": "",
            "age": "",
            "nationality": "",
            "occupation": cls.OCCUPATIONS[0],
            "drive": "",
            "health": 1,
            "stability": 1,
            "sanity": 4,
            "investigative": cls.investigative_abilities,
            "general": cls.general_abilities,
            "suspicion": 0,
            "sourcesOfStability": [],
            "pillarsOfSanity": [],
            "contacts": [],
            "inventory": []
        }

    @classproperty
    def investigative_abilities(cls):
        abilities = []
        for cat in cls.CATEGORIES:
            for name in cls.CATEGORIES[cat]:
                ability = {"name": name, "value": 0, "category": cat}
                if name == "district knowledges":
                    ability["districts"] = [{"name": district, "value": 0}
                                            for district in cls.DISTRICTS]
                elif name == "languages":
                    ability["languages"] = []
                abilities.append(ability)
        return abilities

    @classproperty
    def general_abilities(cls):
        return [{"name": ability, "value": 0,
                 "investigative": ability in cls.GENERAL_INVESTIGATIVE}
                for ability in cls.GENERAL]
