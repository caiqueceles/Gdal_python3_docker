# run docker with gdal, python 3 and jupyter

Docker is an app that controls the process in containers
This manual aims to use this container with the main tools.

link para docker with R
https://colinfay.me/docker-r-reproducibility/
https://towardsdatascience.com/reproducible-work-in-r-e7d160d5d198



## pre - requisite
    
vscode installation:
docker installation:

to download the folder: click here
https://github.com/caiqueceles/Gdal_python3_docker.git

The gdal_python3_docker folder contains all the files needed to run python 3 and jupyter.


the folder content:
data: all input data for the scripts
output: the output folder used to save all the necessary output from the scripts.
src: contains all codes (scripts) and is the app folder when the container is running
other files : these are the files that generate and control the virtual environment 


## building an image (it is like a installation file) for the first time

Run in the terminal:

```
docker-compose build
```

## Make the image run as a container process
Run in the terminal:
```
./up.sh
```

Now it is all installed and working (Python3, Jupyter, GDAL and libraries)
Have fun!!!


## Running a python script
Once the container is running, run inside the container (in /app) the command:
python NAMESCRIPT.py

```
python script/py_point_to_MDS_filter.py
```

Check image in the output


##  Start jupyter: copy this link in the browser
http://127.0.0.1:8008/?token=55823d0ba2d38a542305271c1fb68bfccdef227680059b62


### to connect vscode to jupyter
Command Palette (Ctrl+Shift+P)
jupyter: Specify local or remote jupyter server for connections
And copy link above
and reload the vscode


## Debug (optional)
Once the container is running, run inside the container (in /app) the command:
./debug.sh NOMESCRIPT.py

```
./debug script/py_point_to_MDS_filter.py
```

After click in the debug icon, run the debug scrip (play icon)


## To install a library, open a terminal (out of container process) (optional)
Go to terminal tab > new terminal

In the project directory, execute:
./install.sh LIBRARYNAME

```
./install.sh pandas
```

## After install new libraries (recommended)

After installing one or many new libraries, it is needed to build the image again
For this it is needed to stop the container process and build the image again

In the project directory, execute:

```
docker-compose down
```

```
docker-compose build
```

```
./up.sh
```



