# Import the champions
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


def likelihood(x, length):
	"""
	Likelihood function associated with exponential decay 
	over a range from 1 to 20
	"""

	norm = length * (np.exp(-1 / length) - np.exp(-20 / length))
	return np.exp(-x / length) / norm


def normalize(x_data, y_data):
	"""
	Normalize a discrete data set using rectangular integration
	"""

	norm = np.sum(y_data) * (x_data[1] - x_data[0])
	return y_data / norm
	
	
def update(frame, x_values, y_values, ax, data, colors):
	"""
	Update posterior and plot new curve
	"""
	
	y_values *= likelihood(data[frame], x_values)
	y_values = normalize(x_values, y_values)

	# Label if multiple of 10 data sets
	if (frame+1) % 10 == 0:
		ax.plot(x_values, y_values, color=colors[frame], label=f"N = {frame+1}")
	else:
		ax.plot(x_values, y_values, color=colors[frame])


if __name__ == '__main__':

	# Import data
	data = np.loadtxt('radioactive.dat')

	# Range of possible characteristic lengths
	start = 2
	end = 30
	npoints = 1000
	x_values = np.linspace(start, end, num=npoints)

	# Uniform prior
	y_values = np.ones(npoints) / (end - start)

	# Prepare figure
	fig = plt.figure(figsize=(10, 5))
	ax = fig.add_subplot((111))

	# Setup color map
	cmap = plt.get_cmap('inferno')
	colors = [cmap(i) for i in np.linspace(0, 1, data.shape[0])]

	# Configure the plot
	fps = 60
	font = 16
	ax.set_xlim([start, end])
	ax.set_xlabel(r'Characteristic length $\lambda$ (cm)', fontsize=font)
	ax.set_ylabel('Probability density', fontsize=font)
	ax.legend(loc='upper right', fontsize=font-5)

	# Animate the diagram
	ani = FuncAnimation(fig, update, data.shape[0], 
						fargs=(x_values, y_values, ax, data, colors), 
						interval=1000/fps)
	#ani.save('circle.gif', writer='imagemagick', fps=fps)
	plt.show()