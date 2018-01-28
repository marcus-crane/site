class Media:

    def __init__(self, name, image, link):
        self.name = name
        self.image = image
        self.link = link

    def __str__(self):
        return self.name

class Book(Media):

    def __init__(self, name, image, link, author):
        super().__init__(name, image, link)
        self.author = author

    def export(self):
        book = {
            'name': self.name, 'image': self.image,
            'link': self.link, 'author': self.author
        }
        return book

class Episode(Media):

    def __init__(self, name, image, link, series):
        super().__init__(name, image, link)
        self.series = series

    def export(self):
        episode = {
            'name': self.name, 'image': self.image,
            'link': self.link, 'series': self.series
        }
        return episode

class Game(Media):

    def __init__(self, name, image, link, playtime):
        super().__init__(name, image, link)
        self.playtime = playtime

class Song(Media):

    def __init__(self, name, image, link, artist):
        super().__init__(name, image, link)
        self.artist = artist

    def export(self):
        song = {
            'name': self.name, 'image': self.image,
            'link': self.link, 'artist': self.artist
        }
        return song
