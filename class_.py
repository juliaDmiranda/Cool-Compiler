from Id import Ids
import re

class Token():
    def __init__(self, str_, line):
        self.token = str_
        self.id = self.classify()
        self.line = line
    
    def __str__ (self):
        return f"{self.token} : {self.id.name}, line {self.line}\n"
        
    def classify(self):
        '''Method that classifies a given token in a identifier'''

        if( self.token == "false" or self.token == "true"):
            return Ids.match(self.token)
        else:
            return Ids.match(self.token.lower())