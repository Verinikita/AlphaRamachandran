
######FETCH
from Bio.PDB import PDBList
from typing import Union


def fetch(pdb: Union[str, list]):
    def start(pdb_id: str):
        return PDBList().retrieve_pdb_file(pdb_code=pdb_id, pdir='PDB', file_format='pdb')

    if type(pdb) is str:
        return start(pdb_id=pdb)
    if type(pdb) is list:
        return [start(pdb_id=entry) for entry in pdb]


##PHI-PSI
from Bio.PDB import PDBParser, PPBuilder
from math import pi
from rich.console import Console
from rich.table import Table

console = Console(color_system='windows')


def phi_psi(pdb_file, return_ignored=False):
    def get_ignored_res(file: str):
        x, y, ignored, output = [], [], [], {}
        for model in PDBParser().get_structure(id=None, file=file):
            for chain in model:
                peptides = PPBuilder().build_peptides(chain)
                for peptide in peptides:
                    for aa, angles in zip(peptide, peptide.get_phi_psi_list()):
                        residue = chain.id + ":" + aa.resname + str(aa.id[1])
                        output[residue] = angles

        for key, value in output.items():
            # Only get residues with both phi and psi angles
            if value[0] and value[1]:
                x.append(value[0] * 180 / pi)
                y.append(value[1] * 180 / pi)
            else:
                ignored.append((key, value))

        return output, ignored, x, y

    def start(fp: str):
        phi_psi_data, ignored_res, x, y = get_ignored_res(file=fp)

        if return_ignored:
            table = Table(title='Ignored residues')
            table.add_column('Aminoacid\nresidue', style='red')
            table.add_column('\u03C6-\u03C8\nangles', justify='center')
            for _ in ignored_res:
                table.add_row(_[0], str(_[1]))
            console.print(table)

            return phi_psi_data, ignored_res
        else:
            return phi_psi_data

    if type(pdb_file) is str:
        output = start(fp=pdb_file)
    if type(pdb_file) is list:
        output = []
        for file in pdb_file:
            output.append(start(fp=file))

    return output

##PLOT
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from Bio.PDB import PDBParser, PPBuilder
from pkg_resources import resource_stream
from math import pi


def plot(pdb_file, cmap='magma', alpha=0.75, dpi=100, save=True, show=False, out='plot.png'):
    batch_mode = isinstance(pdb_file, list)

    def get_ignored_res(file: str):
        x, y, ignored, output = [], [], [], {}
        for model in PDBParser().get_structure(id=None, file=file):
            for chain in model:
                peptides = PPBuilder().build_peptides(chain)
                for peptide in peptides:
                    for aa, angles in zip(peptide, peptide.get_phi_psi_list()):
                        residue = aa.resname + str(aa.id[1])
                        output[residue] = angles

        for key, value in output.items():
            # Only get residues with both phi and psi angles
            if value[0] and value[1]:
                x.append(value[0] * 180 / pi)
                y.append(value[1] * 180 / pi)
            else:
                ignored.append((key, value))

        return output, ignored, x, y

    size = [(8.5, 5) if batch_mode else (5.5, 5)][0]
    plt.figure(figsize=size, dpi=dpi)
    ax = plt.subplot(111)
    ax.set_title("".join(["Batch" if batch_mode else pdb_file]))

    # Import 'density_estimate.dat' data file
    #Z = np.fromfile(resource_stream('RamachanDraw', '/content/RamachanDraw/data/density_estimate.dat'))
    #Z = np.reshape(Z, (100, 100))

    Z = np.fromfile("./AlphaRamachandran/AlphaRamachan/data/density_estimate.dat")
    Z = np.reshape(Z, (100, 100))

    ax.set_aspect('equal')
    ax.set_xlabel('\u03C6')
    ax.set_ylabel('\u03C8')
    ax.set_xlim(-180, 180)
    ax.set_ylim(-180, 180)
    ax.set_xticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
    ax.set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
    plt.axhline(y=0, color='k', lw=0.5)
    plt.axvline(x=0, color='k', lw=0.5)
    plt.grid(visible=None, which='major', axis='both', color='k', alpha=0.2)

    # Normalize data
    data = np.log(np.rot90(Z))
    ax.imshow(data, cmap=plt.get_cmap(cmap), extent=[-180, 180, -180, 180], alpha=alpha)

    # Fit contour lines correctly
    data = np.rot90(np.fliplr(Z))
    ax.contour(data, colors='k', linewidths=0.5,
               levels=[10 ** i for i in range(-7, 0)],
               antialiased=True, extent=[-180, 180, -180, 180], alpha=0.65)
    

    def start(fp, color=None):
        assert os.path.exists(fp), \
            'Unable to fetch file: {}. PDB entry probably does not exist.'.format(fp)
        phi_psi_data, ignored_res, x, y = get_ignored_res(file=fp)
        ax.scatter(x, y, marker='.', s=3, c="".join([color if color else 'k']), label=fp)
        return phi_psi_data, ignored_res, x, y

    if batch_mode:
        file_output_map = {key: None for key in pdb_file}
        for _, file in enumerate(pdb_file):
            start(fp=file, color=list(mcolors.BASE_COLORS.keys())[_])
            file_output_map[file] = (phi_psi_data, ignored_res, x, y)
        ax.legend(bbox_to_anchor=(1.04, 1), loc='upper left')
    else:
        output = start(fp=pdb_file)

    if save:
        plt.savefig(out)
    if show:
        plt.show()

    # Return params
    if batch_mode:
        return ax, None #file_output_map
    else:
        return ax, None #output
