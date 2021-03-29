#!/usr/bin/env python
# coding: utf-8

# # Actividad Práctica 03:
# 
# José Alejo Eyzaguirre

# In[66]:


import sqlite3


# In[67]:


conexion = sqlite3.connect('nba.sqlite')

cursorx = conexion.cursor()


# ## MISIÓN 1: SQL
# 
# En los siguientes cuadros, se procede a definir la consulta inicial. En esta se trató de desagregar el problema en distintos pequeños problemas. De esta forma se pudo dividir primero el problema de agrupar los jugadores por equipo y luego por edad en orden descendiente, para ello se utilizó la siguiente consulta:
# 

# In[79]:


sql_statement = 'SELECT * FROM (SELECT player,team,age, fouls FROM Stats S ORDER by age DESC) S order BY S.team'

cursorx.execute(sql_statement)

conexion.commit()

cursorx.fetchall()


# Luego llegué a un punto insuperable de como poder filtrar a los 5 jugadores más viejos por equipo, tanto así que publiqué mi primera issue para obtener la respuesta... buscando en internet encontré por mi cuenta el siguiente link http://www.silota.com/docs/recipes/sql-top-n-group.html que la verdad me vino como anillo al dedo. Aplicando el código a nuestra base de datos pude obtener lo que se pedía. Sin embargo, en un computador en particular (MAC) no me funcionó el código, pero después de probar varias veces, utilicé otro computador (Windows) y el programa me corrió perfectamente, por si no les funciona, prueben con otro computador :).

# In[77]:


sql_statement = '''SELECT team, SUM(fouls) AS FALTAS 
FROM 
(SELECT player, age, team, fouls, ROW_NUMBER() OVER (PARTITION BY team ORDER BY age DESC) AS ranking_edad
FROM Stats) R 
WHERE R.ranking_edad <= 5 
GROUP BY team 
ORDER BY FALTAS DESC LIMIT 5'''

cursorx.execute(sql_statement)

conexion.commit()


# In[70]:


cursorx.fetchall()


# ## MISIÓN 1: PYTHON
# 
# Esta misma pregunta quise responderla con Python, dado que la entendí bastante bien, dado que me la estuve cabeceando bastante rato... Para extraer los datos iniciales que voy a usar utilizo una consulta de SQL.

# In[110]:


import collections


# In[106]:


datos = cursorx.execute("SELECT * FROM Stats")


# In[107]:


data = []

for elem in datos.fetchall():
    data.append(elem)

#print(data)


# Solo importo los datos de la tabla Stats porque solo tengo que usar esos...! Primero creo un diccionario con cada uno de los equipos.

# In[144]:


diccionario = {}

for i in range(len(data)):
    diccionario[data[i][4]] = 0
    
#print(diccionario)  

diccionario2 = diccionario


# Luego agrego a mi diccionario con llave el equipo, una lista de tuplas compuesta cada una por la edad y por los fouls cometidos por cada jugador.

# In[169]:


from operator import itemgetter

for i in diccionario.keys():
    equipo = i   
    jugadores_ordenados = []
    
    for j in range(len(data)):
        if data[j][4] == equipo:
            edad = int(data[j][3])
            fouls = int(data[j][14])
            jugadores_ordenados.append([edad, fouls])
    
    #print(jugadores_ordenados)
    #print(jugadores_ordenados[0][1]+jugadores_ordenados[1][1])
            
    ordenada = sorted(jugadores_ordenados, key=itemgetter(0), reverse = True)
    
    diccionario[equipo] = ordenada
    
    fouls_totales_viejos = 0
    
    for i in range(len(ordenada)):
        if i <5:
            fouls_totales_viejos += ordenada[i][1]

    diccionario2[equipo] = fouls_totales_viejos
    
    
    
            
            
        
            
#print(diccionario)
#print(diccionario2)


# Ahora tengo en mi diccionario2, un dict que tiene por llaves los equipos y valores los fouls cometidos por los 5 jugadores más viejos de cada equipo.

# Ahora solo me falta seleccionar los 5 equipos con viejos fouleros.

# In[170]:


lista_final = []

for elem in diccionario2.keys():
    lista_final.append([elem, diccionario2[elem]])

    
orden = sorted(lista_final, key=itemgetter(1), reverse = True)
#print(orden)

for elem in range(5):
    equipo = orden[elem][0]
    fouls = orden[elem][1]
    print(equipo, fouls)


# In[ ]:


conexion.close()

