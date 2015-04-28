# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 18:48:07 2014

@author: Matteo Caffini

Functions for reading Bruker files (2dseq, method, acqp, visu_pars, ...)
"""

import re, os
import numpy as np
from datetime import datetime

def read_2dseq(filename):
    spam = filename.split(os.path.sep)[:-1]
    eggs = os.path.sep.join(spam)
    #filename = '/Users/teo/Desktop/ForMatteo/FVL_25117_NC_2m_a.lf1/1/pdata/1/2dseq'
    #filename = '/Users/teo/Dropbox/KU Leuven/SL_CS_test7.mW1/1/pdata/1/2dseq'
    #file_visu_pars = '/Users/teo/Desktop/ForMatteo/FVL_25117_NC_2m_a.lf1/1/pdata/1/visu_pars'
    file_visu_pars = eggs+'/visu_pars'    
    
    visu_pars = read_parameters(file_visu_pars)
    img_type = visu_pars['VisuCoreWordType']
    img_dims = visu_pars['VisuCoreSize']
    img_frames = visu_pars['VisuCoreFrameCount']
    img_endianness = visu_pars['VisuCoreByteOrder']

    slope = visu_pars['VisuCoreDataSlope']
    offset = visu_pars['VisuCoreDataOffs']
    
    # check endianness and precision
    if img_type == '_32BIT_SGN_INT' and img_endianness == 'littleEndian':
        data_precision = np.dtype('<i4')
    elif img_type == '_32BIT_SGN_INT' and img_endianness == 'bigEndian':
        data_precision = np.dtype('>i4')
    elif img_type == '_16BIT_SGN_INT' and img_endianness == 'littleEndian':
        data_precision = np.dtype('<i2')
    elif img_type == '_16BIT_SGN_INT' and img_endianness == 'bigEndian':
        data_precision = np.dtype('>i2')
    else:
        pass

    file_ID = open(filename, 'r')
    img_data = np.frombuffer(file_ID.read(),dtype=data_precision)
    file_ID.close()

    img = np.reshape(img_data,np.append(img_dims,img_frames),order='F') # reshape in Fortran-like mode (as in Matlab)
    
    # slope and offset correction
#    if img_frames == 1:
#        img = img*slope + offset
#    else:
#        for ii in range(img_frames):
#            img[:,:,ii] = 
#
    return img


def read_parameters(filename):
    """
    Read a Bruker JCAMP-DX file into a dictionary.

    Parameters
    ----------
    filename : str
        Absolute path of Bruker parameters file (JCAMP-DX).

    Returns
    -------
    parameters : dict
        Dictionary of parameters in file.

    See Also
    --------
    Nothing for now

    Notes
    -----
    This function has been written by Matteo Caffini in Paul Delvauxwijk, Leuven

    """    
    #filename = '/Users/teo/Dropbox/KU Leuven/SL_CS_test7.mW1/1/pdata/1/visu_pars'    
    file_ID = open(filename, 'r')
    C = file_ID.read()
    file_ID.close()
        
    C = re.sub('\$\$([^\n]*)\n','',C)
    C = re.split('\s*##',C)
    C.remove('')

    parameters = {'_extra':[]}
    orig = {'_extra':[]}
        
    for ii in range(len(C)):
        parameter_line = C[ii]
        splitter = re.search('=',parameter_line)
        
        # process parameter name
        name = parameter_line[:splitter.start()]
        if '$' in name:
            name = name.replace('$','')
        else:
            pass
        
        # process parameter value
        value = parameter_line[splitter.end():]
        orig[name] = value
        
        if '\n' not in value:
            try:
                value = float(value)
                if round(value) == value:
                    value = int(value)
                else:
                    pass
            except:
                try:
                    value = int(value)
                except:
                    pass
        else:
            splitter = re.search('\n',value)
            first_part = value[:splitter.start()]
            second_part = value[splitter.end():]
            
            first_part = first_part.replace(' ','')
            first_part = first_part.replace('(','')
            first_part = first_part.replace(')','')
            
            try:
                value_size = [int(i) for i in first_part.split(',')]
                value_size = tuple(value_size)
            except:
                pass
            
            second_part = second_part.split()
    
            if len(second_part) == 0:
                second_part = ''
            elif len(second_part) == 1:
                second_part = second_part[0]
                try:
                    second_part = float(second_part)
                    if round(second_part) == second_part:
                        value = int(second_part)
                except:
                    try:
                        value = int(second_part)
                    except:
                        pass
            else:
                second_part = [second_part[i].replace('<','') for i in range(len(second_part))]
                second_part = [second_part[i].replace('>','') for i in range(len(second_part))]
                if ':' in second_part[0]:
                    datestring = ' '.join(second_part)
                    second_part = datetime.strptime(datestring,'%H:%M:%S %d %b %Y')
                else:
                    pass
                try:
                    second_part = np.array(second_part,dtype=float)
                    second_part = np.reshape(second_part,value_size)
                except:
                    pass
            try:        
                second_part = second_part.replace('<','')
                second_part = second_part.replace('>','')
            except:
                pass
            
            value = second_part
        
        parameters[name] = value
    
    del parameters['_extra']
    
    return parameters