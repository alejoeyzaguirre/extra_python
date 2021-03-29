#!/usr/bin/env python
# coding: utf-8

# # Actividad Práctica 04: 
# # Análisis Exploratorio de Datos

# **José Alejo Eyzaguirre**
# 
# Me aparecieron ciertos errores en el código, pero que me permitían correr y seguir. No los pesqué y seguí nomas.

# In[136]:


import numpy as np
import pandas as pd
from IPython.display import display 
import matplotlib.pyplot as plt


# ## Misión 1: Completando Información
# 
# En la siguiente etapa debo más que nada hacer la pega de Limpieza y Depuración de Datos. Para ello debo inicialmente importar la base de datos y de pasada convertirla en un DataFrame.

# In[2]:


data = pd.read_csv('/Users/alejoeyzaguirre/P.C.H/penguins.csv', sep = ',')
data.head()


# Aprovecho rápidamente de observar un poco los datos que se tienen por columna, todo esto con el objetivo de familiarizarme con la base de datos.

# In[3]:


stats = data.describe()
stats.loc['var'] = data.var().tolist()
stats.loc['skew'] = data.skew().tolist()
stats.loc['kurt'] = data.kurtosis().tolist()

display(stats)


# Además aprovechamos de ver la dispersión de manera gráfica con gráficos de caja y bigote, para cada una de las variables cuantitativas que nos dan en la base de datos:
# 
# **1. Culmen Length (mm):**

# In[4]:


data.boxplot(column='culmen_length_mm', color = "blue", patch_artist = "False")
plt.show()

data['culmen_length_mm'].hist(bins=50, color = "green")
plt.show()


# **2. Culmen Depth (mm):**

# In[5]:


data.boxplot(column='culmen_depth_mm', color = "grey", patch_artist = "False")
plt.show()

data['culmen_depth_mm'].hist(bins=50, color = "tomato")
plt.show()


# **3.Flipper Length (mm):**

# In[6]:


data.boxplot(column='flipper_length_mm', color = "skyblue", patch_artist = "True")
plt.show()

data['flipper_length_mm'].hist(bins=50, color = "red")
plt.show()


# **4. Body Mass (g):**
# 
# 

# In[63]:


data.boxplot(column='body_mass_g', color = "green", patch_artist = "True")
plt.show()

data['body_mass_g'].hist(bins=50, color = "brown")
plt.show()


# Es interesante ver y entender mejor cada una de nuestras features. Por un lado tenemos, variables con comportamientos, que dentro de lo poco que se de pingüinos, al parecer se comportan de manera regular. Tanto en temas de dispersión como en temas de medias. Viendo los boxplots de cada variable cuantitativa, notamos que no existen outliers (valores fuera de los bigotes). Sin embargo tenemos distribuciones no muy bien comportadas (no normales), por lo que habrá que tener ojo al reemplazar los valores nulos.
# 
# Sobre las variables cualitativas, podemos ver lo siguiente:
# 
# **1. Especies:**

# In[8]:


data["species"].value_counts()


# **2. Isla:**

# In[9]:


data["island"].value_counts()


# **3. Sexo:**

# In[10]:


data["sex"].value_counts()


# Notamos que Sex tiene un dato malo! Lo cambiamos de inmediato.

# In[11]:


data = data.replace(".", np.nan)


# In[13]:


data["sex"].value_counts()


# Ya habiendo arreglado esa mala imputación procedemos!

# Habiendo realizado la importación, y este rápido análisis de las columnas de la base de datos, debo ahora contabilizar los datos vacíos de la base de datos. Para ello uso la función que se encuentra en la Materia de clases que permite contabilizar el número de datos vacíos por columna o feature.

# In[14]:


data.apply(lambda x: sum(x.isnull()),axis=0)


# ### Tratando Valores Vacíos (NaN):

# Habiendome ya familiarizado con los datos, puedo ahora proceder de manera más fácil a reemplazar los datos vacíos (NaN). Para ello notamos que se debe hacer este proceso de reemplazo con distintos criterios dependiendo de los tipos de variables y de sus características.
# 
# Cómo se vió en clases, se debe primero dividir la base de datos entre data de entrenamiento y data de validación. Por qué se debe hacer esto, porque para reemplazar los valores vacíos de la data de testeo, se debe antes tomar decisiones a partir de la data de entrenamiento. Ya que, como dijo el profesor Hans Löbel en clases: *Las decisiones de limpieza y depuración se hacen con la info del set de entrenamiento. El set de Testeo es víctima de las decisiones tomadas para el set de entrenamiento*.
# 
# Por ello procedemos en primer lugar a dividir la data de forma aleatoria en un set de entrenamiento y en uno de testeo, con el comando usado en la ayudantía.

# In[69]:


from sklearn.model_selection import train_test_split

train, test = train_test_split(data, test_size=0.3)


# In[70]:


train


# In[71]:


test


# Entonces analizamos ahora la data de entrenamiento, en especial los valores vacíos existentes en esa base.

# In[72]:


train.apply(lambda x: sum(x.isnull()),axis=0)


# In[73]:


test.apply(lambda x: sum(x.isnull()),axis=0)


# In[74]:


train.describe()


# Por lo tanto, lo que se hará es tomar un criterio de reemplazo de los datos que sea válido. Vamos revisando por columna, en orden:
# 
# **1. Culmen Length (mm):**
# 
# Si notamos esta variable, tiene un comportamiento bastante bien distribuido. Bastante centrado y con estadísticos bastante bien comportados (dada la ausencia de outliers). El histograma muestra que los datos, están bastante centrados, pero no distribuyen normal... sino que una especie de distribución con dos jorobas no muy agradable de apreciar. Por estar razones, pese a que se cree que es el camino fácil pero no lo es, y dado que son pocos los datos vacíos se rellenará los datos vacíos con la media de esta columna.

# In[75]:


train.boxplot(column='culmen_length_mm', color = "blue", patch_artist = "False")
plt.show()

train['culmen_length_mm'].hist(bins=50, color = "green")
plt.show()


# In[76]:


media = train['culmen_length_mm'].mean()
train['culmen_length_mm'].fillna(media.round(1), inplace = True)


# Después de haber hecho el reemplazo, notamos con el cuadro siguiente que la media no cambio (obviamente) pero la desviación estándar sí cambió. Si bien el cambio es leve, son estos los impacto que hay que reducir a la hora de imputar valores faltantes.

# In[77]:


train.describe()


# In[78]:


train.apply(lambda x: sum(x.isnull()),axis=0)


# En lo siguiente se hará el reemplazo de los datos vacíos en el set de testeo, según lo visto en clases, cito nuevamente al profesor Hans: *Las decisiones de limpieza y depuración se hacen con la info del set de entrenamiento. El set de Testeo es víctima de las decisiones tomadas para el set de entrenamiento*. 
# 
# Además pregunté en el Foro Discord (en el Canal *Dudas de Enunciado* del Lab 04), que si al reemplazar con la media, en alguna columna, debía reemplazar en el set de testeo con la media de la columna respectiva de solo el test de entrenamiento, y el profesor me respondió: "Exacto". 
# 
# Digo todo esto, porque al conversar con compañeros, nadie estaba tan al tanto de este "detalle". De hecho publiqué una Issue sobre el tema, y lamentablemente no me la pudieron responder. Así que, si esto no es correcto, lo tomo como supuesto (supongo que de manera válida) para las demás imputaciones de valores.  

# In[79]:


test.head()


# In[80]:


# Rellenamos con la media de la columna de la data de entrenamiento.
test['culmen_length_mm'].fillna(media.round(1), inplace = True)


# Notamos que efectivamente se eliminó el dato vacío.

# In[82]:


test.apply(lambda x: sum(x.isnull()),axis=0)


# **2. Culmen Depth (mm):**
# 
# Al igual que la primera variable, esta también tiene un comportamiento bastante bien distribuido según sus estadístcos y gráficos de caja-bigote e histograma, en la data de Entrenamiento. Si bien la distribución, no es muy normal, se cree que es una buena estrategia reemplazar nuevamente los valores vacíos por la media de la columna. Esta decisión se da porque la media es parecida a la mediana (por la ausencia de outliers) y porque no tiene sentido calibrar un modelo de regresión lineal, que prediga el valor, ya que son pocos los datos vacíos a rellenar en esta columna.

# In[83]:


train.boxplot(column='culmen_depth_mm', color = "tomato", patch_artist = "False")
plt.show()

train['culmen_depth_mm'].hist(bins=50, color = "skyblue")
plt.show()


# In[84]:


media = train['culmen_depth_mm'].mean()
train['culmen_depth_mm'].fillna(media.round(1), inplace = True)


# Procedemos a rellenar los datos vacíos de esta columna entonces, con la media del set de entrenamiento.

# In[85]:


train.apply(lambda x: sum(x.isnull()),axis=0)


# In[86]:


train.describe()


# Nuevamente notamos que la media de esta variable obviamente se mantiene constante y que la desviación estándar, SÍ cambia.
# 
# Procedemos a hacer el mismo ajuste a la data de testeo:

# In[88]:


test.head()


# In[90]:


test.apply(lambda x: sum(x.isnull()),axis=0)


# **3. Sex:**
# 
# Se modifica esta variable primero, porque se quiere tener esta variable arreglada para después poder imputar los valroes de Flipper Length. Primero observemos como se comporta esta variable:

# In[91]:


train["sex"].value_counts()


# Notamos que si bien la moda es Female, solo hay un pigüino de diferencia, por lo que no sería prudente reemplazar los datos vacíos con la moda de esta variable. Además notamos que hay un dato que corresponde a un punto, procedemos a reemplazar este dato por un NaN.

# In[92]:


train["sex"].value_counts()


# In[ ]:


train["sex"].fillna(method ='bfill', inplace = True) 


# Notamos que ya se corrigió este error en los datos. Ahora podemos seguir imputando los valores correspondientes para los valores faltantes. Lo que se hace es rellenar los datos con el comando interpolate, este permite

# In[94]:


train.apply(lambda x: sum(x.isnull()),axis=0)


# In[95]:


train["sex"].value_counts()


# Notamos que si bien cambió levemente la proporción de sexo de los pingüinos, este cambio no fue muy dramático. Esperemos que sea acorde, este reemplazo, por lo menos en temas de proporciones, no fue tan invasivo en la data de entrenamiento.
# 
# Ahora rellenamos la data de testeo con el mismo método.

# In[96]:


test["sex"].fillna(method ='bfill', inplace = True) 


# In[97]:


test.apply(lambda x: sum(x.isnull()),axis=0)


# **4. Flipper Length (mm):**
# 
# Esta variable es distinta a las demás. Los datos vacíos son más numerosos, por lo que vale la pena hacer un relleno un poco más complejo. El que propongo es hacer un relleno por media, según raza y según sexo. Esto tiene sentido al revisar el siguiente gráfico de boxplots.
# 
# Para esto es necesario usar la función `fage` vista en la materia de clases.

# In[98]:


train.boxplot(column='flipper_length_mm', by = ['species','sex'], rot = 90, color = "Tomato", figsize = (10,10))


# In[99]:


tabla = train.pivot_table(values='flipper_length_mm', index='species' ,columns='sex', aggfunc=np.median)
tabla


# In[100]:


def fage(x):
    return tabla.loc[x['species'],x['sex']]

train[train['flipper_length_mm'].isnull()].apply(fage, axis=1)


# In[ ]:


train['flipper_length_mm'].fillna(train[train['flipper_length_mm'].isnull()].apply(fage, axis=1), inplace=True)


# In[102]:


train.apply(lambda x: sum(x.isnull()),axis=0)


# Ahora debemos rellenar la data de Testeo con esta información. Me hubiese encantado rellenar con estas mismas medias calculadas para la data de entrenamiento. Sin embargo, no supe como hacerlo así que mil perdones pero tendré que rellenar con las medias correspondientes al set de entrenamiento : (.

# In[105]:


tablo = test.pivot_table(values='flipper_length_mm', index='species' ,columns='sex', aggfunc=np.median)
tablo


# In[106]:


def fago(x):
    return tablo.loc[x['species'],x['sex']]

test[test['flipper_length_mm'].isnull()].apply(fago, axis=1)


# In[ ]:


test['flipper_length_mm'].fillna(test[test['flipper_length_mm'].isnull()].apply(fago, axis=1), inplace=True)


# In[108]:


test.apply(lambda x: sum(x.isnull()),axis=0)


# **Body Mass (g):**
# 
# La siguiente columna, al tener pocos NaN (solo 2) y ser dentro de bien comportada, su distribución es ligeramente más normal que las otras variables. Por lo que basta con rellenar con la media en ambos sets entrenamiento y validación.

# In[109]:


media = train['body_mass_g'].mean()
train['body_mass_g'].fillna(media.round(1), inplace = True)


# In[110]:


train.apply(lambda x: sum(x.isnull()),axis=0)


# Ahora con el set de entrenamiento (no es necesario, porque no hay observaciones nulas en esta columna en este set), pero el código sería el siguiente:

# In[111]:


test['body_mass_g'].fillna(media.round(1), inplace = True)


# In[112]:


test.apply(lambda x: sum(x.isnull()),axis=0)


# Podemos ver que finalmente, se limpiaron todos los datos vacíos de la base de datos. Ahora podemos prodecer a la siguiente misión.

# ## Misión 2: Predicción de la Especie
# 
# Ya con los datos completos, su objetivo construir modelos que permitan predecir la especie de un pingüino dadas sus características. En particular, deberá evaluar dos posibles estrategias para construir modelos:

# ### Predicción Tradicional:
# 
# Se debe dividir la data en data del tipo X e y, donde y será la Especie (columna `species`) y las demás formarán parte de los X. También es importante hacer que todas las variables cualitativas pasen a ser cualitativas. Siguiendo los pasos de la ayudantía y lo hecho en clases, entonces, se hace lo siguiente:
# 
# Partamos por ajustar las variables cualitativas a cuantitativas.

# In[ ]:


from sklearn.preprocessing import LabelEncoder

var_mod = ['species','island','sex']
le = LabelEncoder()
for i in var_mod:
    train[i] = le.fit_transform(train[i])


# In[ ]:


train.drop("Unnamed: 0", axis = 1, inplace = True )


# In[118]:


train.head()


# In[ ]:


var_mod = ['species','island','sex']
le = LabelEncoder()
for i in var_mod:
    test[i] = le.fit_transform(test[i])


# In[ ]:


test.drop("Unnamed: 0", axis = 1, inplace = True )


# In[120]:


test.head()


# Ahora definimos nustros X y nuestro y, para el set de entrenamiento y para el de validación.

# In[121]:


X_train = train.drop('species', axis=1)


# In[126]:


y_train = train['species']


# In[128]:


display(X_train)


# In[127]:


display(y_train)


# Procedemos a hacer lo mismo con nuestro set de Testeo.

# In[129]:


X_test = test.drop('species', axis=1)


# In[130]:


y_test = test["species"]


# In[131]:


display(X_test)


# In[132]:


display(y_test)


# **Empezamos ahora a usar los modelos como se vió en la ayudantía**. 
# 
# En la ayudantía no se usó un set de validación, por lo que acá tampoco. No es la idea comparar modelos, sino que mostrar distintos modelos que sirvas (Regresión lineal obviamente no sirve) y ver el rendimiento de cada uno. Es importante tener en cuenta que no porque un modelo tenga mejor rendimiento en el set de testeo será mejor. Para decir eso, es más correcto, evaluar los distintos modelos en un set de validación (una parte del set de train) y ver cual se desempeña mejor. Teniendo el mejor modelo en mano, procedo a evaluar el ganador con el set de Testeo.
# 
# ### KNN:
# 
# Este modelo tiene un 76% de desempeño.

# In[133]:


from sklearn import datasets, metrics, neighbors, decomposition, manifold

knn = neighbors.KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)
predicted = knn.predict(X_test)


# In[134]:


print("Accuracy: %s" % metrics.balanced_accuracy_score(y_test, predicted))


# ### Support Vector Machine (SVM):
# 
# Veamos como funciona, notamos que la accuracy cayó...! Nuevamente no podemos concluir que conviene usar KNN, porque no fuimos rigurosos al no definir el Validation Set. Seleccionamos el kernel, `rbf`, ya que creo que será mejor que polimomial o lineal.

# In[137]:


from sklearn.svm import SVC

svm = SVC(kernel='rbf') 
svm.fit(X_train, y_train)
predicted = svm.predict(X_test)

print("Accuracy: %s" % metrics.accuracy_score(y_test, predicted))
print("Balanced accuracy: %s" % metrics.balanced_accuracy_score(y_test, predicted))


# ### Red Neuronal:
# 
# La verdad es que es el que más fe le tengo. Veamos como le va, con 115 nodos escondidos. Sin embargo, no fue mejor que el KNN. 

# In[171]:


from sklearn.neural_network import MLPClassifier

mlp = MLPClassifier(hidden_layer_sizes=(115,), max_iter=10000) # 10
mlp.fit(X_train, y_train)
predicted = mlp.predict(X_test)

print("Accuracy: %s" % metrics.balanced_accuracy_score(y_test, predicted))


# ### Predicción Jerárquica:
# 
# Primero debo definir una columna que se llamará "Adelie". En esta todas las variables serán 0 salvo si la observación corresponde a esta misma especie. De esta forma es más posible lograr el famoso *One versus All* que nos piden. La columna 0 corresponde, a la Dummy Adelie. 

# In[175]:


dummies = pd.get_dummies(train["species"])


# In[176]:


train2 = pd.concat([train, dummies], axis = 1)


# In[177]:


train2


# In[181]:


train2.drop(1, axis = 1, inplace = True )


# In[ ]:


train2.drop(2, axis = 1, inplace = True )


# In[187]:


train2.drop("species", axis = 1, inplace = True )


# In[188]:


train2


# Hacemos lo mismo con la data de Testeo.

# In[180]:


dummy = pd.get_dummies(test["species"])
test2 = pd.concat([test, dummy], axis = 1)
test2


# Ahora debemos asignar a partir de cada set los X e y respectivos.

# In[185]:


test2.drop(1, axis = 1, inplace = True )
test2.drop(2, axis = 1, inplace = True )
test2


# In[186]:


test2.drop("species", axis = 1, inplace = True )


# Creamos ahora los X_train, y_train, X_test e y_test.

# In[189]:


X_train2 = train2.drop(0, axis=1)


# In[190]:


y_train2 = train2[0]


# In[191]:


X_test2 = test2.drop(0, axis = 1)


# In[192]:


y_test2 = test2[0]


# In[193]:


X_test2


# ### Creación de Modelos:
# 
# **1. Regresión Logística:**
# 
# Primero partimos con un modelo de Regresión Logística. Tiene un rendimiento bastante bueno! 99%

# In[195]:


from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train2,y_train2)
predictions = model.predict(X_test2)
accuracy = metrics.accuracy_score(y_test2, predictions)    
print("Rendimiento : %s" % "{0:.3%}".format(accuracy))


# **2. Red Neuronal:**
# 
# Veamos como nos va con este modelo. Tiene un 72% de Accuracy. Esto es bueno, pero llama más la atención la efectividad de la regresión logística.

# In[196]:


from sklearn.neural_network import MLPClassifier

mlp = MLPClassifier(hidden_layer_sizes=(115,), max_iter=10000) # 10
mlp.fit(X_train2, y_train2)
predicted = mlp.predict(X_test2)

print("Accuracy: %s" % metrics.balanced_accuracy_score(y_test2, predicted))


# ### Paso 2 de la Misión:
# 
# En este paso se eliminarán de Train y de Test todas las observaciones que sean de la especie Adelaide. Ahora nos quedamos en nuestra data con una columna, que será nuestro y que es 1 si es de la especie "Gentoo" y 0 si es "Chinstrar".

# In[218]:


train3 = train[train.species != 0] 


# In[219]:


train3


# Siguiendo los mismos pasos que antes, creo ahora una columna dummies para la especie. 

# In[220]:


dummies = pd.get_dummies(train3["species"])


# In[221]:


train4 = pd.concat([train3, dummies], axis = 1)


# In[222]:


train4


# In[225]:


train4 = train4.drop("species", axis = 1)


# In[ ]:


train4 = train4.drop(2, axis = 1)


# In[228]:


train4


# Hago lo mismo con mi data de Testeo.

# In[232]:


test3 = test[test.species != 0] 


# In[233]:


test3


# In[234]:


dummy = pd.get_dummies(test3["species"])


# In[235]:


test4 = pd.concat([test3, dummy], axis = 1)


# In[236]:


test4


# In[237]:


test4 = test4.drop("species", axis = 1)


# In[238]:


test4 = test4.drop(2, axis = 1)


# In[239]:


test4


# In[240]:


X_train4 = train4.drop(1,axis=1)


# In[241]:


y_train4 = train4[1]


# In[242]:


X_test4 = test4.drop(1,axis=1)


# In[243]:


y_test4 = test4[1]


# ### Creación de Modelos:
# 
# **Regresión Logística:**
# 
# Veamos como nos va: Upaa tenemos un rendimiento buenísimo, de 100%! Nuestro modelo esta muy bueno.

# In[244]:


from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train4,y_train4)
predictions = model.predict(X_test4)
accuracy = metrics.accuracy_score(y_test4, predictions)    
print("Rendimiento : %s" % "{0:.3%}".format(accuracy))


# **Red Neuronal:**
# 
# Veamos como nos va con 115 hidden layers. Rendimiento de 50%. Peor que regresión logística.

# In[245]:


from sklearn.neural_network import MLPClassifier

mlp = MLPClassifier(hidden_layer_sizes=(115,), max_iter=10000) # 10
mlp.fit(X_train4, y_train4)
predicted = mlp.predict(X_test4)

print("Accuracy: %s" % metrics.balanced_accuracy_score(y_test4, predicted))


# In[ ]:




