# Import the champions
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Animation parameters
tot_seconds = 1
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
unit_circle = np.vstack((x_pos[None, :], y_pos[None, :]))

'''
Create static pillars
'''

# Pillar parameters
num_pillars_x = 5
pillar_spacing = 1
pillar_radius = 0.1

pillar_list = []
pillar_circle = pillar_radius * unit_circle
pillar_centers = np.empty((2, num_pillars_x ** 2))

for x in range(num_pillars_x):
    for y in range(num_pillars_x):
        index = x * num_pillars_x + y
        x_pos = x * pillar_spacing
        y_pos = y * pillar_spacing
        pos = np.array([[x_pos, y_pos]])

        pillar_centers[:, index] = pos
        pillar_list.append(pillar_circle + pos.T)

min_dim = -2 * pillar_radius
max_dim = num_pillars_x - 1 + 2 * pillar_radius

'''
Create ball object
'''

class Ball:
    speed = 5e-2

    def __init__(self, position, direction, pillar_centers, pillar_radius,
                 min_x, max_x, min_y, max_y, pbc, graph):

        self.position = position
        self.velocity = direction / np.linalg.norm(direction) * self.speed
        self.pillar_centers = pillar_centers
        self.pillar_radius = pillar_radius
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.pbc   = pbc
        self.graph = graph

        self.width_x = max_x - min_x
        self.width_y = max_y - min_y

    def update(self):

        # DEBUG HERE PLS
        self.graph.set_offsets(self.velocity * 40)
        return

        # Move ball forward
        self.position += self.velocity

        # Check pillar collisions
        deltas = pillar_centers - self.position[:, None]
        squares = np.square(deltas)
        mags = np.sum(squares, axis=0)
        distances = np.sqrt(mags)
        this = np.where(distances < self.pillar_radius)

        # Collision with circle
        if this[0].shape[0] != 0:
            center = pillar_centers[:, this[0]][:, 0]
            direction = self.position - center
            velocity = direction / np.linalg.norm(direction) * self.speed
            self.velocity = velocity

        # Check wall collisions
        if self.pbc:
            if self.position[0] < self.min_x:
                self.position[0] += self.width_x
            elif self.position[0] > self.max_x:
                self.position[0] -= self.width_x
            if self.position[1] < self.min_y:
                self.position[1] += self.width_y
            elif self.position[1] > self.max_y:
                self.position[1] -= self.width_y

        else:
            if self.position[0] < self.min_x or self.position[0] > self.max_x:
                self.velocity[0] *= -1.0
            if self.position[1] < self.min_y or self.position[1] > self.max_y:
                self.velocity[1] *= -1.0

        # Update plot
        self.graph.set_offsets(self.position)


'''
Plot system
'''

# Initiate axes
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)

# Initial pillar posititions
for pillar_line in pillar_list:
    ax.plot(pillar_line[0, :], pillar_line[1, :], '-r')

# Initial ball positions
num_balls = 5
init_pos = np.array([0.5, 0.5])

ball_list = []
angles = np.linspace(0.1, 2.7, num=num_balls)

for i in range(num_balls):

    init_dir = np.array([np.cos(angles[i]), np.sin(angles[i])])
    graph = ax.scatter(init_pos[0], init_pos[1], c='b')
    ball_list.append(Ball(init_pos, init_dir, pillar_centers,
                          pillar_radius, min_dim, max_dim, min_dim, max_dim,
                          True, graph))


# Update axes
def update(frame, ball_list):

    for ball in ball_list:
        ball.update()


'''
Configure plot settings
'''

# Set limits for the plots
ax.set_xlim([min_dim, max_dim])
ax.set_ylim([min_dim, max_dim])
ax.set_xticks([])
ax.set_yticks([])

'''
ANIMATE THE DIAGRAM
'''

ani = FuncAnimation(fig, update, tot_frames, fargs=[ball_list], interval=1000 / fps)
# ani.save('chaos.gif', writer='imagemagick', fps=fps)
plt.show()
