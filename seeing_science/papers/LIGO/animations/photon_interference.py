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
phase_offset = np.pi
period = 2*np.pi/omega
y_in_arr = np.add(y_pos_arr, phase)
y_in_arr2 = np.add(y_in_arr, phase_offset)


# stack values together into a single array
wave1 = np.stack((x_pos_arr, np.sin(y_in_arr)), axis=2)
wave2 = np.stack((x_pos_arr, np.sin(y_in_arr+3)), axis=2)


# # x-positions of peaks of both sin waves so vertical lines can be added to the plots
# firstpeak1 = x_pos[np.where(wave1[:50,0,1] == np.max(wave1[:50,0,1]))]
# peaks1 = np.arange(firstpeak1-50, 50, period)

# firstpeak2 = x_pos[np.where(wave2[:50,0,1] == np.max(wave2[:50,0,1]))]
# peaks2 = np.arange(firstpeak2-50, 50, period)

# print(np.shape(wave2))
# print(firstpeak2)

# exit()

'''
CREATE SUPERPOSITION OBJECT
'''
supdata = np.stack((x_pos_arr, np.sin(y_in_arr) + np.sin(y_in_arr2) - 3), axis=2)


'''
INITIALIZE PLOT
'''
# initiate the axes
fig,ax1 = plt.subplots(1)
ax1.set_xlim((0,10))

# disable the tickmarks on the axes
ax1.tick_params(bottom = False, left = False, labelbottom = False, labelleft = False)

# set the initial position for the sine waves
sin1 = ax1.plot(wave1[:,0,0], wave1[:,0,1], zorder=10)[0]

sin2 = ax1.plot(wave2[:,0,0], wave2[:,0,1], zorder=10)[0]

sup = ax1.plot(supdata[:,0,0], supdata[:,0,1], zorder=10)[0]


ax1.axhline(-3, color='k', zorder=0)
ax1.axhline(0, color='k', zorder=0)
ax1.axhline(3, color='k', zorder=0)

# peaklines1 = ax1.vlines(peaks1, color='k', ymin=-3, ymax=4)
# peaklines2 = ax1.vlines(peaks2, color='k', ymin=-3, ymax=4)




'''
ANIMATE
'''

# function to move from one frame to the next
def update(frame):
	ax1.cla()
	ax1.set_xlim((0,10))
	
	ax1.plot(wave1[:,frame,0], wave1[:,frame,1])
	ax1.plot(wave2[:,frame,0], wave2[:,frame,1])
	ax1.plot(supdata[:,frame,0], supdata[:,frame,1])
	
	# ax1.vlines(peaks1-phase[frame]/omega, color='k', ymin=-3, ymax=4)
	# ax1.vlines(peaks2-phase[frame]/omega, color='k', ymin=-3, ymax=4)
	ax1.axhline(-3, color='k', zorder=0, lw=0.5)
	ax1.axhline(0, color='k', zorder=0, lw=0.5)
	ax1.axhline(3, color='k', zorder=0, lw=0.5)


ani = FuncAnimation(fig, update, tot_frames, interval=1000/fps, blit=False, repeat=True)
ani.save('test1.gif', writer='pillow', fps=fps)


exit()

'''
CREATE SPIRAL TO MODEL GRAVITATIONAL WAVES
'''
# make an array of different theta values
theta = np.arange(0, 8*np.pi, 0.1)

# coefficients to play with
a = 10
b = 0.25 # number of turns
c = 5. # vary this to get the width of the spiral

framelist = []

x = 0

# loop through frames - each frame is changing by a phase dph 
# this change happens in the limits of dt
phlist = np.linspace(0., 2*np.pi, num=tot_frames)

for dph in phlist:

	# t is the parametrization
	for dt in np.arange(0., np.pi/2., np.pi/2.0):
		
		dt = dt + dph

		x = a*np.cos(theta + dt)*np.exp(b*theta)
		y = a*np.sin(theta + dt)*np.exp(b*theta)

		dt = dt + np.pi/c

		x2 = a*np.cos(theta + dt)*np.exp(b*theta)
		y2 = a*np.sin(theta + dt)*np.exp(b*theta)

		xf1 = np.concatenate((x, x2[::-1]))
		yf1 = np.concatenate((y, y2[::-1]))

		# plot the second spiral
		dt2 = dt + np.pi

		x = a*np.cos(theta + dt2)*np.exp(b*theta)
		y = a*np.sin(theta + dt2)*np.exp(b*theta)

		dt2 = dt2 + np.pi/c

		x2 = a*np.cos(theta + dt2)*np.exp(b*theta)
		y2 = a*np.sin(theta + dt2)*np.exp(b*theta)

		xf2 = np.concatenate((x, x2[::-1]))
		yf2 = np.concatenate((y, y2[::-1]))


	xyf1 = np.stack((xf1, yf1), axis=1)
	xyf2 = np.stack((xf2, yf2), axis=1)

	xyf = np.concatenate((xyf1, xyf2))
	
	framelist.append(xyf)
	

'''
INITIALIZE GRAVITATIONAL WAVE ANIMATION
'''
# initialize axes
fig2,ax2 = plt.subplots(1)
ax2.set_xlim((-300,300))
ax2.set_ylim((-300,300))

# disable the tickmarks on the axes
ax2.tick_params(bottom = False, left = False, labelbottom = False, labelleft = False)
# set the aspect ratio to 1
ax2.set_aspect(aspect=1)

# define the inital spiral - matplotlib treats this as a polygon object
spiral = ax2.fill(framelist[0][:,0], framelist[0][:,1])[0]

# define two circle objects to represent the black holes

BH_dist = 20 # black hole radial distance from the origin

circ1 = plt.Circle((-BH_dist, 0), radius = 15, fc='k', fill=True, zorder=12)
circ2 = plt.Circle((BH_dist, 0), radius = 15, fc='k', fill=True, zorder=12)

circ3 = plt.Circle((0,0), radius = BH_dist, fc='white', fill=True, zorder=10)

#initialize the two BH circles by adding them to the axes as a patch
ax2.add_patch(circ1)
ax2.add_patch(circ2)
ax2.add_patch(circ3)

# add an additional stationary white circle as a patch to avoid
# the weird-looking center of the spiral


# define the function to update the spiral each frame
def updatespiral(frame):
	ax2.cla()
	
	# fix the axes (.cla clears this)
	ax2.set_xlim((-300,300))
	ax2.set_ylim((-300,300))
	
	# move to the next frame in the spiral animation
	ax2.fill(framelist[frame][:,0], framelist[frame][:,1], color='b', zorder=10)[0]
	
	# change the center position of the two circle patches
	x = BH_dist*np.cos(phlist[frame])
	y = BH_dist*np.sin(phlist[frame])
	circ1.center = (BH_dist*np.cos(phlist[frame]),BH_dist*np.sin(phlist[frame]))
	circ2.center = (BH_dist*np.cos(phlist[frame] + np.pi),BH_dist*np.sin(phlist[frame] + np.pi))
	
	# add them to the axes as patches again
	ax2.add_patch(circ1)
	ax2.add_patch(circ2)
	ax2.add_patch(circ3)


# create the animation
ani = FuncAnimation(fig2, updatespiral, frames = tot_frames, interval=1000/fps, blit=False, repeat=True)
ani.save('spiral1.gif', writer='pillow', fps=fps)
plt.show()