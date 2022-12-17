import json
import dataclasses
import os
from dataclasses_json import dataclass_json   

@dataclass_json
@dataclasses.dataclass
class instr:
    op: str
    x : int
    y : int

@dataclass_json
@dataclasses.dataclass
class arg:
    name:str 
    _type:str

@dataclass_json
@dataclasses.dataclass
class Function:
    name : str
    _type : str
    args: list[list]
    instr : list[instr]
    
@dataclass_json
@dataclasses.dataclass
class Master:
    functions :list[Function]
        

def convertOp(op):
    opBril = ["add", "sub","mul","div","eq","lt","le" ]
    opCool = ["+"  , "-"  ,"*"  ,"/"  ,"=" ,"<" ,"<=" ]
    re =  [ob for ob,oc in zip(opBril,opCool) if oc==op]
    return re[0]