# Link to main file

- [README.md](../../README.md)

# How to setup the configuration file

```json
{
    "figure": {                         // Figure related configuration
        "size": [12, 10],               // Set the figure size on inches
        "limits": {                     // To setup the limits
            "use_custom_limits": true,  // Flag to indicate wheter or not to use the custom limits provided below
            "x": {                      // x limits
                "min": 0,
                "max": 235
            },
            "y": {                      // y limits
                "min": 0,
                "max": 235
            }
        },
        "dots_per_inch": 400,           // resolution, pixels per inch
        "marker_size": 0.1,             // marker size for reference points
        "z_expansion": 1,               // expansion ratio for z axis in order to flatten the plots. z_limits = (z_min - Config.Figure.z_expansion * z_range; z_max + Config.Figure.z_expansion * z_range)
        "views": [                      // List of views to be plotted
            [45, 30],                   // [azimuth, elevation] of the view
            [135, 30],
            [225, 30],
            [315, 30]
        ]
    },

    "grid": {           // refrence points provided will be interpolated on this grid
        "shape": {      // shape of the grid
            "x": 100,
            "y": 100
        }
    },

    "color_bar": {      // colorbar setup for z values coloring
        "shrink": 0.5,  // scales the colorbar relative to its default (1.0) size
        "pad": 0.1,     // place further with regards to the plot
        "aspect": 10    // lengh/width of the bar
    },

    "z_probe_bias": {
        "x": -32,
        "y": -25
    }
}
```