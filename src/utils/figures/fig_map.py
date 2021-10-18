
import pysal as ps

import matplotlib.pyplot as plt
import numpy as np

from pysal.model import spreg

from libpysal.weights import lag_spatial
from pysal.explore import esda

from  context import * 


plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["mathtext.default"] = 'regular'

## font size of figure

SMALL_SIZE = 18
MEDIUM_SIZE = 20
BIGGER_SIZE = 20
Legend_size = 16

plt.rc('font', size=BIGGER_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=Legend_size)    # legend fontsize
    


def moran_residual_scatter(X, y, W, title_var ,outputname ,  weigh_area =[0], jupyter=0):
    # print('ok')

    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["mathtext.default"] = 'regular'

    ## font size of figure
    SMALL_SIZE = 20
    MEDIUM_SIZE = 22
    BIGGER_SIZE = 22

    plt.rc('font', size=BIGGER_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=18)    
    
    
    m3 =  spreg.OLS(y=y, x=X, w=W,spat_diag=True, moran=True)

    # ypredt= np.exp(stats.norm.rvs( m3.betas[0]+m3.betas[1]*X , m3.sig2, 1000)).mean(axis=1)

    residuol= y - np.array(m3.betas[0]+ m3.betas[1]*(X))

    elev_mean = np.array(residuol)
    # elev_mean = np.array(residuol)
  
    elev_meanLag = lag_spatial(W, elev_mean)
    # print(elev_meanLag )
    # elev_meanLagQ10 = ps.Quantiles(elev_meanLag, k=10)
    b,a = np.polyfit( elev_mean.flat , elev_meanLag, 1)

    if weigh_area[0]!=0:
        # m3 =  ps.spreg.OLS(y=y, x=X, w=W,spat_diag=True, moran=True)
        
        m3, result_alo_exp  = regression.weight_loglog_linear_fit(X.flat, X.flat,np.array(weigh_area.flat)  )
        
        # m3= rodarfit_w(linear_fit, X.flat, y.flat,   np.array(weigh_area.flat)        )

        # ypredt= np.exp(stats.norm.rvs( m3.betas[0]+m3.betas[1]*X , m3.sig2, 1000)).mean(axis=1)

        residuol=y - np.array(m3[0]+ m3[1]*(X))

        elev_mean = np.array(residuol)
        # elev_mean = np.array(residuol)
    
        elev_meanLag = lag_spatial(W, elev_mean)
        # print(elev_meanLag )
        # elev_meanLagQ10 = ps.Quantiles(elev_meanLag, k=10)
        b,a = np.polyfit( elev_mean.flat , elev_meanLag, 1)
        elev_mean = residuol #* weigh_area/sum(weigh_area )*np.mean(weigh_area )
        # print(elev_mean )
        elev_meanLag = lag_spatial(W, elev_mean)
        b,a = np.polyfit( elev_mean.flat , elev_meanLag, 1)

        # print(elev_meanLag )
        # elev_meanLagQ10 = ps.Quantiles(elev_meanLag, k=10)
       



    y= np.array(elev_mean)
    I_elev_mean = esda.Moran(y, W)

    f, ax = plt.subplots(1, figsize=(8, 6))

    ax.plot(elev_mean, elev_meanLag, '.', ms=10, color='black', alpha=0.4)

    # dashed vert at mean of the last year's PCI
    ax.vlines(elev_mean.mean(), elev_meanLag.min(), elev_meanLag.max(), linestyle='--')
    # dashed horizontal at mean of lagged PCI
    ax.hlines(elev_meanLag.mean(), elev_mean.min(), elev_mean.max(), linestyle='--')

    # red line of best fit using global I as slope
    ax.plot(elev_mean, a + b*elev_mean, 'k', label='Slope:%0.3f, p:%0.3f' %(I_elev_mean.I, I_elev_mean.p_sim))
    if weigh_area[0]!=0:
        ax.plot([0,1],[1,0], 'w' , alpha=1 ) #,label='OLS Slope:%0.3f, p:%0.3f' %(0, 0)  )
    else:
        ax.plot([0,1],[1,0], 'w' , alpha=1 ,label='OLS Slope:%0.3f, p:%0.3f' %(m3.moran_res[0],m3.moran_res[2])  )
    ax.set_title(title_var)
    ax.set_ylabel('Spatial Lag of residual')
    ax.set_xlabel('residual')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.tick_params(top='off',  right='off')
    ax.legend( loc='upper left', fancybox=True, frameon=False ,  framealpha=0.5 , scatterpoints = 1)

    f.set_tight_layout(True)
    if jupyter==1:
        plt.show()
    else:
        plt.savefig(outputname, dpis=300 )
        plt.close('all')








def moran_autocorrelation_scatter(X, y, W, title_xylabel ,outputname , xlim, jupyter=0):
    
    b,a = np.polyfit(X, y, 1)
    I_H_mean = esda.Moran(y, W)
    # print(I_H_mean)

    f, ax = plt.subplots(1, figsize=(8, 6))

    ax.plot(X, y, '.', color='firebrick', alpha=0.4)

    # dashed vert at mean of the last year's PCI
    ax.vlines(X.mean(), y.min(), y.max(), linestyle='--')
    # dashed horizontal at mean of lagged PCI
    ax.hlines(y.mean(), X.min(), X.max(), linestyle='--')

    # red line of best fit using global I as slope
    ax.plot(X, a + b*X, 'r', label='Slope:%0.3f, p:%0.3f' % (I_H_mean.I, I_H_mean.p_sim))
    ax.set_title(title_xylabel[0])
    ax.set_xlabel(title_xylabel[1])
    ax.set_ylabel(title_xylabel[2])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.tick_params(top='off',  right='off')
    ax.set_xlim(xlim)
    ax.legend( loc='upper left', fancybox=True, frameon=False ,  framealpha=0.5 , scatterpoints = 1)

    f.set_tight_layout(True)
    if jupyter==1:
        plt.show()
    plt.savefig(outputname+'_x_autocorreletion.png', dpis=300 )

    # print(I_H_mean.I, I_H_mean.p_sim)