# plaync
This app is a web page that plays mp3 files on the server.</br>
The server plays the music sending the sound by its audio output.</br>
The server could be installed in a Raspberry.</br>
The server is flask.
To start the app in a pi:
cd /home/pi/plaync
export set FLASK_APP=/home/pi/plaync/play
flask run --host=0.0.0.0 --port=5000 &

The devices can access the app, e.g. 192.168.1.2:5000
