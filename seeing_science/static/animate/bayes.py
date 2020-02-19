# Import the champions
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Likelihood function
def likelihood(x, length):
    
    normalization = length * (np.exp(-1 / length) - np.exp(-20 / length))
    return np.exp(-x / length) / normalization
	

def normalize(x_data, y_data):
    """
    Normalize a discrete data set using rectangular integration
    """
    norm = np.sum(y_data) * (x_data[1] - x_data[0])
    return y_data / norm
	



# Importing the data
data = np.loadtxt('radioactive.dat')
N_max = data.shape[0]

# Range of possible characteristic lengths
start = 2
end = 30
npoints = 1000
x_values = np.linspace(start, end, num=npoints)

# Uniform prior
y_values = np.ones(npoints) / (end - start)

# Prepare figure
fig = plt.figure(figsize=figsize)
ax = fig.add_subplot((111))

# Setup color map
cmap = plt.get_cmap('inferno')
colors = [cmap(i) for i in np.linspace(0, 1, N_max)]

# Iteratively compute the posteriors (using all the data)
N = N_max
for n, decay_x in enumerate(data[:N]):
    
    y_values *= likelihood(decay_x, x_values)
    y_values = normalize(x_values, y_values)
    
    # Label if multiple of 10 data sets
    if (n+1) % 10 == 0:
        ax.plot(x_values, y_values, color=colors[n], label=f"N = {n+1}")
    else:
        ax.plot(x_values, y_values, color=colors[n])

# Configure the plot
ax.set_xlim([start, end])
ax.set_xlabel(r'Characteristic length $\lambda$ (cm)', fontsize=font)
ax.set_ylabel('Probability density', fontsize=font)
ax.legend(loc='upper right', fontsize=font-5)

















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