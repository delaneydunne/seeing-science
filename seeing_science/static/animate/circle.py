# Import the champions
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

'''
CREATE CIRCLE OBJECT
'''

# Generate circle position array
circle_angles = np.linspace(0, 2*np.pi)
x_pos = np.cos(circle_angles)
y_pos = np.sin(circle_angles)
unit_circle = np.hstack((x_pos[:,None], y_pos[:,None]))

'''
GENERATE DATA SETS
'''

# Animation parameters
tot_frames = 60
fps = 30

# Generate expanding circle
data = [frame * unit_circle for frame in range(tot_frames)]

'''
PLOT SYSTEM
'''

# Initiate axes for crystal diagram and pair correlation function
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)

# Initial positions
line = ax.plot(data[0][:,0], \
				data[0][:,1], \
				'-')[0]

# Update axes
def update(frame):

	line.set_data(data[frame][:,0:2].T)

'''
CONFIGURE PLOT SETTINGS
'''

# Set limits for the plots
font = 16
size = tot_frames
ax.set_xlim([-size, size])
ax.set_ylim([-size, size])
ax.set_title('Expanding Circle', fontsize=font)

'''
ANIMATE THE DIAGRAM
'''

ani = FuncAnimation(fig, update, tot_frames, interval=1000/fps)
ani.save('circle.gif', writer='imagemagick', fps=fps)
plt.show()