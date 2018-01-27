class Media:

    def __init__(self, name, image, link):
        self.name = name
        self.image = image
        self.link = link

    def __str__(self):
        return self.name

class Book(Media):

    def __init__(self, name, image, link, author):
        super().__init__(self, name, image, link)
        self.author = author

    def export(self):
        book = {
            'name': self.name, 'image': self.image,
            'link': self.link, 'author': self.author
        }
        return book

class Episode(Media):

    def __init__(self, name, image, link, time, series):
        super().__init__(name, image, link)
        self.time = time
        self.series = series

class Game(Media):

    def __init__(self, name, image, link, playtime):
        super().__init__(name, image, link)
        self.playtime = playtime

class Song(Media):

    def __init__(self, name, image, link, time, artist):
        super().__init__(name, image, link)
        self.time = time
        self.artist = artist