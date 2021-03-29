#!/usr/bin/env python
# coding: utf-8

# # Laboratorio 04:
# ## Pandas, Scikit Learn
# 
# **José Alejo Eyzaguirre**

# In[1]:


import numpy as np
import pandas as pd
from IPython.display import display 
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import datasets, metrics, neighbors, decomposition, manifold
from sklearn.preprocessing import LabelEncoder


# In[2]:


pwd


# ## Misión 1: Conociendo e importando los Datos
# 
# En la siguiente misión la idea es familiarizarse con las bases de datos a trabajar. Para esto primero se visualizó cada una de ellas en su formato CSV. Luego se importó cada una de estas y se comenzó a mirar con *ojo crítico* los datos, con especial detalle en el nombre de las columnas. 
# 
# El gran desafío para esta misión, a mi gusto, fue seleccionar las 10 variables a presentar con sus respectivos estadísticos. La razón de esto, radica en que si bien yo estudio Ingeniería Comercial, y he tenido varios ramos de Finanzas, nunca me ha ido muy bien en esos ramos, por lo que me costó mucho seleccionar que variables serían importantes para las misiones próximas. Sin embargo, intenté hacer lo mejor y repasando mis cuadernos de esos cursos, seleccioné inicialmente un gran grupo de variables que me parecieron importantes, para luego quedarme con solo 10 de estas columnas *preseleccionadas*.
# 
# 

# Las variables preseleccionadas fueron las siguientes:
# 
# y = Retorno (Price VAR [%]) o Class
# 
# X = 
# Revenue \
# Operating Income - Operating Expenses \
# EBIT: Earnings before interest and taxes\
# ROE \
# Dividends per share  \
# Property Plants & equipment  \
# EPS Diluted \
# Goodwill and Intangible Assets  \
# Long-Term investments  \
# Free Cash Flow \
# Short Term Debt  \
# Long Term Debt  \
# Total Shareholders Equity  \
# Retained Earnings  \
# Investments  \
# Operating Cash Flow  \
# Price book value ratio  \
# PriceToSalesRatio  \
# returnOnAssets  \
# returnOnEquity  \
# returnOnCapitalEmployed  \
# debtRatio  \
# debtEquityRatio  \
# Revenue per Share  \
# Operating Cash Flow per Share \
# Net Income per Share  \
# Shareholders Equity per Share  \
# Market Cap  \
# Enterprise Value  \
# Net Current Asset Value  \
# ROE  \
# Debt Growth  \
# Asset Growth  \
# Sector (Variable Cualitativa)  \
# Graham Number (Valor razonable de una acción) \
# 
# Como en futuras misiones se pide, evaluar que acción es la más conveniente de comprar, se intentó dividir desde ya (aprovechando el proceso de familiarización) las distintas variables entre las independientes o **features** y la variable de interés, que en este caso es el Retorno. Si bien me hubiera encantado, encontrar alguna forma de calcular el **Sharpe Ratio** de alguna de estas acciones (usando alguna medida de la volatilidad de la acción), no pude encontrar alguna forma de armar este índice. Sin embargo, suponiendo que los agentes que asesoramos son neutrales al riesgo, podría ser una buena métrica para un inversionista común, de que acción conviene más comprar o no, el Retorno por sí solo.
# 
# Sin embargo, es importante recalcar, que acciones que a veces tienen un mayor Retorno a veces lo tienen a costa de que la empresa, a la cual pertenece la acción, se esta exponiendo a mucho riesgo o el mercado en el cual opera tiene una volatilidad muy grande. Por esta razón, es importante suponer que la recomendación futura se hace a un individuo neutral al riesgo, que solo busca un mayor retorno, no el "mayor retorno, más seguro".

# En los siguientes cuadros de código, se importa cada una de las bases de datos, con su respectivo separador. Luego se hace una previsualización de cada unos de estos, con los comandos `head()` y `tail()`.

# In[3]:


data_2014 = pd.read_csv('/Users/alejoeyzaguirre/P.C.H/financial_data/2014_Financial_Data.csv', sep = ',')
data_2014.head()


# Para hacer la preselección de las variables, fue necesario revisar lo que significaba cada una de ellas. Gracias a que los nombres de estas estaban bastante claros, este proceso no implicó revisar los manuales de explicación de las bases de datos en la web.

# In[4]:


for i in data_2014.columns:
    print(i)


# Por defecto, pandas solo muestra un número reducido de columnas, para poder ver todas estas se utiliza el siguiente código. De esta forma podemos familirizarnos con los datos, en el mismo Jupyter Notebook, sin tener que recurrir a otros servidores.
# 

# In[5]:


pd.set_option('display.max_columns', None)
data_2014.head()


# In[6]:


data_2015 = pd.read_csv('/Users/alejoeyzaguirre/P.C.H/financial_data/2015_Financial_Data.csv', sep = ',')
data_2015.tail()


# In[7]:


data_2016 = pd.read_csv('/Users/alejoeyzaguirre/P.C.H/financial_data/2016_Financial_Data.csv', sep = ',')
data_2016.head()


# In[8]:


data_2017 = pd.read_csv('/Users/alejoeyzaguirre/P.C.H/financial_data/2017_Financial_Data.csv', sep = ',')
data_2017.head()


# In[9]:


data_2018 = pd.read_csv('/Users/alejoeyzaguirre/P.C.H/financial_data/2018_Financial_Data.csv', sep = ',')
data_2018.head()


# ## Estadísticos:
# 
# Luego de esta previsualización, de las distintas bases *Financial Data* de cada año, se empieza a estudiar los estadísticos de solo 10 de todas las variables entregadas. Para ello fue necesario seleccionar a partir de las variables preseleccionadas a 10 de estas, que me parecieron importantes y útiles para futuras misiones. Las seleccionadas son las siguientes:
# 
# 1. PRICE VAR [%] (Retorno)
# 2. Free Cash Flow
# 3. Goodwill and Intangible Assets
# 4. Dividend per Share
# 5. Debt Equity Ratio
# 6. Market Capitalization
# 7. Class
# 8. Sector
# 9. ROE
# 10. Price Book Value Ratio
# 
# Estas variables fueron seleccionadas a partir de lo aprendido en cursos de Finanzas. Las variable 5 fue seleccionada como proxy del riesgo de la firma a la cual la acción corresponde. Las variables 2, 3, 4, 6, 9 y 10 fueron seleccionadas como reflejo de la "calidad" de las empresas de cada acción.
# 
# En particular las variables 6 y 10, son importantes de agregar porque existe un estudio famoso de Fama, French y Carhart (del cual nace el famoso modelo de Asset Pricing Theory de Fama, French & Carhart), que demuestra el efecto sobre el retorno esperado de las acciones de estas dos variables (Factor HML y factor SMB). Hubiera sido ideal tener alguna variable que represente el retorno del Mercado ponderado por las respectivas capitalizaciones, para así tener una feature que represente el factor de Mercado (central en el Capital Asset Pricing Model o más famosamente llamado CAPM), si bien podemos armar esta variable se dejará esta pega para más adelante.
# 
# El Free Cash Flow, es importante de agregarlo dado que a partir de este se puede obtener el EBITDA, y además esta variable permite valorizar acciones como también es una forma de controlar por la liquidez de la empresa (que se ha demostrado tener efectos sobre el retorno esperado). Lo mismo ocurre con los Dividendos por acción, según el Modelo de Gordon, se pueden valorizar acciones a partir del Valor Presente de los Dividendos a repartir por acción.
# 
# La variables primera, es considerada como la variable de estudio (por lo pedido en la Misión 5). Se cree que esta variable resume bastante bien, lo que le podría interesar a un inversionista para comprar en el futuro. Además la variable 7, puede ser también considerada como una variable de estudio (como se pide en la Misión 4), ya que esta dummy señala si las acciones son convenientes de comprar o no.

# En los siguientes cuadros se hace el análisis por cada año, de los estadísticos de cada una de las 10 variables. Sin embargo, los comentarios exigidos se harán sobre los estadísticos de las columnas de la base de datos "mergeada" con la data de entrenamiento agrupada en un solo Data Frame.

# ### Año 2014
# 
# 

# In[10]:


#[["EPS Diluted", "EBIT", "Goodwill and Intangible Assets", "Short-term debt", "debtEquityRatio", "Market Cap", "returnOnEquity", "Sector", "ROE", "priceBookValueRatio"]]

data_2014[["2015 PRICE VAR [%]", "Free Cash Flow", "Goodwill and Intangible Assets", "Dividend per Share",            "debtEquityRatio", "Market Cap", "Class", "ROE",             "priceBookValueRatio"]].describe()


# In[11]:


data_2014["Sector"].value_counts()


# ### Año 2015

# In[12]:


data_2015[["2016 PRICE VAR [%]", "Free Cash Flow", "Goodwill and Intangible Assets", "Dividend per Share",            "debtEquityRatio", "Market Cap", "Class", "ROE",             "priceBookValueRatio"]].describe()


# In[13]:


data_2015["Sector"].value_counts()


# ### Año 2016

# In[14]:


data_2016[["2017 PRICE VAR [%]", "Free Cash Flow", "Goodwill and Intangible Assets", "Dividend per Share",            "debtEquityRatio", "Market Cap", "Class", "ROE",             "priceBookValueRatio"]].describe()


# In[15]:


data_2016["Sector"].value_counts()


# ### Año 2017

# In[16]:


data_2017[["2018 PRICE VAR [%]", "Free Cash Flow", "Goodwill and Intangible Assets", "Dividend per Share",            "debtEquityRatio", "Market Cap", "Class", "ROE",             "priceBookValueRatio"]].describe()


# In[17]:


data_2017["Sector"].value_counts()


# ### Año 2018

# In[18]:


data_2018[["2019 PRICE VAR [%]", "Free Cash Flow", "Goodwill and Intangible Assets", "Dividend per Share",            "debtEquityRatio", "Market Cap", "Class", "ROE",             "priceBookValueRatio"]].describe()


# In[19]:


data_2018["Sector"].value_counts()


# ## Estadísticos importantes:
# 
# En la siguiente sección se hará un análisis de los estadísticos de las 10 variables elegidas para comentar, pero solo para la base de datos de entrenamient `Train Data`. Esta Data Frame corresponde a la base de datos de Entrenamiento, que consiste en un `Merge` de las filas de las bases de datos 2014 al 2017. No se hace un análisis de los estadísticos de la Data de Testeo (correspondiente a la del año 2018), porque por lo visto en clases, no se deben tomar decisiones a partir de la Data de Testeo, por lo que me pareció innecesario.
# 
# ### Data de Entrenamiento:
# 
# Primero se debe concatenar las bases de datos, para obtener el Data Frame de Entrenamiento:

# In[20]:


train_data = pd.concat([data_2014, data_2015, data_2016, data_2017])

train_data.shape


# Notamos que la Concatenación resultó bien. Sin embargo, las últimas columnas de "*Año* Price VAR [%]" hay que agruparlas en una sola, que refleje la variación del precio de la acción entre ese año y el anterior, es decir el Retorno de la acción, de ese año en particular. Además, de eso notamos que el índice ahora ya no nos sirve, tenemos índices repetidos. Esto se evidencia al ver el número de filas (17.685) y el índice final que tenemos (4956). Por ello antes que nada, debemos resetear el índice para así tener un índice, que sirve como identificador único de cada observación.

# In[21]:


train_data = train_data.reset_index(drop=True)


# Habiendo ya arreglado el problema del índice procedemos.
# 
# **EL SIGUIENTE PASO CORRESPONDE A UNA RESOLUCIÓN DE CONFLICTO QUE DEBERÍA SER REALIZADA EN LA MISIÓN 2**. Sin embargo, para poder realizar el análisis de la columna `Return` es necesario arreglarla ahora. Pero esta resolución de conflicto corresponde a la primera a realizar en la misión 2.
# 
# Para agruparlas de manera más rápida se reeemplaza primero todos los valores vacíos por un 0, y luego se suman las respectivas columnas. Entonces, para cada observación del año la columna `Retorno` será una suma de tres ceros más un valor que corresponde a la variación de esa acción, del año que corresponde. Sin embargo, este método no sería válido si tuviésemos acciones que no tienen un valor para su retorno. Por ello es necesario revisar si existen datos que tienen un *NaN* en su valor de Retorno.

# In[22]:


data_2014.apply(lambda x: sum(x.isnull()),axis=0).tail()


# In[23]:


data_2015.apply(lambda x: sum(x.isnull()),axis=0).tail()


# In[24]:


data_2016.apply(lambda x: sum(x.isnull()),axis=0).tail()


# In[25]:


data_2017.apply(lambda x: sum(x.isnull()),axis=0).tail()


# In[26]:


data_2018.apply(lambda x: sum(x.isnull()),axis=0).tail()


# Como se puede ver más arriba, no existen datos vacíos en ninguna base de datos en la variable *AÑO* PRICE VAR [%]. Por lo tanto, es válido, rellenar con ceros todos los datos vacíos y luego sumar las 4 columnas para obtener el retorno correspondiente a cada acción en el año respectivo que se representa en la base.
# 
# Entonces, reemplazo con cero los valores vacíos:

# In[27]:


#Reemplazo por ceros los NaN
for i in range(5, 9):
    string = "201{} PRICE VAR [%]".format(i)
    train_data[string].fillna(0, inplace = True)  


# Y ahora sumo las 4 columnas agrupándola en una sola columna que se llama `Return`.

# In[28]:


train_data["Return"] = train_data["2015 PRICE VAR [%]"] + train_data["2016 PRICE VAR [%]"] +                        train_data["2017 PRICE VAR [%]"] + train_data["2018 PRICE VAR [%]"] 

display(train_data['Return'].head())
display(train_data['Return'].tail())


# Revisamos ahora, que efectivamente la nueva columna `Retorno` tenga puramente valores No Nulos. Notando que es cierto.

# In[29]:


train_data.apply(lambda x: sum(x.isnull()),axis=0).tail()


# Notamos que la variable no tiene ningún dato del tipo *NaN*, por ende para cada acción de cada uno de los años de la data de entrenamiento tenemos un valor para su retorno.
# 
# 
# Habiendo realizado ya este trabajo previo podemos recién ahora estudiar con mayor detención los estadísticos de las 10 variables a estudiar, ya mencionadas más arriba.

# In[30]:


resumen = train_data[["Return", "Free Cash Flow", "Goodwill and Intangible Assets", "Dividend per Share",            "debtEquityRatio", "Market Cap", "Class", "ROE",             "priceBookValueRatio"]]

display(resumen.describe())


# En la siguiente tabla se muestran los mismos estadísticos que en la anterior pero se agregan además los segundo, tercero y cuarto momento de cada una de las 10 columnas seleccionadas. La verdad es nunca entendí bien, como usar estos estadísticos, así que no los usaré en el análisis. 
# 
# **LA SIGUIENTE TABLA ES LA QUE SE USA PARA HACER EL ANÁLISIS ESTADÍSTICO, DE LA SIGUIENTE SECCIÓN.**

# In[31]:


#Otros momentos

stats = resumen.describe()
stats.loc['var'] = resumen.var().tolist()
stats.loc['skew'] = resumen.skew().tolist()
stats.loc['kurt'] = resumen.kurtosis().tolist()

display(stats)


# ### Comentarios Estadísticos (10 variables)
# 
# Sobre las variables numéricas (todas menos Sector), se puede decir lo siguiente:
# 
# 1. **`Return`**: El retorno tiene un promedio bastante alto, que bordea el 331% de variación de precio entre un año y otro. Esto es bastante curioso, dado que es raro tener variaciones de precio tan fuertes para las distintas acciones, y por lo tanto es más raro aún que el promedio de los retornos sea así de alto. Al ver el valor máximo, podemos notar que es un outlier tremendo, rodeando un retorno porcentual de casi dos millones y medio.  Si bien esto puede ser cierto será interesante en la etapa de visualización de los datos estudiar la distribución de esta variable. Sin embargo, si nos adelantamos un poco podemos ver el siguiente gráfico de caja y bigote para esta variable, y un histograma.

# In[32]:


train_data.boxplot(column='Return', color = "blue", patch_artist = "False")
plt.show()

train_data['Return'].hist(bins=10, color = "blue")
plt.show()


# - Después de ver estos gráficos queda, en cierto sentido, demostrado que unos cuantos valores que se escapan de la distribución, deben ser culpables de el promedio sesgado de esta variable `Return`. Datos como la desviación estándar (bastante grande) y los cuartiles (visualizados en el Caja-Bigote) soportan también esta teoría. 
# 
# 
# 2. **`Free Cash Flow`**: Nuevamente observamos un promedio bastante alto que bordea los 440 millones. Esto puede ser más realista, y al observar los valores de los cuartiles, notamos que esta variable tiene un recorrido bastante ampliio. En el Caja Bigote y el Histograma ilustrados podemos observar más atentamente lo dicho anteriormente.

# In[33]:


train_data.boxplot(column='Free Cash Flow', color = "red", patch_artist = "True")
plt.show()

train_data['Free Cash Flow'].hist(bins=10, color = "red")
plt.show()


# - Viendo el caja bigote podemos notar que hay outliers notorios, especialmente en los valores inferiores de esta columna. Además la desviación estándar, por el recorrido amplio de esta variable, es bastante alta. 
# 
# 3. **`Goodwill and Intangible Assets`**: Notamos que el mínimo de esta columna es coherente (no existe Goodwill negativo). Era de esperar que esta variable tuviera también un amplio recorrido, lo cual se refleja en sus cuartiles y en su media bastante grande, que supera los 1000 millones. La distribución se puede ver mejor en el siguiente caja bigote e histograma:

# In[34]:


train_data.boxplot(column='Goodwill and Intangible Assets', color = "tomato", patch_artist = "True")
plt.show()

train_data['Goodwill and Intangible Assets'].hist(bins=10, color = "tomato")
plt.show()


# - Se puede ver claramente como existen valores que se escapan fuertemente de la caja (un bigote bastante largo). Nuevamente una desviación estándar bastante alta soporta esta teoría de alta dispersión de las variables.
# 
# 4. **`Dividend per Share`**: Al fin logramos observar distribuciones con valores menos abultados. Tenemos una media de 15.676 y un caja bigote e histograma, que ilustran la distribución de la variable, que se ve en el siguiente cuadro:

# In[35]:


train_data.boxplot(column='Dividend per Share', color = "salmon", patch_artist = "True")
plt.show()

train_data['Dividend per Share'].hist(bins=10, color = "salmon")
plt.show()


# - Sin embargo aún no nos libramos de los outliers... estos deberán ser tratados en las misiones futuras. En este caso es brutal como una sola acción hace que nuestro caja bigote nuevamente se vea totalmente comprimido a la parte inferior del cuadro graficado. Este outlier es también culpable de una desviación estándar, completamente desproporcional a lo que realmente debiera ser, si ese dato se omitiese.
# 
# 5. **`Debt Equity Ratio`**: Al trabajar con una razón o fracción entre la deuda y el patrimonio, no se debieran ver medias muy lejanas a un valor entre 0 y 1. El momento de la media, es coherente con esto y los distintos cuartiles también soportan esta teoría, con una mediana y media cercanas a 0,5. El caja bigote e histograma, para esta variable es el siguiente:

# In[36]:


train_data.boxplot(column='debtEquityRatio', color = "green", patch_artist = "True")
plt.show()

train_data['debtEquityRatio'].hist(bins=10, color = "green")
plt.show()


# - Nuevamente notamos el mismo problema, outliers fuertemente distanciados, y en este caso hacia arriba y también hacia abajo (abultando la desviación estándar). Claramente los outliers tendrán que ser tratados en la fase de limpieza y depuración de los datos.
# 
# 6. **`Market Capitalization`**: Esta variable es de esperar que tenga mucha dispersión y que este afectada por outliers que muevan la aguja en los distintos momentos. La media para esta variable supera los 10.000 millones y notamos que existe una gran desviación estándar, con la caja entre los 100 y 1000 millones de dólares. La media es lejana a la mediana. 
# 
# - Además el mínimo es coherente, encontrándose este en el cero. La desviación estándar es realmente tremenda. El tema de la dispersión de los datos se puede entender mejor en el siguiente Caja-Bigote e histograma:

# In[37]:


train_data.boxplot(column='Market Cap', color = "skyblue", patch_artist = "True")
plt.show()

train_data['Market Cap'].hist(bins=10, color = "skyblue")
plt.show()


# - Nuevamente notamos que tenemos un outlier que se escapa del resto de los datos hacia arriba (no pueden escaparse hacia abajo, porque esta limitado por el cero). La desviación estándar es así de tremenda, nuevamente por la presencia de outliers.
# 
# 7. **`Class`**: Al ser esta una variable dicotómica, no tenemos problemas de Outliers. Al observar la media podemos notar que existen más acciones convenientes de comprar que no convenientes, pero no por mucha diferencia (la media es de 0.515). Notamos además que los valores de esta columna dicotómica son coherentes, teniendo como máximo a 1 y mínimo a 0. 
# 
# - Para esta variable no tiene sentido graficar un boxplot, ya que la dispersión de los datos entre una opción u otra no se visualiza. En este caso se hace solo un histograma para entender mejor la dispersión.

# In[38]:


train_data['Class'].hist(bins=2, color = "skyblue")
plt.show()


# - La siguiente tabla también es bastante útil ya que, al igual que el histograma, nos muestra que efectivamente hay más acciones convenientes de comprar que menos, en nuestra data de entrenamiento. Más abajo en la descripción de la Variable `Sector` se hace una tabla dinámica interesante que involucra esta variable `Class`.

# In[39]:


train_data["Class"].value_counts()


# 8. **`ROE`**: Esta variable tiene un recorrido menos amplio que la gran mayoría de las otras. Sin embargo, el hecho de que la media se distancia de la mediana, es signo de que esta columna también esta contaminada por outliers, que deberán ser tratados en la Misión 2. El siguiente Caja-Bigote y el Histograma Rosado, es fiel reflejo de la dispersión contaminada de los datos:

# In[40]:


train_data.boxplot(column='ROE', color = "pink", patch_artist = "True")
plt.show()

train_data['ROE'].hist(bins=10, color = "pink")
plt.show()


# - Notamos que nuevamente tenemos outliers hacia arriba, con 4 que se escapan bastante de la caja y del bigote. Nuevamente esta contaminación de los outliers tiene las mismas consecuencias ya mencionadas en los análisis de las otras variables.
# 
# 9. **`Price Book Value Ratio`**: Al ser esta variable una razón, debieramos tener recorridos menos amplios. Sin embargo, el máximo y el mínimo de esta columna no soportan esta hipótesis, probablemente por la presencia de outliers como se ha visto en las demás columnas. La media es superior a 15000 y la mediana es bastante cercana a cero. Viendo el boxplot de esta columna notamos que efectivamente hay presencia de Outliers. El histograma muestra la distribución concentrada, y aparece una sola barra grande por la presencia de outliers...

# In[41]:


train_data.boxplot(column='priceBookValueRatio', color = "orange", patch_artist = "True")
plt.show()

train_data['Market Cap'].hist(bins=10, color = "orange")
plt.show()


# - Efectivamente, notamos que existen outliers en la distribución. Además es interesante ver lo compacto de la caja. Esto se puede deber a dos razones:
# 1. A que el gráfico se ajustó de esa manera, para representar fielmente a todos los datos, incluidos a los outliers. 
# 2. A que los datos están bastante condensados, y solo unos pocos se escapan de esta tendencia.
# 
# - Fuera de esto, los datos claramente sufren las consecuencias de la presencia de estos valores extremos, con desviaciones estándar descomunales y con medias lejanas a la mediana.
# 
# 10. **`Sector`**: Esta variable cualitativa, no queda dentro de la tablita del describe. Sin embargo, es importante analizarla. Tenemos que una gran mayoría de las empresas que transan acciones (que están en nuestra base de datos) son del sector financiero, luego del sector de cuidado de la salud y luego de Tecnología. Hoy en día con la crisis del coronavirus, se ha puesto en evidencia el hecho de que ciertos sectores son más vulnerables a los nuevos tiempos. Por lo que en las misiones siguientes será vital tener en cuenta el sector de la acción para ver si esta es recomendable o no (en temas de mayor o menor retorno).

# In[42]:


train_data["Sector"].value_counts()


# - A modo de entender mejor esta variable se procede a armar una tabla dinámica que muestre la media de retorno para cada uno de los sectores y para cada una de las clases de acción. 
# 
# - **NOTA :EN LA MISIÓN 3 SE REVISARÁN ESTAS MISMAS TABLAS PERO CON LA LIMPIEZA DE DATOS DE LA MISIÓN 2 YA REALIZADA.**

# In[43]:


dinamica = train_data.pivot_table("Return", index = "Sector")

rank = dinamica.reindex(dinamica['Return'].sort_values(ascending=False).index)

display(rank)


# - Es interesante notar cuales son los sectores con acciones de mayor retorno promedio. El top 3 está conformado por el sector de Real Estate o inmobiliario (que si bien tiene mayor retorno es bastante cíclico [sufre de las fluctuaciones del mercado]), luego por las Tech-Companies ya que son las compañías que *la llevan* hoy en día y finalmente las de los sectores financieros, que son verdaderas maquinitas de dinero. Las de peor retorno promedio son las de energía, pero suelen ser bastante seguras y poco volátiles. Este ranking es en cierto sentido coherente con el modelo de CAPM, ya que señala que las acciones de mayor retornos son las más cíclicas o volátiles y las de menor retorno las más seguras o menos volátiles. 

# - La siguiente tabla divide los datos por sector y por clase; y presenta la media del retorno de cada uno de estos 22 grupos. Notamos que Class, efectivamente considera el retorno como una variable importante a la hora de decidir si la acción es conveniente o no (valor 1 de la columna `Class`), lo cual se demuestra para cada uno de los sectores.

# In[44]:


train_data.pivot_table("Return", index = "Sector", columns = "Class")


# ## Misión 2: Limpieza y Depuración

# En la siguiente misión se deben llevar a cabo 5 resoluciones de conflicto que permitan luego trabajar con los datos. Se deben eliminar los datos vacíos, y reemplazar con un cierto criterio a estos. Además se deben eliminar las incoherencias y los datos extremos o outliers, bajo un cierto criterio.

# ### 1. Agrupando las Columnas PRICE VAR [%]:
# 
# Esta resolución de conflicto ya se realizó en la misión 1. Se hizo con anterioridad, dado que era necesario para poder estudiar la distribución de la variable Retorno de toda la Data de Entrenamiento. Para que no sea necesario subir, el código utilizado más arriba fue el siguiente, habiendo ya revisado que no existiesen datos vacíos en ninguna de las bases de datos, en la columna *Año* PRICE VAR [%]:

# In[45]:


#Reemplazo por ceros los NaN
#for i in range(5, 9):
    #string = "201{} PRICE VAR [%]".format(i)
    #train_data[string].fillna(0, inplace = True)
    
#train_data["Return"] = train_data["2015 PRICE VAR [%]"] + train_data["2016 PRICE VAR [%]"] + \
                       #train_data["2017 PRICE VAR [%]"] + train_data["2018 PRICE VAR [%]"] 

#train_data.head()

train_data.apply(lambda x: sum(x.isnull()),axis=0).tail()


# Notamos que vía esta resolución de conflicto que agrupó la variable *Año* PRICE VAR [%], ya que al hacer el Concatenate de las bases correspondientes al año 2014, 2015, 2016 y 2017; quedamos con 4 columnas PRICE *Año* VAR [%], que al tener las distintas columnas (de las bases de los distintos años) nombres distintos, quedan con NaN los datos no correspondientes a la base que contiene la columna PRICE *Año* VAR [%] de un año en particular.
# 
# De esta forma solucionamos el conflicto de tener 4 columnas distintas que hacen referencia a una misma feature (`Retorno`). Ahora las tenemos agrupado en una sola columna, como se debe.

# Como ya no será necesario utilizarlas en futuras misiones, ya que son rebundantes, se procederá a *dropear* las columnas que no se necesitan del tipo *Año* PRICE VAR [%].

# In[46]:


for i in range(5, 9):
    string = "201{} PRICE VAR [%]".format(i)
    train_data.drop(string, axis = 1, inplace = True )

train_data.head()


# ### 2. Tratando los NaN (Round 1):
# 
# Para las variables que **NO** consideramos dentro de las 10 variables *importantes* en la Misión 1, se procederá a rellenar con la mediana de esa columna todos los datos faltantes. Como se argumenta más abajo, el problema de rellenar con la media en estos datos es que, la media puede estar contaminada por la presencia de Outliers, que se escapan demasiado del resto de la muestra o columna, por eso preferimos ser más conservadores y rellenar estos datos faltantes con el dato de *al medio*.
# 
# Primero selecciono las columnas numéricas (no dicotómicas) y las columnas que no pertenecen a las 10 seleccionadas en la Misión 1.
# 
# Revisando rápidamente las columnas, se puede notar que hay una columna fuera de las 10 seleccionadas, que podría ser dicotómica, sin embargo si analizamos los valores que toma, notamos que esta es una *excepción*, ya que solo toma el valor de 1. Rellenar los datos faltantes de esta columna con unos, no será problema. Sin embargo, esta variable no presenta datos vacíos. Y ade´mas como no aporta ninguna variabilidad, y por lo tanto información, a un futuro posible modelo, se podría incluso *dropear*.

# In[47]:


train_data["operatingProfitMargin"].value_counts()


# In[48]:


train_data["operatingProfitMargin"].describe()


# In[49]:


columnas = ["operatingProfitMargin", "Class"]

train_data[columnas].apply(lambda x: sum(x.isnull()),axis=0)


# Ahora armamos el set de columnas que vamos a utilizar para rellenar con la mediana.

# In[50]:


cols = [col for col in train_data.columns if col not in ["Return", "Free Cash Flow",                                                          "Goodwill and Intangible Assets",                                                          "Dividend per Share",                                                          "debtEquityRatio",                                                          "Market Cap", "Class",                                                          "ROE", "priceBookValueRatio",                                                          "Sector", "Unnamed: 0"
                                                        ]]

train_data[cols]


# Luego a las columnas numéricas, y las no pertenecientes a las 10 seleccionadas se rellenarán los datos vacíos con la media de la columna. De esta forma, se logra resolver el conflicto de valores faltantes en estas columnas.

# In[51]:


train_data[cols] = train_data[cols].apply(lambda x: x.fillna(x.median()),axis=0)


# In[52]:


train_data[cols].apply(lambda x: sum(x.isnull()),axis=0)


# In[53]:


train_data.head()


# **Aplicando el criterio a la Data de Testeo (Año 2018)**:
# 
# Como se vió en clases, se debe aplicar el mismo criterio de resolución de conflicto en la Data de Testeo, pero además no podemos usar información de la Data de Testeo para imputar estos valores. En otras palabras, la Data de Testeo es en cierto sentido Víctima de las decisiones tomadas para las base del 2014 al 2017 (`train_data`).
# 
# Por lo tanto debemos proceder a trabajar desde ya la data del 2018, de ahora en adelante `test_data`.
# 

# In[54]:


test_data = data_2018
test_data.tail()


# Además aprovecho de agregar una columna `Return` que en este caso corresponde solo a la columna `2019 PRICE VAR [%]`, y botamos la columna PRICE VAR, de esta forma tenemos ambas bases de datos con las mismas features. No es necesario entonces, hacer la agregación de columnas que se hizo en la primera resolución de conflicto. Por esta razón, se parte resolviendo conflictos en la data de testeo, recién en esta segunda resolución de conflicto.

# In[55]:


test_data["Return"] = test_data["2019 PRICE VAR [%]"]

test_data.drop('2019 PRICE VAR [%]', axis = 1, inplace = True )

test_data.head()


# Entonces ahora podemos proceder a imputar la mediana de las columnas de la data de entrenamiento, sobre los datos vacíos de nuestra `test_data`.

# In[56]:


for col in cols:
    mediana = train_data[col].median()
    test_data[col].fillna(mediana, inplace = True)
    
test_data[cols]


# In[57]:


test_data


# In[58]:


test_data[cols].apply(lambda x: sum(x.isnull()),axis=0)


# ### 3. Tratando los NaN (Round 2):
# 
# En esta resolución de conflicto se rellenan los valores faltantes de las 10 columnas seleccionadas en la misión 1. Eso si, primero debemos revisar en que columnas de las 10 existen datos faltantes:
# 

# In[59]:


diez = ["Return", "Free Cash Flow","Goodwill and Intangible Assets",  "Dividend per Share",         "debtEquityRatio", "Market Cap", "Class", "ROE", "priceBookValueRatio", "Sector"]

train_data[diez].apply(lambda x: sum(x.isnull()),axis=0)


# In[60]:


test_data[diez].apply(lambda x: sum(x.isnull()),axis=0)


# Estudiemos como se comportan las distintas columnas con datos vacíos según la Class que tiene. En otras palabras, se hará por cada una de las variables de la lista de las `Diez` (que tengan datos vacíos), una tabla dinámica que muestre la mediana de cada columna según si las muestras pertenecen a un cierto sector, y si son de una Clase de la clase 0 o 1. Usamos la mediana, porque como vimos en la Misión 1, la muestra esta fuertemente contaminada con la presencia de outliers que se escapan de la realidad, por eso creo que una buena forma de evitar esta influencia, es pararse en el dato de al medio (con la columna ordenada) y reemplazar por ese dato.

# In[61]:


diez_con_nan = ["Free Cash Flow", 'Goodwill and Intangible Assets', 'Dividend per Share', 'debtEquityRatio',                 'Market Cap', 'ROE', 'priceBookValueRatio']

for col in diez_con_nan:
    print('\n\n')
    print("\t Tabla para la Variable {} \n".format(col))
    table = train_data.pivot_table(values= col , index='Sector', columns = "Class", aggfunc=np.median)
    display(table)


# Notamos rápidamente que los distintos grupos tienen medias distintas en general. Por ello dado que estas variables serán más importantes (por el criterio de selección dicho en la M1), procuraremos ser más específicos en el *relleno* de los valores nulos. Utilizando la media de la categoría a la cual corresponde esta observación, para hacer este *relleno*. Un ejemplo característico de esto, es
# 
# Hay solo una de estas variables que no presenta gran diferencia entre los distintos grupos, esta es la tabla correspondiente a la columna `Dividend per Share`. Por esta razón, dado que no es necesario diferenciar las medias a utilizar como *relleno*, se rellenan los datos faltantes de esa columna con la media de esa columna completa. Partamos por eso:

# In[62]:


media = train_data['Dividend per Share'].mean()
train_data["Dividend per Share"].fillna(media, inplace = True)
test_data["Dividend per Share"].fillna(media, inplace = True)


# Revisamos que efectivamente se hayan reemplazado todos estos datos vacíos, en la data de entrenamiento y en la de Testeo.

# In[63]:


train_data[diez].apply(lambda x: sum(x.isnull()),axis=0)


# In[64]:


test_data[diez].apply(lambda x: sum(x.isnull()),axis=0)


# Notamos rápidamente que estamos OK. Es decir, nos deshicimos exitosamente de los datos vacíos.

# Ahora procedamos con rellenar los datos faltantes de cada una de las columnas que aún nos quedan con datos vacíos de nuestras 10 originales. Para esto usaremos la función `fage` que se nos entregó en la materia de clases.

# In[65]:


train_data


# In[66]:


diez_con_nan2 = ["Free Cash Flow", 'Goodwill and Intangible Assets', 'debtEquityRatio',                 'Market Cap', 'ROE', 'priceBookValueRatio']


for col in diez_con_nan2:
    table = train_data.pivot_table(values= col , index='Sector' ,columns='Class', aggfunc=np.median)
    def fage(x):
        return table.loc[x['Sector'],x['Class']]
    
    train_data[train_data[col].isnull()].apply(fage, axis=1)
    train_data[col].fillna(train_data[train_data[col].isnull()].apply(fage, axis=1), inplace=True)    


# In[67]:


train_data[diez_con_nan2].apply(lambda x: sum(x.isnull()),axis=0)


# Ahora nos gustaría hacer lo mismo con el set de Testeo. Solo que en este caso utilizar la tabla que se origina con las medianas de la data de entrenamiento, para rellenar los datos vacíos de la tabla de Testeo.

# In[68]:


for col in diez_con_nan2:
    table = train_data.pivot_table(values= col , index='Sector' ,columns='Class', aggfunc=np.median)
    def fage(x):
        return table.loc[x['Sector'],x['Class']]
    
    test_data[test_data[col].isnull()].apply(fage, axis=1)
    test_data[col].fillna(test_data[test_data[col].isnull()].apply(fage, axis=1), inplace=True)    


# In[69]:


test_data[diez_con_nan2].apply(lambda x: sum(x.isnull()),axis=0)


# In[70]:


train_data


# In[71]:


test_data


# ### 4. Tratando los Outliers (Round 1):
# 
# Como se vió en la misión anterior los outliers están siendo mucho estorbo, lo cual se demuestra en los distintos estadísticos de las 10 columnas representadas.
# 
# Para tratar los datos extremos, se seleccionarán todas las columnas con medias bastante grandes (para así solo despejar outliers en columnas que son potencialmente víctimas de outliers). A estas columnas se les aplicará el criterio de eliminar los datos que estén bajo el percentil 0.005 y los que estén sobre el percentil 0.995. 
# 
# En el siguiente cuadro se seleccionan las columnas, pero antes selecciono las columnas numéricas para así aplicar luego a mi `train_data`.

# In[72]:


numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']

train_data_num = train_data.select_dtypes(include=numerics).fillna(0)

columnas_a_limpiar = []
for col in train_data_num.columns:
    if train_data[col].mean() > 1000000:
        columnas_a_limpiar.append(col)


# In[73]:


print(len(columnas_a_limpiar))


# In[74]:


test_data["Free Cash Flow"].describe()


# Notamos que se seleccionaron de manera correcta las columnas. Por ejemplo, la columna `Free Cash Flow`, efectivamente tiene media "grande" y tiene un valor mínimo bastante pequeño.

# In[75]:


def util(data, col):
    lim_inf = data[col].quantile(0.005)
    lim_sup = data[col].quantile(0.995)
    cleaned_data = data.loc[(data[col] >= lim_inf) & (data[col] <= lim_sup)]
    return cleaned_data

for col in columnas_a_limpiar:    
    train_data = util(train_data, col)


# In[76]:


train_data


# Lamentablemente perdimos hartos datos, pese a haber tenido un criterio bastante blando con los outliers. Quedamos con 10879 observaciones de Entrenamiento, bastante menos que lo que teníamos antes.
# 
# Sin embargo, ahora si estudiamos un box-plot de la columna `Free Cash Flow`, por ejemplo, podremos notar que ahora SÍ se ve la caja. Esto es señal de una buena ditribución, más libre de la influencia de outliers.

# In[77]:


train_data.boxplot(column = "Free Cash Flow")


# Ahora debo hacer el mismo procedimiento con la data de Testeo. En este caso, como la Data de Testeo es víctima de las decisiones tomadas en la data de entrenamiento. Se deben despejar todos los datos de la data de testeo que cumplan, con estar entre los valores del percentil 0.005 y el 0.995, pero OJO, estos valores corresponden a los de los percentiles de la data de Entrenamiento.
# 
# Debemos crear otra función `util`, que ahora reciba como inputs, la data de entrenamiento, la de testeo y una columna en particular.

# In[78]:


def util2(train, test, col):
    lim_inf = train[col].quantile(0.005)
    lim_sup = train[col].quantile(0.995)
    cleaned_data = test.loc[(test[col] >= lim_inf) & (test[col] <= lim_sup)]
    return cleaned_data

for col in columnas_a_limpiar:    
    test_data = util2(train_data, test_data, col)


# In[79]:


test_data


# Nuevamente notamos que perdemos una buena cantidad de datos, pero ahora en el Set de Testeo. Lamentable, pero se logran resultados menos sesgados y más generalizables a la data del mundo real, ya que es más útil que nuestro modelo sirva para predecir las acciones comunes, que intente explicar a todaaas las acciones. 
# 
# Igual es importante tener en cuenta que si bien se pierden filas, igual se tiene una magnitud bastante grande de datos. 

# ### 5. Tratando Outliers (Round 2):
# 
# Ahora nos preocupamos de, los datos con media pequeña. La idea acá es desepejar los datos que sean como valores por acción, fracciones, o valores de ese tipo y tratar los outliers presentes en estas columnas. Recordemos que en la Misión 1, priceBookValueRatio también sufría de outliers. Si miramos un boxplot de algunas de estas variables lo podremos notar rápidamente.

# In[80]:


train_data.boxplot(column = "priceBookValueRatio")


# La idea entonces es tratar también estas columnas, y librarnos de esos "puntos locos", que se pueden ver en el boxplot que se encuentra en el superior. Procedemos entonces a tratar las columnas de "media chica", que son parte de las 10 seleccionadas en el ejercicio. Se hace esto, dado que al resolver el conflicto, eliminando las observaciones mayores al percentil 0.999, para todas las con media menor a 1.000.000 se pierden muchísimas variables, quedando con solo 2851 observaciones para entrenar. Por esta razón, solo se resuelve este conflicto para las acciones interesantes según lo dicho en la misión 1.
# 
# Siguiendo la misma lógica que en la resolución de conflicto número 4, se resuelve este desafío.

# In[81]:


columnas_a_limpiar2 = ['Return', 'Dividend per Share', 'debtEquityRatio', 'ROE', 'priceBookValueRatio']


# In[82]:


train_data["Return"].quantile(0.999)


# In[83]:


def util3(data, col):
    lim_sup = data[col].quantile(0.999)
    cleaned_data = data.loc[(data[col] <= lim_sup)]
    return cleaned_data

for col in columnas_a_limpiar2:    
    train_data = util(train_data, col)


# In[84]:


train_data


# Dado que solo trabajamos dos columnas, se nos van pocas observaciones de la base de datos de entrenamiento. Procedemos ahora a resolver el mismo conflicto, para estas mismas 5 variables, despejando todos los valores que estén sobre el percentil 0.999 de la data de Entrenamiento, de esa columna respectiva. 
# 
# Siguiendo la misma lógica que en la misión 4, al tratar la data de testeo se procede a resolver el ejercicio, para el cual es necesario definir una cuarta función `util4`.

# In[85]:


def util4(train, test, col):
    lim_sup = train[col].quantile(0.995)
    cleaned_data = test.loc[(test[col] <= lim_sup)]
    return cleaned_data

for col in columnas_a_limpiar2:    
    test_data = util4(train_data, test_data, col)


# In[86]:


test_data


# Nuevamente pierdo un poco más de observaciones...
# 
# **Comentarios Generales M2:** Fue interesante jugar con los datos, en esta etapa. Siento que la verdadera familiarización con la Base se logró acá y no en la Misión 1. Lamentablemente en la resolución de conflicto 4, se perdieron muchas observaciones del set de testeo y del set de Entrenamiento, sin embargo es importante despejar outliers disruptivos ya que sesgan bastante las estimaciones del modelo. En algún momento, se me pasó por la cabeza la idea de reemplazar la columna de la observación, que era outlier en vez de eliminar o *dropear* toda una fila, pero me pareció que esto sería una forma bastante grave de alterar la realidad que verá el modelo.
# 
# Pese a esto último, igual terminamos con un set de Entrenamiento bastante grande así que espero, que en esta misión no haya tomado los pasos equivocados, prefiriendo tener observaciones ordinarias pero en menor cantidad, en vez de tener más observaciones pero algunas muchas con alta probabilidad de sesgar nuestras futuras estimaciones. Esto último, es un fiel reflejo del famoso *trade-off* entre Cantidad y Calidad. 

# Antes de pasar a la siguiente misión *reseteamos* los índices de las data frames de testeo y de entrenamiento, así nos quedan en ambas tablas los índices de cada observación ordenados.

# In[87]:


train_data = train_data.reset_index(drop=True)
test_data = test_data.reset_index(drop=True)


# ## Misión 3: Visualización:
# 
# En esta misión se visualizarán los datos, de manera original. Si bien, a lo largo del trabajo hasta ahora, se hicieron múltiples visualizaciones (tablas dinámicas, histogramas y cajas y bigote), estas estaban bastante sesgadas ya que sufrían de sesgos por la presencia de outliers, valores vacíos, etc.
# 
# ### Análisis de las Variables Dependientes:
# 
# Partamos viendo como nos quedan ahora nuestra futura variable dependiente **`Return`**, en términos de distribución.

# In[88]:


train_data.boxplot(column='Return', color = "blue", patch_artist = "True", figsize = (15, 6))
plt.show()


plt.figure(figsize = (15,6))
sns.histplot(data=train_data, x="Return", kde=True, color = "tomato")
plt.show()


# Notamos que esta variable ahora tiene un comportamiento bastante armónico, en términos de distribución. Si bien, aún existen outliers que se escapan de los bigotes, estos son bastante pequeños, ahora podemos ver una caja claramente y también podemos ver un histograma distribuido en un plano sin ajustes de escala (como el que veíamos en la misión 1). La distribución de esta variable podría ser una Distribución Weibull (no se mucho de estadística, pero en Google se veía parecida : ) ).
# 
# Veamos ahora como es el retorno por Sector. Esto lo podemos ver de dos formas distintas, la primera es a través de diagramas del tipo caja-bigote que muestren la distribución del retorno por cada sector. Pero antes veamos las medias de los retornos, por cada sector a través de una Tabla Dinámica, ordenada de mayor a menor retorno. Luego se puede ver el caja bigote del retorno por sector.

# In[89]:


dinamica = train_data.pivot_table("Return", index = "Sector")

rank = dinamica.reindex(dinamica['Return'].sort_values(ascending=False).index)

display(rank)


# In[90]:


rank.plot(kind="bar", color = "forestgreen", grid = True, figsize = (15, 8))
plt.show()


# A partir solo de este gráfico, claramente NO recomendaríamos invertir en el sector Energía, los retornos promedio son NEGATIVOS! Si recomendamos el sector de Tecnologías y de Utilities.

# In[91]:


plt.figure(figsize = (16,10))
sns.set_style('dark')
sns.set_palette('bright', 100)
sns.set_context('paper', font_scale = 1.5)
sns.boxplot(x = 'Sector', y = 'Return', data = train_data)
plt.xticks(rotation=45)
plt.show()


# Los cajas y bigote muestran, que distintos sectores tienen distintas distribuciones. En ese sentido, ciertos sectores aseguran mayores o menores retornos. También los sectores con cajas que están por completo más arriba que otros sectores, es más probable obtener retornos invirtiendo en ellos. Por último, cajas más largas, significa en cierto sentido, que ese sector presenta más volatilidad, y por ende es más riesgoso. El sector de Salud presenta, esta característica. 
# 
# Veamos que pasa cuando separamos las columnas, por sector y por **`Class`**. En teoría Class muestra, las acciones convenientes, veamos que pasa.

# In[92]:


tabla2 = train_data.pivot_table("Return", index = "Sector", columns = "Class")
display(tabla2)


# In[93]:


tabla2.plot(kind= "bar", color = ["black", "red"], figsize = (15,8), stacked = True, grid = True)
plt.show()


# Claramente, la feature `Class`, contempla el retorno en su criterio para seleccionar que acción es más o menos conveniente. Esto se nota en las barras negras, negativas y las rojas positivas. Es decir, las acciones de Class con valor 1, tienen retornos promedio positivo en todos los sectores. Lo contrario ocurre para las acciones de Class 0 para todos los sectores.

# In[94]:


plt.figure(figsize = (16,10))
sns.set_style('dark')
sns.set_palette('bright', 100)
sns.set_context('paper', font_scale = 1.5)
sns.boxplot(x = 'Return', y = 'Sector', data = train_data, hue = "Class")
plt.show()


# In[95]:


plt.figure(figsize = (16,10))
sns.set_style('dark')
sns.set_palette('bright', 100)
sns.set_context('paper', font_scale = 1.5)
sns.violinplot(x = 'Sector', y = 'Return', data = train_data, hue = "Class", split = 'True')
plt.xticks(rotation=45)
plt.show()


# Es interesante notar como los distintos sectores tienen distintas distribuciones de retorno. Algunos sectores presentan cajas o distribuciones más extendidas y otros sectores cajas o distribuciones menos extendidas. Como se dijo previamente sectores con cajas más largas, son a priori sectores con más volatilidad, como se dijo previamente.
# 
# #### Reducción de Dimensiones:
# 
# En el siguiente cuadro se tratará de construir a través de un análisis de componentes principales una representación de las variables según su valor de `Class`. Para implementar este código me basé fuertemente en lo explicado en este link: https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60 
# 
# Primero, debo definir las variables X o features, para ello voy a aprovechar de eliminar la columna del nombre de las acciones como nos sugirió el profesor Hans Löbel.  

# In[96]:


train_data.drop("Unnamed: 0", axis = 1, inplace = True )
test_data.drop("Unnamed: 0", axis = 1, inplace = True )


# In[97]:


features = []

for col in train_data_num.columns:
    if col not in ["Return", "Class"]:
        features.append(col)
    


# In[98]:


from sklearn.preprocessing import StandardScaler

x = train_data.loc[:, features].values
y = train_data.loc[:,['Class']].values
x = StandardScaler().fit_transform(x)


# In[99]:


from sklearn.decomposition import PCA
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])


# In[100]:


finalDf = pd.concat([principalDf, train_data[['Class']]], axis = 1)


# In[101]:


fig = plt.figure(figsize = (15,4))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = [0, 1]
colors = ['tomato','skyblue']
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['Class'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()


# Notamos que vía este análisis de Componentes Principales, que separa TODAS las columnas en estos dos ejes, no se puede identificar claramente que observaciones perteneces a cada valor de `Class`, 0 o 1. Esto es señal de que el PCA no salió bien, probablemente esto ocurre por el exceso de features que se utiliza, que impide hacer una reducción de dimensiones que permita identificar cada clase.
# 
# Veamos que pasa si tratamos de hacer lo mismo, pero ahora en vez de usar todas las Features de la Base de Datos usamos solo las 8 Features posibles de las 10 que elegimos en la Misión 1.

# In[102]:


features2 = ["Free Cash Flow",  "Goodwill and Intangible Assets", "Dividend per Share",              "debtEquityRatio", "Market Cap", "Class", "ROE", "priceBookValueRatio"]


# In[103]:


x = train_data.loc[:, features2].values
y = train_data.loc[:,['Class']].values
x = StandardScaler().fit_transform(x)


# In[104]:


pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])


# In[105]:


finalDf = pd.concat([principalDf, train_data[['Class']]], axis = 1)


# In[106]:


fig = plt.figure(figsize = (15,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
targets = [0, 1]
colors = ['yellow','blue']
for target, color in zip(targets,colors):
    indicesToKeep = finalDf['Class'] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
ax.legend(targets)
ax.grid()


# Notamos que con los Features que le dimos, no es claro distinguir entre las observaciones o acciones de buena calidad o recomendables (Class = 1) de las de mala calidad o *no recomendables* (Class = 0).
# 
# Veamos que logramos con un análisis del tipo t-SNE. Para hacer este desarrollo, utilicé lo sacado del link que usé para hacer el PCA y también lo visto en la ayudantía 3 con Pablo Seisdedos.

# In[107]:


x = train_data.loc[:, features2].values
y = train_data.loc[:,['Class']].values
x = StandardScaler().fit_transform(x)

TSNE = manifold.TSNE(n_components=2)


# In[110]:


projected = TSNE.fit_transform(x)


# In[111]:


plt.figure(figsize=(15,10))
plt.scatter(projected[:, 0], projected[:, 1], c=y, edgecolor='none', alpha=0.5, cmap=plt.cm.get_cmap('prism', 2))
plt.xlabel('TSNE 1')
plt.ylabel('TSNE 2')
plt.colorbar()
plt.show()


# Notamos que con esta estrategia se pueden identificar, mejor las acciones. Podemos identificar de mejor manera los dos grupos de acciones los de `Class` igual a 0 (rojos) y los de `Class` igual a 1 (verdes).
# 
# Es muy interesante ver como se generan dos puntos de acumulación o **clusters** (los circulos verde y rojos) en la parte del medio y arriba del cuadro. Estos representan puntos de acumulación de las observaciones que son de Class cero o uno.

# ### Análisis de Features:
# 
# En esta sección, dadas todas las features que tenemos, no se hará muchas visualizaciones. Pero sí se harán una serie de visualizaciones interesantes, que permitirán familiarizarnos aún más con los datos.
# 
# En primer lugar vemos una distribución de las observaciones, en la data de entrenamiento según sector. Para ello me pareció útil, representar este conteo en un gráfico de torta como el que se ve más abajo. Los 3 sectores con más acciones como representantes son:
# 1. Servicios Financieros.
# 2. Empresas del Cuidado de la Salud.
# 3. Empresas de Tecnología o Tech-Companies.

# In[112]:


tablon = train_data["Sector"].value_counts()
sizes = tablon.values


# In[113]:


tablon.index


# In[114]:


labels = 'Financial Services', 'Healthcare', 'Technology', 'Industrials', 'Consumer Cyclical', 'Basic Materials',          'Real Estate', 'Consumer Defensive', 'Energy', 'Utilities', 'Communication Services'


# In[115]:


plt.figure(figsize=(15,15))
plt.pie(sizes, autopct='%1.1f%%', labels = labels,
        shadow=True, startangle=90)

plt.show()


# Además puede ser interesante ver la distribución de algunas de las demás variables dependientes después de la Misión 2.

# In[116]:


plt.figure(figsize = (15,6))
sns.histplot(data=train_data, x="Market Cap", kde=True, color = "brown")
plt.show()


# La distribución de esta variable se asemeja bastante a una Chi-Cuadrado. 
# 
# Veamos la distribución de más variables, post Depuración. En el siguiente cuadro veremos que pasa con la columna `priceBookValueRatio`.  

# In[117]:


plt.figure(figsize = (15,6))
sns.histplot(data=train_data, x="priceBookValueRatio", kde=True, color = "black")
plt.show()


# Viendo esta gráfica notamos que la variable `priceBookValueRatio` distribuye Fisher (F). Sin la línea de kde, me fue difícil predecir como era la distribución de esta variable. Este atributo de la librería `seaborn`, ayuda mucho en ese sentido.

# Notamos que `priceBookValueRatio` distribuye prácticamente log-normal o también chi-cuadrado. Es agradable ver gráficos más anchos, que los que veíamos en la Misión 1. Esto último se da, por la gran pega que implicó la Misión 2.
# 
# Por último analizamos la variable `ROE`.

# In[118]:


plt.figure(figsize = (16,8))
sns.histplot(data=train_data, x="ROE", kde=True, color = "red")
plt.show()


# Notamos que esta variable distribuye bastante parecido a una distribución normal, que tiene una desviación estándar bastante baja. La media y moda, se centra en el cero y la frecuencia está más acumulada hacia el lado negativo, es decir, que hay más observaciones con `ROE` negativo.

# Si bien podría hacer muchísimo análisis de los distintos features, me pareció interesante hacer el análisis de las distribuciones de distintas de estas, ya que en parte estas determinan la futura convergencia y la velocidad de esta en su camino al óptimo (es decir, hacia los parámetros que minimizan la función de costo).

# ### Análisis de Correlaciones:
# 
# En los siguientes cuadros se mostrará una visualización interesante de la correlación entre distintos pares de. variables. Partamos por la correlación entre la razón `EBITDA` y `Return`. Veamos que pasa:

# In[119]:


plt.figure(figsize = (16,16))
sns.set_style('dark')
sns.set_palette('bright', 100)
sns.set_context('paper', font_scale = 1.5)
sns.jointplot(x = 'EBIT', y = 'Return', data = train_data, kind = 'reg' )
plt.show()


# Notamos que hay una correlación positiva entre ambas variables. Notar también que en el *eje X de arriba*, se muestra la distribución de la variable `EBIT` y en el *eje y de la derecha* se muestra la dsitribución de la variable `Return`.
# 
# Como he podido aprender en mis ramos de Finanzas, un mayor `EBIT` debiera ir acompañado de un mayor `Free Cash Flow`. Veamos que pasa:

# In[120]:


plt.figure(figsize = (16,16))
sns.set_style('dark')
sns.set_palette('hls', 100)
sns.set_context('paper', font_scale = 1.5)
sns.jointplot(x = 'EBIT', y = 'Free Cash Flow', data = train_data, kind = 'reg' )
plt.show()


# Claramente existe la relación positiva que habíamos predicho previamente. Esto sugiere que efectivamente un mayor `EBIT` esta correlacionado con un mayor `Free Cash Flow`, que según nuestra teoría se debiera dar por la relación lineal que tienen ambas variables.

# Ahora hagamos un análisis, de la relación entre inversiones y el nivel de deuda de una empresa. Veamos si más inversión esta correlacionado con un mayor endeudamiento (`Total debt`).

# In[121]:


plt.figure(figsize = (16,16))
sns.set_style('dark')
sns.set_palette('Spectral', 100)
sns.set_context('paper', font_scale = 1.5)
sns.jointplot(x = 'Investments', y = 'Total debt', data = train_data, kind = 'reg' )
plt.show()


# **Comentarios Generales Misión 3:**
# 
# Me encantó esta misión, lo pasé muy bien haciéndola. Ahora si que me conozco las bases de datos perfectamente. Siempre, me ha gustado mucho poder visualizar bien lo que uno hace, y que mejor que hacer visualizaciones gráficas de ello para realizarlo. Intenté, ser preciso pero siento que cada una de las gráficas es importante. Espero no haber sido latero.

# ## Misión 4: Entrenamientos de Modelos Parte 1.
# 
# Como vimos en clases antes de partir entrenando los modelos es imporante extraer una porción de la data de entrenamiento para usarla como data de validación. La idea de esto, es tener una porción de los datos, que no se utilizará para testear la generalización del modelo ni para entrenar. 
# 
# Con el set de validación, se pone a prueba la generalización de los distintos modelos a crear. Sería bastante mal hecho, si creyera que un modelo con un alto porcentaje de aciertos en la data de entrenamiento, es el mejor. Esto porque es posible que tengamos modelos, que acierta muchísimo en la data de entrenamiento (casi 100%) pero es probable que se esté *pecando* de **Overfitting**, es decir que el modelo no se puede extrapolar para predecir data distinta a la de entrenamiento.
# 
# Por otro lado, tampoco sería correcto (pero no tan grave como lo primero) seleccionar el mejor modelo, a partir de sus aciertos en la data de testeo. Esto porque, el objetivo de ver que tanto acierta el modelo en la data de testeo es ver que tanto puede generalizar el modelo con data completamente nueva, y no si es mejor o peor que los otros modelos. Por ello, hay que ser riguroso y dividir de forma aleatoria la data de entrenamiento en dos para tener un nuevo set que se llamará **val**. 
# 
# Antes de hacer la división conviene primero convertir nuestra variable `Sector`, la única variable cualitativa que nos interesa, en una variable cuantitativa. Aprovechamos de hacer lo mismo para la data de Testeo. Partimos por eso entonces:

# In[122]:


le = LabelEncoder()
train_data['Sector'] = le.fit_transform(train_data['Sector'])


# In[123]:


le2 = LabelEncoder()
test_data['Sector'] = le2.fit_transform(test_data['Sector'])


# Revisamos que haya cambiado nuestra variable `Sector` en ambos sets, como se ve más abajo estamos OK.

# In[124]:


train_data['Sector'].value_counts()


# In[125]:


test_data['Sector'].value_counts()


# Ahora procedemos a dividir nuestra data de entrenamiento en 2. Para quedar con nombres más agradables de programar, ahora tendremos 3 sets de data, con los respectivos nombres:
# 
# 1. `train`
# 2. `val`
# 3. `test`
# 
# El primero, corresponde a un 90% del set de entrenamiento que tenemos hasta el momento `train_data`. El segundo corresponde a un 20% del set de entrenamiento que tenemos hasta el momento `train_data`. El último, es el mismo set de testeo que tenemos hasta este momento, solo que le cambiamos el nombre para simplificar el código futuro.

# In[126]:


from sklearn.model_selection import train_test_split
train, val = train_test_split(train_data, test_size=0.2)
test = test_data


# In[127]:


train.shape


# In[128]:


val.shape


# In[129]:


test.shape


# Notamos que efectivamente se hizo la división en las proporciones pedidas. Además esta división se realizó de manera aleatoria, por lo que no tendremos una data con datos característicos de un año nomas.
# 
# Antes de partir modelando aprovechamos de *resetear* el índice de los dos primeros sets `train` y `val`.

# In[130]:


train = train.reset_index(drop=True)


# In[131]:


val = val.reset_index(drop=True)


# ## Modelación:
# 
# Para modelar con Clasificación debemos definir nuestros sets X e Y, para cada uno de los sets de Data que armamos justo antes. Por lo que entendí en la Lectura del Enunciado, el objetivo de esta misión más que nada es utilizar distintos modelos, por lo que se usarán para predecir a `Class` todas las demás variables de las diez seleccionadas en la misión 1 y solo variará el modelo utilizado.
# 
# Cada modelo se entrenará con el set de entrenamiento con las 10 features seleccionadas en la misión 1. Luego se evaluará el rendimiento de cada uno de estos modelos en la data de validación y se seleccionará al que tenga el mayor rendimiento en la data de valiación (`val`), para luego testearlo en el set de `test`.
# 
# Se usarán los siguientes modelos:
# 1. KNN Neighbours
# 2. Decision Tree Classifier
# 3. Random Forest Classifier
# 4. Support Vector Machine
# 5. Red Neuronal (MLP)
# 6. Regresión Logística (usando Sigmoid Function).
# 
# Partamos entonces, primero hay que definir la matriz X de la data de entrenamiento, de la de validación y de la de testeo. Lo mismo con la variable y.

# In[132]:


ten = ["Free Cash Flow", 'Goodwill and Intangible Assets', 'debtEquityRatio',                 'Market Cap', 'ROE', 'priceBookValueRatio', 'Sector', 'Dividend per Share']

X_train = train[ten]


# In[133]:


y_train = train['Class']


# In[134]:


X_val = val[ten]


# In[135]:


y_val = val['Class']


# In[136]:


X_test = test[ten]


# In[137]:


y_test = test['Class']


# Habiendo ya creado las distintas matrices X necesarias, así como los vectores y, podemos proceder a trabajar con los modelos.
# 
# 
# #### 1. KNN Neighbours:

# In[138]:


knn = neighbors.KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)
predicted = knn.predict(X_val)


# In[139]:


print("Accuracy: %s" % metrics.balanced_accuracy_score(y_val, predicted))
print("Confusion matrix:")
plt.figure(figsize = (10,8))
sns.set_style('dark')
sns.set_palette('hls', 100)
sns.set_context('paper', font_scale = 1.5)
sns.heatmap(metrics.confusion_matrix(y_val, predicted), annot=True)
plt.show()


# El rendimiento de este clasificador de KNN Neighbours es de 59%. Como se ve en el mapa de calor, si bien hay muchas a las cuales se le achunta, hay muchísimas observaciones, a las que no lo estamos logrando *achuntar*, esperamos encontrar mejoras en los siguientes modelos.

# #### 2. Decision Tree Classifier:

# In[144]:


from sklearn.tree import DecisionTreeClassifier

tree = DecisionTreeClassifier(max_depth=100)
tree.fit(X_train, y_train)
predicted = tree.predict(X_val)


# In[145]:


print("Accuracy: %s" % metrics.accuracy_score(y_val, predicted))
print("Confusion matrix:")
plt.figure(figsize = (10,8))
sns.set_style('dark')
sns.set_palette('hls', 100)
sns.set_context('paper', font_scale = 1.5)
sns.heatmap(metrics.confusion_matrix(y_val, predicted), annot=True)
plt.show()


# Mejoramos claramente el nivel de precisión, ahora alcanza un nivel de 62,4%. Por ahora es preferible un Árbol de Decisión que un modelo del tipo KNN Neighbours. Debiera mejorar aún más la capacidad de achuntar a la data de validación, con los nuevos modelos a utilizar.
# 
# #### 3. Random Forest Classifier:
# 
# Este modelo debiera si o sí, tener una mejor precisión que los otros modelos ya utilizados. Esto porque en general la precisión mejora, cuando se pasa de un Árbol de Decisión a un Random Forest, ya que en cierto sentido un modelo de Random Forest es como el promedio de resultados de múltiples árboles de decisión.

# In[158]:


from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(n_estimators=100) #numero de arboles
forest.fit(X_train, y_train)
predicted = forest.predict(X_val)


# In[159]:


print("Accuracy: %s" % metrics.accuracy_score(y_val, predicted))
print("Confusion matrix:")

plt.figure(figsize = (10,8))
sns.set_style('dark')
sns.set_palette('hls', 100)
sns.set_context('paper', font_scale = 1.5)
sns.heatmap(metrics.confusion_matrix(y_val, predicted), annot=True)
plt.show()


# Efectivamente mejoró la precisión, este modelo de Random Forest Classifier con 10 árboles, entrega un nivel de aciertos de la data de validación de 66,02%. Por ahora, este es nuestro modelo preferido.
# 
# **4.1 Support Vector Machine (kernel = linear):**
# 
# Por lo que revisé en los libros y en internet, un modelo de SVM varía mucho según el kernel que se utilice, por ello estudiaremos la efectividad de este modelo con sus tres kernels posibles.

# In[160]:


from sklearn.svm import SVC


# In[161]:


#svm = SVC(kernel='linear')
#svm.fit(X_train, y_train)
#predicted = svm.predict(X_val)


# In[162]:


#Medidas de rendimiento
#print("Accuracy: %s" % metrics.accuracy_score(y_test, predicted))
#print("Balanced accuracy: %s" % metrics.balanced_accuracy_score(y_test, predicted))
#print("Confusion matrix:")
#plt.figure(figsize = (10,8))
#sns.set_style('dark')
#sns.set_palette('hls', 100)
#sns.set_context('paper', font_scale = 1.5)
#sns.heatmap(metrics.confusion_matrix(y_val, predicted), annot=True)
#plt.show()


# Lamentablemente este modelo no logró correrse en mi computador... Esperé mucho rato y nunca se terminó de ejecutar. Quizás en otro computador podría ver como se comporta el SVM con kernel lineal.

# **4.2 Support Vector Machine (kernel = poly):**

# In[163]:


svm = SVC(kernel='poly')
svm.fit(X_train, y_train)
predicted = svm.predict(X_val)


# In[164]:


#Medidas de rendimiento
print("Accuracy: %s" % metrics.accuracy_score(y_val, predicted))
print("Balanced accuracy: %s" % metrics.balanced_accuracy_score(y_val, predicted))
print("Confusion matrix:")
plt.figure(figsize = (10,8))
sns.set_style('dark')
sns.set_palette('hls', 100)
sns.set_context('paper', font_scale = 1.5)
sns.heatmap(metrics.confusion_matrix(y_val, predicted), annot=True)
plt.show()


# Este modelo tiene una capacidad de acierto relativamente baja, en comparación a los otros modelos vistos anteriormente. Tanto el *achunte* normal como el balanceado, con suerte superan el 50% (accuracy de 51,8%). Es interesante además notar que su capacidad de predecir cuando una acción es de la clase 0 es bastante nula, mientras que el modelo sin importar los features de la observación que ve, predice que esta es de Clase 1.
# 
# Dada la baja accuracy, casi que es preferible lanzar una moneda, que usar este modelo para predecir la Clase de la acción... Es posible, que el modelo no sea bien usado en este caso o que haya un problema en los features usados, que impiden calibrar y llevar a cabo un buen modelo.

# **4.3 Support Vector Machine (kernel = rbf):**

# In[165]:


svm = SVC(kernel='rbf')
svm.fit(X_train, y_train)
predicted = svm.predict(X_val)


# In[166]:


#Medidas de rendimiento
print("Accuracy: %s" % metrics.accuracy_score(y_val, predicted))
print("Balanced accuracy: %s" % metrics.balanced_accuracy_score(y_val, predicted))
print("Confusion matrix:")
plt.figure(figsize = (10,8))
sns.set_style('dark')
sns.set_palette('hls', 100)
sns.set_context('paper', font_scale = 1.5)
sns.heatmap(metrics.confusion_matrix(y_val, predicted), annot=True)
plt.show()


# Este modelo de SVM con kernel `rbf`, no mejora en comparación al otro SVM con kernel del tipo `poly` este igual tiene un accuracy bastante reducido. Este caso es más preferible lanzar una moneda, que creer en nuestro modelo, que el caso anterior. Aún preferimos el Clasificador de Random Forest.
# 
# #### 5. Red Neuronal:

# In[167]:


from sklearn.neural_network import MLPClassifier


# In[168]:


mlp = MLPClassifier(hidden_layer_sizes=(100,), max_iter=10000) # 10
mlp.fit(X_train, y_train)
predicted = mlp.predict(X_val)


# In[169]:


#Medidas de rendimiento
print("Accuracy: %s" % metrics.accuracy_score(y_val, predicted))
print("Confusion matrix:")
plt.figure(figsize = (10,8))
sns.set_style('dark')
sns.set_palette('hls', 100)
sns.set_context('paper', font_scale = 1.5)
sns.heatmap(metrics.confusion_matrix(y_val, predicted), annot=True)
plt.show()


# Este modelo de Red Neuronal (MLP) con tamaño 100 para las Hidden Layers, tampoco logra superar al Random Forest. Tiene una capacidad de acierto que supera el 50%, alcanzando un valor de 54%, pero no por mucho. 
# 
# Este modelo, no repele una clase en particular (como pasaba con los SVM con Kernel `poly` con la clase 0), sino que este modelo predice que las acciones son de clase cero, cuando lo son y cuando no lo son. Y también predice que acciones son de la clase 1, cuando son y también cuando no lo son.
# 
# #### 6. Regresión Logística:
# 

# In[170]:


from sklearn.linear_model import LogisticRegression


# In[171]:


model = LogisticRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_val)
accuracy = metrics.accuracy_score(y_val, predictions)    


# In[172]:


print("Accuracy: %s" % metrics.accuracy_score(y_val, predictions))
print("Confusion matrix:")
plt.figure(figsize = (10,8))
sns.set_style('dark')
sns.set_palette('hls', 100)
sns.set_context('paper', font_scale = 1.5)
sns.heatmap(metrics.confusion_matrix(y_val, predictions), annot=True)
plt.show()


# Notamos que este modelo tiene una capacidad de acierto que supera por bastante más el 50%. La *accuracy* de nuestro modelo de regresión logística es de 56.7%. Este modelo es preferible a nuestro modelo de 5 de Red Neuronal, a los dos SVM ejecutados y a el modelo KNN , sin embargo, aún se prefiere un modelo de árbol.
# 
# Luego de haber revisado cada uno de estos modelos, podemos concluir que **el mejor modelo es el Random Forest Classifier** con 100 árboles. Este modelo es nuestro ganador. Veamos como se comporta a la hora de intentar predecir la data de testeo.
# 
# ### Ganador: Random Forest (en Testeo)

# In[193]:


forest2 = RandomForestClassifier(n_estimators=100)
forest2.fit(X_train, y_train)
predicted = forest2.predict(X_test)


# In[194]:


print("Accuracy: %s" % metrics.accuracy_score(y_test, predicted))
print("Confusion matrix:")

plt.figure(figsize = (10,8))
sns.set_style('dark')
sns.set_palette('hls', 100)
sns.set_context('paper', font_scale = 1.5)
sns.heatmap(metrics.confusion_matrix(y_test, predicted), annot=True)
plt.show()


# Notamos que nuestro modelo ganador de `Random Forest` con 100 árboles, generaliza bastante bien la data de testeo. Tiene un porcentaje de acierto o *achunte* de al rededor de 66.32%. 
# 
# **Comentarios Generales M4:**
# 
# En primer lugar, debo decir que fue muy interesante y entretenido ver el funcionamiento y los resultados de cada uno de los distintos modelos representados. Sin embargo, a la vez fue bastante frustrante notar que con las 8 features usadas, que esperaba que íbamos a poder predecir perfectamente que acción era recomendable de comprar o no, el modelo no fue tan poderoso. Este problema se podría arreglar con más features o con más datos. Más datos no podemos conseguir, pero lo que sí podríamos hacer es ampliar o cambiar el set de columnas utilizados para armar la matriz `X`. Pese a que se consideró la opción, se guardaron las ganas de esto para la misión 5, que busca más que nada variar el número de columnas utilizadas y encontrar las 10 mejores para incluir.

# ## Misión 5: Selección de mejores features

# Para esta misión se hará lo siguiente: Se realizarán 10 *for loops*, en que en cada uno de ellos se irá añadiendo una nueva variable o feature a la regresión (se utilizará regresión lineal en esta sección, esto porque como la variable `Return` es continua, me pareció un buen modelo a utilizar), dependiendo cual entrega la mayor el mayor R^2 al añadirse a la regresión.
# 
# La dinámica será la siguiente: 
# 
# - Partimos con cero features, por lo que el primer for loop, entrenará un modelo de regresión lineal con un solo feature. Se recorrerá cada una de las columnas (válidas a utilizar) y se guardará el nombre de la columna que tenga la mayor accuracy al ser feature de la regresión.
# 
# - Luego cuando ya se tenga una variable, se procederá a hacer el segundo *for loop*. En este se recorrerá cada una de las columnas y se entrenará un modelo de regresión lineal. **El modelo que tenga el menor Error Cuadrático Medio** (E.C.M), **en la data de validación** nos señalará cual es la segunda feature a considerar.
# 
# - Luego se repite el mismo proceso hasta tener un modelo de regresión lineal con 10 features.
# 
# 
# Primero debo agrupar las columnas que puedo utilizar como features. Estas serían todas las de la base de datos menos `Return` (variable y), `Class` (tengo entendido que no era legal usarla, sino lo aplico como supuesto) y el nombre de la acción tampoco la consideraremos.
# 
# Hay que tener ojo en *for loops* avanzados, en no agregar columnas a la regresión que ya han sido añadidas, así no tenemos problemas de Independencia lineal.

# In[226]:


options = []
for col in train.columns:
    if col != "Return" and col != "Class":
        options.append(col)


# Habiendo ya agrupado las posibles opciones de features en la lista `options` podemos proceder a entrenar los 10 modelos. Aprovecho de crear una función que haga más elegantes los for loops futuros.

# In[227]:


from sklearn.linear_model import LinearRegression

def regresion(X_t, y_t, X_v, y_v):
    model = LinearRegression()
    model.fit(X_t, y_t)
    predictions = model.predict(X_v)
    accuracy = metrics.mean_squared_error(y_v, predictions) 
    return accuracy


# Notamos que para correr un modelo de regresión es necesario que la matriz X, ya sea de entrenamiento o de validación tenga más de una columna. Agregamos entonces una columna de unos a cada vector X, y así tenemos armada la matriz X de features. 

# In[228]:


y_t = train["Return"]
y_v = val["Return"]

dimt = train.shape[0]
beta_0t = pd.Series(np.ones(dimt))

dimv = val.shape[0]
beta_0v = pd.Series(np.ones(dimv))


# Además aprovecho de definir desde ya, la lista de mejores variables. Se usa una lista, para tener a estas ordenadas de mejor a peor.

# In[229]:


ganadoras = []


# In[230]:


minimo = np.inf
col_ganadora = []
for col in options:
    X_t = train[col]
    X_t = pd.concat([beta_0t, X_t], axis=1)
    X_v = val[col]
    X_v = pd.concat([beta_0v, X_v], axis=1)  
    acc = regresion(X_t, y_t, X_v, y_v)
    if acc < minimo:
        minimo = acc  
        col_ganadora.append(col)
        
winner = col_ganadora[-1]
ganadoras.append(winner)
winner


# Claramente el último elemento añadido a la lista, es el que tiene el menor ECM. Esto significa, que el modelo con la última variable añadida a la lista `col_ganadora`, que se llama `ROE`, entrenado con la data de entrenamiento de esa columna y validada con la data de validación, es la mejor feature para explicar `Return`.
# 
# En lo siguiente haremos nuevamente el mismo proceso, solo que ahora se entrenará un modelo que ya contiene nuestra variable ganadora en el primer loop, en este caso la variable `ROE`.

# In[231]:


col1t = train["ROE"]
col1v = val["ROE"]

minimo = np.inf
col_ganadora = []
for col in options:
    X_t = train[col]
    X_t = pd.concat([beta_0t, col1t, X_t], axis=1)
    X_v = val[col]
    X_v = pd.concat([beta_0v, col1v, X_v], axis=1)  
    acc = regresion(X_t, y_t, X_v, y_v)
    if acc < minimo:
        minimo = acc  
        col_ganadora.append(col)
        
winner = col_ganadora[-1]
ganadoras.append(winner)
winner


# Nuestra segunda columna ganadora, es `Free Cash Flow Yield`. Esta columna, no la teníamos contemplada como *importante* en la Misión 1, , sin embargo si se había contemplado que `Free Cash Flow` sola, podría ser una variable importante (tan mal no estabamos jaja). Esta columna, es la segunda columna más fuerte a la hora de predecir nuestra variable `Return`. Ad
# 
# Hacemos nuevamente el mismo proceso que antes, para encontrar la tercera mejor variable.

# In[232]:


col2t = train["Free Cash Flow Yield"]
col2v = val["Free Cash Flow Yield"]

minimo = np.inf
col_ganadora = []
for col in options:
    X_t = train[col]
    X_t = pd.concat([beta_0t, col1t, col2t, X_t], axis=1)
    X_v = val[col]
    X_v = pd.concat([beta_0v, col1v, col2v, X_v], axis=1)  
    acc = regresion(X_t, y_t, X_v, y_v)
    if acc < minimo:
        minimo = acc  
        col_ganadora.append(col)
        
winner = col_ganadora[-1]
ganadoras.append(winner)
winner


# La tercera columna ganadora, es `Preferred Dividends`. Lamentablemente esta columna, tampoco fue de las 10 seleccionadas en la Misión 1. Pero igual se sabía que los dividendos tendrían un rol importante para explicar el retorno, por ello se había usado la variable `Dividend per Share`.

# In[233]:


col3t = train["Preferred Dividends"]
col3v = val["Preferred Dividends"]

minimo = np.inf
col_ganadora = []
for col in options:
    X_t = train[col]
    X_t = pd.concat([beta_0t, col1t, col2t, col3t, X_t], axis=1)
    X_v = val[col]
    X_v = pd.concat([beta_0v, col1v, col2v, col3v, X_v], axis=1)  
    acc = regresion(X_t, y_t, X_v, y_v)
    if acc < minimo:
        minimo = acc  
        col_ganadora.append(col)
        
winner = col_ganadora[-1]
ganadoras.append(winner)
winner


# Nuestra cuarta columna ganadora es `cashRatio`. Esta es otra columna, que no teníamos incorporada desde la misión 1, pero que tiene mucho que ver con la variable que habíamos contemplado `Free Cash Flow`.
# 
# Veamos que pasa con las siguientes variables.

# In[234]:


col4t = train["cashRatio"]
col4v = val["cashRatio"]

minimo = np.inf
col_ganadora = []
for col in options:
    X_t = train[col]
    X_t = pd.concat([beta_0t, col1t, col2t, col3t, col4t, X_t], axis=1)
    X_v = val[col]
    X_v = pd.concat([beta_0v, col1v, col2v, col3v, col4v, X_v], axis=1)  
    acc = regresion(X_t, y_t, X_v, y_v)
    if acc < minimo:
        minimo = acc  
        col_ganadora.append(col)
        
winner = col_ganadora[-1]
ganadoras.append(winner)
winner


# La quinta columna ganadora es `Payables`. Sigamos.

# In[235]:


col5t = train["Payables"]
col5v = val["Payables"]

minimo = np.inf
col_ganadora = []
for col in options:
    X_t = train[col]
    X_t = pd.concat([beta_0t, col1t, col2t, col3t, col4t, col5t, X_t], axis=1)
    X_v = val[col]
    X_v = pd.concat([beta_0v, col1v, col2v, col3v, col4v, col5v, X_v], axis=1)  
    acc = regresion(X_t, y_t, X_v, y_v)
    if acc < minimo:
        minimo = acc  
        col_ganadora.append(col)
        
winner = col_ganadora[-1]
ganadoras.append(winner)
winner


# La sexta feature ganadora es `Effect of forex changes on cash`. Sigamos.

# In[236]:


col6t = train["Effect of forex changes on cash"]
col6v = val["Effect of forex changes on cash"]

minimo = np.inf
col_ganadora = []
for col in options:
    X_t = train[col]
    X_t = pd.concat([beta_0t, col1t, col2t, col3t, col4t, col5t, col6t, X_t], axis=1)
    X_v = val[col]
    X_v = pd.concat([beta_0v, col1v, col2v, col3v, col4v, col5v, col6v, X_v], axis=1)  
    acc = regresion(X_t, y_t, X_v, y_v)
    if acc < minimo:
        minimo = acc  
        col_ganadora.append(col)
        
winner = col_ganadora[-1]
ganadoras.append(winner)
winner


# La séptima feature es `Tax assets`. Sigamos.

# In[237]:


col7t = train["Tax assets"]
col7v = val["Tax assets"]

minimo = np.inf
col_ganadora = []
for col in options:
    X_t = train[col]
    X_t = pd.concat([beta_0t, col1t, col2t, col3t, col4t, col5t, col6t, col7t, X_t], axis=1)
    X_v = val[col]
    X_v = pd.concat([beta_0v, col1v, col2v, col3v, col4v, col5v, col6v, col7v, X_v], axis=1)  
    acc = regresion(X_t, y_t, X_v, y_v)
    if acc < minimo:
        minimo = acc  
        col_ganadora.append(col)
        
winner = col_ganadora[-1]
ganadoras.append(winner)
winner


# La octava feature es `10Y Revenue Growth (per Share)`. Seguimos.

# In[238]:


col8t = train["10Y Revenue Growth (per Share)"]
col8v = val["10Y Revenue Growth (per Share)"]

minimo = np.inf
col_ganadora = []
for col in options:
    X_t = train[col]
    X_t = pd.concat([beta_0t, col1t, col2t, col3t, col4t, col5t, col6t, col7t, col8t, X_t], axis=1)
    X_v = val[col]
    X_v = pd.concat([beta_0v, col1v, col2v, col3v, col4v, col5v, col6v, col7v, col8v, X_v], axis=1)  
    acc = regresion(X_t, y_t, X_v, y_v)
    if acc < minimo:
        minimo = acc  
        col_ganadora.append(col)
        
winner = col_ganadora[-1]
ganadoras.append(winner)
winner


# La novena feature es `companyEquityMultiplier`. Esta variable, podría representar lo que buscabamos explotar al agregar la variable `Goodwill and Intangible Assets` en los modelos de la misión 4. Se buscaba explotar el efecto de *inmaterial* de la compañía sobre el retorno.
# 
# Sigamos.

# In[239]:


col9t = train["companyEquityMultiplier"]
col9v = val["companyEquityMultiplier"]

minimo = np.inf
col_ganadora = []
for col in options:
    X_t = train[col]
    X_t = pd.concat([beta_0t, col1t, col2t, col3t, col4t, col5t, col6t, col7t, col8t, col9t, X_t], axis=1)
    X_v = val[col]
    X_v = pd.concat([beta_0v, col1v, col2v, col3v, col4v, col5v, col6v, col7v, col8v, col9v, X_v], axis=1)  
    acc = regresion(X_t, y_t, X_v, y_v)
    if acc < minimo:
        minimo = acc  
        col_ganadora.append(col)

winner = col_ganadora[-1]
ganadoras.append(winner)
winner


# In[240]:


ganadoras


# La décima feature es `debtEquityRatio`. Ahora que ya encontramos las 10 mejores variables, tenemos listo nuestro modelo de regresión lineal que contiene a las 10 mejores features de toda la base de datos, para predecir el retorno de una acción. Las 10 variables ganadoras son las siguientes:
# 
# 1. ROE
# 2. Free Cash Flow Yield
# 3. Preferred Dividends
# 4. cashRatio
# 5. Payables
# 6. Effect of forex changes on cash
# 7. Tax assets
# 8. 10Y Revenue Growth (per Share)
# 9. companyEquityMultiplier
# 10. debtEquityRatio
# 
# Lamentablemente, de las 10 variables que habíamos pronosticado en la Misión 1 que supuestamente eran *ultra importantes*, nos damos cuenta que esto no era así. Si bien, muchas de las columnas representaban variables parecidas a algunas por las cuales nosotros habíamos apostado, casi ninguna calzó perfectamente (solo la décima de `debtEquityRatio`.
# 
# Sobre cambios en la Misión 2, estos cambios no fueron necesarios ya que en la misión 2 se hizo un trabajo riguroso de limpieza y depuración. Si bien, podría haber sido mejor volver a la misión 2 y ser más detallista en la Limpieza, imputación y depuración de estas 10 columnas ganadoras, como lamentablemente no tengo mucho tiempo, no alcancé a hacerlo. Espero que no afecta tanto las respuestas y resultados. 
# 
# Por otro lado, de clases entendí, que no es necesario que cambie los features usados en esa misión, por lo que tampoco hice cambios en esa misión.
# 
# Ahora veamos como se comporta este modelo de 10 features con la data de testeo. Para ello debemos definir las matrices X con las 10 features respectivas y los vectores y de la data de training y de testeo.

# In[241]:


X_tr = train[ganadoras]
y_tr = train["Return"]
X_te = test[ganadoras]
y_te = test["Return"]
acc = regresion(X_tr, y_tr, X_te, y_te)
print(acc)


# El error cuadrático medio de nuestro modelo de regresión, entrenado con el set de entrenamiento `train`, en el set de testeo es de 2217,7. Esta cifra hace referencia de su capacidad de generalización.
# 
# **Comentarios Generales M5:** En esta misión se implementó una técnica, quizás no muy indicada para encontrar las 10 mejores variables. A mi gusto, es bien intuitiva y me hizo sentido su aplicación
