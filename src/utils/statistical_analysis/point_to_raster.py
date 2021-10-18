
import numpy as np
import pandas as pd


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

