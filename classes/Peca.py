class Peca():
    def __init__(self, nEsq=None, nDir=None):
        self.nEsq = nEsq
        self.nDir = nDir

    def __str__(self):
        return "(" + str(self.nEsq) +"|"+ str(self.nDir) + ")"