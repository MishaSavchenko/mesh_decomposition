import zmq
import dill 

context = zmq.Context()

print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

v = lambda : print("asdadasdasdzxvzcvzxcsd")

a = dill.dumps(v)
socket.send(a)
