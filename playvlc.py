import subprocess
import time
import threading

#------------------------------------
#------------------------------------
class links():
    def __init__(self, n, link, nombre):
        self.n = n
        self.link = link
        self.nombre = nombre
#------------------------------------
class playvlc:

    lista=[]
    eventend = threading.Event()
    threadend = threading.Thread()
    ssh = None
    filerep = ""

    def __init__(self, filerep, filelinks):
        self.filerep = filerep
        self.lista = self.getlinks(filelinks) #lista de links

    def play(self, n):

        if self.ssh != None :
            self.ssh.kill()
        
        self.threadend = threading.Thread(name='end', target=self.play_on, args=(self.eventend, self.lista[n].link)) 
        self.threadend.start()

    def play_on(self, e, filen):    
        self.ssh = subprocess.Popen([self.filerep, filen],
                        stdin =subprocess.PIPE,
                        stdout=subprocess.PIPE,

                        stderr=subprocess.PIPE,
                        universal_newlines=True, 
                        bufsize=0)
    
    def stop(self):
        if self.ssh != None :            
            self.ssh.terminate()    
            time.sleep(0.2)        

    def getlista(self):
        return self.lista

    def getlinks(self, filen):
        i=0
        lista=[]
        f = open(filen, "r")
        for line in f:              
            res = line.replace("\n","")
            direcc = res.split(",")[0]
            nom = direcc[0:10]
            if len(res.split(",")) > 1 :
                nom = res.split(",")[1]
            
            lista.append(links( i, direcc, nom))
            i+=1

        f.close()
        return lista  
