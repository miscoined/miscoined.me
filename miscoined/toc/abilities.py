"""
Ability related functions and constants
"""


class classproperty(property):
    """Helper decorator to combine @classmethod and @property"""
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class Abilities:

    INVESTIGATIVE_CATEGORIES = {
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

    @classproperty
    def investigative(cls):
        abilities = []
        for cat in cls.INVESTIGATIVE_CATEGORIES:
            for ability in cls.INVESTIGATIVE_CATEGORIES[cat]:
                ability_dict = {
                    "name": ability,
                    "value": 0,
                    "type": "investigative",
                    "category": cat
                }
                if ability == "district knowledges":
                    ability_dict["districts"] = {
                        district: 0 for district in cls.DISTRICTS}
                elif ability == "languages":
                    ability_dict["languages"] = []
                abilities.append(ability_dict)
        return abilities

    @classproperty
    def general(cls):
        return [{
            "name": ability,
            "value": 0,
            "type": "general",
            "investigative": ability in cls.GENERAL_INVESTIGATIVE
        } for ability in cls.GENERAL]
