# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 12:30:15 2014

@author: teo
"""
import os, re
from warnings import warn


# JCAMP-DX functions

def read_jcamp(filename):
    """
    Read a Bruker JCAMP-DX file into a dictionary.

    Creates two special dictionary keys _coreheader and _comments Bruker
    parameter "$FOO" are extracted into strings, floats or lists and assigned
    to dic["FOO"]

    Parameters
    ----------
    filename : str
        Filename of Bruker JCAMP-DX file.

    Returns
    -------
    dic : dict
        Dictionary of parameters in file.

    See Also
    --------
    write_jcamp : Write a Bruker JCAMP-DX file.

    Notes
    -----
    This is not a fully functional JCAMP-DX reader, it is only intended
    to read Bruker acqus (and similar) files.

    """
    dic = {"_coreheader": [], "_comments": []}  # create empty dictionary
    f = open(filename, 'rb')

    # loop until EOF
    while len(f.read(1)):

        f.seek(-1, os.SEEK_CUR)  # rewind 1 byte
        line = f.readline().rstrip()    # read a line

        if line[:6] == "##END=":
            #print "End of file"
            break
        elif line[:2] == "$$":
            dic["_comments"].append(line)
        elif line[:2] == "##" and line[2] != "$":
            dic["_coreheader"].append(line)
        elif line[:3] == "##$":
            try:
                key, value = parse_jcamp_line(line, f)
                dic[key] = value
            except:
                warn("Unable to correctly parse line:" + line)
        else:
            warn("Extraneous line:" + line)

    return dic



def parse_jcamp_line(line, f):
    """
    Parse a single JCAMP-DX line

    Extract the Bruker parameter name and value from a line from a JCAMP-DX
    file.  This may entail reading additional lines from the fileobj f if the
    parameter value extends over multiple lines.

    """

    # extract key= text from line
    key = line[3:line.index("=")]
    text = line[line.index("=") + 1:].lstrip()

    if "<" in text:   # string
        while ">" not in text:      # grab additional text until ">" in string
            text = text + "\n" + f.readline().rstrip()
        value = text[1:-1]  # remove < and >

    elif "(" in text:   # array
        num = int(line[line.index("..") + 2:line.index(")")]) + 1
        value = []
        rline = line[line.index(")") + 1:]

        # extract value from remainer of line
        for t in rline.split():
            value.append(parse_jcamp_value(t))

        # parse additional lines as necessary
        while len(value) < num:
            nline = f.readline().rstrip()
            for t in nline.split():
                value.append(parse_jcamp_value(t))

    elif text == "yes":
        value = True

    elif text == "no":
        value = False

    else:   # simple value
        value = parse_jcamp_value(text)

    return key, value


def parse_jcamp_value(text):
    """
    Parse value text from Bruker JCAMP-DX file returning the value.
    """
    if "<" in text:
        return text[1:-1]  # remove < and >
    elif "." in text or "e" in text or 'inf' in text:
        return float(text)
    else:
        return int(text)

file_visu_pars = open('/Users/teo/Dropbox/KU Leuven/SL_CS_test7.mW1/1/pdata/1/visu_pars', 'r')
aa = file_visu_pars.readlines()
filename = '/Users/teo/Dropbox/KU Leuven/SL_CS_test7.mW1/1/pdata/1/visu_pars'
bb = read_jcamp_teo(filename)