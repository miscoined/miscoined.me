"""
Ability related functions and constants
"""

class classproperty(property):
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

    @classmethod
    def _ability_to_dict(cls, ability):
        d = {"value": 0}
        if ability == "district knowledges":
            d["districts"] = {district: 0 for district in cls.DISTRICTS}
        elif ability == "languages":
            d["languages"] = []
        if ability in cls.GENERAL_INVESTIGATIVE:
            d["investigative"] = True
        return d

    @classproperty
    def investigative(cls):
        return {
            cat: {
                ability: cls._ability_to_dict(ability)
                for ability in cls.INVESTIGATIVE_CATEGORIES[cat]
            } for cat in cls.INVESTIGATIVE_CATEGORIES
        }

    @classproperty
    def general(cls):
        return {
            ability: cls._ability_to_dict(ability) for ability in cls.GENERAL
        }

