import argparse
import os
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata

# Types
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy import ndarray
from numpy.typing import NDArray
from pandas import DataFrame

# matplotlib.use('WebAgg')  # Set to WebAgg for web-based interactive plotting. TYo be used with plt.show()

class Config:

    class Figure:
        ''''''
        size = (12, 10)
        dots_per_inch = 400
        marker_size = 1
        z_expansion = 0.5

        # List of different view angles (azimuth, elevation)
        views = [
            (45, 30),   # View from corner
            (135, 30),  # View from corner
            (225, 30),  # View from corner
            (315, 30),  # View from corner
            # (90, 45),   # View from the side
            # (180, 30),  # View from the back
            # (270, 45),  # View from the left
        ]

        class Limits:
            use_custom_limits = False,
            x_max = 235,
            x_min = 0,
            y_max = 235,
            y_min = 0,

    class Grid:
        class Shape:
            x = 100
            y = 100

    class ColorBar:
        shrink = 0.5
        pad = 0.1
        aspect = 10

    class ZProbeBias:
        x = -32
        y = -25

    def set_plot_parameters(json_dict: dict):
        '''Set the plot parameters from json dictionary'''
        # Store figure parameters
        Config.Figure.size = json_dict["figure"]["size"]
        Config.Figure.dots_per_inch = json_dict["figure"]["dots_per_inch"]
        Config.Figure.marker_size = json_dict["figure"]["marker_size"]
        Config.Figure.z_expansion = json_dict["figure"]["z_expansion"]
        Config.Figure.Limits.use_custom_limits = json_dict["figure"]["limits"]["use_custom_limits"]
        Config.Figure.Limits.x_min = json_dict["figure"]["limits"]["x"]["min"]
        Config.Figure.Limits.x_max = json_dict["figure"]["limits"]["x"]["max"]
        Config.Figure.Limits.y_min = json_dict["figure"]["limits"]["y"]["min"]
        Config.Figure.Limits.y_max = json_dict["figure"]["limits"]["y"]["max"]

        # Store grid parameters
        Config.Grid.Shape.x = json_dict["grid"]["shape"]["x"]
        Config.Grid.Shape.y = json_dict["grid"]["shape"]["y"]

        # Store color bar parameters
        Config.ColorBar.shrink = json_dict["color_bar"]["shrink"]
        Config.ColorBar.pad = json_dict["color_bar"]["pad"]
        Config.ColorBar.aspect = json_dict["color_bar"]["aspect"]

        # Store z probe bias
        Config.ZProbeBias.x = json_dict["z_probe_bias"]["x"]
        Config.ZProbeBias.y = json_dict["z_probe_bias"]["y"]

# --------- Data management functions ---------

def extract_df_coordinates(csv_df: DataFrame) -> tuple[ndarray, ndarray]:
    '''Extract csv data coordinates as numpy array'''
    return csv_df.iloc[:, 1].values, csv_df.iloc[:, 2].values, csv_df.iloc[:, 3].values

def extract_grid_coordinates(grid_data: ndarray):
    '''Extract grid coordinates'''
    return grid_data[0], grid_data[1], grid_data[2]

def flatten_grid_coordinates(grid_x: ndarray, grid_y: ndarray, grid_z: ndarray):
    '''Flatten the 2D arrays into 1D arrays'''
    return grid_x.flatten(), grid_y.flatten(), grid_z.flatten()

# --------- Figures functions ---------

def prepare_plot():
    '''Prepare main features from plots'''
    # Create a figure and 3D axes
    fig = plt.figure(figsize=Config.Figure.size)
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
    # plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

    # Labels
    ax.set_xlabel('X Coordinate [mm]')
    ax.set_ylabel('Y Coordinate [mm]')
    ax.set_zlabel('Z Height [mm]')

    return fig, ax

def scale_xy_axis(ax: Axes, x: ndarray, y: ndarray):
    '''Set x-y axis limits to mantain proportional scaling between the x and y axes'''
    
    # Configure x-y limits
    # ---------------------------------

    if Config.Figure.Limits.use_custom_limits:
        ax.set_xlim(
            Config.Figure.Limits.x_min,
            Config.Figure.Limits.x_max)
        ax.set_ylim(
            Config.Figure.Limits.y_min,
            Config.Figure.Limits.y_max)
        
    else:
        # Get x and y ranges
        x_max, x_min = x.max(), x.min()
        x_range = x_max - x_min
        y_max, y_min = y.max(), y.min()
        y_range = y_max - y_min

        if x_range > y_range:
            # Compute x border spacing
            x_border_spacing = x_range * 0.05

            # Compute max min border limits
            x_max_border = x_max + x_border_spacing
            x_min_border = x_min - x_border_spacing

            # Set x limits
            ax.set_xlim(x_min_border, x_max_border)

            # Compute x axis dimension
            x_axis_dimension = x_max_border - x_min_border

            # Compute y border spacing
            y_border_spacing = (x_axis_dimension - y_range) / 2

            # Set y limits
            y_max_border = y_max + y_border_spacing
            y_min_border = y_min - y_border_spacing
            ax.set_ylim(y_min_border, y_max_border)

        else:
            # Compute x border spacing
            y_border_spacing = y_range * 0.05

            # Compute max min border limits
            y_max_border = y_max + y_border_spacing
            y_min_border = y_min - y_border_spacing

            # Set x limits
            ax.set_ylim(y_min_border, y_max_border)

            # Compute x axis dimension
            y_axis_dimension = y_max_border - y_min_border

            # Compute y border spacing
            x_border_spacing = (y_axis_dimension - x_range) / 2

            # Set y limits
            x_max_border = x_max + x_border_spacing
            x_min_border = x_min - x_border_spacing
            ax.set_xlim(x_min_border, x_max_border)
    
def scale_z_axis(ax: Axes, z: ndarray):
    '''Scale Z axis taking into acount the z expansion provided by configuration'''
    # Get z limits and range
    z_min, z_max = np.min(z), np.max(z)
    z_range = z_max - z_min

    # Set new Z-limits to make the plot "flatter" by expanding the Z range
    ax.set_zlim(
        z_min - Config.Figure.z_expansion * z_range,
        z_max + Config.Figure.z_expansion * z_range)

def add_color_bar(fig: Figure, ax: Axes, surf):
    '''Add a color bar to the plot'''
    color_bar = fig.colorbar(surf, ax=ax, 
                             shrink=Config.ColorBar.shrink,
                             aspect=Config.ColorBar.aspect,
                             pad=Config.ColorBar.pad)
    color_bar.set_label('Z Height (mm)', rotation=270, labelpad=15)

def save_figures(plot_type, output_path_base, fig: Figure, ax: Axes):
    '''Check output path existence. Save the figures provided by configuration->figure->views'''
    # Check output path existence
    if (not os.path.exists(output_path_base)):
        os.makedirs(output_path_base)

    # Save the plot from different views
    for i, (azim, elev) in enumerate(Config.Figure.views):
        ax.view_init(elev=elev, azim=azim)
        output_path = os.path.join(output_path_base, f"{plot_type}_{i + 1}.png")
        fig.savefig(output_path, dpi=Config.Figure.dots_per_inch)
        print(f"Plot saved to {output_path}")

def save_top_figure(plot_type, output_path_base,
                    fig: Figure, ax: Axes,
                    x: ndarray, y: ndarray, z: ndarray):
    '''Create a 3D figure locking from the top'''
    # Create a top view (problems showing scatter)
    ax.view_init(elev=90, azim=-90)  # View from the top
    # Offset Z value for scatter
    z +=0.01
    # Replot scatter
    ax.scatter(x, y, z, c='r', marker='o', s=Config.Figure.marker_size, alpha=1.0)
    # Save top view with a different filename
    output_path = os.path.join(output_path_base, f"{plot_type}_top.png")
    fig.savefig(output_path, dpi=Config.Figure.dots_per_inch)
    print(f"Plot saved to {output_path}")
    
    # Close the plot to release resources
    plt.close()

def create_and_save_2D_view(plot_type, output_path_base, reference_points_df, grid_data):
    '''Create a 2D view from the top and save it into separate file.'''
    # Create a figure
    fig2 = plt.figure(figsize=Config.Figure.size)
    ax2 = fig2.add_subplot(111)

    # Add labels
    ax2.set_xlabel('X Coordinate [mm]')
    ax2.set_ylabel('Y Coordinate [mm]')

    # Extract csv data coordinates
    x, y, _ = extract_df_coordinates(reference_points_df)

    # Extract grid coordinates
    grid_x, grid_y, grid_z = extract_grid_coordinates(grid_data)

    # Scale x y axis to mantain aspect ratio. Scale z axis
    scale_xy_axis(ax2, x, y)

    # Plot the contour (flat 2D view)
    c = ax2.contourf(grid_x, grid_y, grid_z, 20, cmap='viridis')  # 20 levels in the color map

    # Add color bar
    color_bar = fig2.colorbar(c) # Z Height [mm]

    # Add colorbar label
    color_bar.set_label('Z Height (mm)', rotation=270, labelpad=15)

    # Scatter plot
    ax2.scatter(x, y, c='r', marker='o', s=Config.Figure.marker_size, alpha=1.0)

    # Save top view with a different filename
    output_path =  os.path.join(output_path_base, f"{plot_type}_contourf.png")
    fig2.savefig(output_path, dpi=Config.Figure.dots_per_inch)
    print(f"Plot saved to {output_path}")

# --------- MAIN FUNCTIONS ---------

def argument_parser():
    '''Custom argument parser'''
    parser = argparse.ArgumentParser(
                    prog='plot_bed_leveling',
                    description='Creates diferent types of plots to visualize a 3D printer bed leveling',
                    epilog='Enjoy it :)')
    
    parser.add_argument('--csv_path', required=True, help="Csv path")
    parser.add_argument('--output_path_base', required=True, help="output root path")
    parser.add_argument('--plot_type', choices=["surface", "trisurf"], required=True, help="Plot type")
    
    # Get default config path
    cwd = os.getcwd()
    parser.add_argument('--config_path', required=False, help="Configuration file path",
                        default=os.path.join(cwd, 'config', 'config.json'))

    # Collect the arguments
    args = parser.parse_args()

    return args

def read_config(config_path) -> dict:
    '''Read json configuration file'''
    # Open JSON file
    f = open(config_path)

    # Save json object as a dictionary
    json_data = json.load(f)
    print(f"Configuration data:\n{json_data}")

    return json_data

def csv_2_df(csv_path):
    '''Read and proces the csv returning pandas dataframe'''

    # Load CSV into a pandas DataFrame
    csv_df = pd.read_csv(csv_path, sep=";", dtype={"_x_": np.float64 ,"_y_": np.float64, "z_offset_0.01mm": np.float64})
    print(csv_df)

    # Z input step is 0.01mm
    csv_df.iloc[:, 3] = csv_df.iloc[:, 3].values * 0.01

    return csv_df

def process_csv_df(csv_df: DataFrame):
    '''As the measurements from the csv are done with a dial indicator 
    (reloj comparador en español), z measurements must be inverted in
    order to get the "real" height of the bed.'''
    
    # Copy the original df to create the biased (the one with z probe xy bias)
    biased_csv_df = csv_df.copy(deep=True)

    # Apply to it z probe XY bias
    biased_csv_df.iloc[:, 1] = csv_df.iloc[:, 1] + Config.ZProbeBias.x
    biased_csv_df.iloc[:, 2] = csv_df.iloc[:, 2] + Config.ZProbeBias.y

    # If custom limist are provided by configuration
    if Config.Figure.Limits.use_custom_limits:
        # Get the mask for those values inside the limits
        mask_x = (biased_csv_df.iloc[:, 1] >= Config.Figure.Limits.x_min) & \
                 (biased_csv_df.iloc[:, 1] <= Config.Figure.Limits.x_max)
        mask_y = (biased_csv_df.iloc[:, 2] >= Config.Figure.Limits.y_min) & \
                 (biased_csv_df.iloc[:, 2] <= Config.Figure.Limits.y_max)
        mask = mask_x & mask_y

        # Create empty processed dataframe
        processed_csv_df = pd.DataFrame(columns=biased_csv_df.columns)

        # Filter input values
        processed_csv_df.iloc[:, 1] = biased_csv_df.iloc[:, 1][mask]
        processed_csv_df.iloc[:, 2] = biased_csv_df.iloc[:, 2][mask]
        processed_csv_df.iloc[:, 3] = biased_csv_df.iloc[:, 3][mask]
    
    else:  # With no custom limits
        # Place the biased data into processed df
        processed_csv_df = biased_csv_df

    # Get the range of values in z
    z_range = processed_csv_df.iloc[:, 3].max() - processed_csv_df.iloc[:, 3].min()

    # Modify df to invert z values
    processed_csv_df.iloc[:, 3] = z_range - processed_csv_df.iloc[:, 3]

    # Get the middle value
    z_middle = processed_csv_df.iloc[:, 3].min() + z_range/2
    
    # Divide the max and min values in 2 even sides
    processed_csv_df.iloc[:, 3] -= z_middle

    print(f"x min: {processed_csv_df.iloc[:, 1].min()}")
    print(f"x max: {processed_csv_df.iloc[:, 1].max()}")
    print(f"y min: {processed_csv_df.iloc[:, 2].min()}")
    print(f"y max: {processed_csv_df.iloc[:, 2].max()}")
    print(f"z min: {processed_csv_df.iloc[:, 3].min()}")
    print(f"z max: {processed_csv_df.iloc[:, 3].max()}")

    return processed_csv_df

def create_interpolated_grid(csv_df):
    '''Create a grid interpolating the csv data values, return a 3d numpy array with the grid'''
    # Extract csv data coordinates
    x, y, z = extract_df_coordinates(csv_df)

    # Create a grid to interpolate the Z values onto
    grid_x, grid_y = np.mgrid[min(x):max(x):Config.Grid.Shape.x*1j,
                              min(y):max(y):Config.Grid.Shape.y*1j]

    # Interpolate z points
    grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')  # Cubic interpolation for smoothness

    return np.array([grid_x, grid_y, grid_z])

# --------- Main plot functions ---------

def plot_surface(reference_points_df, grid_np, output_path_base):
    '''Surface plot'''
    plot_type = "surface"

    # Extract reference points coordinates
    x, y, z = extract_df_coordinates(reference_points_df)

    # Extract grid coordinates
    grid_x, grid_y, grid_z = extract_grid_coordinates(grid_np)

    # Prepare main features from plot
    fig, ax = prepare_plot()

    # Scale the plot axis
    scale_xy_axis(ax, x, y)
    scale_z_axis(ax, z)

    # Set title
    ax.set_title('Surface Plot')

    surf = ax.plot_surface(grid_x, grid_y, grid_z, cmap='viridis', edgecolor='none')

    # Plot the points
    ax.scatter(x, y, z, c='r', marker='o', s=Config.Figure.marker_size, alpha=1.0)  # You can adjust color and marker style

    # Add color bar
    add_color_bar(fig, ax, surf)

    # Save 3D figures
    save_figures(plot_type, output_path_base, fig, ax)

    # Save top view figure
    save_top_figure(plot_type, output_path_base, fig, ax, x, y, z)

    # Create and save 2D view
    create_and_save_2D_view(plot_type, output_path_base, reference_points_df, grid_np)

def plot_trisurf(reference_points_df, grid_np, output_path_base):
    '''Triangles surface plot'''
    plot_type = "trisurf"

    # Extract reference points coordinates
    x, y, z = extract_df_coordinates(reference_points_df)

    # Extract grid coordinates
    grid_x, grid_y, grid_z = extract_grid_coordinates(grid_np)

    # Flatten the 2D arrays into 1D arrays
    x_flat, y_flat, z_flat = flatten_grid_coordinates(grid_x, grid_y, grid_z)

    # Prepare main features from plot
    fig, ax = prepare_plot()

    # Set title
    ax.set_title('Triangles surface Plot')

    # Scale the plot axis
    scale_xy_axis(ax, x, y)
    scale_z_axis(ax, z)

    # Plot the surface using trisurf
    surf = ax.plot_trisurf(x_flat, y_flat, z_flat, cmap='viridis')

    # Plot the points
    ax.scatter(x, y, z, c='r', marker='o', s=Config.Figure.marker_size, alpha=1.0)  # You can adjust color and marker style

    add_color_bar(fig, ax, surf)

    save_figures(plot_type, output_path_base, fig, ax)

    save_top_figure(plot_type, output_path_base, fig, ax, x, y, z)

    create_and_save_2D_view(plot_type, output_path_base, reference_points_df, grid_np)

if __name__ == "__main__":

    # Get inputs
    args = argument_parser()

    # Store plot parameter from configuration file
    Config.set_plot_parameters(read_config(args.config_path))

    # Read/process csv
    csv_df = csv_2_df(args.csv_path)

    # Invert input z measurements
    processed_csv_df = process_csv_df(csv_df)

    # Create interpolated grid
    grid_np = create_interpolated_grid(processed_csv_df)
    
    if args.plot_type == "surface":
        plot_surface(processed_csv_df, grid_np, args.output_path_base)

    elif args.plot_type == "trisurf":
        plot_trisurf(processed_csv_df, grid_np, args.output_path_base)

