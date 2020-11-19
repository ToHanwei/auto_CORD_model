#!coding: utf-8

import os

class Prepare():
    """
    Prepare file class
    """

    def __init__(self):
        self.condn = {
            "GLY": "G", "ALA": "A", "VAL": "V",
            "LEU": "L", "ILE": "I", "PRO": "P",
            "PHE": "F", "TYR": "Y", "TRP": "W",
            "SER": "S", "THR": "T", "CYS": "C",
            "MET": "M", "ASN": "N", "GLN": "Q",
            "ASP": "D", "GLU": "E", "LYS": "K",
            "ARG": "R", "HIS": "H"
        }

    def seqio(self, seqfile):
        """
        read fasta format file
        """
        outdict = {}
        with open(seqfile) as seqf:
            seqs = seqf.read().split('>')[1:]
        for seq in seqs:
            lines = seq.split('\n')
            header = lines[0]
            aads = ''.join(lines[1:])
            outdict[header] = aads
        return outdict

    def read_files(indir):
        """
        get files in folder
        """
        files = os.listdir(indir)
        files = [os.path.join(indir, _) for _ in files]
        return files

    def extract_seq_from_pdb(self, pdb):
        """
        extract sequence from pdb format
        """
        sourid = '-1'
        res = []
        atoms = [line for line in open(pdb) if line[:6]=="ATOM  "]
        for atom in atoms:
            resid = atom[22:26].strip()
            if sourid != resid:
                resname = atom[17:20]
                resname = self.condn[resname]
                res.append((resid, resname))
                sourid = resid
        return res

    def read_site(self, sitefile):
        """
        read site file
        """
        sites = open(sitefile).readlines()[1:]
        sites = [s.split(',')[1:3] for s in sites]
        print(sites)


if __name__ == "__main__":
    test = Prepare()
    #test.extract_seq_from_pdb('test.pdb')
    test.read_site('test.csv')
