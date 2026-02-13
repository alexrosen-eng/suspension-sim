

class Suspension:

    def __init__(self):
        self.points = []
        self.links = []

    
    def add_point(self, point):
        self.points.append(point)

    
    def add_link(self,link):
        self.links.append(link)

    def constraints(self):
        return [link.constraint() for link in self.links]