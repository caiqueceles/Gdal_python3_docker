
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import ndimage
import time, sys
import pandas as pd


##################################################
rootdir = '/app/script/'
sys.path.append(rootdir)
from context import *
##################################################



### lendo arquivo binario do numpy
df = np.load("../data/lidar.npy")
print(df)


### function to create the image
def GridTab( data, size, stat ):
	"""[summary]

	Args:
		data (numpy): array with x y z of point lifar
		size (integer): mapv pixel size
		stat (string): stat type

	Returns:
		data frame: with x columns and y as rowns
	"""
	### definition of input data as data frame
	dfcxyz= pd.DataFrame(data, columns=['x', 'y', 'z'] )
	### Setting the x and y classes of pixel size
	dfcxyz['cx10'] = data[:,0]/size
	dfcxyz['cy10'] = data[:,1]/size
	dfcxyz['cx10']=dfcxyz['cx10'].astype(int)
	dfcxyz['cy10']=dfcxyz['cy10'].astype(int)
	dfcxyz['X']=dfcxyz['cx10']*size
	dfcxyz['Y']=dfcxyz['cy10']*size
	### pivot tables to create the images or models
	MD = pd.pivot_table(dfcxyz, index= 'Y', columns= 'X', values = 'z', aggfunc=stat)
	## inverting the order of y utm that is in the crescent order
	MDR=np.flipud(MD) 
	## returning the image in the form of pandas data
	return  MDR




### function to median filter the raster
def MD_filter(data, size, nt):
	"""[summary]

	Args:
		data (data frame): image in data frame format
		size (integer): windows size
		nt (integer): number of interaction 

	Returns:
		data frame: with x columns and y as rowns and fill null
	"""
	print('start of filter function')
	print('Number of lines with NaN remaining:')
	print(np.isnan(data).any(1).sum())

	ni=range(data.shape[0])
	nj=range(data.shape[1])
	i=0
	j=0
	t=0
	MD=np.matrix(data)
	footprint= np.ones((size,size))
	ntf= range(nt)
	for t in ntf:
		# plt.close("all")
		plt.imshow(MD, cmap=plt.cm.gray, interpolation='nearest' )
		plt.title('Modelo Digitais da superficie')
		plt.xlabel('E UTM (m)')
		plt.ylabel('N UTM (m)')
		plt.ion()
		plt.show()

		plt.pause(2)
		print('Numero de linhas com NaN restante:')
		print(np.isnan(MD).any(1).sum())
		MD_med= np.matrix(ndimage.median_filter(MD, footprint=footprint))
		MD_nan=np.matrix(np.isnan(MD))

		for i in ni:
		    for j in range(200):
		  	 	if 1 == MD_nan[i,j]:
		  	 		MD[i,j]= MD_med[i,j]


	print( '....filter end.......')
	print('Number of lines with NaN remaining:')
	print(np.isnan(MD).any(1).sum())
	return MD


### applying the function and calculating the MDS
MDmax= GridTab( df, 1, 'max')
# point_to_raster



# filter_raster
MDF=MD_filter( MDmax, 5 , 5)
# = MD_filter[ MD]



f = plt.figure()
plt.imshow(MDF, cmap=plt.cm.gray, interpolation='nearest' )
plt.title('MDS')
plt.xlabel('E UTM (m)')
plt.ylabel('N UTM (m)')
plt.show()
f.savefig("../output/figura.png")

