#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 22:25:05 2016

@author: huster-wgm
"""

import numpy as np


# refer to https://en.wikipedia.org/wiki/DNA_codon_table
aa_code_dict = {
                'A': ['GCT', 'GCC', 'GCA', 'GCG'],
                'R': ['CGT', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'],
                'N': ['AAT', 'AAC'],
                'D': ['GAT', 'GAC'],
                'C': ['TGT', 'TGC'],
                'Q': ['CAA', 'CAG'],
                'E': ['GAA', 'GAG'],
                'G': ['GGT', 'GGC', 'GGA', 'GGG'],
                'H': ['CAT', 'CAC'],
                'I': ['ATT', 'ATC', 'ATA'],
                'M': ['ATG'],
                'L': ['TTA', 'TTG', 'CTT', 'CTC', 'CTA', 'CTG'],
                'K': ['AAA', 'AAG'],
                'F': ['TTT', 'TTC'],
                'P': [  'CCT', 'CCC', 'CCA', 'CCG'],
                'S': ['TCT', 'TCC', 'TCA', 'TCG', 'AGT', 'AGC'],
                'T': ['ACT', 'ACC', 'ACA', 'ACG'],
                'W': ['TGG'],
                'Y': ['TAT', 'TAC'],
                'V': ['GTT', 'GTC', 'GTA', 'GTG'],
                '*': ['TAA', 'TGA', 'TAG'],  # represents stop codon
                }


def key_by_value(dicts, search_value):
    for key, values in dicts.items():
        if search_value in values:
            return key


def DNA_to_AA(seq):
    aa_seq = []
    coding_len = len(seq) // 3
    for i in range(0, coding_len):
        DNA_code = seq[i*3:i*3+3]
        DNA_code = ''.join(DNA_code)
        # match DNA_code to Amino acid
        aa = key_by_value(aa_code_dict, DNA_code)
        aa_seq.append(aa)
    return np.array(aa_seq)


def DNA_MW(seq, dna_len):
    # calulate molecular weight of DNA sequence
    # Molecular Weight = (An x 313.21) + (Tn x 304.2) + (Cn x 289.18) + \
    #                    (Gn x 329.21) - 61.96 + 79.0
    # refer to http://biotools.nubic.northwestern.edu/OligoCalc.html
    GC_num = sum(seq == 'G')+sum(seq == 'C')
    AT_num = sum(seq == 'A')+sum(seq == 'T')
    assert GC_num + AT_num == dna_len, 'Sequence mix with none DNA code'
    gc_rate = round(GC_num / dna_len*100, 1)
    dna_mw = round(GC_num*(313.21+304.2)+AT_num*(289.18+329.21)+17.04*2, 1)
    return dna_mw, gc_rate


def Protein_MW(seq, aa_components):
    # Make a dictionary for AA acid residue weight
    # refer to http://www.its.caltech.edu/~ppmal/sample_prep/work3.html
    aa_weigt_dict = {
                     'G': 57.052,
                     'A': 71.079,
                     'S': 87.078,
                     'P': 97.117,
                     'V': 99.133,
                     'T': 101.105,
                     'C': 103.144,
                     'I': 113.16,
                     'L': 113.16,
                     'N': 114.104,
                     'D': 115.089,
                     'Q': 128.131,
                     'K': 128.174,
                     'E': 129.116,
                     'M': 131.198,
                     'H': 137.142,
                     'F': 147.177,
                     'R': 156.188,
                     'Y': 163.17,
                     'W': 186.213,
                     '*': 0,  # represent stop codon
                     }
    aa_mw = 0
    # calculate molecular weight of Protein sequence
    for i in aa_weigt_dict.keys():
        aa_num = aa_components[i]
        aa_mw += aa_num*aa_weigt_dict[i]
    # add one H2O
    aa_mw += 18.0
    return round(aa_mw, 2)


def Protein_components(seq):
    # initial amino acid component to zeros
    aa_component = {
                 'G': 0,
                 'A': 0,
                 'S': 0,
                 'P': 0,
                 'V': 0,
                 'T': 0,
                 'C': 0,
                 'I': 0,
                 'L': 0,
                 'N': 0,
                 'D': 0,
                 'Q': 0,
                 'K': 0,
                 'E': 0,
                 'M': 0,
                 'H': 0,
                 'F': 0,
                 'R': 0,
                 'Y': 0,
                 'W': 0,
                 '*': 0,  # represent for stop
                 }
    for i in seq:
        aa_component[i] += 1
    # ε = (nW×5500) + (nY×1490) + (nC×125)
    # refer to https://tools.thermofisher.com/content/sfs/brochures/ \
    # TR0006-Extinction-coefficients.pdf
    abs_coeff = (aa_component['W']*5500 +
                 aa_component['Y']*1490 +
                 aa_component['C']*125)
    return aa_component, abs_coeff


class Bio_calculator():
    # initialize
    def __init__(self, seq, seq_type):
        # remove empty spaces
        seq = seq.replace(' ', '')
        # remove change line mark
        seq = seq.replace('\n', '')
        # remove comma
        seq = seq.replace('\r', '')
        seq = list(seq)
        # assign valuabe to self
        self.seq_type = seq_type
        self.seq = np.array(seq)
        assert self.seq_type in ['DNA', 'Protein'], "Wrong sequence type"

    def DNA_calculator(self):
        seq_type = self.seq_type
        if seq_type == 'DNA':
            # DNA sequence
            dna_len = len(self.seq)
            aa_seq = DNA_to_AA(self.seq)
            dna_mw, gc_rate = DNA_MW(self.seq, dna_len)
            # assign parameters to self object
            self.dna_seq = ''.join(self.seq)
            self.dna_len = dna_len
            self.dna_mw = dna_mw
            self.gc_rate = gc_rate
            self.aa_seq = ''.join(aa_seq)
            # repalce the seq with amino sequence
            self.seq = aa_seq
        else:
            self.dna_seq = None
            self.dna_mw = None
            self.gc_rate = None
            # calculate DNA length
            dna_len = len(self.seq)*3
            self.dna_len = dna_len
            self.aa_seq = ''.join(self.seq)
            # amino acid seqence
            aa_len = len(self.seq)
            self.aa_len = aa_len
        return 0

    def Protein_calculator(self):
        # get protein molecular weight
        aa_components, abs_coeff = Protein_components(self.seq)
        aa_mw = Protein_MW(self.seq, aa_components)
        self.aa_len = len(self.seq)-aa_components['*']
        self.aa_mw = aa_mw
        self.aa_components = aa_components
        self.abs_coeff = abs_coeff
        self.nb_stop = aa_components['*']
        return 0

    def Protein_con(self, width, a_280, dilution):
        # refer to https://tools.thermofisher.com/content/sfs/brochures/ \
        # TR0006-Extinction-coefficients.pdf
        # c = A / ε L ( = A / ε when L = 1 cm)
        # unit of molar concentration is 'μM/L'
        molar_con = round(a_280 / (self.abs_coeff * width) * dilution*10**6, 2)
        # protein concentration (unit is 'mg/mL')
        pro_con = round(molar_con * self.aa_mw/(10**6), 2)
        self.pro_con = pro_con
        self.molar_con = molar_con
        self.measure = True
        self.dilution = dilution
        return 0


if __name__ == '__main__':
    # test with GAPDH sequence
    seq_test = ('ATGACTATCAAAGTAGGTATCAACGGTTTTGGCCGTATCGGTCGCATTGTTTTCCGTGCTGCTCAGAAACGTTCT\
                GACATCGAGATCGTTGCAATCAACGACCTGTTAGACGCTGATTACATGGCATACATGCTGAAATATGACTCCACT\
                CACGGCCGTTTCGACGGTACCGTTGAAGTGAAAGACGGTCATCTGATCGTTAACGGTAAAAAAATCCGTGTTACC\
                GCTGAACGTGATCCGGCTAACCTGAAATGGGACGAAGTTGGTGTTGACGTTGTCGCTGAAGCAACTGGTCTGTTC\
                CTGACTGACGAAACTGCTCGTAAACACATCACCGCTGGTGCGAAGAAAGTGGTTATGACTGGTCCGTCTAAAGAC\
                AACACTCCGATGTTCGTTAAAGGCGCTAACTTCGACAAATATGCTGGCCAGGACATCGTTTCCAACGCTTCCTGC\
                ACCACCAACTGCCTGGCTCCGCTGGCTAAAGTTATCAACGATAACTTCGGCATCATCGAAGGTCTGATGACCACC\
                GTTCACGCTACTACCGCTACTCAGAAAACCGTTGATGGCCCGTCTCACAAAGACTGGCGCGGCGGCCGCGGCGCT\
                TCCCAGAACATCATCCCGTCCTCTACCGGTGCTGCTAAAGCTGTAGGTAAAGTACTGCCAGAACTGAATGGCAAA\
                CTGACTGGTATGGCGTTCCGCGTTCCGACCCCGAACGTATCTGTAGTTGACCTGACCGTTCGTCTGGAAAAAGCT\
                GCAACTTACGAGCAGATCAAAGCTGCCGTTAAAGCTGCTGCTGAAGGCGAAATGAAAGGCGTTCTGGGCTACACC\
                GAAGATGACGTAGTATCTACCGATTTCAACGGCGAAGTTTGCACTTCCGTGTTCGATGCTAAAGCTGGTATCGCT\
                CTGAACGACAACTTCGTGAAACTGGTATCCTGGTACGACAACGAAACCGGTTACTCCAACAAAGTTCTGGACCTG\
                ATCGCTCACATCTCCAAATAA')
    seq_type_test = 'DNA'
    test = Bio_calculator(seq_test, seq_type_test)
    print('Perform DNA calculation')
    test.DNA_calculator()
    print('DNA SEQ:', test.dna_seq, '\n',
          'DNA_LEN:', test.dna_len, ' bp', '\n',
          'DNA_MW:', test.dna_mw, ' g/mol', '\n',
          'DNA_gc_rate:', test.gc_rate, '%', '\n',
          'Amino_acid SEQ:', test.aa_seq, '\n',
          )

    print('Perform Protein calculation')
    test.Protein_calculator()
    print('Amino_acid LEN:', test.aa_len, '\n'
          'Protein_MW:', test.aa_mw, ' g/mol', '\n',
          'Protein components:', test.aa_components, '\n',
          'Protein absorbance coeff:', test.abs_coeff, '\n')



