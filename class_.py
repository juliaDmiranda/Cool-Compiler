'''
Classe representante de cada token
'''
from Id import Ids
import re

class Token():
    def __init__(self, str_, line):
        self.token = self.tiraT(str_)
        self.id = self.classify()
        self.line = line
    
    def idEqual(self, object) -> bool:
        if (self.id == object):
            return True
        else:
            return False
    
    def __str__ (self):
        return f"{self.token} : {self.id.name}, line {self.line}\n"

    def tiraT(self, str):
        if(str!="\t"):
            return str.replace("\t","")
        else:
            return str
            
    def classify(self):
        '''The method that classifies a given token in an identifier'''

        if( self.token == "false" or self.token == "true" or self.token[0].isupper() and self.token.lower()!="class"):
            return Ids.match(self.token)
        else:
            return Ids.match(self.token.lower())
