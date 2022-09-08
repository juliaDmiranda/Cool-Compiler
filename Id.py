from enum import Enum, auto
import re

class Ids(Enum):    
    CLASS_ID              =  auto(), "class"         
    SEMICOLON_ID          =  auto(), ";"           
    QUOTE_ID              =  auto(), '"'           
    DOT_ID                =  auto(), "."           
    COMMA_ID              =  auto(), ","           
    COLON_ID              =  auto(), ":"           
    INHERITS_ID           =  auto(), "inherits"   
    IF_ID                 =  auto(), "if"          
    ELSE_ID               =  auto(), "else"        
    FI_ID                 =  auto(), "fi"          
    WHILE_ID              =  auto(), "while"       
    LOOP_ID               =  auto(), "loop"        
    POOL_ID               =  auto(), "pool"        
    LET_ID                =  auto(), "let"         
    IN_ID                 =  auto(), "in"          
    CASE_ID               =  auto(), "case"        
    OF_ID                 =  auto(), "of"          
    ESAC_ID               =  auto(), "esac"        
    NEW_ID                =  auto(), "new"         
    ISVOID_ID             =  auto(), "isvoid"      
    PLUS_ID               =  auto(), "+"           
    MINUS_ID              =  auto(), "-"           
    ASTERISK_ID           =  auto(), "*"           
    F_SLASH_ID            =  auto(), "/"           
    TIDE_ID               =  auto(), "~"           
    LESS_THAN_ID          =  auto(), "<"           
    LESS_THAN_EQUAL_TO_ID =  auto(), "<="          
    EQUAL_TO_ID           =  auto(), "="           
    NOT_ID                =  auto(), "not"         
    O_BRACKETS            =  auto(), "{"           
    C_BRACKETS            =  auto(), "}"           
    O_PARENTHESIS         =  auto(), "("           
    C_PARENTHESIS         =  auto(), ")"           
    ATT_ID                =  auto(), "<-"          
    ID_ID                 =  auto(), ">" 
    TRUE_ID               =  auto(), "true"       
    FALSE_ID              =  auto(), "false"  
    STRING_ID             =  auto(), "..."   
    DIGITS                =  auto(), "..."

    @classmethod
    def match(self, str='oi'):
        if(str.isdigit()):
            return self.DIGITS
        if(str[0] =='"' and str[-1::] == '"'):
            return self.STRING_ID
        elif(str == "false"):
            return self.FALSE_ID
        elif("^[-+]?[0-9]+$" in str):
            return self.DIGIT
        elif(str == "true"):
            return self.TRUE_ID
        else:
            for i in self: 
                if (i.value[1] == str):
                    return i
            return self.ID_ID

if __name__ == "__main__":
    print(Ids.match("main"))
    print(Ids.match("false"))
    print(Ids.match("FAlse"))
    print(Ids.match("ElSe"))