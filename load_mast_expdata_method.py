# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 21:05:04 2023

@author: user
"""

import glob
import numpy as np 
import SOLPS_set as sps


d = sps.mast_comp_dic()
od = sps.Setting_dic()
# print(type(d))

def mast_base_dir():
    basedrt, topdrt, tpdrt= sps.set_wdir()
    gbase = '{}/{}/{}'.format(topdrt, od['DEV'], d['Shot'])
    gdir = glob.glob('{}/g{}*'.format(gbase, d['Shot']))
    
    shift_list = list(d['shift_dic'].keys())
    # print(type(shift_list))
    a_shift = d['a_shift']
    for aa in shift_list:
        if aa == a_shift:  
            filename = d['series_dic'][aa]
            shift = d['shift_file_dic'][aa]
            newbase = '{}/{}/{}/{}/{}'.format(basedrt, od['DEV'], 
                                            d['Shot'], shift, filename)
            tbase = '{}/{}/{}/{}'.format(basedrt, od['DEV'], d['Shot'], shift)
            adir = {}
            for i in d['Output']:
                adir[i] = '{}/{}'.format(newbase, i)
     
    attempt = str(sps.s_number(adir['Output'], series_flag= None)[0])
    shift_value = d['shift_dic'][a_shift]
    
    mast_basedir = {'basedrt': basedrt, 'topdrt': topdrt, 'gbase': gbase, 
                    'gdir': gdir, 'simudir': newbase, 'simutop': tbase, 
                    'outputdir': adir}

    return mast_basedir, attempt, shift_value

mwd = sps.mast_comp_dic_withshift()


def mast_withshift_dir():
    basedrt, topdrt, tpdrt= sps.set_wdir()
    gbase = '{}/{}/{}'.format(topdrt, od['DEV'], d['Shot'])
    gdir = glob.glob('{}/g{}*'.format(gbase, d['Shot']))
    shift_list = list(mwd['shift_dic'].keys())
    # print(type(shift_list))
    a_shift = mwd['multi_shift']
    simudir_dic = {}
    simutop_dic = {}
    outputdir_dic = {}
    att_dic = {}
    for aa in a_shift:
        for s in shift_list:
            if aa == s:
                i = shift_list.index(aa)
                filename = mwd['series'][i]
                newbase = '{}/{}/{}/{}/{}'.format(basedrt,od['DEV'], d['Shot'],
                                           mwd['shift_filelist'][i], filename)
                tbase = '{}/{}/{}/{}'.format(basedrt, od['DEV'], 
                                      d['Shot'], mwd['shift_filelist'][i])
                adir = {}
                for i in d['Output']:
                    adir[i] = '{}/{}'.format(newbase, i)
                 
                att_dic[aa] = str(sps.s_number(adir['Output'], series_flag= None)[0])
                
                simudir_dic[aa] = newbase
                simutop_dic[aa] = tbase
                outputdir_dic[aa] = adir
    
    mast_withshift_dir_dic = {'basedrt': basedrt, 'topdrt': topdrt, 
                              'gbase': gbase, 'gdir': gdir, 
                              'simudir': simudir_dic, 'simutop': simutop_dic, 
                              'outputdir': outputdir_dic}
    
    
    return mast_withshift_dir_dic, att_dic


mcds = sps.mast_comp_dir_series()

def mast_series_dir(series_flag):
    if series_flag == 'change_den':
        mcds = sps.mast_comp_dir_series()
    elif series_flag == 'eireneN':
        mcds = sps.mast_comp_dir_eireneN()
    else:
        print('please check series_flag')
       
    basedrt, topdrt, tpdrt= sps.set_wdir()
    gbase = '{}/{}/{}'.format(topdrt, od['DEV'], mcds['Shot'])
    gdir = glob.glob('{}/g{}*'.format(gbase, mcds['Shot']))
    newbase = glob.glob('{}/{}/{}/{}/*{}'.format(basedrt,od['DEV'], mcds['Shot'], 
                                       mcds['shift'], mcds['tail']))
    tbase = '{}/{}/{}/{}'.format(basedrt, od['DEV'], 
                                 mcds['Shot'], mcds['shift'])

    attempt_dic = {}
    new_dic = {}
    for i in newbase:
        if series_flag == 'change_den':
            attempt_dic[sps.s_number(i, series_flag)[0][0]] = sps.s_number(i, series_flag)[0][1]
            new_dic[sps.s_number(i, series_flag)[0][0]] = i
        elif series_flag == 'eireneN':
            attempt_dic[sps.s_number(i, series_flag)[0][1]] = sps.s_number(i, series_flag)[0][0]
            new_dic[sps.s_number(i, series_flag)[0][1]] = i
    # print(attempt_list)
    
    adir = {}
    for ii in attempt_dic.keys():
        adir[ii] = {}
        for j in mcds['Output']:
            adir[ii][j] = '{}/{}'.format(new_dic[ii], j)
    
    mast_basedir = {'basedrt': basedrt, 'topdrt': topdrt, 'gbase': gbase, 
                    'gdir': gdir, 'simudir': new_dic, 'simutop': tbase, 
                    'outputdir': adir}

    return mast_basedir, attempt_dic


def read_mastfile(mastfile_loc):
    with open(mastfile_loc, mode='r') as dfile:
        lines = dfile.readlines()
    
    profiles = {}
    nlines_tot = len(lines)
    psi_n = np.zeros(nlines_tot)
    ne = np.zeros(nlines_tot)
    ne_er = np.zeros(nlines_tot)
    te = np.zeros(nlines_tot)
    te_er = np.zeros(nlines_tot)
    
    i = 0
    
    while i < nlines_tot:
        r_line = lines[i].split()
        psi_n[i] = float(r_line[0])
        ne[i] = float(r_line[1])*pow(10, -20)
        ne_er[i] = float(r_line[2])*pow(10, -20)
        te[i] = float(r_line[3])/1000
        te_er[i] = float(r_line[4])/1000
        i += 1

    profiles['psi_normal'] = psi_n
    profiles['electron_density(10^20/m^3)'] = ne
    profiles['density error(10^20/m^3)'] = ne_er
    profiles['electron_temperature(KeV)'] = te
    profiles['temperature error(10^20/m^3)'] = te_er
    return profiles


def read_fitfile(mastfile_loc):
    with open(mastfile_loc, mode='r') as dfile:
        lines = dfile.readlines()
    
    profiles = {}
    nlines_tot = len(lines)
    psi_n = np.zeros(nlines_tot)
    ne = np.zeros(nlines_tot)
    te = np.zeros(nlines_tot)
    i = 0
    
    while i < nlines_tot:
        r_line = lines[i].split()
        psi_n[i] = float(r_line[0])
        ne[i] = float(r_line[1])*pow(10, 20)
        te[i] = float(r_line[2])*1000
        i += 1

    profiles['psi_normal'] = psi_n
    profiles['electron_density(m^(-3))'] = ne
    profiles['electron_temperature(eV)'] = te
    return profiles