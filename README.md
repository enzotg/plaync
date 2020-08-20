# plaync
This app is intended to set a raspberry pi like a centralized mp3 player. The interfaz is via web.
The pi play the music sending the sound by its audio output.
The app is in a flask server. 

To start the app in a pi:
cd /home/pi/plaync
export set FLASK_APP=/home/pi/plaync/play
flask run --host=0.0.0.0 --port=5000 &

The devices can access the app, e.g. 192.168.1.2:5000
