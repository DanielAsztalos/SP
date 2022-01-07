import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import struct

class Particle:
    def __init__(self, color, id_, x, y):
        self.color = color
        self.pid = id_
        self.x = x
        self.y = y
        
    def __str__(self):
        return " ".join([str(self.color), str(self.pid), str(self.x), str(self.y)])

def read_data():
    inf = open("particles.mvi", "rb")
    frames = []

    while True:
        buffer = inf.read(4)
        if not buffer:
            break
    
        size = struct.unpack("i", buffer)[0]
    
        frame_number = struct.unpack("i", inf.read(4))[0]
        
        frame = []
    
        for i in range(size):
            color = struct.unpack("i", inf.read(4))[0]
            id_ = struct.unpack("i", inf.read(4))[0]
            x = struct.unpack("f", inf.read(4))[0]
            y = struct.unpack("f", inf.read(4))[0]
            _ = struct.unpack("f", inf.read(4))
    
            frame.append(Particle(color, id_, x, y))

        frames.append(frame)
    return frames

frames = read_data()

fig, ax = plt.subplots(figsize=(10, 8))

line = ax.scatter([], [])

ax.set_xlim(0, 200)
ax.set_ylim(0, 200)

def animate(frame_num):
    x_data, y_data, color = [], [], []

    for particle in frames[frame_num]:
        x_data.append(particle.x)
        y_data.append(particle.y)
        color.append(particle.color)

    sizes = [20] * len(color)
    line.set_offsets(np.array([x_data, y_data]).T)
    line.set_array(np.array(color) - 2)
    line.set_sizes(np.array(sizes))
    return line

anim = FuncAnimation(fig, animate, frames=len(frames), interval=1)
plt.show()