#######################################################################
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    ###################################################################
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    ###################################################################
    def __neq__(self, other):
        return not(self == other)
