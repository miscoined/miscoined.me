"""Flask configuration"""

from os import path


class Config:
    """Config object"""
    DATA_DIR = "data"
    BLANK_CHARACTER_FILE = path.join(DATA_DIR, "character.json")
    OCCUPATIONS_FILE = path.join(DATA_DIR, "occupations.json")
    ABILITIES_FILE = path.join(DATA_DIR, "abilities.json")

    CHARACTER_DIR = path.join(DATA_DIR, "characters")
