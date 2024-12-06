import argparse

def parse_pdb(file_path):
    atoms = {}
    links = []
    found_link = False
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                atom_number = int(line[6:11].strip())
                atom_type = line[12:16].strip()
                residue_name = line[17:20].strip()
                chain_id = line[21].strip()
                residue_number = int(line[22:26].strip())
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                atoms[(atom_type, residue_name, chain_id, residue_number)] = (x, y, z)
            elif line.startswith("LINK"):
                found_link = True
                atom1_type = line[12:16].strip()
                res1_name = line[17:20].strip()
                chain1_id = line[21].strip()
                res1_number = int(line[22:26].strip())
                atom2_type = line[42:46].strip()
                res2_name = line[47:50].strip()
                chain2_id = line[51].strip()
                res2_number = int(line[52:56].strip())
                links.append(((atom1_type, res1_name, chain1_id, res1_number), 
                              (atom2_type, res2_name, chain2_id, res2_number)))
    
    if not found_link:
        print("\nBad input!\n\nYour pdb file does not express the coordination bonds between the amino acids and the zinc ion.")
        
    return atoms, links
    
def extract_coordinates(atoms, links):
    coordinates = {}
    for (atom1, atom2) in links:
        if atom1 in atoms:
            coordinates[atom1] = atoms[atom1]
        if atom2 in atoms:
            coordinates[atom2] = atoms[atom2]
    return coordinates
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pdb_file", help="Path to the PDB file", required=True)
    args = parser.parse_args()
    pdb_file_path = args.pdb_file
    atoms, links = parse_pdb(pdb_file_path)
    coordinates = extract_coordinates(atoms, links)
    for atom_info, (x, y, z) in coordinates.items():
        atom_type, res_name, chain_id, res_number = atom_info
        print(f"Atom: {atom_type} Residue: {res_name} Chain: {chain_id} Residue Number: {res_number}")
        print(f"Coordinates: {x}, {y}, {z}\n")
if __name__ == "__main__":
    main()
