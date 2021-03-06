import math
import numpy as np
from numpy import linalg as LA
from math import pi
from qiskit import QuantumCircuit as QCirc, ClassicalRegister as CReg, QuantumRegister as QReg, execute as exe
from qiskit.tools.visualization import circuit_drawer as CDraw
from qiskit.quantum_info import state_fidelity as SFad
from qiskit import BasicAer as BAer
from qiskit.tools.visualization import *

A=np.array([ [pi,-pi/2],[-pi/2,pi] ])
b=np.array([ [0.5547],[-0.83205] ])
#expected output x=A^-1*b/norm(A^-1*b)=[0.2425,-0.9701]

v=np.array([ b[0][0], b[1][0] ])
v=v/LA.norm(v)
print("initial state: ", v)

qr = QReg(4)                                                #create 4 quantum register named qr
cr = CReg(1)                                                 #create 1 classical register named cr
c = QCirc(qr,cr)                                            #create quantum circuit for qr and cr named c

c.initialize(v,[qr[3]]) #reversed order

c.h(qr[1])
c.h(qr[2])
c.cu3(pi,pi,0,qr[2],qr[3])
c.cu3(2*pi,0,0,qr[1],qr[3])
c.swap(qr[1],qr[2])
c.h(qr[2])
c.cu3(0,-pi/2,0,qr[2],qr[1])
c.u1(-pi/4,qr[2])
c.h(qr[1])

c.cu3(2*math.asin(1/pi),0,0,qr[1],qr[0])
c.cu3(2*math.asin(2/pi),0,0,qr[2],qr[0])
th=2*math.asin(2/(3*pi))-2*math.asin(1/pi)-2*math.asin(2/pi)
c.cu3(th/2,0,0,qr[1],qr[0])
c.cx(qr[2],qr[1])
c.cu3(-th/2,0,0,qr[1],qr[0])
c.cx(qr[2],qr[1])
c.cu3(th/2,0,0,qr[2],qr[0])

c.h(qr[1])
c.u1(pi/4,qr[2])
c.cu3(0,pi/2,0,qr[2],qr[1])
c.h(qr[2])
c.swap(qr[1],qr[2])
c.cu3(2*pi,0,0,qr[1],qr[3])
c.cu3(pi,-pi,0,qr[2],qr[3])
c.h(qr[1])
c.h(qr[2])

#c.x(qr[0])
#c.measure(qr[0],cr[0])
#c.reset(qr[0])

c.draw(filename='./Resources/Circuit.pdf', output='mpl')

Usim = BAer.get_backend('statevector_simulator')
job = exe(c, Usim)
X = job.result().get_statevector(c)
print(X)

#|1><1| projective measurement only half down indices remains.
#(original order & index start from 1)

x = np.array([X[2-1],X[10-1]])
x = x / LA.norm(x)
print("simulation answer: ", x)
print("true answer: ",  [0.2425,-0.9701])

#backend = BAer.get_backend('qasm_simulator')
#job = exe(c, backend, shots=1024)
#job.result().get_counts(c)
