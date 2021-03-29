#!/usr/bin/env python
# coding: utf-8

# # Actividad Práctica 01, José Alejo Eyzaguirre Ercilla

# ### Importación de Paquetes.

# In[1]:


import random


# Se utilizó el siguiente cuadro de código, para probar los distintos métodos del paquete random.

# In[54]:


#Este cuadro se uso para entender mejor las aleatorizaciones a realizar.

lambd = 0.2
print(random.expovariate(lambd))

ac = 0
n = 0
while n < 101:
    random.choices(["adelanto", "no adelanto"], [0.9, 0.1])
    if r == ["liviano"]:
        ac += 1
    n += 1
    
print(ac /100)
print(random.randint(0,1))

print(random.uniform(0.2,1))


# ### Clase Auto:
# 
# Se crea una clase `auto` que heredará su estructura a distintas especializaciones de esta o subclases. En particular, existen tres subclases de autos los de `carrera`, los `pesados` y los`livianos`. La cantidad que llega a la autopista de cada uno de estos esta dada por una cierta proporción.
# 
# La posición actual representa el metro en la pista en que se ubica el centro del vehículo, a modo de simplificación se supone que un auto necesita en todo momento 10 metros como "espacio vital" (el auto se encuentra en medio de estos 10 kms). Entonces cada posición será representada como el decámetro que corresponde en esta pista de 100 kms, en cada pista entonces hay 10.000 puestos, que solo pueden ser ocupados por un auto a la vez. El primer decámetro es la posición 1. Si un auto adelanta no puede estar en el mismo decámetro o posición que otro auto en la pista izquierda.

# In[59]:


class auto:
    def __init__(self, t_ingreso):
        self.t_ingreso = t_ingreso #En minutos.
        self.velocidad_promedio = 0 #En kms por hora
        self.velocidad_adelanto = 0 #En kms por hora
        self.pista_actual = "derecha"
        self.posicion_actual = 0 #En decámetros
        self.probabilidad_adelanto = 0
        
    def pos_actual(self):
        pass



# ### Subclase Auto de Carrera:
# 
# Se define la subclase auto de `carrera` que hereda de la clase auto. En esta se crean los distintos métodos con las especificaciones puntuales de este tipo de autos.
# 
# 

# In[56]:


class carrera(auto):
    def __init__(self, t_ingreso):
        super().__init__(t_ingreso)
        self.velocidad_promedio = random.randint(100, 140) #En kms por hora
        self.velocidad_adelanto = 150 #En kms por hora
        self.pista_actual = "derecha"
        self.posicion_actual = 0 #En decámetros
        self.velocidad_actual = self.velocidad_promedio
        self.probabilidad_adelanto = random.uniform(0.8, 1)
    
    #Por cada t, es decir por cada minuto, se calcula la posición del auto.
    def pos_actual(self):
        pos_actual = self.velocidad_actual*(1/60) #en kms.
        if pos_actual < 100:
            self.posicion_actual += pos_actual/100 #En decámetros.
            self.posicion_actual = int(self.posicion_actual)
            return self.posicion_actual
        else:
            self.posicion_actual = "Salió"
    
    #Condiciones de adelanto van en la misma simulación, que no haya ningún auto en la posicion actual en la pista
    #izquierda (utilizar un if) y si tiene un auto en la posición de frente, sino no puede adelantar y 
    #sigue avanzando por la pista derecha.
    
    def adelanto(self, auto_a_adelantar):
        r = random.choices(["adelanto", "no adelanto"],[self.probabilidad_adelanto, 1 - self.probabilidad_adelanto])      
        if r == "adelanto" and auto_a_adelantar.posicion_actual == self.posicion_actual + 1: #La segunda condición no es necesaria, iría en la simulación.
            self.pista_actual = "izquierda"
            self.velocidad_actual = self.velocidad_adelanto
        else: #si no adelanta se tiene que ir lento atrás del auto de enfrente.
            self.velocidad_actual = auto_a_adelantar.velocidad_actual
    
    #Defino el método de volver a la pista derecha, condiciones dadas en la simulación misma. Solo se puede volver
    #en el caso en que no haya ningún auto en la pista derecha de la autopista en esa posición (utilizar un if).
    #si no se cumple la condición debe seguir avanzando por la pista izquierda a la velocidad de adelantamiento.
    def vuelvo(self):
        self.pista_actual = "derecha"
        #Mantiene la velocidad de adelanto...


# ### Subclase Auto Liviano:
# 
# Se define la subclase auto `liviano` que hereda de la clase auto. En esta se crean los distintos métodos con las espeficaciones puntuales de este tipo de autos.

# In[58]:


class liviano(auto):
    def __init__(self, t_ingreso):
        super().__init__(t_ingreso)
        self.velocidad_promedio = random.randint(80, 120) #En kms por hora
        self.velocidad_adelanto = 130 #En kms por hora
        self.pista_actual = "derecha"
        self.posicion_actual = 0 #En decámetros
        self.velocidad_actual = self.velocidad_promedio
        self.probabilidad_adelanto = random.uniform(0.4, 0.8)
    
    #Por cada t, es decir por cada minuto, se calcula la posición del auto.
    def pos_actual(self):
        pos_actual = self.velocidad_actual*(1/60) #en kms.
        if pos_actual < 100:
            self.posicion_actual += pos_actual/100 #En decámetros.
            self.posicion_actual = int(self.posicion_actual)
            return self.posicion_actual
        else:
            self.posicion_actual = "Salió"
        
    
    #Condiciones de adelanto van en la misma simulación, que no haya ningún auto en la posicion actual en la pista
    #izquierda y si tiene un auto en la posición de al frente (utilizar un if), sino no puede adelantar y sigue avanzando por la pista derecha.
    def adelanto(self, auto_a_adelantar):
        r = random.choices(["adelanto", "no adelanto"],[self.probabilidad_adelanto, 1 - self.probabilidad_adelanto])      
        if r == "adelanto" and auto_a_adelantar.posicion_actual == self.posicion_actual + 1: #La segunda condición no es necesaria, iría en la simulación.
            self.pista_actual = "izquierda"
            self.velocidad_actual = self.velocidad_adelanto
        else: #si no adelanta se tiene que ir lento atrás del auto de enfrente.
            self.velocidad_actual = auto_a_adelantar.velocidad_actual
    
    #Defino el método de volver a la pista derecha, condiciones dadas en la simulación misma. Solo se puede volver
    #en el caso en que no haya ningún auto en la pista derecha de la autopista en esa posición (utilizar un if).
    #si no se cumple la condición debe seguir avanzando por la pista izquierda a la velocidad de adelantamiento.
    def vuelvo(self):
        self.pista_actual = "derecha"
        self.velocidad_actual = self.velocidad_promedio


# ### Subclase Auto Pesado:
# 
# Se define la subclase auto `pesado`que hereda de la clase auto. En esta se crean los distintos métodos con las espeficaciones puntuales de este tipo de autos.
# 

# In[ ]:


class pesado(auto):
    def __init__(self, t_ingreso):
        super().__init__(t_ingreso)
        self.velocidad_promedio = random.randint(70, 100) #En kms por hora
        self.velocidad_adelanto = 110 #Auto pesado no adelanta, el 110 es por la buena onda...
        self.pista_actual = "derecha"
        self.posicion_actual = 0 #En decámetros
        self.velocidad_actual = self.velocidad_promedio
        self.probabilidad_adelanto = random.uniform(0.4, 0.8) #Por la buena onda también.
    
    #Por cada t, es decir por cada minuto, se calcula la posición del auto.
    def pos_actual(self):
        pos_actual = self.velocidad_actual*(1/60) #en kms.
        if pos_actual < 100:
            self.posicion_actual += pos_actual/100 #En decámetros.
            self.posicion_actual = int(self.posicion_actual)
            return self.posicion_actual
            
        else:
            self.posicion_actual = "Salió"
    #pesado no adelanta pero sirve para asegurar que este se queda tras el auto que alcanzó a su misma velocidad.
    def adelanto(self, auto_a_adelantar):
        self.velocidad_actual = auto_a_adelantar.velocidad_actual
    
    
    


# ### Clase Autopista
# En el siguiente cuadro, se crea esta clase, que contiene dos pistas. Las pistas serán representadas por un diccionario cada una en que la llave de cada elemento es un auto y el valor es la posición en la pista (donde la posición es donde se ubica la mitad del auto). Se supone además que cada
# 
# La posición representa el metro en la pista en que se ubica el centro del vehículo, a modo de simplificación se supone que un auto necesita en todo momento 10 metros como "espacio vital" (el auto se encuentra en medio de estos 10 kms). Entonces cada posición será representada como el decámetro que corresponde en esta pista de 100 kms, en cada pista entonces hay 10.000 puestos, que solo pueden ser ocupados por un auto a la vez. El primer decámetro es la posición 1. Si un auto adelanta no puede estar en el mismo decámetro o posición que otro auto en la pista izquierda.
# 
# Para crear la autopista norte y sur, basta con crear dos objetos del tipo autopista.
# 
# En esta clase un auto es un atributo.

# In[60]:


#ingresar longitud en decámetros
class autopista:
    def __init__(self, lambda_dir, longitud):
        self.lamda_dir = lambda_dir
        
        #Diccionario en que las llaves son la posición en la pista y el valor el id del auto.
        self.pista_izquierda = dict()
        for i in range(longitud):
            self.pista_izquierda[i] = 0
        self.pista_derecha = dict()
        for i in range(longitud):
            self.pista_derecha[i] = 0
       
        self.id_autos = dict()
        self.lambda_dir = lambda_direccion
        self._id = 0
    
    #Ingresa auto cada cierto tiempo determinado por random.expovariate(lambd).
    def ingresa_auto(self, velocidad_adelanto, t):
        self._id += 1
        tipo = random.choices(["carrera", "liviano", "pesado"],[0.1, 0.5, 0.4])       
        if tipo == "liviano":
            auto1 = liviano(t)        
        elif tipo == "pesado":
            auto1 = pesado(t)        
        elif tipo == "carrera":
            auto1 = carrera(t)
        
        #Si no entró un auto recién entonces entra el auto, a modo de simplificación se supone que si hay un auto que
        #sigue en la posición 1, entonces el auto no ingresa a la carretera.
        if 1 not in self.pista_derecha.values():
            self.pista_derecha[1] = self._id
            self.id_autos[self._id] = auto1
    
    #Esta clase es más o menos un intento de hacer la simulación rapidamente...
    #Para actualizar posiciones en cada pista se utiliza este método. Es una especie método "avancen", se aplica cada minuto.
    def actualizar_pistas(self):
        
        for llave in self.id_autos.keys():                     
            auto_actual = self.id_autos[llave]
            #Si es el primer auto este avanza nomas...
            
            if llave == 1:
                posicion_ahora = auto_actual.pos_actual()
                self.pista_derecha[posicion_ahora] = llave      
            
            #OJO: Se supone que solo se puede topar con el auto de al frente!!!
            else:
                auto_adelante = self.id_autos[llave - 1]
                #Si tengo un auto justo al frente y no hay autos a la izquierda... adelanto. Reviso los posibles casos.
                if auto_adelante.posicion_actual <= auto_actual.pos_actual() and self.pista_izquierda[auto_actual.posicion_actual] == 0 and auto_actual.pista_actual == "derecha":
                    auto_actual.adelantar(auto_adelante)
                    if auto_actual.pista_actual == "izquierda": #Si efectivamente adelanta...
                        self.pista_izquierda[self._id] = auto_actual.posicion_actual
                        #Sigue en la pista izquierda avanzando.
                        if auto_actual.pos_actual() >= auto_adelante.posicion_actual and self.pista_izquierda[auto_actual.pos_actual()] == 0:
                            auto_actual.pos_actual()
                
                elif auto_adelante.posicion_actual <= auto_actual.pos_actual() and self.pista_izquierda[auto_actual.posicion_actual] == 0 and auto_actual.pista_actual == "izquierda":
                    #Caso en que va en la pista izquierda, pero se topa al auto de al frente adelantando. No alcance a hacerla, perdón!
                    pass
                
                elif auto_adelante.posicion_actual > auto_actual.pos_actual() and self.pista_izquierda[auto_actual.posicion_actual] == 0 and auto_actual.pista_actual == "izquierda":
                    auto_actual.vuelvo()                                           
                else:
                    auto_actual.pos_actual() #Auto avanza nomas.
                
            
            
            
            
            
            
            
            
        
       
            
        



        
        

