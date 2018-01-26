import csv

class Book:
    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self.cover = kwargs['cover']
        self.link = kwargs['link']
        self.overview = kwargs['overview']
        self.author = kwargs['author']

    def save(self):
        with open('data/books.csv', 'a', newline='') as csvfile:
            bookwriter = csv.writer(csvfile)
            bookwriter.writerow([self.title, self.cover, self.link,
                                  self.overview, self.author])