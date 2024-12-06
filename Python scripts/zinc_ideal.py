import numpy as np
import math
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

distances = {
    "ND_HIS": 2.11,
    "OD_ASP_NEAR": 2.06,
    "OD_ASP_LONGER": 2.18,
    "O1_IDEAL": 2.17,
    "O2_IDEAL": 2.59
}
angles = {
    ("ND_HIS", "OD_ASP_NEAR"): 107.98,
    ("ND_HIS", "O1_IDEAL"): 97.23,
    ("ND_HIS", "O2_IDEAL"): 94.59,
    ("ND_HIS", "OD_ASP_LONGER"): 102.43,
    ("OD_ASP_NEAR", "O1_IDEAL"): 152.04,
    ("OD_ASP_NEAR", "O2_IDEAL"): 97.57,
    ("OD_ASP_NEAR", "OD_ASP_LONGER"): 89.86,
    ("O1_IDEAL", "O2_IDEAL"): 67.89,
    ("O1_IDEAL", "OD_ASP_LONGER"): 96.47,
    ("O2_IDEAL", "OD_ASP_LONGER"): 158.36
}
def deg_to_rad(degrees):
    return degrees * np.pi / 180

angles_rad = {k: deg_to_rad(v) for k, v in angles.items()}
def deduce_missing_atoms(known_atoms, distances, angles_rad):
    Zn = known_atoms["ZN"]
    guesses = []
    missing_keys = []
    for atom, dist in distances.items():
        if atom not in known_atoms:
            guess = Zn + np.array([dist, 0, 0])
            guesses.append(guess)
            missing_keys.append(atom)
    def objective_function(positions):
        pos = {k: np.array(v) for k, v in zip(missing_keys, positions.reshape(-1, 3))}
        pos.update(known_atoms)
        obj_val = 0

        for atom, dist in distances.items():
            if atom in pos:
                obj_val += (np.linalg.norm(pos[atom] - Zn) - dist) ** 2

        for (atom1, atom2), angle in angles_rad.items():
            if atom1 in pos and atom2 in pos:
                vec1 = pos[atom1] - Zn
                vec2 = pos[atom2] - Zn
                cosine_angle = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
                obj_val += (np.arccos(cosine_angle) - angle) ** 2

        return obj_val
    initial_guesses = np.array(guesses).flatten()
    result = minimize(objective_function, initial_guesses, method='BFGS')
    optimized_positions = result.x.reshape(-1, 3)
    missing_atoms_positions = {atom: pos for atom, pos in zip(missing_keys, optimized_positions)}
    return missing_atoms_positions

#################################################
#						#
#						#
#		INPUT START			#
#						#
#						#
#################################################

known_atoms = {
    "ZN": np.array([19.238, -18.038, -2.791]),
    "ND_HIS": np.array([20.962, -17.521, -3.779]),
    "OD_ASP_NEAR": np.array([18.523, -16.336, -2.454]),
    "OD_ASP_LONGER": np.array([18.223, -18.903, -4.212])
}

#################################################
#						#
#						#
#		INPUT END			#
#						#
#						#
#################################################

missing_atoms = deduce_missing_atoms(known_atoms, distances, angles_rad)
print("   ")
print("   ")
print(f"x y z Vset r type")
for atom, coords in missing_atoms.items():
    print(f"{coords[0]:.3f} {coords[1]:.3f} {coords[2]:.3f} -2.00 1.20 acc")
print("   ")
print("   ")
print("   ")
print("   ")
print("   ")
print("   ")
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for atom, coord in known_atoms.items():
    ax.scatter(*coord, label=atom)
for atom, coord in missing_atoms.items():
    ax.scatter(*coord, label=atom)
Zn = known_atoms["ZN"]
for atom, coord in known_atoms.items():
    if atom != "ZN":
        ax.plot([Zn[0], coord[0]], [Zn[1], coord[1]], [Zn[2], coord[2]], 'k--')
for atom, coord in missing_atoms.items():
    ax.plot([Zn[0], coord[0]], [Zn[1], coord[1]], [Zn[2], coord[2]], 'k--')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
plt.show()

