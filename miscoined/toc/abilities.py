"""
Hold ability classes
"""


class Abilities():
    INVESTIGATIVE_CATEGORIES = {
        "academic": ["accounting", "anthropology", "archaeology",
                     "architecture", "art history", "biology",
                     "correspondance", "cthulu mythos", "cryptography",
                     "district knowledges", "geology", "history", "law",
                     "library use", "languages", "medicine", "occupt",
                     "physics", "theology"],
        "interpersonal": ["bullshit detector", "bargain", "bureaucracy",
                          "cop talk", "credit rating",
                          "flattery", "interrogation", "intimidation",
                          "oral history", "reassurance", "streetwise"],
        "technical": ["art", "astronomy", "chemistry", "craft", "dreaming",
                      "evidence collection", "forgery", "forensics",
                      "locksmith", "outdoorsman", "pharmacy", "photography"]
    }

    GENERAL = ["athletics", "conceal", "disguise", "driving",
               "electrical repair", "explosives", "filch", "firearms",
               "first aid", "fleeing", "hypnosis", "magic",
               "mechanical repair", "piloting", "preparedness",
               "psychoanalysis", "riding", "scuffling", "sense trouble",
               "shadowing", "stealth", "weapons"]

    GENERAL_INVESTIGATIVE = ["disguise", "electrical repair", "explosives",
                             "mechanical repair"]

    def __init__(self, name, description=None, value=0):
        self.name = name
        self.value = value
        self.description = (f"Ability {name}" if description is None
                            else description)

    @classmethod
    def investigative(cls):
        abilities = {
            cat: {
                ability: {"value": 0}
                for ability in cls.INVESTIGATIVE_CATEGORIES[cat]
            } for cat in cls.INVESTIGATIVE_CATEGORIES
        }
        abilities["academic"]["district knowledges"]["districts"] = {}
        abilities["academic"]["languages"]["languages"] = []
        return abilities

    @classmethod
    def general(cls):
        abilities = {
            ability: {"investigative": False, "value": 0}
            for ability in cls.GENERAL
        }
        for ability in cls.GENERAL_INVESTIGATIVE:
            abilities[ability]["investigative"] = True
        return abilities

    @classmethod
    def all(cls):
        return {"investigative": cls.investigative(),
                "general": cls.general()}

