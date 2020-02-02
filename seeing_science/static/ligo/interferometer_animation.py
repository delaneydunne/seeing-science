# Import the champions
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, RadioButtons


fps = 60.0
tot_frames = 300

#frames for the changing plot
tot_frame1 = 60
tot_frame2 = 120
tot_frame3 = 300

sin = np.sin
pi = np.pi
A = 1
frame = 0
len_x = 1000



'''
Plotting the system
'''






x_pos = np.linspace(0, 2*np.pi, len_x)
#print(x_pos)
y_pos =np.array( [np.sin(frame/10 + x_pos) for frame in range(tot_frames)])
print(y_pos.shape)
sinx_wave = np.zeros((tot_frames,2, len_x))
#sinx_wave = np.zeros(( tot_frames,len_x,2))

#sinx_wave[0][:][0] = 1
#print(sinx_wave)

for i in range(tot_frames):
	sinx_wave[i][:][0] = x_pos
	sinx_wave[i][:][1] = y_pos[i]

'''
Plotting sin x consant on the y axis
'''



'''
def xpos2(y)
	return np.array( [np.sin(frame/10 + y) for frame in range(tot_frame)])
'''

def xpos2(y,y_2):
	ar1 = np.array( [np.sin(frame/10 + y)  for frame in range(tot_frame1)])
	ar2 = np.array( [np.sin(frame/10 + y_2)  for frame in range(tot_frame1, tot_frame2)])
	#print(ar1.shape)
	ar3 = np.array( [np.sin(frame/10 + y) for frame in range(tot_frame2, tot_frames)])
	#print(ar2.shape)
	'''
	decoy_1 = np.empty(ar2.shape)
	decoy_1[-120:, :] = ar1
	decoy_ar_r = np.stack((decoy_1, ar2), axis=1)
	ar_r = decoy_ar_r[-1000:,:]
	'''
	ar_r = np.concatenate((ar1,ar2,ar3), axis = 0)
	print(ar_r.shape)
	return ar_r

y_pos2 = np.linspace(0, 2*np.pi, len_x)
y_pos3 = np.linspace(0, 5, len_x)
x_pos2 = xpos2(y_pos2,y_pos3)
#print(x_pos2[0])
#print(x_pos2[150])
siny_wave = np.zeros((tot_frames,2, len_x))


'''
y-positions for the vertical line
'''
y_posv1 = np.array( [2*np.pi  for frame in range(tot_frame1)])
y_posv2 = np.array([5  for frame in range(tot_frame1, tot_frame2)])
y_posv3 = np.array([2*np.pi  for frame in range(tot_frame2, tot_frame3)])
y_posh = np.concatenate((y_posv1, y_posv2, y_posv3), axis = 0)
print(y_posh.shape)
print(y_posh[110])



for i in range(tot_frame1):
	siny_wave[i][:][0] = y_pos2
	siny_wave[i][:][1] = x_pos2[i]



for i in range(tot_frame1, tot_frame2):
	siny_wave[i][:][0] = y_pos3
	siny_wave[i][:][1] = x_pos2[i]

for i in range(tot_frame2, tot_frames):
	siny_wave[i][:][0] = y_pos2
	siny_wave[i][:][1] = x_pos2[i]

#print(siny_wave)

'''
print(sinx_wave)
print()
'''
print(sinx_wave[1][0][0])

'''
print(sinx_wave)
print()
print()
print(sinx_wave[:][2][0])
'''
#data = [np.vstack((x[:,None], y[:,None])) for x, y in zip(x_pos, y_pos)]

'''
y_pos3 = np.linspace(0, 2*np.pi, len_x)
def xpos2(y):
	return np.array( [np.sin(frame/10 + y) for frame in range(tot_frames)])
x_pos3 = xpos2(y_pos3)
siny_wave2 = np.zeros((tot_frames,2, len_x))
for i in range(tot_frames):
	siny_wave2[i][:][0] = y_pos3
	siny_wave2[i][:][1] = x_pos3[i]
'''


fig, ax = plt.subplots()

y = 0
x = 0
z = 9


# ax.hline(y)

ax.plot([0, 2*pi], [y, y], 'k-', lw=2) # x -leg
ax.plot([2*pi,2*pi], [-1, 1], 'k-', lw=2)
#ax.plot([x, x], [0,2*pi], 'k-', lw=2) # y-leg
#ax.plot([-1,1], [2*pi, 2*pi], 'k-', lw=2)

# disable the tickmarks on the axes
ax.tick_params(bottom = False, left = False, labelbottom = False, labelleft = False)



ax.set_xlim([-1, 2*pi+2])
ax.set_ylim([-1,2*pi+2])

y_in = 2*np.pi

line, = ax.plot(sinx_wave[0][0][:],sinx_wave[0][1][:], 'r-')
line2, = ax.plot(siny_wave[0][1][:],siny_wave[0][0][:], 'g-')
line3, = ax.plot([-10, 10], [z, z], 'k-', lw=2)
line4, = ax.plot([-10, 10], [z, z], 'k--', lw=2)
line5, = ax.plot([0, 0], [0,y_in], 'k-', lw=2) # y-leg
line6, = ax.plot([-1,1], [y_in,y_in], 'k-', lw=2)


def update(frame):
	
	line.set_ydata(sinx_wave[frame][1][:])
	line2.set_data(siny_wave[frame][1][:],siny_wave[frame][0][:])
	line3.set_ydata(z - frame/20)
	line4.set_ydata(z + 2 - frame/20)
	line5.set_ydata([0,y_posh[frame]])
	line6.set_ydata([y_posh[frame],y_posh[frame]])
	#print(y_posh[frame])
	#print(frame)

	
ani = FuncAnimation(fig, update, tot_frames, interval= fps, blit=False,repeat=True, save_count=200)
ani.save('interferometer.gif', writer='pillow', fps=fps)






