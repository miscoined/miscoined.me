"""Hold character-related classes and functions"""

import miscoined.toc.data as data


class Character:
    """A Trail of Cthulu character."""

    @classmethod
    def new(cls):
        """Return a new trail of cthulu character dict."""
        character = data.blank_character()
        character['investigative'] = data.investigative_abilities()
        character['general'] = data.general_abilities()
        return character

    @classmethod
    def put(cls, char):
        """Put character data into a character file."""
        data.put_file(
            'CHARACTER_DIR',
            "".join(f"{char['player']}_{char['name']}.json".split()).lower(),
            char
        )
