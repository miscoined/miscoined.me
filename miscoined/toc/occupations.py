"""
Hold occupations
"""


class Occupations:

    OCCUPATIONS = [{
        "name": "antiquarian",
        "credit rating": {"min": 2, "max": 5},
        "abilities": ["architecture", "art history", "bargain", "history",
                      "languages", "law", "library use"],
    }, {
        "name": "author",
        "credit rating": {"min": 1, "max": 3},
        "abilities": ["art", "history", "languages", "library use", "oral history",
                      "bullshit detector"],
    }]
