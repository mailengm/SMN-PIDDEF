# SMN-PIDDEF
Storm Tracking. Nowcasting

Primer intento de *algoritmo de aprendizaje*.

Siguiendo los pasos de **Lei Han** y **Juanzhen Sun** en
*"A Machine Learning Nowcasting Method based on Real-time Reanalysis
Data"*, intentamos replicar sus resultados usando los datos de rayos que tenemos.

## Descripción

La primer parte del algoritmo busca las etiquetas usando los datos del radar. 
El archivo de etiqueta es una `Grid` de PyART que vale 1 cuando el valor de reflectividad está
por encima de 35dBZ y 0 cuando está por debajo.



