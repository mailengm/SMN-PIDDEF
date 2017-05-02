# SMN-PIDDEF
Storm Tracking. Nowcasting
Datos de Rayos
Datos de Radar

## Datos disponibles

Tengo datos de radar y rayos ubicados en una red de 240x240. 

### SVM

La idea es usar los datos de radar como etiqueta y los de rayos como características.

#### Radar

Las etiquetas se consiguen proponiendo un umbral, en este caso 35dBZ; las celdas con reflectividad superior se etiquetan como 1, y las de reflectividad inferior como 0.

#### Características

Se obtuvo una grilla donde cada celda tiene la cantidad de rayos que cayeron ahí durante ese volumen y la diferencia con el número de rayos del volumen siguiente. (GET Training Set)

Luego se computó una red con los vecinos cercanos y se calcularon las mismas cosas. (SVM)

#### SVM

Se usó la función SVC de scikitlearn. 
C=5.0
kernel=rbf

Primero se calculó la predicción para cada volumen. Se guardaron todos los support vectors.
