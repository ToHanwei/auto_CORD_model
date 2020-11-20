#!coding: utf-8

import os
import pandas as pd

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
        outsites = []
        #fragsite = []
        #siteflag = 'None'
        sites = open(sitefile).readlines()[1:]
        for site in sites:
            sis = site.split(',')
            resid = sis[1]
            sit = sis[2].replace('x', '.')
            if len(sit.split('.')[0]) == 2:
                sit = 'None'
            #if sit.split('.')[0] == siteflag:
            #    fragsite.append((resid, sit))
            #else:
            #    siteflag = sit.split('.')[0]
            #    outsites.append(fragsite)
            #    fragsite = []
            #    fragsite.append((resid, sit))
            outsites.append((resid, sit))
        return outsites

    def split_seq(self, sites, seq):
        """
        split pdb sequence
        """
        reslist = []
        resfrag = []
        siteflag = 'None'
        for i, resd in enumerate(seq):
            resid = resd[0]
            res = resd[1]
            siteid = sites[i][0]
            site = sites[i][1]
            fragname = site.split('.')[0]
            assert resid == siteid, print('res ID not match')
            if fragname == siteflag:
                resfrag.append((site, res))
            else:
                siteflag = fragname
                reslist.append(resfrag)
                resfrag = []
                resfrag.append((site, res))
        return reslist

    def query_seq(self, queryfile):
        """
        read query file
        """
        data = pd.read_csv(queryfile)
        for row in data.iterrows():
            CAnuming = row[1]['CAnumFrag'].split('#')
            fragment = row[1]['fragment']
            header = row[1]['header']
            


if __name__ == "__main__":
    test = Prepare()
    files = test.read_files()
    #pdb_seq = test.extract_seq_from_pdb('test.pdb')
    #pdb_site = test.read_site('test.csv')
    #test.split_seq(pdb_site, pdb_seq)
    #test.query_seq('99883.csv')
