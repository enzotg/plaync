from flask import Flask

import os


#----------------------------------
def getpath():
    
    if os.sep == "\\" :
        return "F:/Mp3/_Nacional"
    
    inipathfile = "./inipath.txt"

    if not os.path.exists(inipathfile):
        with open(inipathfile, 'w'): pass

    f = open(inipathfile, "r")
    inipath = f.readline()
    inipath = inipath.replace("\n","")
    f.close()
    
    return inipath
#----------------------------------

app = Flask(__name__)
inipath = getpath()

from app import views

