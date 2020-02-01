# Import libraries
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

'''
CREATE SINE WAVE OBEJCTS
'''

# create a sin wave with angular frequency omega, changing in time
# an offset can be added to this to put two waves out of phase and also to change the time the sin wave is 
# being displayed as 

sin_res = 100
omega = 2 #angular frequency

x_pos =  np.linspace(0, 10, num=sin_res)
y_pos = np.sin(x_pos*omega)



'''
DEFINE ANIMATION PARAMETERS
'''
# Animation parameters
spatial_resolution = 0.1
tot_frames = 360
fps = 30
dx = 0.1


'''
GENERATE DATA SETS
'''
# input to the sin function
y_in = np.array(x_pos*omega).reshape(sin_res,1)

# x-positions for all frames
x_pos_arr = np.tile(x_pos.reshape(sin_res,1), (1, tot_frames))


# y-positions for all frames
y_pos_arr = np.tile(y_in, (1, tot_frames))


# generate phase changing with time
phase = spatial_resolution*np.arange(tot_frames)

# offset y-positions for each individual frame
phase_offset = 0
y_in_arr = np.add(y_pos_arr, phase)
y_in_arr2 = np.add(y_in_arr, phase_offset)


# stack values together into a single array
wave1 = np.stack((x_pos_arr, np.sin(y_in_arr)), axis=2)
wave2 = np.stack((x_pos_arr, np.sin(y_in_arr2)+3), axis=2)



'''
CREATE SUPERPOSITION OBJECT
'''
supdata = np.stack((x_pos_arr, np.sin(y_in_arr) + np.sin(y_in_arr2) - 3), axis=2)


'''
INITIALIZE PLOT
'''
# initiate the axes
fig,ax1 = plt.subplots(1)

# set the initial position for the sine waves
sin1 = ax1.plot(wave1[:,0,0], wave1[:,0,1])[0]

sin2 = ax1.plot(wave2[:,0,0], wave2[:,0,1])[0]

sup = ax1.plot(supdata[:,0,0], supdata[:,0,1])[0]


'''
ANIMATE
'''

# function to move from one frame to the next
def update(frame):
	sin1.set_data(wave1[:,frame,0], wave1[:,frame,1])
	sin2.set_data(wave2[:,frame,0], wave2[:,frame,1])
	sup.set_data(supdata[:,frame,0], supdata[:,frame,1])
	


ani = FuncAnimation(fig, update, tot_frames, interval=1000/fps, blit=False, repeat=True)
ani.save('test1.gif', writer='pillow', fps=fps)
