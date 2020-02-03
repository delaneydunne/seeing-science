# Import the champions
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Animation parameters
tot_seconds = 5
fps = 60

# Total number of frames
tot_frames = int(fps * tot_seconds)

'''
Create unit circle
'''

# Generate circle position array
num = 100
circle_angles = np.linspace(0, 2 * np.pi, num=num)
x_pos = np.cos(circle_angles)
y_pos = np.sin(circle_angles)
unit_circle = np.vstack((x_pos[None,:], y_pos[None,:]))

'''
Create static pillars
'''

# Pillar parameters
num_pillars_x = 5
pillar_spacing = 1
pillar_radius = 0.3

pillar_list = []
pillar_circle = pillar_radius * unit_circle
pillar_centers = np.empty((2, num_pillars_x**2))

for x in range(num_pillars_x):
	for y in range(num_pillars_x):
		
		index = x * num_pillars_x + y
		x_pos = x * pillar_spacing
		y_pos = y * pillar_spacing
		pos = np.array([[x_pos, y_pos]])
		
		pillar_centers[:, index] = pos
		pillar_list.append(pillar_circle + pos.T)

'''
Create ball object
'''

num_balls = 1
init_pos = np.array([0, 0]) * 1.0
init_dir = np.array([1, 1]) * np.sqrt(2) / 2

class Ball:
	
	speed = 1e-1
	
	def __init__(self, position, direction, pillar_centers, pillar_radius, graph):
		self.position = position
		self.velocity = direction * self.speed
		self.pillar_centers = pillar_centers
		self.pillar_radius = pillar_radius
		self.graph = graph
	
	def update(self):
		self.position += self.velocity
		
		# Ignore pillar collisions
		self.graph.set_offsets(self.position)

'''
Plot system
'''

# Initiate axes
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)

# Initial pillar posititions
for pillar_line in pillar_list:
	ax.plot(pillar_line[0,:], pillar_line[1,:], '--r')

# Initial ball positions
ball_list = [Ball(init_pos, init_dir, pillar_centers, pillar_radius, \
			ax.scatter(init_pos[0], init_pos[1])) for i in range(num_balls)]

# Update axes
def update(frame):
	for ball in ball_list:
		ball.update()

'''
Configure plot settings
'''

# Set limits for the plots
ax.set_xlim([-2 * pillar_radius, num_pillars_x - 1 + 2 * pillar_radius])
ax.set_ylim([-2 * pillar_radius, num_pillars_x - 1 + 2 * pillar_radius])
ax.set_xticks([])
ax.set_yticks([])

'''
ANIMATE THE DIAGRAM
'''

ani = FuncAnimation(fig, update, tot_frames, interval=1000/fps)
#ani.save('animation.gif', writer='imagemagick', fps=fps)
plt.show()