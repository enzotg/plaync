from app import app
from app import inipath
from flask import Flask, render_template
from flask import request
import json
from . repr import repr
from . playvlc import playvlc


rep = repr(inipath, '.mp3')
pvlc = playvlc("cvlc","radiolist.txt")
#pvlc = playvlc("C:\Program Files (x86)\Windows Media Player\wmplayer.exe","radiolist.txt")
listam =[]

@app.route("/")
def home():
    pvlc.stop()
    rep.init()       
    listam = rep.getlista()
    return render_template("home.html", lista=listam, sou="m")

@app.route("/radio/")
def radio():     
    rep.quit()       
    l = pvlc.getlista()
    #return render_template("radio.html", lista=l)
    return render_template("home.html", lista=l, sou="r")

@app.route("/buscar/")
def buscar():             
    listam = rep.getlista()                   
    listares = []
    for r in listam:
        if r.prim:
            listares.append(r)
    return render_template("home.html", lista=listares, sou="b")

@app.route('/radioplayone/', methods=['POST'])
def radioplayone():     
    if request.method == "POST":                  
        res = request.get_data()          
        resp_dict = json.loads(res)        
        res = pvlc.play(int(resp_dict['datos']))

    return ""


@app.route('/buscarn/', methods=['POST'])
def buscarn():     
    if request.method == "POST":   
        listam = rep.getlista()               
        listares = []
        res = request.data      
        
        for r in listam:
            if r.nombre.lower().find(res.decode("utf-8").lower()) >= 0:
                listares.append([r.nombre, r.nombrecompl, r.n])

    return json.dumps(listares)

@app.route('/getcarp/', methods=['POST'])
def getcarp():     
    if request.method == "POST":   
        listam = rep.getlista()               
        listares = []
        #res = request.data      
        
        for r in listam:
            if r.prim:
                listares.append([r.carpeta, r.n])

    return json.dumps(listares)

@app.route('/play/', methods=['POST'])
def play():     
    if request.method == "POST":  
        rep.init()
        rep.play()        
    return "play"

@app.route('/playone/', methods=['POST'])
def playone():     
    if request.method == "POST":          
        res = request.get_data()          
        resp_dict = json.loads(res)        
        res = rep.playone(int(resp_dict['datos']))    
        
        print(rep.getcurrplay())

    return rep.getcurrplay()

@app.route('/buttonpanel/', methods=['GET'])
def buttonpanel():     
    if request.method == "GET":   
        
        res = request.args.get('button')

        if res == "Stop":
            rep.stop()        
        elif res == "Prev":
            rep.prev()   
        elif res == "Next":
            rep.next()   
        elif res =="Play":
            rep.play()
        elif res == "Stopr":
            pvlc.stop()
        

    return res


@app.route('/volume/', methods=['POST'])
def volume():     
    if request.method == "POST":      
        res = request.get_data()          
        resp_dict = json.loads(res)       
        rep.setvolume(float(resp_dict['datos']) / 100 )        
    return "volume"

@app.route('/getvolume/', methods=['POST'])
def getvolume():     
    if request.method == "POST":         
        pass  
    return rep.getvolume() * 100

@app.route('/radiostop/', methods=['POST'])
def radiostop():     
    if request.method == "POST":          
        pvlc.stop()       
        
    return "stop"


@app.route('/getcurrplay/', methods=['GET','POST'])
def getcurrplay():     
    if request.method == "GET":         
        f = rep.getcurrplayo()
        n = str(f.n)
        serializ = f'{{"carpeta":"{f.carpeta}", "n":"{n}", "nombre":"{f.nombre}" }}'
        return serializ

    if request.method == "POST":         
        f = rep.getcurrplayo()
        return f.nombrecompl

@app.route('/postsel/', methods=['POST'])
def postsel():     
    if request.method == "POST":          
        res = request.get_data()          
        resp_dict = json.loads(res)        
        #res = rep.playone(int(resp_dict['datos']))
    return "play"

@app.route("/about/")
def about():
    return render_template("about.html")


