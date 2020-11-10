"""
#####################################################################
################# BioSNICAR_GO DRIVER SCRIPT ########################

This script is used to configure the 2-stream radiative transfer
model BioSNICAR_GO. Here variable values are defined, the model called
and the results plotted.

NB. Setting Mie = 1, GO = 0 and algal impurities = 0 is equivalent to
running the original SNICAR model of Flanner et al. (2007, 2009)

NB: if using only granular layers, recommend using the faster Toon et al
tridiagonal matix solver (by setting TOON = True), however this will not
include any specular reflection components. If solid ice layers are
included in the ice/snow column, the ADDING-DOUBLING solver must be used
(i.e. ADD_DOUBLE = True).

Author: Joseph Cook, October 2020

######################################################################
######################################################################

"""
from snicar8d_mie import snicar8d_mie
from snicar8d_GO import snicar8d_GO
import matplotlib.pyplot as plt
import numpy as np

# set dir_base to the location of the BioSNICAR_GO_PY folder

dir_base = '/home/joe/Code/BioSNICAR_GO_PY/'

##############################
# 1) Choose plot/print options
###############################


show_figs = True # toggle to display spectral albedo figure
save_figs = True # toggle to save spectral albedo figure to file
savepath = dir_base # base path for saving figures
print_BBA = True # toggle to print broadband albedo to terminal
print_band_ratios = False # toggle to print various band ratios to terminal
smooth = True # apply optional smoothing function (Savitzky-Golay filter)
window_size = 11 # if applying smoothing filter, define window size
poly_order = 3 # if applying smoothing filter, define order of polynomial

##################################################################
# 2) CHOOSE METHOD FOR DETERMINING OPTICAL PROPERTIES OF ICE GRAINS
# for small spheres choose Mie, for hexagonal plates or columns of any size
# choose GeometricOptics
#####################################################################

Mie = True
GeometricOptics = False

# If Mie = True, select solver (only Toon available for GO mode).
TOON = False # toggle Toon et al tridiagonal matrix solver
ADD_DOUBLE = True # toggle adding-doubling solver


######################################
## 3. RADIATIVE TRANSFER CONFIGURATION
#######################################

DIRECT   = 1        # 1= Direct-beam incident flux, 0= Diffuse incident flux
APRX_TYP = 1        # 1= Eddington, 2= Quadrature, 3= Hemispheric Mean
DELTA    = 1        # 1= Apply Delta approximation, 0= No delta
solzen   = 10      # if DIRECT give solar zenith angle (degrees from 0 = nadir, 90 = horizon)


#############################################
## 4. SET PHYSICAL PROPERTIES OF THE ICE/SNOW
#############################################

# grain shapes are only active in Mie scattering mode - GO assumes hexagonal columns.
# snw_shp can be 0 = sphere, 1 = spheroid, 2 = hexagonal plate, 3= koch snowflake
# shp_fctr = ratio of nonspherical grain effective radii to that of equal-volume sphere
    # 0=use recommended default value (He et al. 2017);
    # use user-specified value (between 0 and 1)
    # only activated when sno_shp > 1 (i.e. nonspherical)

dz = [0.001, 0.01, 1, 1, 10] # thickness of each vertical layer (unit = m)
nbr_lyr = len(dz)  # number of snow layers
layer_type = [0,0,1,1,1]
R_sfc = 0.15 # reflectance of undrlying surface - set across all wavelengths
rho_snw = [600, 600, 910, 910, 910] # density of each layer (unit = kg m-3)
rds_snw = [2000,2000,2000,2000,2000] # effective grain radius of snow/bubbly ice
rwater = [0, 0, 0, 0, 0] # if  using Mie calculations, add radius of optional liquid water coating
snw_shp =[0,0,0,0,0] # grain shape(He et al. 2016, 2017)
shp_fctr = [0,0,0,0,0] # shape factor (ratio of aspherical grain radii to that of equal-volume sphere)
snw_ar = [0,0,0,0,0] # aspect ratio (ratio of width to length)

# if using GeometricOptics, set side_length and depth
side_length = [30000,30000,30000,30000,30000] 
depth = [30000,30000,30000,30000,30000]


#######################################
## 5) SET LAP CHARACTERISTICS
#######################################

nbr_aer = 16 # Define total number of different LAPs/aerosols in model

# set filename stubs
stb1 = 'RealPhenol_algae_geom_' # %name stub 1
stb2 = '.nc'  # file extension
wrkdir2 = str(dir_base + '/Data/Algal_Optical_Props/') # working directory
snw_stb1 = 'snw_alg_' # name stub for snow algae

# CHOOSE DIMENSIONS OF GLACIER ALGAE 1
algae_r = 6 # algae radius
algae_l = 60 # algae length
#glacier_algae1 = str(wrkdir2+stb1+str(algae_r)+'_'+str(algae_l)+stb2) # create filename string
glacier_algae1 = str(wrkdir2+'RealPhenol_algae_geom_{}_{}.nc'.format(algae_r,algae_l))

# CHOOSE DIMENSIONS OF GLACIER ALGAE 2
algae2_r = 2 # algae radius
algae2_l = 10 # algae length
glacier_algae2 = str(wrkdir2+stb1+str(algae2_r)+'_'+str(algae2_l)+stb2) # create filename string

# CHOOSE SNOW ALGAE DIAMETER
snw_algae_r = 1 # snow algae diameter
snw_alg = str(wrkdir2+snw_stb1+str(snw_algae_r)+stb2) # create filename string

# SET UP IMPURITY MIXING RATIOS
# PARTICLE MASS MIXING RATIOS (units: ng(species)/g(ice), or ppb)

for x in [0]:
    
    mss_cnc_soot1 = [0,0,0,0,0]    # uncoated black carbon
    mss_cnc_soot2 = [0,0,0,0,0]    # coated black carbon
    mss_cnc_dust1 = [0,0,0,0,0]    # global average dust 1
    mss_cnc_dust2 = [0,0,0,0,0]    # global average dust 2
    mss_cnc_dust3 = [0,0,0,0,0]    # global average dust 3
    mss_cnc_dust4 = [0,0,0,0,0]    # global average dust 4
    mss_cnc_ash1 = [0,0,0,0,0]    # volcanic ash species 1
    mss_cnc_GRISdust1 = [0,0,0,0,0]    # GRIS dust 1 (Cook et al. 2019 "mean")
    mss_cnc_GRISdust2 = [0,0,0,0,0]    # GRIS dust 2 (Cook et al. 2019 HIGH)
    mss_cnc_GRISdust3 = [0,0,0,0,0]    # GRIS dust 3 (Cook et al. 2019 LOW)
    mss_cnc_GRISdustP1 = [0,0,0,0,0]  # GRIS dust 1 (Polashenki2015: low hematite)
    mss_cnc_GRISdustP2 = [0,0,0,0,0]  # GRIS dust 1 (Polashenki2015: median hematite)
    mss_cnc_GRISdustP3 = [0,0,0,0,0]  # GRIS dust 1 (Polashenki2015: median hematite)
    mss_cnc_snw_alg = [0,0,0,0,0]    # Snow Algae (spherical, C nivalis)
    mss_cnc_glacier_algae1 = [100000,0,0,0,0]    # glacier algae type1
    mss_cnc_glacier_algae2 = [0,0,0,0,0]    # glacier algae type2 


    ##########################################################################
    ################## CALL FUNCTIONS AND PLOT OUTPUTS #######################
    ##########################################################################

    # SET FILE NAMES CONTAINING OPTICAL PARAMETERS FOR ALL IMPURITIES:

    FILE_soot1  = 'mie_sot_ChC90_dns_1317_2.nc'
    FILE_soot2  = 'miecot_slfsot_ChC90_dns_1317_2.nc'
    FILE_dust1  = 'aer_dst_bln_20060904_01.nc'
    FILE_dust2  = 'aer_dst_bln_20060904_02.nc'
    FILE_dust3  = 'aer_dst_bln_20060904_03.nc'
    FILE_dust4  = 'aer_dst_bln_20060904_04.nc'
    FILE_ash1  = 'volc_ash_mtsthelens_20081011.nc'
    FILE_GRISdust1 = 'dust_greenland_Cook_CENTRAL_20190911.nc'
    FILE_GRISdust2 = 'dust_greenland_Cook_HIGH_20190911.nc'
    FILE_GRISdust3 = 'dust_greenland_Cook_LOW_20190911.nc'
    FILE_GRISdustP1 = 'dust_greenland_L_20150308.nc'
    FILE_GRISdustP2 = 'dust_greenland_C_20150308.nc'
    FILE_GRISdustP3 = 'dust_greenland_H_20150308.nc'
    FILE_snw_alg  = snw_alg # snow algae (c nivalis)
    FILE_glacier_algae1 = glacier_algae1 # Glacier algae
    FILE_glacier_algae2 = glacier_algae2 # Glacier algae

    #########################################################
    # Error catching: invalid combinations of input variables
    #########################################################

    if Mie == True and GeometricOptics == True:

        raise ValueError("ERROR: BOTH MIE AND GO MODES SELECTED: PLEASE CHOOSE ONE")

    elif TOON == True and ADD_DOUBLE == True:

        raise ValueError("ERROR: BOTH SOLVERS SELECTED: PLEASE CHOOSE EITHER TOON OR ADD_DOUBLE")
    
    # elif np.sum(layer_type) < 1 and ADD_DOUBLE==True:

    #     raise Warning("There are no ice layers in the model - use Toon et al tridiagonal matrix solver")

    # elif np.sum(layer_type) > 0 and TOON == True:

    #     raise Warning("There are ice layers in the model - please use the adding-doubling solver")

    #######################################
    # IF NO INPUT ERRORS --> FUNCTION CALLS
    #######################################

    elif Mie == True:

        [wvl, albedo, BBA, BBAVIS, BBANIR, abs_slr, heat_rt] =\
        snicar8d_mie(dir_base, DIRECT, layer_type, APRX_TYP, DELTA, solzen, TOON, ADD_DOUBLE, R_sfc, dz,\
        rho_snw, rds_snw, rwater, nbr_lyr, nbr_aer, snw_shp, shp_fctr, snw_ar, mss_cnc_soot1, mss_cnc_soot2,\
        mss_cnc_dust1, mss_cnc_dust2, mss_cnc_dust3, mss_cnc_dust4, mss_cnc_ash1, mss_cnc_GRISdust1,\
        mss_cnc_GRISdust2, mss_cnc_GRISdust3, mss_cnc_GRISdustP1, mss_cnc_GRISdustP2, mss_cnc_GRISdustP3,\
        mss_cnc_snw_alg, mss_cnc_glacier_algae1, mss_cnc_glacier_algae2, FILE_soot1, FILE_soot2, FILE_dust1,\
        FILE_dust2, FILE_dust3, FILE_dust4, FILE_ash1, FILE_GRISdust1, FILE_GRISdust2, FILE_GRISdust3,\
        FILE_GRISdustP1, FILE_GRISdustP2,FILE_GRISdustP3, FILE_snw_alg, FILE_glacier_algae1, FILE_glacier_algae2)

    elif GeometricOptics == True:

        [wvl, albedo, BBA, BBAVIS, BBANIR, abs_slr, heat_rt] = \
        snicar8d_GO(dir_base, DIRECT, APRX_TYP, DELTA, solzen, R_sfc, dz, \
        rho_snw, side_length, depth, nbr_lyr, nbr_aer, mss_cnc_soot1, mss_cnc_soot2, mss_cnc_dust1, mss_cnc_dust2,\
        mss_cnc_dust3, mss_cnc_dust4, mss_cnc_ash1, mss_cnc_GRISdust1, mss_cnc_GRISdust2, mss_cnc_GRISdust3,\
        mss_cnc_GRISdustP1, mss_cnc_GRISdustP2, mss_cnc_GRISdustP3, mss_cnc_snw_alg, mss_cnc_glacier_algae1,\
        mss_cnc_glacier_algae2, FILE_soot1, FILE_soot2, FILE_dust1, FILE_dust2, FILE_dust3, FILE_dust4, FILE_ash1,\
        FILE_GRISdust1, FILE_GRISdust2, FILE_GRISdust3, FILE_GRISdustP1, FILE_GRISdustP2, FILE_GRISdustP3,\
        FILE_snw_alg, FILE_glacier_algae1, FILE_glacier_algae2)

    else:
        
        print("NEITHER MIE NOR GO MODE SELECTED: PLEASE CHOOSE ONE")
    
    ########################
    # PLOTTING AND PRINTING
    ########################

    if smooth:
        from scipy.signal import savgol_filter
        yhat = savgol_filter(albedo, window_size, poly_order)
        albedo = yhat

    if print_band_ratios:

        I2DBA = albedo[40]/albedo[36]
        I3DBA = (albedo[36] - albedo[40]) / albedo[45]
        NDCI = ((albedo[40]-albedo[38])-(albedo[45]-albedo[38]))*((albedo[40]-albedo[38])/(albedo[45]-albedo[38]))
        MCI = (albedo[40]-albedo[36])/(albedo[40]+albedo[36])
        II = np.log(albedo[26])/np.log(albedo[56])

        print("\nINDEX VALUES")
        print("2DBA Index: ",I2DBA)
        print("3DBA index: ", I3DBA)
        print("NDCI index: ", NDCI)
        print("MCI index: ", MCI)
        print("Impurity Index: ", II)

    if print_BBA:

        print('BROADBAND ALBEDO = ', BBA)

    #### PLOT ALBEDO ######
    plt.plot(wvl, albedo)

plt.ylabel('ALBEDO'), plt.xlabel('WAVELENGTH (microns)'), plt.xlim(0.3,1.5),
plt.ylim(0,1), plt.axvline(x = 0.68,color='g',linestyle='dashed')

if save_figs:
    plt.savefig(str(savepath+"spectral_albedo.png"))
    plt.show()

if show_figs:
    plt.show()