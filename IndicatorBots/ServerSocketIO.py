import socket
import json
import numpy
import eventlet
import Indicators
import socketio

print("starrt")

def ServerResponseConvertor(serverResponse):
    serverResponse = json.dumps(serverResponse)
    # serverResponse = bytes(serverResponse,encoding="utf-8")
    return serverResponse

def CalculateRequest(message):
    # clientMsg = json.loads(message)
    clientMsg = message
    funcName = clientMsg['function']
    print("requested function is:", funcName)
    print("requested args is:", clientMsg['args'])
    try:
        reqFunc = getattr(Indicators, funcName)
    except:
        reqFunc = None
    try:
        if reqFunc is not None:
            reqArgs = clientMsg['args']
            if reqArgs is not None:
                result = reqFunc(*reqArgs)
            else:
                result = reqFunc()
            status = 1
            serverResponse = {'status':status, 'id':clientMsg['id'], 'results':result}
        else:
            status = 0
            serverResponse = {'status':status, 'id':clientMsg['id'], 'error':"Function doesn't exist"}
    except Exception as e:
        status = 0
        serverResponse = {'status':status, 'id':clientMsg['id'], 'error':str(e)}
    serverResponse = ServerResponseConvertor(serverResponse)
    return serverResponse

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    sio.emit("asghar server")
    print('message ', data)
    

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('Indicator')
def msgg(sid, data):
    print("request received")
    answer = CalculateRequest(data)
    print("answer is:", answer)
    # sio.emit("Indicator", answer)
    sio.emit('my event', {'answer': answer})


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
