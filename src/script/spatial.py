import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import descartes


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



fig, ax = plt.subplots()
gapsmax.plot(ax=ax)
strikes.plot(ax=ax)
buffer1.plot(ax=ax, color='gray')


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
    brings2dif.boundary.plot(ax=ax, color='k')
    i+=1


allbuffer = buffer1.append(colrings)
allbuffer.boundary.plot(ax=ax, color='blue')

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
print(allbufferdf)

nameunion = gapsmax.nstrike.values
print(nameunion)

selallbufferdf = allbufferdf.loc[allbufferdf.nstrike==nameunion[0],:]
print(selallbufferdf)

selgapsmax = gapsmax.loc[gapsmax.nstrike==nameunion[0],:]
print(selgapsmax)

# uniongapsrings = selallbufferdf.geometry.union(selgapsmax)
# uniongapsrings = selallbufferdf.overlay(selgapsmax, how='union')
# uniongapsrings = selallbufferdf.union(selgapsmax, align=False)

uniongapsrings = gpd.overlay(selallbufferdf,selgapsmax, how='union')
# uniongapsrings = gpd.sjoin(selallbufferdf,selgapsmax, how='inner')


print(uniongapsrings)

plt.close()

fig, ax = plt.subplots()
allbufferdf.boundary.plot(ax=ax)
gapsmax.plot(ax=ax)
selallbufferdf.boundary.plot(ax=ax, color='r')
selgapsmax.boundary.plot(ax=ax, color='k')
uniongapsrings.boundary.plot(ax=ax, color='green')


plt.show()














