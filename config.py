"""Flask configuration"""

from os import path


class Config:
    """Config object"""
    DATA_DIR = "data"
    BLANK_CHARACTER_FILE = path.join(DATA_DIR, "character.json")
    OCCUPATIONS_FILE = path.join(DATA_DIR, "occupations.json")

    CHARACTER_DIR = path.join(DATA_DIR, "characters")

    ABILITIES_DIR = path.join(DATA_DIR, "abilities")
    GENERAL_ABILITIES_FILE = path.join(ABILITIES_DIR, "general.json")
    INVESTIGATIVE_ABILITIES_FILE = path.join(ABILITIES_DIR,
                                             "investigative.json")
