# Zinc Package for AutoDock Bias
R. Buccheri¹, A. Coco¹, A. Rescifina¹\
¹*University of Catania*

[![Python](https://img.shields.io/badge/Python-3.11.7-blue.svg)](https://www.python.org/)

A Python script was created to improve the docking of ligands to HDAC enzymes. This script enhances the recognition of the Zn²⁺ ion by the AutoDock Bias package, implemented in MGLTools (https://ccsb.scripps.edu/mgltools/downloads/).
## System Requirements
* Linux-based operating system (e.g., Ubuntu, Debian, Fedora, CentOS)
* Python 3.11

## Package Requirements
* numpy
* scipy
* matplotlib

To install required packages run:
````
$ pip install numpy scipy matplotlib
````
## Protein preparation
**Pay attention!** The protein must be prepared using ChimeraX software (we used v1.7.1) for the scripts to work properly.

ChimeraX software can be downloaded for free from https://www.cgl.ucsf.edu/chimerax/download.html.

## Tutorial
The script is an implementation of the AutoDock Bias package. If you are new to AutoDock Bias, we recommend referring to the tutorial in the User Guide (https://autodockbias.wordpress.com/).

The Zinc Package consists of two scripts that must be copied and pasted into the working folder containing the protein with zinc ion. 

**STEP 1**\
At this point the script can be launched:

````
$ python parse_pdb.py -p protein_name.pdb
````
*-p* option can be replaced with *--pdb_file* option.

*parse_pdb.py* outputs the positions of the zinc atom and its coordinating atoms found in the pdb file. Zinc in HDAC enzymes is always coordinated by one nitrogen atom of a histidine residue and two oxygen atoms of two aspartate residues.

Output exemple:
````
Atom: ND1 Residue: HIS Chain: A Residue Number: 180
Coordinates: 40.013, 9.259, 122.679

Atom: ZN Residue: ZN Chain: A Residue Number: 402
Coordinates: 38.798, 7.508, 121.912

Atom: OD2 Residue: ASP Chain: A Residue Number: 267
Coordinates: 39.849, 7.596, 120.012

Atom: OD2 Residue: ASP Chain: A Residue Number: 178
Coordinates: 39.588, 5.917, 123.179
````
\
**STEP 2**\
Once you have the coordinates, open the zinc_ideal.py script and insert the x, y, z coordinates in the appropriate section:
````
#################################################
#						#
#						#
#		INPUT START			#
#						#
#						#
#################################################

known_atoms = {
    "ZN": np.array([38.798, 7.508, 121.912]),
    "ND_HIS": np.array([40.013, 9.259, 122.679]),
    "OD_ASP_NEAR": np.array([39.849, 7.596, 120.012]),
    "OD_ASP_LONGER": np.array([39.588, 5.917, 123.179])
}

#################################################
#						#
#						#
#		INPUT END			#
#						#
#						#
#################################################
````
*Note*: You will need to measure the distances of the oxygen atoms from the zinc and enter the coordinates of the closest oxygen in OD_ASP_NEAR and the farthest oxygen in OD_ASP_LONGER.

Run the script:
````
$ python zinc_ideal.py
````
This will open a 3D view of the predicted positions. If everything went well, you should see a representation like in **Figure 1**. Don't worry if the terminal returns a Warning message.

<img src="/Figure1.png" width="602" height="500" alt="Figure1">

**Figure 1.** 3D representation of the zinc chelation network in the receptor (ZN, ND_HIS, OD_ASP_NEAR, OD_ASP_LONGER) and the predicted ideal interaction positions (O1_IDEAL, O2_IDEAL).

*python zinc_ideal.py* outputs the cooridnates of the predicted ideal positions:
````
x y z Vset r type
37.064 7.817 123.180 -2.00 1.20 acc
36.949 9.063 120.977 -2.00 1.20 acc
````
\
**STEP 3**\
At this point you can add the zinc coordinates to the *ligand_dock.bpf* file along with any other bias positions.
## Citations
If you found Zinc Package useful in your own research please cite:

[ARTICLE REFERENCE]