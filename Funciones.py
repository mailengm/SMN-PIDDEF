"""
##TODO 
Hacer una librería de esto
"""
from matplotlib import pyplot as plt
from matplotlib import colors
from sklearn.svm import SVC
import numpy as np
import glob
import pyart
import scipy.io as sio
import re

def read_files(day,init_time):
    day = str(day)
    init_time = str(init_time)
    path_user_radar = './febdBZ/'+ day + '/'
    FileList_radar = np.sort(glob.glob(path_user_radar+'*.nc'))
    
    file2read_radar=0
    for i in range(len(FileList_radar)):
        file2read_radar_time = FileList_radar[i].split('_')[1][:4]
        if (file2read_radar_time == init_time):
            file2read_radar = FileList_radar[i]
    
    return(file2read_radar)
 



def chequear_existencia(day,init_time):
    day = str(day)
    init_time = str(init_time)
    path_user_radar = './febdBZ/'+ day + '/'
    FileList_radar = np.sort(glob.glob(path_user_radar+'*.nc'))
    existencia = False
    for i in range(len(FileList_radar)):
        file2read_radar_time = FileList_radar[i].split('_')[1][:4]
        if (file2read_radar_time == init_time):
            existencia=True
    if not existencia:
        print('No se encontró el archivo',day, init_time)
    return(existencia)

def get_volumes(day, init_time, bins=240,diff=30):
    diff=diff/10
    day = str(day)
    init_time = str(init_time)
    path_user_radar = './febdBZ/'+ day + '/'
    FileList_radar = np.sort(glob.glob(path_user_radar+'*.nc'))
    proof = 0
    file2read_radar=0
    
    for i in range(len(FileList_radar)):
        file2read_radar_time = FileList_radar[i].split('_')[1][:4]
        if (file2read_radar_time == init_time):
            file2read_radar = FileList_radar[i]
            proof= int(i+diff)
           
    
    file2follow = FileList_radar[proof]   
               

    radar = pyart.io.read(file2read_radar)
    radar2 = pyart.io.read(file2follow)
    
    gatefilter = pyart.filters.GateFilter(radar)
    
    gatefilter.exclude_transition()
    gatefilter.exclude_masked('dBZ')
    
    grid = pyart.map.grid_from_radars((radar,), 
                                gatefilters=(gatefilter, ),
                                grid_shape=(1, bins, bins),
                                grid_limits=((0, 0), (-bins*1000, bins*1000), (-bins*1000, bins*1000)),
                                fields=['dBZ'])
    
    gatefilter2 = pyart.filters.GateFilter(radar2)
    
    gatefilter2.exclude_transition()
    gatefilter2.exclude_masked('dBZ')
    
    grid2 = pyart.map.grid_from_radars(
        (radar2,), gatefilters=(gatefilter2, ),
        grid_shape=(1, bins, bins),
        grid_limits=((0, 0), (-bins*1000, bins*1000), (-bins*1000, bins*1000)),
        fields=['dBZ'])
            
            
    
    return (grid,grid2)

def get_labels(lines,threshold=35):
    samples = []
    eventos = len(lines)
    for i in range(eventos):
        (fecha,hora)=(lines[i].strip().split("\t")[0],lines[i].strip().split("\t")[1])
        if chequear_existencia(fecha,hora):
            samples.append(get_volumes(fecha,hora)[1])
        else:
            eventos=eventos-1
    
    labels = []
    for i in range(eventos):
        grid = samples[i].fields['dBZ']['data'][0]
        for x in range(240):
            for y in range(240):
                if not grid.mask[x,y]:
                    if grid[x,y]<35:
                        grid.data[x,y]=0
                    else:
                        grid.data[x,y]=1
        labels.append(grid)
    return(labels)

def get_rays(day):
    folder=str(day)[:6]
    dia=str(day)
    path_user_rayos = './rayos/'+ folder + '/' + dia
    # Con esto levanto todos los datos de rayos país ese día
    with open(path_user_rayos+'.txt') as f:
        lights = f.readlines()
    return(lights)

def get_limits(day,init_time):
    grid=get_volumes(day,init_time)[0]
    lat_grid = grid.get_point_longitude_latitude(level=0, edges=False)[1]
    lon_grid = grid.get_point_longitude_latitude(level=0, edges=False)[0]
    extLat   = [np.amin(lat_grid),np.amax(lat_grid)]
    extLon   = [np.amin(lon_grid),np.amax(lon_grid)]
    return(extLon,extLat)

def rayos_correctos(archivo,limite_tiempo,limite_lon,limite_lat):
    index = []
    for i in range(len(archivo)):
        foo=archivo[i].split()
        t=(foo[3]+foo[4]+foo[5])
        if (t<limite_tiempo[1]) and (t>limite_tiempo[0]) :
            
            if(float(foo[7])>limite_lat[0]) and (float(foo[7])<limite_lat[1]):
                
                if(float(foo[8])>limite_lon[0]) and (float(foo[8])<limite_lon[1]):
                    index.append(i)
    return(index)
    
