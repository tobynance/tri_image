#######################################################################
class RandomNumber(object):
    def __init__(self):
        self.index = 0

    ###################################################################
    def __call__(self, low, high):
        self.index += 1
        return self.index

#######################################################################
def withRandom(function):
    #raise Exception
    def randomDecorator(*args):
        #raise Exception
        import random
        randint = random.randint
        random.randint = RandomNumber()
        try:
            retVal = function(*args)
        finally:
            random.randint = randint
        #raise Exception
        return retVal
    return randomDecorator
