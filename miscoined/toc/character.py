"""Hold character-related classes and functions"""

import miscoined.toc.data as data


class Character:
    """A Trail of Cthulu character."""

    @classmethod
    def new(cls):
        """Return a trail of cthulu character dict."""
        character = data.load_file("BLANK_CHARACTER_FILE")
        character["abilities"] = data.abilities()
        return character

    @classmethod
    def load(cls, name=None):
        """Return a trail of cthulu character loaded from a file."""
        return data.load_char(name)

    @classmethod
    def put(cls, char, name=None):
        """Put character data into a character file."""
        if name is None:
            name = "".join(char['name'].split())
        data.put_file('CHARACTER_DIR', name, char)
        return name
