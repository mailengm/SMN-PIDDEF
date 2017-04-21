## Funciones para los datos de radar y rayos

- **read_files**(day,init_time): Esta función me devuelve el nombre del archivo que contiene el volumen de radar
  correspondiente a esa fecha y hora
  
- **chequear_existencia**(day,init_time): Esta función es True si el archivo existe, y False si no

- **get_volumes**(day,init_time,bins=240,diff=30): esta función me da las grillas del volumen pedido y el volumen a un
tiempo posterior.

- **get_labels**(lines,threshold=35): Esta función me devuelve una grilla que vale 1 cuando cierto volumen tiene un valor
de dBZ mayor al threshold y 0 si está por debajo.

- **get_rays**(day): Esta función me devuelve el archivo que contiene los rayos de ese día.

- **get_limits**(day, init_time): Esta función me da los límites de los datos del radar.

- **rayos correctos**(archivo, limite_tiempo, límite_lon, limite_lat, bins): Esta función me devuelve los índices de los 
rayos sobre una grilla cuadrada de tañamo indicado que se superpone con la grilla del volumen de radar.

- **grid_rayos**(datos_samples,bins): Esta función me devuelve una grilla que contiene la cantidad de rayos que cayeron 
en casa celda.
