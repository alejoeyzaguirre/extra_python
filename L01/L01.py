#!/usr/bin/env python
# coding: utf-8

# # Laboratorio 01, José Alejo Eyzaguirre
# 
# 

# ### Importación de Librerías a usar:

# In[16]:


import random
import datetime
from datetime import datetime


# ### Definición de Parámetros Externos:
#     
# Se define `luz_exterior` y también `temperatura_exterior`. Para la medición de la luz exterior se supone que existe un sensor que mide la luz exterior sin sesgo alguno.

# In[17]:


#Dada la estructura de simulación diaria, luz exterior recibiría un integer que va creciendo a medida que transcurren la horas.

class luz_exterior:
    def __init__(self, hora):
        self.hora = hora % 24
        if 6 <= self.hora <= 12:
            self.valor = (self.hora - 6)*(100/6)
        elif 12 < self.hora <= 19:
            self.valor = (100 - (self.hora - 12)*(100/7))
        else:
            self.valor = 0

class temperatura_exterior:
    def __init__(self, medicion_Luz):
        self.L = medicion_Luz
        self.temp = self.L * (3/10) + random.randint(-10, 10)

luz_ext = luz_exterior(16).valor
print(luz_ext)

#Suponiendo que tenemos un sensor que mide sin sesgo la luz exterior.
temp_ext = temperatura_exterior(luz_ext).temp
print(temp_ext)


# ## Creación de Objetos (Plantas)
# Se crea el objeto `planta` y sus respectivas subclases, `tomate`, `lechuga`y `cilantro`. 
# 
# Cada planta tiene el método cosechar y crecer. El primero de estos disminuye el tamaño **n** de cada planta. Solo en el caso de los tomates existen condiciones para esta cosecha.
# 
# Por otro lado, la planta crece (método de cada planta) a medida que tiene un nivel de humedad que esta a menos de 20 puntos de la humedad óptima, esta no puede ser ni tan alta ni tan baja, sino no crece. Además las plantas crecen de noche, por lo que solo crece cuando se esta oscuro. Si se cumplen estas condiciones, por cada hora la lechuga obtiene una un cuarto de hoja. Análogamente, si se cumplen estas condiciones, la planta tomate obtendrá 0.25 tomates nuevos por hora, sin importar su tipo. Además el tomate se pone cada vez menos ácido a medida que crece, cayendo el porcentaje de esta a medida que crece en un 1% por cada hora de crecimiento. Lo mismo con el cilantro, si las mismas condiciones se cumplen la planta de cilantro gana 0.25 ramas nuevas por hora.
# 
# (Supuesto, las plantas no mueren. Si tienen humedad cero, aún siguen vivas.)

# In[31]:



class planta:
    
    def __init__(self, fecha_plantacion, humedad_optima, humedad_actual):
        #Ingresar fecha como un str del tipo, '03-10-2020'
        self.fecha_plantacion = datetime.strptime(fecha_plantacion, '%d-%m-%Y')
        self.humedad_optima = humedad_optima
        self.humedad_actual = humedad_actual
        self.total_cosechado = 0
    
    def cosechar(self, numero, h):
        pass
    
    def crecer(self):
        pass


class lechuga(planta):
    def __init__(self, fecha_plantacion, humedad_optima, humedad_actual, n_hojas):
        super().__init__(fecha_plantacion, humedad_optima, humedad_actual)
        self.n_hojas = n_hojas
        if self.n_hojas > 40:
            self.tamano = "grande"
        elif 10<= self.n_hojas <= 40:
            self.tamano = "mediana"
        else:
            self.tamano = "chica"

    def cosechar(self, hojas_extraidas, h):
        
        #No pesco la hora.
        if self.n_hojas > hojas_extraidas:
            self.n_hojas = self.n_hojas - hojas_extraidas
            self.total_cosechado += hojas_extraidas
        else:
            self.n_hojas = 0
            self.total_cosechado += self.n_hojas
        return True
    
        if self.n_hojas > 40:
            self.tamano = "grande"
        elif 10<= self.n_hojas <= 40:
            self.tamano = "mediana"
        else:
            self.tamano = "chica"

    def crecer(self, h):
        if (self.humedad_optima - 20 < self.humedad_actual < self.humedad_optima + 20) and ((h % 24)>19) or ((h % 24)<= 6):
            self.n_hojas += 0.25
        #Actualizamos tamaño de lechuga.
        if self.n_hojas > 40:
            self.tamano = "grande"
        elif 10<= self.n_hojas <= 40:
            self.tamano = "mediana"
        else:
            self.tamano = "chica"
        

class tomate(planta):
    """tomate es una planta específica, HERENCIA"""

    def __init__(self, fecha_plantacion, humedad_optima, humedad_actual, raza, n_tomates, acidez):
        super().__init__(fecha_plantacion, humedad_optima, humedad_actual)
        self.raza = raza
        self.n_tomates = n_tomates
        self.acidez = float(acidez)

    def cosechar(self, num_extraido, h):
        h1 = h % 24
        #ahora = datetime.datetime.now() #Para calcular la hora actual, pero acá se tiene que usar h así que no se usa.
        
        if num_extraido >= self.n_tomates:
            #print("No se pueden sacar más tomates de los que se tienen, lo siento."
            pass
        
        elif self.raza == "normal":
            self.n_tomates = self.n_tomates - num_extraido
            self.total_cosechado += num_extraido
            #print("Cosecho tomate normal")
            return True
        
        elif self.raza == "cherry" and h1 < 12:
            #print("No se puede cosechar a esta hora un Tomate Cherry, avíspate")
            pass
        
        elif self.raza == "cherry" and h1 >= 12:
            #print("SÍ Cosecho Cherry")
            self.n_tomates = self.n_tomates - num_extraido
            self.total_cosechado += num_extraido
            return True

    def crecer(self, h):
        if (self.humedad_optima - 20 < self.humedad_actual < self.humedad_optima + 20) and ((h % 24)>19) or ((h % 24)<= 6):
            self.n_tomates += 0.25
            if self.acidez - 0.01 >= 0:
                self.acidez -= 0.01


class cilantro(planta):

    def __init__(self, fecha_plantacion, humedad_optima, humedad_actual, n_ramas):
        super().__init__(fecha_plantacion, humedad_optima, humedad_actual)
        self.n_ramas = n_ramas

    def cosechar(self, num_extraido,h):
        if num_extraido > self.n_ramas:
            #print("No se pueden sacar más ramas de las que se tienen... falta tiempo")
            pass

        else:
            self.n_ramas = self.n_ramas - num_extraido
            self.total_cosechado += num_extraido
            return True

    def crecer(self, h):
        if (self.humedad_optima - 20 < self.humedad_actual < self.humedad_optima + 20) and ((h % 24)>=19) or ((h % 24)<= 6):
            self.n_ramas += 0.25


# In[32]:


#Cuadro para probar la funcionalidad de las plantas.

args_l = ['04-12-2018', 25, 40, 39.9]
l1 = lechuga(*args_l)
print(l1.n_hojas)
print(l1.tamano)

args_t1 = ['06-01-2019', 40, 32, "cherry", 32, 0.5]
t1 = tomate(*args_t1)

args_t2 = ['26-05-2018', 50, 21, "normal", 13, 0.8]
t2 = tomate(*args_t2)

args_c = ['24-10-2019', 37, 12.54564, 58]
c1 = cilantro(*args_c)
h = 21
print(h%24)
print(l1.humedad_optima -20)
print(l1.humedad_actual)
print(l1.humedad_optima + 20)

l1.crecer(21)
l1.crecer(22)
l1.crecer(23)
l1.crecer(24)


print(l1.n_hojas)
print(l1.tamano)

l1.cosechar(l1.n_hojas/5, 342)
print(l1.n_hojas)
print(l1.tamano)


# ### Creación de Objetos (Sensor)
# Se crea el objeto `Sensor` y sus respectivas subclases: Sensor de `Humedad`, Sensor de`Temperatura` y de `Luz`. Cada sensor sigue las recomendaciones dadas en el enunciado. Sin embargo, se tiene ojo con no entregar resultados de medición ilógicos, en el sentido que no se escapen de los valores posibles que puede tener cada medición.
# 
# En el caso del sensor de temperatura, se asume que este esta sesgado al alza. En otras palabras, se asume que en el interior del invernadero existe una temperatura mayor a la del exterior, y por eso en cada medición se **suma** un número aleatorio entre uno y cinco.

# In[33]:




class sensor:
    def __init__(self, planta):
        self.planta = planta
        self.ultima_medicion = 0

    def medir(self, parametro_exterior):
        pass


class humedad(sensor):
    """Sensor de Humedad"""

    def __init__(self, planta):
        super().__init__(planta)
        self.ultima_medicion = planta.humedad_actual

    def medir(self, humedad_exterior=0):
        # No existe data sobre la humedad exterior
        #print("Esto es la última medicion de humedad" + str(self.ultima_medicion))
        #print("Ultima medicion humedad " +str(planta.humedad_actual))
        dev = planta.humedad_actual - random.randint(1, 30)
        #print("Esto es dev " + str(dev) )
        if dev >= 0:
            #print("Medicion Humedad Común y Corriente")
            self.ultima_medicion = dev
            planta.humedad_actual = dev
            return dev
        else:
            self.ultima_medicion = 0
            planta.humedad_actual = 0
            return 0


class temperatura(sensor):
    """Sensor de Temperatura"""

    def medir(self, temperatura_exterior):
        dev = temperatura_exterior + random.randint(1, 5)
        while not -30 < dev < 50:
            dev = temperatura_exterior + random.randint(1, 5)

        self.ultima_medicion = dev
        return dev

class luz(sensor):
    """Sensor de Luz interna del Invernadero."""

    def medir(self, luz_exterior):
        dev = luz_exterior + random.randint(5, 10)
        # print("Esta es DEV " + str(dev) )
        if dev >= 100:
            self.ultima_medicion = 100
            return 100
        elif dev <= 0:
            self.ultima_medicion = 0
            return 0
        else:
            self.ultima_medicion= dev
            return dev
   


# ### Creación de Objetos (Regador)
# 
# Se crea el objeto `Regador`. Este objeto se asigna a cada planta y vía su método _Regar_ aumenta la humedad de la planta que riega. Al ser la sugerencia del enunciado bastante lógica, se toma esta, pero con modificaciones, como dada. Entonces la planta será regada si y solo sí la luz externa es mayor o igual a **40**, la temperatura **exterior** es mayor a **10** grados celsius y cuando la humedad de esta es menor a **60** (en el enunciado se sugiere, regar cuando es menor a 12, a mi gusto es preferible no dejar que la humedad de las plantas baje tanto, y que se aproveche de regar cuando es posible.). 
# 
# Como los regadores no son todos iguales y a veces hay más o menos presión, la humedad de la planta aumenta en un valor aleatorio entre 10 y 30.

# In[34]:


class regador:
    
    def __init__(self, planta):
        self.planta = planta

    
    def regar(self, hora):
        
        # print("Luz " + str(luz_exterior(hora).valor))
        antes = self.planta.humedad_actual
         
        if luz_exterior(hora).valor >= 40 and self.planta.humedad_actual < 60 and temperatura_exterior(luz_exterior(hora).valor).temp > 10:
            # print("En esto AUMENTA la humedad  " + str(hora) +"  "+ str(temperatura_exterior(luz_exterior(hora).valor).temp))
            aleatorio = random.randint(10, 30)
            if self.planta.humedad_actual + aleatorio <= 100:
                self.planta.humedad_actual += aleatorio
                
            else:
                self.planta.humedad_actual = 100
            
            return True
                        


# ### Creación del Objeto Invernadero
# 
# Se crea el invernadero en sí. Este objeto contiene dentro sensores, plantas, regadores. Además dentro de el los parámetros pueden ser distintos a los de afuera.
# 
# Dentro de esta clase, se crearon distintos atributos que tienen la forma de diccionarios, para facilitar el orden de la información del invernadero. Se creó un diccionario para cada tipo de sensor y para cada tipo de regador, donde el valor es el sensor o regador mismo y la llave el ID de la planta que mide. También se creo un diccionario que cuenta la cantidad de Lechugas, Tomates y Cilantros que hay en el invernadero (en este caso el ID es la llave y el valor corresponde al número de plantas de ese tipo que hay dentro de este). Por último, el diccionario más importante es el que tiene como llave el ID de la planta, y como valor las plantas mismas.
# 
# Se utilizar el método __repr__ para que cuando se imprima un objeto del tipo invernadero, aparezca de inmediato el número de plantas que tiene de cada tipo.

# In[35]:


class invernadero:
    """Construcción que contiene plantas, que se encuentran plantadas en su interior."""
    
    def __init__(self):
        self.last_id = 0
        self.plantas_dict = dict()
        self.contador = dict()
        self.sensores_hum = dict()
        self.sensores_temp = dict()
        self.sensores_luz = dict()
        self.regadores = dict()
        self.num_lechugas = 0
        self.num_tomates = 0
        self.num_cilantros = 0
        self.contador["Lechugas"] = 0
        self.contador["Tomates"] = 0
        self.contador["Cilantros"] = 0

    def nueva_lechuga(self, fecha_plantacion, humedad_optima, humedad_actual, n_hojas):
        self.last_id += 1
        self.num_lechugas += 1
        self.contador["Lechugas"] += 1
        l = lechuga(fecha_plantacion, humedad_optima, humedad_actual, n_hojas)
        self.plantas_dict.update({self.last_id: l})
        #Creo un sensor de cada tipo para esta lechuga y lo agrego al diccionario.
        self.sensores_hum.update({self.last_id :humedad(l)})
        self.sensores_temp.update({self.last_id: temperatura(l)})
        self.sensores_luz.update({self.last_id: luz(l)})
        self.regadores.update({self.last_id: regador(l)})

        

    def nuevo_tomate(self, fecha_plantacion, humedad_optima, humedad_actual, raza, n_tomates, acidez):
        self.last_id += 1
        self.num_tomates += 1
        self.contador["Tomates"] += 1
        t = tomate(fecha_plantacion, humedad_optima, humedad_actual, raza, n_tomates, acidez)
        self.plantas_dict.update({self.last_id: t})
        self.sensores_hum.update({self.last_id :humedad(t)})
        self.sensores_temp.update({self.last_id: temperatura(t)})
        self.sensores_luz.update({self.last_id: luz(t)})
        self.regadores.update({self.last_id: regador(t)})

    def nuevo_cilantro(self, fecha_plantacion, humedad_optima, humedad_actual, n_ramas):
        self.last_id += 1        
        self.num_cilantros += 1
        self.contador["Cilantros"] += 1
        c = cilantro(fecha_plantacion, humedad_optima, humedad_actual, n_ramas)
        self.plantas_dict.update({self.last_id: c})
        self.sensores_hum.update({self.last_id :humedad(c)})
        self.sensores_temp.update({self.last_id: temperatura(c)})
        self.sensores_luz.update({self.last_id: luz(c)})
        self.regadores.update({self.last_id: regador(c)})
        
    def __repr__(self):
        s = self.__doc__  # esto retorna el string del comienzo de la clase, la documentación que la describe
        return s + "\n" + "\n".join(
            "Tipo de Planta: {} | Cantidad: {}".format(planta, self.contador[planta]) for planta in self.contador.keys())


# ### Simulación
# 
# Se crea la simulación de nuestro invernadero. Se inicializan distintas plantas que pueden ser reinicializadas con valores de parámetros seleccionados de manera aleatoria. Estas plantas creadas son agregadas a el Invernadero.
# Luego se pregunta por el número de días a considerar en la simulación. La simulación asume que se parte en un día a las 00:00, luego a medida que van transcurriendo las horas, el invernadero empieza a tener acción.
# 
# En la simulación se crean 4 plantas de cada tipo posible, una lechuga, un tomate cherry, un tomate normal y un cilantro. Los parámetros de cada una de estas plantas fueron seleccionados arbitrariamente, pero el algoritmo funciona con cualquier set de parámetros, siempre y cuando cumpla con los requisitos de cada variable pedida.
# 
# Se consideró en el invernadero creado, que solo se mediría la humedad 6 veces al día, cada 4 horas, y no a toda hora. Por último, algunos puntos de decisión importantes sobre la cosecha son que:
# 1. La humedad de la planta se debe encontrar entre la humedad óptima de la planta más 20 y esta misma pero menos 20.
# 2. La planta debe tener un número de hojas, tomates o ramas mayor a 10.
# 3. Cada vez que se cosecha se extraen solo la mitad de las hojas, tomates o ramas de la planta.

# In[39]:


# Defino mi invernadero (clase).
inv1 = invernadero()
# Definir plantas, sensores y regadores respectivos... crearlos, darles vida. Los agrego a mi invernadero.
# Justo antes de hoy a las 00:00 cada una de estas plantas tiene un cierto tamaño
args_l = ['04-12-2018', 78, 40, 40]
inv1.nueva_lechuga(*args_l)

args_t1 = ['06-01-2019', 89, 53, "cherry", 32, 0.5]
inv1.nuevo_tomate(*args_t1)

args_t2 = ['26-05-2018', 91, 45, "normal", 13, 0.8]
inv1.nuevo_tomate(*args_t2)

args_c = ['24-10-2019', 30.21, 90, 58]
inv1.nuevo_cilantro(*args_c)

print(inv1)

dias_a_simular = int(input("¿Cuántos días desea que dure la simulación?"))
hora = 0
# Parto hoy a las 00:00 de la noche.
while hora <= dias_a_simular * 24:
    h = hora % 24
    # Evalúo parámetros
    l_ext = luz_exterior(h).valor
    # Suponiendo que tenemos un sensor que mide sin sesgo la luz exterior.
    t_ext = temperatura_exterior(l_ext).temp
    # Para cada planta del invernadero: Evaluar su nivel de los sensores. Actualizar sus últimas mediciones.
    for last_id in inv1.plantas_dict:
        planta = inv1.plantas_dict[last_id]
        
        #Creamos los sensores:
        sens_hum = inv1.sensores_hum[last_id]
        sens_temp = inv1.sensores_temp[last_id]
        sens_luz = inv1.sensores_luz[last_id]
        
        # Primero riego cada planta si se puede...
        inv1.regadores[last_id].regar(h)
        hum_antes = planta.humedad_actual
        if inv1.regadores[last_id].regar(h) == True and isinstance(planta, lechuga):
            print("\n---------------------------------------RIEGO---------------------------------------------" +
                  "\nSe regó la lechuga con el ID: " + str(last_id) + 
                  "\nEsta tenía un nivel de humedad de: " + str(hum_antes) + 
                  "\nAdemás tenía una temperatura de: " + str(sens_temp.ultima_medicion) + 
                  "\nPor último, estaba recibiendo un nivel de luz de: " + str(sens_luz.ultima_medicion) +
                 "\n------------------------------------------------------------------------------------")
        elif inv1.regadores[last_id].regar(h) == True and isinstance(planta, tomate):
            print("\n----------------------------------------RIEGO--------------------------------------------" +
                  "\nSe regó un tomate con el ID: " + str(last_id) + 
                  "\nEste tenía un nivel de humedad de: " + str(hum_antes) + 
                  "\nAdemás tenía una temperatura de: " + str(sens_temp.ultima_medicion) + 
                  "\nPor último, estaba recibiendo un nivel de luz de: " + str(sens_luz.ultima_medicion) +
                 "\n------------------------------------------------------------------------------------")
            
        elif inv1.regadores[last_id].regar(h) == True and isinstance(planta, cilantro):
            print("\n-----------------------------------------RIEGO-------------------------------------------" +
                  "\nSe regó un cilantro con el ID: " + str(last_id) + 
                  "\nEste tenía un nivel de humedad de: " + str(hum_antes) + 
                  "\nAdemás tenía una temperatura de: " + str(sens_temp.ultima_medicion) + 
                  "\nPor último, estaba recibiendo un nivel de luz de: " + str(sens_luz.ultima_medicion)+
                 "\n------------------------------------------------------------------------------------")
            
        # Cada planta crece...
        planta.crecer(h)
        
        # Y al final de la hora, presenta los siguientes valores, según los sensores:
        
        #MEDIR HUMEDAD SOLO CUANDO LA HORA ES MÚLTIPLO DE 6, humedad se mide 4 veces al día.
        if h % 4 == 0:           
            medicion_hum = sens_hum.medir()

        medicion_temp = sens_temp.medir(t_ext)
        medicion_luz = sens_luz.medir(l_ext)


        # if condiciones óptimas están dadas, cosechar. Si no sigue el tiempo.
        humedad_optima = planta.humedad_optima
        if (humedad_optima-20 <= medicion_hum <= humedad_optima+20):
            if isinstance(planta, lechuga) and planta.n_hojas > 10:
                planta.cosechar(planta.n_hojas/2, h)
                if planta.cosechar(planta.n_hojas/2, h) == True:
                    print("\n---------------------------COSECHA--------------------------------------------------" +
                          "\nSe cosechó una Planta del tipo Lechuga con el ID: " + str(last_id) + 
                          "\nEsta se cosechó cuando la planta tenía un nivel de humedad de: " + str(planta.humedad_actual) + 
                          "\nUna temperatura de: " + str(medicion_temp) + 
                          "\nY un nivel de luz de: " + str(medicion_luz) + 
                          "\n\nLa planta actualmente contiene: " + str(planta.n_hojas) + " hojas"
                          "\n------------------------------------------------------------------------------------")

            elif isinstance(planta, tomate) and planta.n_tomates > 10:
                planta.cosechar(planta.n_tomates/2, h)
                if planta.cosechar(planta.n_tomates/2, h) == True:
                    print("\n---------------------------COSECHA--------------------------------------------------" +
                          "\nSe cosechó una Planta del tipo Tomate " + str(planta.raza) + " con el ID: " + str(last_id) + 
                          "\nEsta se cosechó cuando la planta tenía un nivel de humedad de: " + str(planta.humedad_actual) + 
                          "\nUna temperatura de: " + str(medicion_temp) + 
                          "\nY un nivel de luz de: " + str(medicion_luz) + 
                          "\n\nLa planta actualmente contiene: " + str(planta.n_tomates) + " tomates"
                          "\n------------------------------------------------------------------------------------")
                    
            elif isinstance(planta, cilantro) and planta.n_ramas > 10:
                planta.cosechar(planta.n_ramas/2, h)
                if planta.cosechar(planta.n_ramas/2, h) == True:
                    print("\n---------------------------COSECHA--------------------------------------------------" +
                          "\nSe cosechó una planta del tipo Cilantro con el ID: " + str(last_id) + 
                          "\nEsta se cosechó cuando la planta tenía un nivel de humedad de: " + str(planta.humedad_actual) + 
                          "\nUna temperatura de: " + str(medicion_temp) + 
                          "\nY un nivel de luz de: " + str(medicion_luz) + 
                          "\n\nLa planta actualmente contiene: " + str(planta.n_ramas) + " ramas"
                          "\n------------------------------------------------------------------------------------")
                    
    hora += 1

print("\n\n\n##################################TOTALES COSECHADOS#########################################")
for last_id in inv1.plantas_dict:
    planta = inv1.plantas_dict[last_id]
    if isinstance(planta, lechuga):
        print("\nA la Lechuga con el ID " + str(last_id) + ", se le cosecharon en total: " + str(planta.total_cosechado) + " hojas.")
    
    elif isinstance(planta, tomate):
        print("\nA el Tomate " + str(planta.raza) + " con el ID " + str(last_id) + ", se le cosecharon en total: " + str(planta.total_cosechado) + " tomates.")
    
    elif isinstance(planta, cilantro):
        print("\nA el Cilantro con el ID " + str(last_id) + ", se le cosecharon en total: " + str(planta.total_cosechado) + " ramas.")
    

