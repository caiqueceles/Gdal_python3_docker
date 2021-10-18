

import numpy as np
import matplotlib.pyplot as plt


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
		print('Number of lines with NaN remaining:')
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
