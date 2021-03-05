#!/usr/bin/env python
# -*- charset utf8 -*-
import pyaudio
import numpy
import requests

RATE = 44100
BUFFER = 882
p = pyaudio.PyAudio()

stream = p.open(
    format = pyaudio.paFloat32,
    channels = 1,
    rate = RATE,
    input = True,
    output = False,
    frames_per_buffer = BUFFER
)

r = range(0,int(RATE/2+1),int(RATE/BUFFER))
l = len(r)
signalpeaks = [0]*l


def init_line():
        line1.set_data(r, [-1000]*l)
        line2.set_data(r, [-1000]*l)
        return (line1,line2,)

def update_line():
    try:
        data = numpy.fft.rfft(numpy.fromstring(
            stream.read(BUFFER), dtype=numpy.float32)
        )
    except IOError:
        pass
    data = numpy.log10(numpy.sqrt(
        numpy.real(data)**2+numpy.imag(data)**2) / BUFFER) * 10
    return numpy.argmax(data)

counter1 = 0
counter2 = 0
while True:
    maxf = update_line()
    signalpeaks = numpy.array(signalpeaks)
    signalpeaks = signalpeaks*0.95
    print(maxf)
    if (signalpeaks[maxf] < 100):
        signalpeaks[maxf] += 15
    if (numpy.sum(signalpeaks[25:30]) > 50 and sum(signalpeaks[30:32]) > 50):
        print(maxf)
        requests.get("http://192.168.0.132/LED=ON")
        signalpeaks = signalpeaks*0
    if (numpy.sum(signalpeaks[33:35]) > 50 and sum(signalpeaks[36:40]) > 50):
        print(maxf)
        requests.get("http://192.168.0.132/LED=OFF")
        signalpeaks = signalpeaks*0
    if (numpy.sum(signalpeaks[18:22]) > 50 and sum(signalpeaks[22:27]) > 50):
        print(maxf)
        requests.get("http://192.168.0.167/LED=ON")
        signalpeaks = signalpeaks*0

    if (numpy.sum(signalpeaks[25:30]) > 50 and sum(signalpeaks[36:40]) > 50):
        print(maxf)
        requests.get("http://192.168.0.167/LED=OFF")
        signalpeaks = signalpeaks*0


print(signalpeaks)
