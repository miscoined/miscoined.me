"""Hold character-related classes and functions"""

import json
import os.path

from miscoined import app


class Character:
    """A Trail of Cthulu character."""

    @classmethod
    def new(cls):
        """Return a trail of cthulu character dict."""
        with open(app.config["BLANK_CHARACTER_FILE"]) as fp:
            character = json.load(fp)
        character["abilities"] = cls.abilities()
        return character

    @classmethod
    def load(cls, name=None):
        """Return a trail of cthulu character loaded from a file."""
        with open(os.path.join(app.config["CHARACTER_DIR"], name + ".json")) as fp:
            return json.load(fp)

    @classmethod
    def put(cls, char, name=None):
        """Put character data into a character file."""
        if name is None:
            name = "".join(char["name"].split())
        with open(os.path.join(app.config["CHARACTER_DIR"], name + ".json"), "w") as fp:
            json.dump(char, fp, indent=2)
        return name

    @classmethod
    def abilities(cls):
        with open(app.config["ABILITIES_FILE"]) as fp:
            ability_data = json.load(fp)

        abilities = []

        general = ability_data["general"]
        for ability in sorted(general["normal"] + general["investigative"]):
            ability = {"name": ability, "category": ["general"]}
            if ability in general["investigative"]:
                ability["investigative"] = True
            abilities.append(ability)

        investigative = ability_data["investigative"]
        for category in investigative["categories"]:
            for ability in investigative["categories"][category]:
                ability = {"name": ability, "category": ["investigative", category]}
                if ability["name"] == "district knowledges":
                    ability["districts"] = [{"name": district, "value": 0}
                                            for district in investigative["districts"]]
                if ability["name"] == "languages":
                    ability["languages"] = []
                abilities.append(ability)

        for ability in abilities:
            ability["value"] = 0
            ability["temp"] = 0

        return abilities


def occupations():
    with open(app.config["OCCUPATIONS_FILE"]) as fp:
        occupations = json.load(fp)

    for occupation in occupations:
        options = occupation["abilities"].get("options", {"count": 0})
        categories = set(options.get("categories", ["investigative", "general"]))
        if "categories" in options:
            del options["categories"]

        if "allowed" not in options:
            options["allowed"] = []

        options["allowed"].extend(ability["name"] for ability in
                                  Character.abilities()
                                  if set(ability["category"]) | categories)
    return occupations
