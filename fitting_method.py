# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 13:28:56 2023

@author: user
"""

import numpy as np
from scipy.optimize import curve_fit
import load_mast_expdata_method as lmem
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from statistics import stdev

def tanh(r,r0,h,d,b,m):
    return b+(h/2)*(np.tanh((r0-r)/d)+1) + m*(r0-r-d)*np.heaviside(r0-r-d, 1)

def expfit(x,A,l):  #Removed vertical displacement variable B; seemed to cause 'overfitting'
    return A*np.exp(l*x)


def tanh_fit(x_choice, x_coord, ne, te):
    # mast_dat_dict = lmem.read_mastfile(mastloc)
    # psi = mast_dat_dict['psi_normal']
    # ne = mast_dat_dict['electron_density(10^20/m^3)']
    # te = mast_dat_dict['electron_temperature(KeV)']
    
    Ne = ne*pow(10, -19)
    Te = te*pow(10, -3)
    
    if x_choice == 'psiN':
        p0 = [1, 0.4, 0.009, 0.05, 0.5]
        p1 = [1, 0.3, 0.1, 0.001, 0.5]
        popt_ne, pcov_ne = curve_fit(tanh, x_coord, Ne, p0)
        # print(popt_ne)
        popt_te, pcov_te = curve_fit(tanh, x_coord, Te, p1)
        # print(popt_te) 
        tanh_ne_fit = tanh(x_coord, popt_ne[0], popt_ne[1], 
                               popt_ne[2], popt_ne[3], popt_ne[4])*pow(10, 19)
        tanh_te_fit = tanh(x_coord, popt_te[0], popt_te[1], 
                               popt_te[2], popt_te[3], popt_te[4])*pow(10, 3)
    
    
    # elif x_choice == 'RRsep':
    #     p0 = [0.4, 0.005, 0.05, 0.5]
    #     p1 = [2.2, 0.005, 0.05, 3.5]
    #     popt_ne, pcov_ne = curve_fit(tanh_dsa, x_coord, Ne, p0)
    #     print(popt_ne)
    #     popt_te, pcov_te = curve_fit(tanh_dsa, x_coord, Te, p1)
    #     # print(popt_te) 
    #     tanh_ne_fit = tanh_dsa(x_coord, popt_ne[0], popt_ne[1], 
    #                            popt_ne[2], popt_ne[3])*max(ne)
    #     tanh_te_fit = tanh_dsa(x_coord, popt_te[0], popt_te[1], 
    #                            popt_te[2], popt_te[3])*max(te)
    
    
    
    fit_tanh_dic = {'tanh_ne_fit': tanh_ne_fit, 'tanh_te_fit': tanh_te_fit, 
               'popt_ne': popt_ne, 'popt_te': popt_te}
       
    return fit_tanh_dic


def exp_fit(x_choice, x_coord, neuden):
    
    
    NeuDen = neuden/ neuden[0]
    
    if x_choice == 'psiN':
        # pn = [1, 1.015, 200.5]
        pn = [1.015, 200.5]
        x_sh = x_coord - x_coord[0]
        popt_an, pcov_an = curve_fit(expfit, x_sh, NeuDen, pn)
        # print(popt_an)
        
        exp_an_fit = expfit(x_sh, popt_an[0], popt_an[1])*neuden[0]
        
        # plt.figure(figsize=(7,7))
        # plt.yscale('log')
        # plt.plot(x_coord, neuden,'o-', color = 'green', label= 'solps neutral density')
        # plt.plot(x_coord, exp_an_fit, color='r',lw= 5, label= 'exponential fit')
        # plt.xlabel('psiN')
        # plt.ylabel('Neutral Atom (D) Density $(m^{-3})$')
        # plt.title('Neutral density with fits')
        # plt.legend()
        
    elif x_choice == 'RRsep':
        pn = [1.015, 200.5]
        popt_an, pcov_an = curve_fit(expfit, x_coord, NeuDen, pn)
        print(popt_an)
        
        exp_an_fit = expfit(x_coord, popt_an[0], popt_an[1])*max(neuden)
        
    
    fit_exp_dic = {'exp_an_fit': exp_an_fit, 'popt_an': popt_an}
    
    return fit_exp_dic



def linear_fit(x_choice, x_coord, neuden):
    
    NeuDen = np.log(neuden)
    x_sh = x_coord - x_coord[0]
    # new_neuden = np.log(neuden / neuden[0])
    # print(x_sh)
    # print(new_neuden)
    
    if x_choice == 'psiN':
        # pn = [1, 1.015, 200.5]
        pn = [20]
        # popt_an, pcov_an = curve_fit(linefit, x_sh, new_neuden, pn)
        # print(popt_an)
        
        # exp_line_fit = np.exp(linefit(x_sh, popt_an[0]))*neuden[0]
        # print(popt_an[0])
        
        ln_exp_fitcoe = np.polyfit(x_sh, NeuDen, 1 , cov=True)
        # print(ln_exp_fitcoe[0])
        ln_exp_fitpoly = np.poly1d(ln_exp_fitcoe[0])
        
        # print(ln_exp_fitpoly)
        exp_ln_fit = np.exp(ln_exp_fitpoly(x_sh))
        
        # plt.figure(figsize=(7,7))
        # plt.yscale('log')
        # plt.plot(x_coord, neuden,'o-', color = 'green', label= 'solps neutral density')
        # plt.plot(x_coord, exp_line_fit, color='r',lw= 5, label= 'exponential fit')
        # plt.xlabel('psiN')
        # plt.ylabel('Neutral Atom (D) Density $(m^{-3})$')
        # plt.title('Neutral density with fits')
        # plt.legend()
        
    fit_exp_dic = {'exp_line_fit': exp_ln_fit, 'popt_an': ln_exp_fitcoe[0]}
    
    return fit_exp_dic 



"fit dsa with psi"
def dsa_psi_fit(dsa, psi):
    dsa_psi_fitcoe = np.polyfit(psi, dsa, 1 , cov=True)
    # print(dsa_psi_fitcoe[1])
    dsa_psi_fitpoly = np.poly1d(dsa_psi_fitcoe[0])
    
    
    psi_dsa_fit = dsa_psi_fitpoly(psi)
   
    fit_dp_dic = {'dsa_psi_fit': psi_dsa_fit, 'dsa_psi_fitcoe': dsa_psi_fitcoe[0]}
    
    # plt.figure(figsize=(7,7))
    # plt.plot(psi, dsa,'o-', color = 'green', label= 'psi_dsa')
    # plt.plot(psi, psi_dsa_fit, color='r',lw= 5, label= 'psi_dsa_fit')
    # plt.xlabel('psiN')
    # plt.ylabel('R-Rsep')
    # plt.title('psi_dsa_fit')
    # plt.legend()
    
    # print(dsa_psi_fitcoe[0])

    return fit_dp_dic


def flux_expand_fit(RRsep, arclength):
    flux_fitcoe = np.polyfit(RRsep, arclength, 1 , cov=True)
    # print(dsa_psi_fitcoe[1])
    flux_fitpoly = np.poly1d(flux_fitcoe[0])
          
    flux_fit = flux_fitpoly(RRsep)     
    flux_fit_dic = {'flux_fit': flux_fit, 'flux_fitcoe': flux_fitcoe[0]}
    
    # plt.figure(figsize=(7,7))
    # plt.plot(RRsep, arclength,'o-', color = 'green', label= 'psi_dsa')
    # plt.xlabel('R-Rsep')
    # plt.ylabel('arclength')
    # plt.title('flux_expansion_fit')
    # plt.legend()
    
    # print(flux_fitcoe[0])
        
    return flux_fit_dic




def Opacity_calculator(x_choice, x_coord, ne, te, neuden):
    if x_choice == 'psiN':
        fit_tanh_dic = tanh_fit(x_choice, x_coord, ne, te)
        tanh_ne_fit = fit_tanh_dic['tanh_ne_fit']
        dn = round(fit_tanh_dic['popt_ne'][2], 2)
        tanh_te_fit = fit_tanh_dic['tanh_te_fit']
        dtn = round(fit_tanh_dic['popt_te'][2], 2)   
        ne_ped = (fit_tanh_dic['popt_ne'][1] + fit_tanh_dic['popt_ne'][3])*pow(10, 19)
        sym_pt_te = fit_tanh_dic['popt_te'][0]
        sym_pt_ne = fit_tanh_dic['popt_ne'][0]
        # print(sym_pt_te + dn)
        
        "fitting choice 1: in the width, symmetry point +- width/2"
        xcoord_exp = []
        an_cut = []
        index_cut = []
        sym_pt = fit_tanh_dic['popt_ne'][0]
        x_coord_rev = list(reversed(x_coord))
        # print(type(x_coord_rev))
        neuden_rev = list(reversed(neuden))
        # print(type(x_coord_rev))
        for j in range(len(x_coord_rev)):
            if x_coord_rev[j] <= sym_pt_ne + dn and x_coord_rev[j] >= sym_pt_ne - dn:
                xcoord_exp.append(x_coord_rev[j])
                an_cut.append(neuden_rev[j])
                index_cut.append(j)
        
        # print(sym_pt, dn)
        # print(xcoord_exp)
        
        "plot to check the tanh fit result"
        # plt.figure(figsize=(7,7))
        # plt.plot(x_coord, ne,'o-', color = 'b', label= 'solps electron density')
        # plt.plot(x_coord, tanh_ne_fit, color='r',lw= 3, label= 'tanh fit')
        # plt.xlabel('Radial coordinate: $R- R_{sep}$')
        # plt.ylabel('Electron Density $n_e\;(m^{-3})$')
        # plt.title('Electron density with fits')
        # plt.legend()
        
        "print to check the exp fit result"
        # print(dn)
        # print(sym_pt)
        # print(xcoord_exp)
        # print(an_cut)
        
        xcoord_exp = np.asarray(xcoord_exp)
        an_cut = np.asarray(an_cut)
        
        fit_exp_dic = linear_fit(x_choice, xcoord_exp, an_cut)

        
        exp_an_fit = fit_exp_dic['exp_line_fit']
        efold = 1/fit_exp_dic['popt_an'][0]
        n_sep_fit = np.exp(fit_exp_dic['popt_an'][1])
        
        opq = 2*dn/efold
        
        
        result_dic = {'tanh_ne_fit': tanh_ne_fit, 'exp_fit': exp_an_fit,
                      'electron_pedestal_density': ne_ped, 'x_coord_cut': xcoord_exp,
                      'tanh_te_fit': tanh_te_fit, 'pedestal_width': dn, 
                      'temperature_pedestal_width': dtn,
                      'efold_length': efold, 'dimensionless_opaqueness': opq,
                      'ne_symmetry_point': sym_pt, 'te_symmetry_point': sym_pt_te,
                      'n_sep_fit': n_sep_fit, 'sep_index': index_cut                                  
                      }
        
        
        return result_dic
        
    
    elif x_choice == 'RRsep':
        fit_tanh_dic = tanh_fit(x_choice, x_coord, ne, te)
        tanh_ne_fit = fit_tanh_dic['tanh_ne_fit']
        # dn = fit_tanh_dic['popt_ne'][2]
        dn = fit_tanh_dic['popt_ne'][1]
        tanh_te_fit = fit_tanh_dic['tanh_te_fit']
        # dtn = fit_tanh_dic['popt_te'][2]
        dtn = fit_tanh_dic['popt_te'][1]   
        ne_ped = (fit_tanh_dic['popt_ne'][0] + fit_tanh_dic['popt_ne'][2])*max(ne)
        
        "fitting choice 1: in the width, symmetry point +- width/2"
        xcoord_exp = []
        an_cut = []
        for j in range(len(x_coord)):
            if x_coord[j] <= fit_tanh_dic['popt_ne'][0] + dn and x_coord[j] >= fit_tanh_dic['popt_ne'][0] - dn:
                xcoord_exp.append(x_coord[j])
                an_cut.append(neuden[j])
        
        xcoord_exp = np.asarray(xcoord_exp)
        an_cut = np.asarray(an_cut)
        
        fit_exp_dic = exp_fit(xcoord_exp, an_cut)

    
    
    


#--------------------spare-zone--------------------------------------------

# "fitting choice 2: find the point before the kink"
# xcoord_k = []
# an_k_cut = []
# for af in range(len(x_coord_rev)):
#     if x_coord_rev[af] <= sym_pt + dn:
#         xcoord_k.append(x_coord_rev[af])
#         an_k_cut.append(neuden_rev[af])



# "create try and error list"
# n_list = []
# # nn_i = len(xcoord_exp)
# nn_i = 4
# # print(len(xcoord_k))
# while nn_i < len(xcoord_k) + 1:
#     n_list.append(nn_i)
#     nn_i = nn_i + 1
# # print(n_list)

# an_tmp_dic = {}
# x_tmp_dic = {}
# pen_try = []
# len_try = []
# lne = []

# for ak in n_list:
#     x_tmp = []
#     an_tmp = []
#     # print(ak)
#     for ah in range(ak):
#         x_tmp.append(xcoord_k[ah])
#         an_tmp.append(an_k_cut[ah])
#     x_tmp = np.asarray(x_tmp)
#     an_tmp = np.asarray(an_tmp)
#     x_tmp_dic[str(ak)] = x_tmp
#     an_tmp_dic[str(ak)] = an_tmp   
#     # print(ak)
#     # print(x_tmp)
#     # print(an_tmp)
#     fitexp_tmp = exp_fit(x_choice, x_tmp, an_tmp)
#     fitlnexp_tmp = linear_fit(x_choice, x_tmp, an_tmp)
#     pen_try.append(1/fitexp_tmp['popt_an'][1])
#     len_try.append(1/fitlnexp_tmp['popt_an'][0])
#     lne.append(fitlnexp_tmp['popt_an'][0])
    
# diff_len = np.diff(len_try)


# "print to check fit method 2 result"
# # print(n_list)
# # print(n_list[-1])
# # print(x_tmp_dic[str(n_list[-1])])
# # print(pen_try)
# # print(diff_val)

# "plot the method 2 result"
# # plt.figure(figsize=(7,7))
# # plt.errorbar(x_tmp_dic.keys(), pen_try, yerr= stdev(pen_try), fmt = 'o-', color = 'b', label= 'efold_length')
# # plt.xlabel('number of fitting points')
# # plt.title('efold length exp fit')
# # plt.legend()

# # plt.figure(figsize=(7,7))
# # plt.errorbar(x_tmp_dic.keys(), len_try, yerr= stdev(len_try), fmt = 'o-', color = 'b', label= 'efold_length')
# # plt.xlabel('number of fitting points')
# # plt.title('efold length log fit')
# # plt.legend()


# # print(len_try)

# # plt.figure(figsize=(7,7))
# # plt.plot(x_tmp_dic.keys(), lne, 'o-', color = 'b', label= 'efold_length')
# # plt.xlabel('number of fitting points')
# # plt.title('log fit slope')
# # plt.legend()

   
# dis_len = []
# stable_len = []
# for i_diff in diff_len:
#     dis_len.append(abs(i_diff))
#     if abs(i_diff) <= 0.003:
#         stable_len.append(abs(i_diff))

# # print(dis_pen)

# p = list(dis_len).index(stable_len[0])
# # print(diff_pen)
# ind = n_list[p]
# # if p + 1 < len(n_list):
# #     # print(len(n_list))
# #     # print(p)
# #     ind = n_list[p + 1]
# #     # print(ind)
# # elif p + 1 >= len(n_list):
# #     # print(len(n_list))
# #     # print(p)
# #     ind = n_list[p]
# #     # print(ind)
# x_m2 = np.asarray(x_tmp_dic[str(ind)])
# an_m2 = np.asarray(an_tmp_dic[str(ind)])

# # print(x_m2)


# fit_m2_dic = linear_fit(x_choice, x_m2, an_m2)

# exp_fit_m2 = fit_m2_dic['exp_line_fit']
# efold_m2 = 1/fit_m2_dic['popt_an'][0]
# std_m2 = stdev(len_try)/np.sqrt(len(len_try))
# del_x = x_m2[0] - x_m2[-1]

# opq_m2 = 2*dn/efold_m2
