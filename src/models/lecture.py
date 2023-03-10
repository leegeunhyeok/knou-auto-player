class Lecture:
    def __init__(self):
        self.id = ''
        self.title = ''
        self.videos = []

    def __str__(self):
        return f'○ {self.id} :: {self.title}'
