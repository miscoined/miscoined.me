"""
Ability related functions and constants
"""


class classproperty(property):
    """Helper decorator to combine @classmethod and @property"""
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class Abilities:

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
    def to_dict(cls, name, ability_type, **additional):
        ability = {
            "name": name,
            "jsonName": "".join(name.split()),
            "value": 0,
            "type": ability_type
        }
        ability.update(additional)
        return ability

    @classproperty
    def investigative(cls):
        abilities = []
        for cat in cls.CATEGORIES:
            for name in cls.CATEGORIES[cat]:
                ability = cls.to_dict(name, "investigative", category=cat)
                if name == "district knowledges":
                    ability["districts"] = [{"name": district, "value": 0}
                                            for district in cls.DISTRICTS]
                elif name == "languages":
                    ability["languages"] = []
                abilities.append(ability)
        return abilities

    @classproperty
    def general(cls):
        return [cls.to_dict(
            ability, "general",
            investigative=ability in cls.GENERAL_INVESTIGATIVE
        ) for ability in cls.GENERAL]
