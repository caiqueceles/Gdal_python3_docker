import sys
import glob
 
rootdir = 'utils'
for path in glob.glob(f'{rootdir}/*/**/', recursive=True):
    sys.path.append(path)

## my module
from time_helps import print_time
import fig_map
import filter_raster
import point_to_raster
