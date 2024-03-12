
import matplotlib.pyplot as plt
import numpy as np

import floris.flow_visualization as flowviz
import floris.layout_visualization as layoutviz
from floris import FlorisModel


"""
This example makes changes to the given input file through the script.
First, we plot simulation from the input file as given. Then, we make a series
of changes and generate plots from those simulations.
"""

# Create the plotting objects using matplotlib
fig, axarr = plt.subplots(2, 3, figsize=(12, 5))
axarr = axarr.flatten()

MIN_WS = 1.0
MAX_WS = 8.0

# Initialize FLORIS with the given input file via FlorisModel
fmodel = FlorisModel("inputs/gch.yaml")


# Plot a horizatonal slice of the initial configuration
horizontal_plane = fmodel.calculate_horizontal_plane(height=90.0)
flowviz.visualize_cut_plane(
    horizontal_plane,
    ax=axarr[0],
    title="Initial setup",
    min_speed=MIN_WS,
    max_speed=MAX_WS
)

# Change the wind speed
horizontal_plane = fmodel.calculate_horizontal_plane(ws=[7.0], height=90.0)
flowviz.visualize_cut_plane(
    horizontal_plane,
    ax=axarr[1],
    title="Wind speed at 7 m/s",
    min_speed=MIN_WS,
    max_speed=MAX_WS
)


# Change the wind shear, reset the wind speed, and plot a vertical slice
fmodel.set(wind_shear=0.2, wind_speeds=[8.0])
y_plane = fmodel.calculate_y_plane(crossstream_dist=0.0)
flowviz.visualize_cut_plane(
    y_plane,
    ax=axarr[2],
    title="Wind shear at 0.2",
    min_speed=MIN_WS,
    max_speed=MAX_WS
)

# # Change the farm layout
N = 3  # Number of turbines per row and per column
X, Y = np.meshgrid(
    5.0 * fmodel.core.farm.rotor_diameters[0,0] * np.arange(0, N, 1),
    5.0 * fmodel.core.farm.rotor_diameters[0,0] * np.arange(0, N, 1),
)
fmodel.set(layout_x=X.flatten(), layout_y=Y.flatten(), wind_directions=[270.0])
horizontal_plane = fmodel.calculate_horizontal_plane(height=90.0)
flowviz.visualize_cut_plane(
    horizontal_plane,
    ax=axarr[3],
    title="3x3 Farm",
    min_speed=MIN_WS,
    max_speed=MAX_WS
)
layoutviz.plot_turbine_labels(fmodel, axarr[3], plotting_dict={'color':"w"}) #, backgroundcolor="k")
layoutviz.plot_turbine_rotors(fmodel, axarr[3])

# Change the yaw angles and configure the plot differently
yaw_angles = np.zeros((1, N * N))

## First row
yaw_angles[:,0] = 30.0
yaw_angles[:,3] = -30.0
yaw_angles[:,6] = 30.0

## Second row
yaw_angles[:,1] = -30.0
yaw_angles[:,4] = 30.0
yaw_angles[:,7] = -30.0

horizontal_plane = fmodel.calculate_horizontal_plane(yaw_angles=yaw_angles, height=90.0)
flowviz.visualize_cut_plane(
    horizontal_plane,
    ax=axarr[4],
    title="Yawesome art",
    cmap="PuOr",
    min_speed=MIN_WS,
    max_speed=MAX_WS
)

layoutviz.plot_turbine_rotors(fmodel, axarr[4], yaw_angles=yaw_angles, color="c")

# Plot the cross-plane of the 3x3 configuration
cross_plane = fmodel.calculate_cross_plane(yaw_angles=yaw_angles, downstream_dist=610.0)
flowviz.visualize_cut_plane(
    cross_plane,
    ax=axarr[5],
    title="Cross section at 610 m",
    min_speed=MIN_WS,
    max_speed=MAX_WS
)
axarr[5].invert_xaxis()


plt.show()
