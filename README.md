# C. Elegans Model Generation

- [Setup](#setup)
- [Normal Usage](#normal-usage)
- [Configuration File](#configuration-file)
    - [The settings section](#the-settings-section)
    - [The data section](#the-data-section)
- [Cell Key File](#cell-key-file)
- [Model Generation Outline](#cell-key-file)

## Setup
**Anaconda**: I highly recommend you get the Anaconda distribution for Python which can be found [here](https://www.anaconda.com/products/individual). When you install, make sure that you check the box for **"ADD TO PATH"** so that you can run jupyter notebook from the command line. 

**Plotly**: In case you are interested in running visualizations and after you've installed Anaconda, run `conda install -c plotly plotly`.

**Download Script**: Because this script is located on GitHub, you should be able to download the latest version just by clicking the "Code" button on the top-right corner and then clicking "Download ZIP"; you will then need to unzip this. To open up the command line/terminal, navigate to the start menu and search for "Command Prompt" or "Powershell" on Windows. Then navigate to the project folder by typing `cd "C:\This_Project_Path"`.

![download image](https://i.imgur.com/9MlhHNI.png "Download Image")

[Go to top](#c-elegans-model-generation)

## Normal Usage
This code is written so that you will NEVER have to touch the code, only the `config.json` and `cell_key.json` files. To start up the script, navigate to the root directory of the project folder in a terminal and enter `jupyter notebook c_elegans_model_building.py`. This will then open up the jupyter notebook in your default browser. If this doesn't work, then look in the terminal for a link and the copy-paste that into your browser of choice. Afterwards, the only thing the should potentially be edited is the `name = ` variable on the very first line. After the program is run, the output/workspace will be in a subfolder within the `workspace` folder with this `name` preceeded by a run date.

![edit_name](https://i.imgur.com/QxpVbHJ.png "Edit Name")

For the `config.json` file in this directory prior to your first run, make sure that all the filepaths and drive letters are correct since it might be different for different computers. After this check, the only thing that you should ever be editing is the `data -> strains` section by adding to the list that's already there. Make sure that you have the sections `name` which you can choose, `include` is set to `true` if you want it included in the model, and `folderpaths` is a ___list___ of folder locations where the RegA/RegB folders are. A new entry will look something like this, but with a real filepath:

```json
{
    "name": "KP9305_NU",
    "include": true,
    "folderpaths": [
        "Y:\\-\\Cell Tracking Project\\KP9305_NU\\073018_KP9305_NU\\Pos0",
        "Y:\\-\\Cell Tracking Project\\KP9305_NU\\073018_KP9305_NU\\Pos4",
        "Y:\\-\\Cell Tracking Project\\KP9305_NU\\073018_KP9305_NU\\Pos2"
    ]
}
```

Make sure that in these filepaths that you have listed, there is either a `CellKey.xlsx` or `cell_key.json` file. If there is a `CellKey.xlsx` file, but no `cell_key.json` file, the program will parse the Excel file and auotmatically generate the `cell_key.json` file. The program will always prioritize the `.json` file and ignore the `xlsx` file, so make edits in the `.json` file if it's there. This file should look something like what's shown below. If the folder structure of a specific worm is different, reference the [cell key](#cell-key-file) section

```json
{
    "end": 108,
    "mapping": {
        "A1": "cell_name_1",
        "A2": "cell_name_20",
        "A3": "cell_name_5",
    },
    "name": "OD1599_NU_1206_Pos2",
    "outliers": [],
    "start": 15
}
```


Afterwards, hit the "Restart + Run" button on the toolbar which looks like a double forward arrow:

![run script](https://i.imgur.com/k2avJS1.png)

You might be prompted to clear variables; just type 'y' to start a clean run. While the script runs, you will see outputs for potential errors as well as steps. If you wish to ignore the errors, then that's fine, but some will break the code. After the code is completed at Step 8, you will see a `Output location:` filepath for where the model as been placed. You can then stick this into MIPAV to generate a model. For more information about the `config.json` and `cell_key.json` files, read below.

[Go to top](#c-elegans-model-generation)

## Configuration File
**Location**: `config.json`

**Purpose**: This file is responsible for the settings of the entire model.

**Usage**: The first layer of this json file contains a `settings` and a `data` section. The `settings` section contains all of the neccesary default information (more on this later) to generate the model. Within `settings` there are additional sections:

### The `settings` section

The `folderpaths` section is used for importing data and contains the default MIPAV folder structure to be used for each strain's position. The "#" in `data_folderpath` will be replaced by a volume number. You do not need to worry about what that number is, but make sure that "#" is in there somewhere. All of the other folders below that use the `data_folderpath` as the root directory for that volume.
```json
"folderpaths": {
    "side": "RegB",
    "data_folderpath": "Decon_reg_#\\Decon_reg_#_results",
    "straightened_seam_cells": "straightened_seamcells\\straightened_seamcells.csv",
    "straightened_annotations": "straightened_annotations\\straightened_annotations.csv",
    "straightened_lattice": "straightened_lattice\\straightened_lattice.csv",
    "twisted_seam_cells": "seam_cell_final\\seam_cells.csv",
    "twisted_annotations": "integrated_annotation\\annotations.csv",
    "twisted_lattice": "lattice_final\\lattice.csv"
},
```

The `outlier_removal` section is part of Step 2. `remove_outliers` is simply a flag for whether or not you would like to try and remove outliers for this step. If it is true, then outliers will be removed using a Hampel filter according to the window size `window_size` and standard deviation `n_stdev`.
```json
"outlier_removal": {
    "remove_outliers": true,
    "n_stdev": 5,
    "window_size": 5
},
```

The `interpolation` section is part of Step 3. The `total_min` parameter is defines how many minutes the model should be interpolated to. The `min_timepoints_required` is an error flag that will show and log an error if there are less than this value; this is important because interpolation requires a certain number of points to work. The `method` defines the method of interpolation which can take any of the options shown in `kind` parameter of [interp1d](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html#scipy.interpolate.interp1d): `linear`, `nearest`, `zero`, `slinear`, `quadratic`, `cubic`, `previous`, `next`). The `seam_cells_on` section is a mapping of when each seam cell turns on from 0 (model start) to 1 (model end). Currently, most of the cells turn on the at the beginning, but the Q-cells turn on approximately two-thirds of the way through.

```json
"interpolation": {
    "total_min": 420,
    "min_timepoints_required": 3,
    "method": "linear",
    "seam_cells_on": {
        "H0L": 0,
        "H0R": 0,
        "H1L": 0,
        "H1R": 0,
        "H2L": 0,
        "H2R": 0,
        "V1R": 0,
        "V1L": 0,
        "V2R": 0,
        "V2L": 0,
        "V3R": 0,
        "V3L": 0,
        "V4L": 0,
        "V4R": 0,
        "QL": 0.667,
        "QR": 0.667,
        "V5L": 0,
        "V5R": 0,
        "V6L": 0,
        "V6R": 0,
        "TL": 0,
        "TR": 0
    }
}
```

The `warping` section, which is part of Step 5, currently only contains a list of `seam_cells` which are used to actually warp all the points to the warping model. The warp is performed using a thin-plate spline (more on this later).

```
"warping": {
    "seam_cells": [
        "H0L", 
        "H0R", 
        "H1L", 
        "H1R", 
        "H2L", 
        "H2R", 
        "V1R", 
        "V1L", 
        "V2R", 
        "V2L",
        "V3R",
        "V3L",
        "V4L",
        "V4R",
        "V5L",
        "V5R",
        "V6L",
        "V6R",
        "TL",
        "TR"
    ]
}
```

The `smoothing` section is part of Step 4 which generates the warping model and Step 7 which does a moving average of all the annotation points. The `window_size` parameter (not to be confused with the filter window in `outlier_removal`) defines the window size for the moving average. The moving average truncates the windows at endpoints and ignores 0 values (more on this later).

```json
"smoothing": {
    "window_size": 20
}
```

The `mipav_output` section is a part of Step 8, which takes the model and converts from dict/json format to csv format so that MIPAV can generate the appropriate animation. The `labels_on` parameter denotes whether or not labels should be present in the MIPAV animation. It takes a boolean value, `true` or `false`, case sensitive.

```json
"mipav_output": {
    "labels_on": true
}
```

[Go to top](#c-elegans-model-generation)

### The `data` section

The data section contains additional sections as well: `seam_cells` and `strains`. The `seam_cells` section is a list of folder paths/positions to use to create the warping model in Step 4.

```json
"seam_cells": [
            "Y:\\-\\Cell Tracking Project\\JCC596_NU\\091119_Pos3\\Decon_registered",
            "Y:\\-\\Cell Tracking Project\\JCC596_NU\\091119_Pos2\\Decon_registered",
            "Y:\\-\\Cell Tracking Project\\JCC596_NU\\082619_Pos3\\Decon_registered"
]
```

The `strains` section contains a list of information regarding the strains. Each strain contains the `name` which you define, `include` which is whether or not you want to include it in the run sparing you from retyping the information, and `folderpaths` which is a list of the single worm data. Here, I've only listed two strains. Also note that you are not limited to 3 positions per strain.

```json
"strains": [
    {
        "name": "OD1599_NU",
        "include": true,
        "folderpaths": [
            "Y:\\-\\Cell Tracking Project\\OD1599_NU\\OD1599_MostRecent\\120619_Pos2\\Decon_reg",
            "Y:\\-\\Cell Tracking Project\\OD1599_NU\\OD1599_MostRecent\\112719_Pos3\\Decon_Reg",
            "Y:\\-\\Cell Tracking Project\\OD1599_NU\\OD1599_MostRecent\\112619_Pos0\\Decon_reg"
        ]
    },
    {
        "name": "DCR6485_RPM1_NU",
        "include": true,
        "folderpaths": [
            "Y:\\-\\Cell Tracking Project\\DCR6485_RPM1_NU\\011419_Pos0\\Decon_reg",
            "Y:\\-\\Cell Tracking Project\\DCR6485_RPM1_NU\\011419_Pos4\\Decon_reg",
            "Y:\\-\\Cell Tracking Project\\DCR6485_RPM1_NU\\021020_Pos2\\Decon_Reg"
        ]
    }
]
```

[Go to top](#c-elegans-model-generation)

## Cell Key File
**Location**: This file should be located in whatever folder that contains your Reg A/Reg B folders defined in the `config.json` file in the root directory. It should be named `cell_key.json`. Currently, if you have a `CellKey.xlsx` file, the program will automatically generate a json file for you as long as it follows the older format. After this is done, you should go back and check that this information is correct.

**Purpose**: This file defines the `start` and `end` times of the specific worm in a strain as well as mapping IDs from MIPAV to actual cell names. You can also override defaults here (more on this later).

**Usage**: As stated previously, you can define the `start` and `end` volumes here as integers. The `outliers` parameter is a list of volumes to ignore (not currently used), the `name` is any name you can give the specific worm, and the `mapping` is a dictionary containing an ID to cell name association. Both the key and value in `mapping` should be strings.

```json
{
    "end": 108,
    "mapping": {
        "A10": "RMDVR",
        "A14": "ASHL",
        "A15": "RIBL",
        "A5": "OLQVL",
        "A6": "SMDVL",
        "C3": "RIGL",
        "D2": "CEPshVL",
        "D3": "URAVL",
        "D4": "Hyp6"
    },
    "name": "OD1599_NU_1206_Pos2",
    "outliers": [],
    "start": 15
}
```

[Go to top](#c-elegans-model-generation)

### Overiding Defaults
Because MIPAV has changed over the course of this project, we need a way to account for different file structures. If you include a `folderpaths` section like from the config file here, it will read in data according to this structure instead.

```json
{
    "folderpaths": {
        "side": "RegB",
        "data_folderpath": "Decon_reg_#\\Decon_reg_#_results",
        "straightened_seam_cells": "other_straightened_seamcells\\straightened_seamcells.csv",
        "straightened_annotations": "other_straightened_annotations\\straightened_annotations.csv",
        "straightened_lattice": "other_straightened_lattice\\straightened_lattice.csv",
        "twisted_seam_cells": "other_seam_cell_final\\seam_cells.csv",
        "twisted_annotations": "other_integrated_annotation\\annotations.csv",
        "twisted_lattice": "other_lattice_final\\lattice.csv"
    },
    "end": 108,
    "mapping": {
        "A10": "RMDVR",
        "A14": "ASHL",
        "A15": "RIBL",
        "A5": "OLQVL",
        "A6": "SMDVL",
        "C3": "RIGL",
        "D2": "CEPshVL",
        "D3": "URAVL",
        "D4": "Hyp6"
    },
    "name": "OD1599_NU_1206_Pos2",
    "outliers": [],
    "start": 15
}
```

[Go to top](#c-elegans-model-generation)

## Model Generation Outline

The generation of the model is broken down into 8 major steps and I'll be outlining them here.

### Pre-run Processing

First thing you should do is **define the name of the run**, maybe use something like the strain name (e.g. `JCC596_NU`) or some identifier (e.g. `NerveRingTest`). This is used to generated the workspace name so if it is not unique (which is not always a problem), the workspace will be overwritten. Next, the workspace is actually generated. You might notice that what displays is something like `Workspace folderpath: workspace\2020_08_16-JCC596_NU` where the date is tagged onto the run name. This is to keep things more organized when we go back and look a models in the future. After, the `config.json` file is loaded into the program and used throughout the run.

### Step 1: Import all the necessary data

This goes through each of the folders from the `config.json` defined in the `data -> strains` section and loads it into a variable called `compiled_data`. This variable contains each strain's worms as well as each worm's `cell_key`, `seam_cells`, `annotations`, and `errors` found while parsing (more on this below). The program uses a `cell_keys.json` as defined above instead of a `CellKey.xls` for ease of importing the information. However, if a `CellKeys.xlsx` does not exist according to the `get_cell_key`, then the program will try to automatically generate a `cell_keys.json` based of of what's in the Excel file; this operation is performed by the `convert_cell_key_csv2json` function. The output of this step is located in the workspace folder as `1_compiled_data.json`.

**Errors:** In this step, errors are determined within the `get_cell_key` and `parse_mipav_data` functions. Here is a list of checks that it currently does + prints/logs:

- If there is neither a `cell_key.json` or `CellKeys.xlsx` file.
- If there is an empty seam cell file.
- If there is an empty annotation file.
- If there is a mis-match between cells in the twisted and straightened seam cell files. 
- If there is a mis-match between cells in the twisted and straightened annotation files.
- If there are extra seam cells according to what's in `config.json` `settings -> interpolation -> seam_cells_on`
- If there are identical IDs in the straightened annotation files.
- If it failed to read a file.

### Step 2: Outlier detection using a Hampel filter

This goes through each of the worms in each strain and filters each axis according to the parameters defined in `config.json` in the `settings -> outlier_removal` section. Again, `window_size` is the window size for filtering where any window that goes past the data is augmented in a reflection scheme. This was chosen because it was the most natural representation of the data past the endpoints. Additionally, `n_stdev` is just the number of standard deviations past the median to be considered an outlier. If a point is deemed an outlier, it is replaced with the median of the window. The output of this step is located in the workspace folder as `2_compiled_data_no_outliers.json`.

**Errors:** This step currently does not log any errors.

### Step 3: Interpolation to the appropriate time-scale

This goes through each of the worms in each strain and interpolates to a time in minutes based on the method defined in `config.json` (`settings -> interplation -> total_min` and `settings -> interplation -> method`, respectively). It is recommended that `linear` interpolation is used, but as stated previously, you have an option of choosing between `linear`, `nearest`, `zero`, `slinear`, `quadratic`, `cubic`, `previous`, and `next`. Seam cells and annotations are handled differently here because annotations are assumed to exist at the start of the run, but seam cells can turn on a different times. Using what's defined in `config.json`'s `settings -> interplation -> seam_cells_on`, the program either trucancates data that starts earlier than when it's supposed to. If there is less data than what is expected, then the program will simply start it after the designated start time defined in the config file. The output of this step is located in the workspace folder as `3_compiled_data_interpolation.json`.

**Errors:** In this step, errors are to ensure that interpolation is possible and/or meets the number of points required by user-designation in `config.json` in the `settings -> interpolation -> min_timepoints_required` where `min_timepoints_required` refers to the number of raw volumes. It should be noted that the code will break here if the data does not allow for interpolation. Here is a list of checks that it currently does + prints/logs:

- If there are insufficient timepoints for interpolation.

### Step 4: Generate the seam cell warping model

This uses the combined data that has already been loaded in w/ outliers removed, interpolates according to parameters in Step 3, averages the cell positions across multiple worms, and then smooths the averaged positions using a moving average whose window is defined in `config.json` in `settings -> smoothing -> window_size`. This step currently ignores the Q-cells QL and QR. There are currently plans to load in outside models such as from the original Untwisting paper; this is still a work in progress. The output of this step is located in the workspace folder as `4_seam_cell_warping_model.json`.

**Errors:** This step currently does not log any errors.

### Step 5: Warp all individual worms to warping model

This step warps all of the worms in each strain to the warping model created or loaded-in from Step 4. The code first reorders the cells so that each timepoint contains all of the cells necessary for warping. The function `thin_plate_spline_warp` is imported from `thin_plate_spline_warp.py` and is a Python analog of the original MATLAB script used in the previous model building code which can be found [here](https://www.mathworks.com/matlabcentral/fileexchange/37576-3d-thin-plate-spline-warping-function). From there, the function takes in the original control point positions (`warp_from`), the new control point positions (`warp_to`), and the points to be warped from the original space (`ordered_coord_list`). Because there is no identifier for which cell corresponds to which coordinate, the program simply uses a sorted list of the cell names. The output of this step is located in the workspace folder as `5_compiled_data_warped.json`.

**Errors:** This step currently does not log any errors.

### Step 6: Creation of the averaged model

After all of the worms in each strain have been warped, Step 6 averages all of the coordinates together by cell. This includes both seam cells and annotations, but because seam cells were the control points in warping, they are virtually the same as in Step 4 even when averaged. The output of this step is located in the workspace folder as `6_cell_coordinates_by_timepoint.json`.

**Errors:** This step currently does not log any errors.

### Step 7: Creation of the smoothed model

After all of the seam cells and annotations have been averaged, Step 7 smoothes via moving average for each cell by dimension according to the window defined in `settings -> smoothing -> window_size`. The output of this step is located in the workspace folder as `7_cell_coordinates_by_timepoint_smoothed.json`. With this step, the model is now complete.

**Errors:** This step currently does not log any errors.

### Step 8: Output model into MIPAV-readable format

This step takes the model and simply outputs it into the `output` folder in the workspace. The parameters used here are located in  `settings -> mipav_output -> labels_on` which takes a boolean value (`true` or `false`, case sensitive). The program will print out a filepath that can be used with the Untwising Plugin for MIPAV. Simply put this filepath in the "Data directory (marker 1)" field in the GUI and select "create annotation animation" in the Build/Edit section. This will create an `animation` folder in the `output` folder which can then be post-processed using another software like ImageJ.

**Errors:** This step currently does not log any errors.

[Go to top](#c-elegans-model-generation)
