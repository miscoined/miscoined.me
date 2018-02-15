"""Handle data manipulation."""

import json
import os.path

from miscoined import app


def load_file(config_name):
    with open(app.config[config_name]) as fp:
        return json.load(fp)


def put_file(directory, filename, data):
    with open(os.path.join(app.config[directory], filename), "w") as fp:
        return json.dump(data, fp, indent=2)


def occupations():
    occupations = load_file("OCCUPATIONS_FILE")
    for occupation in occupations:
        if "options" not in occupation["abilities"]:
            continue
        options = occupation["abilities"]["options"]
        categories = set(options.get("categories", ["investigative", "general"]))
        if "categories" in options:
            del options["categories"]

        if "allowed" not in options:
            options["allowed"] = []

        options["allowed"].extend(ability["name"] for ability in abilities()
                                  if set(ability["category"]) | categories)
    return occupations


def abilities():
    abilities = []

    ability_data = load_file("ABILITIES_FILE")

    general = ability_data["general"]
    for ability in general["normal"] + general["investigative"]:
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
