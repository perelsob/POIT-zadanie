from threading import Lock
from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect
import MySQLdb       
import math
import time
import configparser as ConfigParser
import random
import serial


async_mode = None

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

ser = serial.Serial("/dev/ttyS0")
ser.boundrate = 9600

open_bool=0


def background_thread(args):
    count = 0  
    dataCounter = 0 
    dataList = []
    val_balik =[]
    

           
    while True:
       
         
        if args:
          w = dict(args).get('w')
          dbV = dict(args).get('db_value')
          open_bool = dict(args).get('open_bool')
          P = dict(args).get('P')
          I = dict(args).get('I')
        else:
          w = 30
          dbV = 'nieco'
          open_bool = 0
          P = 4
          I = 5
        
#         print(args)
#         print(open_bool)        
#         time.sleep(1)
        
        if (open_bool):
          print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeee")

          read_ser = ser.readline()
          data = read_ser.decode().split(';')
          y = data[0]
          angle = data[1]

            
          print(dbV)
          print(args)
          print(w)

          socketio.sleep(2)
          count += 1
          dataCounter +=1

          if dbV == 'start':
            dataDict = {
                "t": time.time(),
                "x": count,
                "w": w,
                "y": y}
       
            dataList.append(dataDict)
              
            val = '{"x": ' + str(count) + ',"w": ' + str(w)+',"y": ' + str(y) + '}'
            val_balik.append(val)
              
          else:
              
              
            if len(val_balik)>0:
              fo = open("static/files/test.txt","a+")    
                # val = '[{"y": 0.6551787400492523, "x": 1, "t": 1522016547.531831}, {"y": 0.47491473008127605, "x": 2, "t": 1522016549.534749}, {"y": 0.7495528524284468, "x": 3, "t": 1522016551.537547}, {"y": 0.19625207463282368, "x": 4, "t": 1522016553.540447}, {"y": 0.3741884249440639, "x": 5, "t": 1522016555.543216}, {"y": 0.06684808042190538, "x": 6, "t": 1522016557.546104}, {"y": 0.17399442194131343, "x": 7, "t": 1522016559.54899}, {"y": 0.025055174467733865, "x": 8, "t": 1522016561.551384}]'
                
            
                
              fo.write("%s\r\n" %val_balik)
              val_balik =[]
                
              
            socketio.emit('my_data',{'x': count,'w': w,'y': y,'angle': angle},namespace='/test')
     




#  "a" - Append - will append to the end of the file
#  "w" - Write - will overwrite any existing content
#  "r" - Read - will read the content of the file
# pri zapise do suboru musia byt na nadradenom adresari nastavene prava na zapis do adresaru

@app.route('/write')
def write2file():
    fo = open("static/files/test.txt","a+")    
    val = '[{"y": 0.6551787400492523, "x": 1, "t": 1522016547.531831}, {"y": 0.47491473008127605, "x": 2, "t": 1522016549.534749}, {"y": 0.7495528524284468, "x": 3, "t": 1522016551.537547}, {"y": 0.19625207463282368, "x": 4, "t": 1522016553.540447}, {"y": 0.3741884249440639, "x": 5, "t": 1522016555.543216}, {"y": 0.06684808042190538, "x": 6, "t": 1522016557.546104}, {"y": 0.17399442194131343, "x": 7, "t": 1522016559.54899}, {"y": 0.025055174467733865, "x": 8, "t": 1522016561.551384}]'
    fo.write("%s\r\n" %val)
    return "done"

@app.route('/read/<string:num>')
def readmyfile(num):
    fo = open("static/files/test.txt","r")
    rows = fo.readlines()
    return rows[int(num)-1]


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    return render_template('graph.html', async_mode=socketio.async_mode)
    
@app.route('/db')
def db():
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  cursor.execute('''SELECT  hodnoty FROM  graph WHERE id=1''')
  rv = cursor.fetchall()
  return str(rv)    

@app.route('/dbdata/<string:num>', methods=['GET', 'POST'])
def dbdata(num):
  db = MySQLdb.connect(host=myhost,user=myuser,passwd=mypasswd,db=mydb)
  cursor = db.cursor()
  print(num)
  cursor.execute("SELECT hodnoty FROM  graph WHERE id=%s", num)
  rv = cursor.fetchone()
  return str(rv[0])
    
@socketio.on('my_event0', namespace='/test')
def event0_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

    
@socketio.on('my_event', namespace='/test')
def test_message(messageW):   
    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['w'] = messageW['value']
    emit('my_response',
         {'data': messageW['value'], 'count': session['receive_count']})
    
@socketio.on('my_eventP', namespace='/test')
def test_message(messageP):   
    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['P'] = messageP['value']
    emit('my_response',
         {'data': messageP['value'], 'count': session['receive_count']})
    
@socketio.on('my_eventI', namespace='/test')
def test_message(messageI):   
    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['I'] = messageI['value']
    emit('my_response',
         {'data': messageI['value'], 'count': session['receive_count']}) 

@socketio.on('db_event', namespace='/test')
def db_message(message):   
#    session['receive_count'] = session.get('receive_count', 0) + 1 
    session['db_value'] = message['value']    
#    emit('my_response',
#         {'data': message['value'], 'count': session['receive_count']})

@socketio.on('open_event', namespace='/test')
def open_event_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    
    ser.write(str(session.get('w', 0)).encode('ascii'))
    print(str(session.get('w', 0)).encode('ascii'))
    print(session.get('w', 0))

    session['open_bool'] = 1

    emit('my_response',
         {'data': 'Open', 'count': session['receive_count']})




@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    ser.close()
    disconnect()

@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread, args=session._get_current_object())
    emit('my_response', {'data': 'Server connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)

#if __name__ == '__main__':
  #  app.run(host="0.0.0.0", port=80, debug=True)
#