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

def get_volpost_data(day,init_time):
    index=0
    
    if chequear_existencia(day,init_time):
        day = str(day)
        init_time = str(init_time)
        path_user_radar = './febdBZ/'+ day + '/'
        FileList_radar = np.sort(glob.glob(path_user_radar+'*.nc'))
        existencia = False
        momento=0
        for i in range(len(FileList_radar)):
            file2read_radar_time = FileList_radar[i].split('_')[1][:4]
            if (file2read_radar_time == init_time):
                index=i+3
        momento= FileList_radar[index].split('_')[1][:4]
        data= str(day)+"\t"+str(momento)
                
    return(data)


def get_volumes(day, init_time, bins=240):
    
    day = str(day)
    init_time = str(init_time)
    path_user_radar = './febdBZ/'+ day + '/'
    FileList_radar = np.sort(glob.glob(path_user_radar+'*.nc'))
    
    file2read_radar=0
    
    for i in range(len(FileList_radar)):
        file2read_radar_time = FileList_radar[i].split('_')[1][:4]
        if (file2read_radar_time == init_time):
            file2read_radar = FileList_radar[i]
            proof= i       
    
    radar = pyart.io.read(file2read_radar)
    
    gatefilter = pyart.filters.GateFilter(radar)
    gatefilter.exclude_transition()
    gatefilter.exclude_masked('dBZ')
    
    grid = pyart.map.grid_from_radars((radar,), 
                                gatefilters=(gatefilter, ),
                                grid_shape=(1, bins, bins),
                                grid_limits=((0, 0), (-bins*1000, bins*1000), (-bins*1000, bins*1000)),
                                fields=['dBZ'])            
            
    
    return (grid)

def get_labels(lines,threshold=35):
    samples = []
    eventos = len(lines)
    for i in range(eventos):
        (fecha,hora)=(lines[i].strip().split("\t")[0],lines[i].strip().split("\t")[1])
        if chequear_existencia(fecha,hora):
            samples.append(get_volumes(fecha,hora))
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
    grid=get_volumes(day,init_time)
    lat_grid = grid.get_point_longitude_latitude(level=0, edges=False)[1]
    lon_grid = grid.get_point_longitude_latitude(level=0, edges=False)[0]
    extLat   = [np.amin(lat_grid),np.amax(lat_grid)]
    extLon   = [np.amin(lon_grid),np.amax(lon_grid)]
    return(extLon,extLat)

def rayos_correctos(archivo,limite_tiempo,limite_lon,limite_lat,bins):
    """
    Esta función me dice las coordenadas de los rayos en la grid
    """
    difLat   = bins/(limite_lat[1]-limite_lat[0])
    difLon   = bins/(limite_lon[1]-limite_lon[0])
    
    index = []
    for i in range(len(archivo)):
        foo=archivo[i].split()
        t=(foo[3]+foo[4]+foo[5])
        if (t<limite_tiempo[1]) and (t>limite_tiempo[0]) :
            
            if(float(foo[7])>limite_lat[0]) and (float(foo[7])<limite_lat[1]):
                
                if(float(foo[8])>limite_lon[0]) and (float(foo[8])<limite_lon[1]):
                    #index.append(i)
                    y=int((float(foo[7])-limite_lat[0])*difLat)
                    x=int((float(foo[8])-limite_lon[0])*difLon)
                    
                    index.append([x,y])
    return(index)
    
    
def grid_rayos(datos_samples,bins=240):
    (fecha,hora)=(datos_samples[0].strip().split("\t")[0],datos_samples[0].strip().split("\t")[1])
    (Lat, Lon)= get_limits(fecha,hora)
    #Indices de los rayos que estan en los límites del radar
    eventos = len(datos_samples)
    index = []
    ##eventos=2
    for i in range(eventos):
        (fecha,hora)=(datos_samples[i].strip().split("\t")[0],datos_samples[i].strip().split("\t")[1])
        if chequear_existencia(fecha,hora):
    
            file2read_radar=read_files(fecha,hora)
            
            horario = (file2read_radar.split('_')[1],file2read_radar.split('_')[4])
            lines = get_rays(fecha)
            ind = rayos_correctos(lines,horario, Lon, Lat,240) 
            
                           
        else:
            eventos=eventos-1
        index.append(ind)
    
    #Ahora solo necesito mapearlos en una grilla
    
    grid_rayos = []
    for i in range (eventos):
        indices=index[i]
        rayos = np.zeros((bins,bins))
        for j in range(len(indices)):
            (x,y)=indices[j]
            rayos[x,y]=rayos[x,y]+1
        grid_rayos.append(rayos)

    return(grid_rayos)
