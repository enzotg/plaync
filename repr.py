from pygame import mixer
import os 
import threading
import time
import pathlib

#------------------------------------
#------------------------------------
class files():
    def __init__(self, n, carpeta, nombre, nombrecompl, prim):
        self.n = n
        self.carpeta = carpeta
        self.nombre = nombre
        self.nombrecompl = nombrecompl
        self.prim = prim
#------------------------------------
class repr:
    lista=[]
    iActual = 0    
    stoppr = False
    playpr = False
    eventend = threading.Event()
    threadend = threading.Thread()
        
    def __init__(self, path, extens):
        self.path = path
        self.lista = self.getFiles(path, extens) #lista de archivos

        mixer.init()      

        self.threadend = threading.Thread(name='end', target=self.wait_for_end, args=(self.eventend, 1)) 
        self.threadend.start()

    def init(self):
        mixer.init() 

    def quit(self):
        mixer.quit() 

    def getFiles(self, path, extens):
        lista=[]
        a = []
        i = 0
        ant = ''
        prim = False
        for r, d, f in os.walk(path):
            d.sort()
            f.sort()
            for file in f:
                if extens in file:                                
                    full = os.path.join(r, file)                    
                    full = full.replace(os.sep, '/')
                    prim = (ant != r)
                    lista.append(files(i, r.replace(os.sep, '/').replace(path, ''), file.replace(extens, ''), full, prim))
                    ant = r
                    i=i+1

        return lista

    def getlista(self):
        return self.lista            
    
    def setvolume(self, val):

        #n = mixer.music.get_volume() + val
        n = val
        if(n < 0) :
            n = 0
        if(n > 1):
            n = 1
        mixer.music.set_volume(n)

    def getvolume(self):
        return mixer.music.get_volume() 

    def play(self):                
        mixer.music.stop()                
        mixer.music.load(self.lista[self.iActual].nombrecompl)                        
        mixer.music.play()         
        
        self.playpr = True
        self.stoppr = False
        self.onplay()
        return self.lista[self.iActual].nombrecompl

    def playone(self, n):        
        self.iActual = n
        self.play()

    def playonen(self, nombrec):        
        i = 0        
        while self.lista[i].nombrecompl != nombrec:
            i += 1
        self.iActual = i
        self.play()

    def stop(self):        
        mixer.music.stop()
        self.stoppr = True

    def pause(self):        
        mixer.music.pause()
        self.stoppr = True
        
    def exit(self):
        self.eventend.set()

    def next(self):                 
        self.incr(1)        
        self.play()
    
    def prev(self):        
        self.incr(-1)        
        self.play()
    
    def nextfold(self):
        i = self.iActual
        c = self.lista[self.iActual].carpeta
        while self.lista[i].carpeta == c:
            i += 1
        incr(i)

    def prevfold(self):
        i = self.iActual
        c = self.lista[self.iActual].carpeta
        while self.lista[i].carpeta == c:
            i -= 1
        incr(i)

    def incr(self, n):
        self.iActual += n
        if(self.iActual < 0):
            self.iActual = len(self.lista) + n
        elif(self.iActual >= len(self.lista)):
            self.iActual = n -1
    
    def getcurrplay(self):       
        res = ""
        if (self.lista ):             
            res = self.lista[self.iActual].nombre        
        
        return res

    def getcurrplayo(self):       
        res = files(0,'','','',False)
        if (self.lista ):             
            res = self.lista[self.iActual]        
        
        return res
    #---Eventos --------------
    def onplay(self):
        print(self.lista[self.iActual].nombrecompl) 

    def onend(self):    
        self.next()
        print("end")

    def wait_for_end(self, e, t):
        i = 0
        while not e.isSet():            
            event_is_set = e.wait(t)            
            if self.playpr :
                if mixer.get_init() != None:
                    if mixer.music.get_busy() == 0 and not self.stoppr :
                        self.onend()



