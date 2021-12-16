import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import descartes

import matplotlib.cm as cm
# from matplotlib.scalebar import ScaleBar
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.gridspec as gridspec
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes




strikes = gpd.read_file("../data/strikes_50ha_UTM_17N.shp")
# gaps = gpd.read_file("../data/Merge_gaps_all_strikes_area.shp")

gapsmax= gpd.read_file('../output/gapsmax.shp')

allbufferdf= gpd.read_file('../output/allbufferdf.shp')

df_gaps_union= gpd.read_file('../output/df_gaps_union.shp')


nameunion = gapsmax.nstrike.values
print(nameunion)




plt.rcParams['font.family'] = 'Times New Roman'
SMALL_SIZE = 10
MEDIUM_SIZE = 12
BIGGER_SIZE = 12
Legend_size = 16
plt.rc('font', size=12)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)
# fig, ax = plt.subplots(figsize = (4,4))

size=[5.9,9.3]
grid=[5,3]


col=[]
abcd = ["(a)", "(b)" , "(c)" ,"(d)", "(e)", "(f)",
"(g)", "(h)" , "(i)" ,"(j)", "(l)", "(m)",
"(n)", "(o)" , "(p)" ,"(q)", "(r)", "(s)" ]
fig = plt.figure( figsize=(size[0],size[1]) , facecolor='w' )
#########################################################################
# gridspec inside gridspec
outer_grid = gridspec.GridSpec(grid[0], grid[1], wspace=0.1, hspace=0.1)
#########################################################################
### plot each imagen in subplot
i=0
for i in range(grid[0]*grid[1]-1):
    
    ax = plt.subplot(grid[0], grid[1], i+1)
    # ax.scatter([0,1],[0,1], c='r')
    # ax.text(0.05, 1.05, abcd[i], transform=ax.transAxes, size=12)
    ax.set_title('Strike '+nameunion[i])

    selallbufferdf = allbufferdf.loc[allbufferdf.nstrike==nameunion[i],:]
    
    selgapsmax = gapsmax.loc[gapsmax.nstrike==nameunion[i],:]
    
    selstrikes = strikes.loc[strikes.nstrike==nameunion[i],:]

    print(df_gaps_union )
    seluniongapsrings = df_gaps_union.loc[df_gaps_union.nstrike_1==nameunion[i],:]
    
    
   
    selallbufferdf.boundary.plot(ax=ax, color='gray', lw=0.8)
    selgapsmax.boundary.plot(ax=ax, color='k', lw=0.5)

    selstrikes.plot(ax=ax, color='k', markersize=10)


    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes("right", size="5%", pad=0.05)
    # im =seluniongapsrings.plot(ax=ax, color=color)

    seluniongapsrings.plot(ax=ax, column='percent_ar', cmap='jet', legend=False, vmin=0, vmax=100, ) #cax=cax)
    
    ax.text(0.05, 1.07, abcd[i], transform=ax.transAxes, size=12)
    ax.set_title('Strike '+nameunion[i])
    
    # cax.set_title( '%')
    # ivider = make_axes_locatable(ax)
    # cax = divider.append_axes("right", size="5%", pad=0.05)
    # clb = plt.colorbar(im, cax=cax)

    # scalebar = AnchoredSizeBar(ax.transData,
    #                         45, '45 m', 'lower left', 
    #                         #    pad=1,
    #                         color='k',
    #                         frameon=False,
    #                         size_vertical=1,
    #                         bbox_to_anchor=(0.035,-0.01),
    #                         bbox_transform=ax.transAxes, 
    #                         )

    # ax.add_artist(scalebar)
    ax.tick_params(left = False, right = False , labelleft = False ,
                    labelbottom = False, bottom = False)

ax1 = plt.subplot(grid[0], grid[1], 15)

# # create the colorbar
norm = colors.Normalize(vmin=0, vmax=100)
cbar = plt.cm.ScalarMappable(norm=norm, cmap='jet')

# divider = make_axes_locatable(ax1)
# cax = divider.append_axes("right", size="10%", pad=0.01)


cax = inset_axes(ax1, width="10%", height="80%", loc='center')
cax.set_title('%')
ax_cbar = fig.colorbar(cbar, cax=cax, orientation='vertical')

# cax.set_title( '%')
# ax_cbar.set_ytick([])
ax1.set_xticks([])
ax1.set_yticks([])
# divider = make_axes_locatable(ax)
# cax = divider.append_axes("right", size="5%", pad=0.05)
# clb = plt.colorbar(im, cax=cax)
for sp1 in ax1.spines.values():
        sp1.set_visible(False)


all_axes = fig.get_axes()
for ax in all_axes:
    for sp in ax.spines.values():
        sp.set_visible(False)

fig.set_tight_layout(True)

# ax.scatter([0,1],[0,1], color='r')

# fig.suptitle('High-resolution map', fontsize=14)
plt.savefig('../output/img.png', dpi=500,  facecolor='white', transparent=False)
plt.close()














