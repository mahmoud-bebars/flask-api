""" 
programaming lang entites
id
Name
released_year
github_rank
link
thumnail
Description
"""


class Lang:
    def __init__(
        self, id, name, released_year, github_rank, link, thumbnail, description
    ):
        self.id = id
        self.name = name
        self.released_year = released_year
        self.github_rank = github_rank
        self.link = link
        self.thumbnail = thumbnail
        self.description = description

    def __repr__(self):
        return "<id {}".format(self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "released_year": self.released_year,
            "github_rank": self.github_rank,
            "link": self.link,
            "thumbnail": self.thumbnail,
            "description": self.description,
        }
