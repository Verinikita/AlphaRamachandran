# AlphaRamachandran is Ramachandran plotting tool


You can draws a Ramachandran plot based on the input PDB file (e.g. 7xlp.pdb). Makes use of a Gaussian KDE (kernel density estimation) to plot the density of favoured torsion angles (&phi; and &psi;).

![](https://github.com/Verinikita/AlphaRamachandran/blob/main/plot.png)

## Installation

Clone the github proyect and run in colab.

```
!git clone https://github.com/Verinikita/AlphaRamachandran.git
```
you can run it from google collaborative by clicking on the button [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/https://colab.research.google.com/github/Verinikita/Prueba/blob/main/Ramaf.ipynb)

## Usage

AlphaRamachandran includes useful functions to effortlessly draw a Ramachandran plot.
Once the repository was cloned, call the functions

```
from AlphaRamachandran.AlphaRamachan import function
```


### Fetch the PDB file from the online repository

To draw a Ramachandran plot, we need a PDB file. You can use a local PDB file by specifying the path. Alternatively, AlphaRamachandran conveniently includes a function to automatically fetch and locally store the PDB file for the given PDB id.

#### Arguments

```
from AlphaRamachandran.AlphaRamachan.function import fetch
fetch(pdb_file)
```

- ```pdb_file (str|list)```: PDB id(s) corresponding to the PDB entry to be downloaded.
- ```Returns```: path to PDB file.

### Extract &phi; and &psi; angles

AlphaRamachandran extracts the &phi; and &psi; angles from the PDB file by taking advantage of the [Biopython](https://biopython.org/) module.
Additionally, aminoacid residues that were not drawn on the plot can be extract using the ```return_ignored``` argument.

#### Arguments

```
from AlphaRamachandran.AlphaRamachan.function import phi_psi 
phi_psi(pdb_file, return_ignored)
```

- ```pdb_file (str)```: PDB id corresponding to the PDB entry to be downloaded.
- ```return_ignored (bool)```:
    - ```True``` returns a list of tuple with the format (aminoacid, (phi, psi))
- ```Returns```: Dictionary with keys as aminoacid residues and values as (phi, psi) angle values.

### Ramachandran plot

Makes use of the [matplotlib](https://matplotlib.org/) module to draw a highly customizable Ramachandran plot.

#### Arguments

```
plot(pdb_file, cmap='magma', alpha=0.75, dpi=100, save=True, show=False, out='plot.png')
```

- ```pdb_file (str|list)```: PDB id(s) corresponding to the PDB entry to be downloaded.
- ```cmap (str)```: colormap to be used (from matplotlib) for the density of the favoured ("allowed") regions; default is <em>viridis</em>.
- ```alpha (float)```: sets the opacity of the colormap (value between 0-1); default is 0.75.
- ```dpi (int)```: resolution (<em>dots per inch</em>); default is 100.
- ```save (bool)```:
    - ```True```: saves the plot locally; default is True.
- ```show (bool)```:
    - ```True```: shows the plot using the Qt5Agg backend; default is False.
- ```out (str)```: filename to be used in case the plot is saved (i.e. ```save=True```); default is <em>plot.png</em>.
- ```Returns```: Ramachandran plot (can be saved locally).

## Example

Herein you will find an example from the PDB id corresponding to the ATP-competitive MEK inhibitor DS03090629 that overcomes resistance conferred by BRAF overexpression in BRAF-mutated melanoma - [7xlp](https://www.wwpdb.org/pdb?id=pdb_00007xlp) - in the Protein Data Bank. 

```
from AlphaRamachandran.AlphaRamachan.function import plot
plot(7xlp)
```

```
from RamachanDraw import fetch, phi_psi, plot

# PDB id to be downloaded
PDB_id = '7xlp'

# Drawing the Ramachandran plot
plot(fetch(PDB_id))

# Generating a dictionary to store the phi and psi angles
# And returning the ignored aminoacid residues
phi_psi_dict, ignored_res = phi_psi(fetch(PDB_id), return_ignored=True)
```
##Previously install the required packages
```
!pip install matplotlib
!pip install Biopython
!pip install typing
#!pip install math
#!pip install pkg-resources
!pip install numpy
!pip install rich
```
