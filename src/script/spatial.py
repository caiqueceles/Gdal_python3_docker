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


strikes = gpd.read_file("../data/strikes_50ha_UTM_17N.shp")
gaps = gpd.read_file("../data/Merge_gaps_all_strikes_area.shp")

#First buffer 5 meters
buffer1 = strikes.geometry.buffer(5)

#Function to create buffer rings
#Two buffers and difference
def rings (strikes, meters):

    brings = strikes.geometry.buffer(meters-5)
    brings2 = strikes.geometry.buffer(meters)
    brings2dif = brings2.difference(brings)

    return brings2dif


#Select total gap area of each strike
listastrike= gaps.nstrike.unique()

i=0
coletor=[]
while i < len(listastrike):

    sel = gaps.loc[gaps['nstrike']==listastrike[i]]
    selmax = sel.loc[sel['date']==sel.date.max()]
    coletor.append(selmax)
    i+=1

gapsmax = pd.concat(coletor)

gapsmax.to_file('../output/gapsmax.shp')

# fig, ax = plt.subplots()
# gapsmax.plot(ax=ax)
# strikes.plot(ax=ax)
# buffer1.plot(ax=ax, color='gray')


#Call function
intervals = np.arange(10,46,5)

colrings = []
i=0
while i < len(intervals):
    #Function parameters: table, intervals
    brings2dif = rings(strikes, intervals[i])
    #colect rings
    colrings.append(brings2dif)
    #Plot
    # brings2dif.boundary.plot(ax=ax, color='k')
    i+=1


allbuffer = buffer1.append(colrings)
# allbuffer.boundary.plot(ax=ax, color='blue')

allbuffer.to_file('../output/allbuffer.shp')

print(allbuffer)
print(gapsmax)

namestrike = strikes.nstrike.values
print(namestrike)

namestrike1 = np.tile(namestrike,9)
print(namestrike1)

# allbufferdf = allbuffer.to_frame()
allbufferdf = gpd.GeoDataFrame(allbuffer)
allbufferdf = allbufferdf.rename(columns={0:'geometry'}).set_geometry('geometry')
print(allbufferdf)

allbufferdf['nstrike'] = namestrike1
print(np.repeat(np.arange(5,46,5),len(intervals)+1 ) )
allbufferdf['idrings'] = np.repeat(np.arange(5,46,5),len(namestrike) )

print(allbufferdf)
allbufferdf.to_file('../output/allbufferdf.shp')

nameunion = gapsmax.nstrike.values
print(nameunion)

col=[]
i=0
while i < len(nameunion ):
    selallbufferdf = allbufferdf.loc[allbufferdf.nstrike==nameunion[i],:]
    
    selgapsmax = gapsmax.loc[gapsmax.nstrike==nameunion[i],:]
    
    selstrikes = strikes.loc[strikes.nstrike==nameunion[i],:]

    uniongapsrings = gpd.overlay(selallbufferdf,selgapsmax, how='union')

    uniongapsrings['area_gap_r']= uniongapsrings.area

    uniongapsrings['percent_area']= uniongapsrings['area_gap_r']/uniongapsrings['F_AREA'] *100
    seluniongapsrings = uniongapsrings.dropna()

    col.append(seluniongapsrings)
    i+=1
# seluniongapsrings = uniongapsrings.loc[uniongapsrings.percent_area > uniongapsrings.percent_area.min(),:]


df_gaps_union = col[0].append(col[1:])

df_gaps_union.to_file('../output/df_gaps_union.shp')
print(df_gaps_union )







# plt.rcParams['font.family'] = 'Times New Roman'
# SMALL_SIZE = 10
# MEDIUM_SIZE = 12
# BIGGER_SIZE = 12
# Legend_size = 16
# plt.rc('font', size=10)          # controls default text sizes
# plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
# plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
# plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
# plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
# plt.rc('legend', fontsize=10)
# # fig, ax = plt.subplots(figsize = (4,4))

# size=[8,6]
# grid=[2,2]


# col=[]
# abcd = ["(a)", "(b)" , "(c)" ,"(d)", "(e)", "(f)",
# "(a)", "(b)" , "(c)" ,"(d)", "(e)", "(f)",
# "(a)", "(b)" , "(c)" ,"(d)", "(e)", "(f)" ]
# fig = plt.figure( figsize=(size[0],size[1]) , facecolor='w' )
# #########################################################################
# # gridspec inside gridspec
# outer_grid = gridspec.GridSpec(grid[0], grid[1], wspace=0.1, hspace=0.1)
# #########################################################################
# ### plot each imagen in subplot
# for i in range(grid[0]*grid[1]):
    
#     ax = plt.Subplot(fig, outer_grid[i])
#     # ax.scatter([0,1],[0,1], c='r')
#     # ax.text(0.05, 1.05, abcd[i], transform=ax.transAxes, size=12)
#     ax.set_title('Strike '+nameunion[i])

#     selallbufferdf = allbufferdf.loc[allbufferdf.nstrike==nameunion[i],:]
    
#     selgapsmax = gapsmax.loc[gapsmax.nstrike==nameunion[i],:]
    
#     selstrikes = strikes.loc[strikes.nstrike==nameunion[i],:]

#     uniongapsrings = gpd.overlay(selallbufferdf,selgapsmax, how='union')

#     uniongapsrings['area_gap_r']= uniongapsrings.area

#     uniongapsrings['percent_area']= uniongapsrings['area_gap_r']/uniongapsrings['F_AREA'] *100
#     seluniongapsrings = uniongapsrings.dropna()

#     col.append(seluniongapsrings)
   
#     selallbufferdf.boundary.plot(ax=ax, color='gray', lw=0.8)
#     selgapsmax.boundary.plot(ax=ax, color='k', lw=0.5)

#     selstrikes.plot(ax=ax, color='k', markersize=10)


#     # divider = make_axes_locatable(ax)
#     # cax = divider.append_axes("right", size="5%", pad=0.05)
#     # im =seluniongapsrings.plot(ax=ax, color=color)

#     uniongapsrings.plot(ax=ax, column='percent_area', cmap='jet', legend=False, vmin=0, vmax=100, ) #cax=cax)
    
#     ax.text(0.05, 1.05, abcd[i], transform=ax.transAxes, size=12)
#     ax.set_title('Strike '+nameunion[i])
    
#     # cax.set_title( '%')
#     # ivider = make_axes_locatable(ax)
#     # cax = divider.append_axes("right", size="5%", pad=0.05)
#     # clb = plt.colorbar(im, cax=cax)

#     # scalebar = AnchoredSizeBar(ax.transData,
#     #                         45, '45 m', 'lower left', 
#     #                         #    pad=1,
#     #                         color='k',
#     #                         frameon=False,
#     #                         size_vertical=1,
#     #                         bbox_to_anchor=(0.035,-0.01),
#     #                         bbox_transform=ax.transAxes, 
#     #                         )

#     # ax.add_artist(scalebar)
#     ax.tick_params(left = False, right = False , labelleft = False ,
#                     labelbottom = False, bottom = False)




# # ax.scatter([0,1],[0,1], color='r')

# fig.suptitle('High-resolution map', fontsize=14)
# plt.savefig('../output/img.png') #, dpi=500, bbox_inches='tight', facecolor='white', transparent=False)
# plt.close()

# print(col)












