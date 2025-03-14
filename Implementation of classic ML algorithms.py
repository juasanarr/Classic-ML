#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
# ===================================================================
# Ampliación de Inteligencia Artificial, 2023-24
# PARTE I del trabajo práctico: Implementación de árboles de decisión 
#                               y random forests
# Dpto. de CC. de la Computación e I.A. (Univ. de Sevilla)
# ===================================================================


# --------------------------------------------------------------------------
# Autor(a) del trabajo:
# APELLIDOS: Sánchez Arroyo
# NOMBRE: Juan Ramón
# ----------------------------------------------------------------------------


# ****************************************************************************************
# HONESTIDAD ACADÉMICA Y COPIAS: un trabajo práctico es un examen. La discusión 
# y el intercambio de información de carácter general con los compañeros se permite, 
# pero NO AL NIVEL DE CÓDIGO. Igualmente el remitir código de terceros, OBTENIDO A TRAVÉS
# DE LA RED, o de cualquier otro medio, se considerará plagio. En particular no se 
# permiten implementaciones obtenidas con HERRAMIENTAS DE GENERACIÓN AUTOMÁTICA DE CÓDIGO. 
# Si tienen dificultades para realizar el ejercicio, consulten con el profesor. 
# En caso de detectarse plagio (previamente con aplicaciones anti-plagio o durante 
# la defensa, si no se demuestra la autoría mediante explicaciones convincentes), 
# supondrá una CALIFICACIÓN DE CERO en la asignatura, para todos los alumnos involucrados. 
# Sin perjuicio de las medidas disciplinarias que se pudieran tomar. 
# *****************************************************************************************


# MUY IMPORTANTE: 
# ===============    
    
# * NO CAMBIAR EL NOMBRE NI A ESTE ARCHIVO NI A LAS CLASES, MÉTODOS
#   Y ATRIBUTOS QUE SE PIDEN. ADEMÁS: NO HACERLO EN UN NOTEBOOK.

# * En este trabajo NO SE PERMITE USAR Scikit Learn, salvo donde se dice expresamente.
#   En particular, si se pide implementar algo, se refiere a implementar en python,
#   sin usar Scikit Learn.  
  
# * Se recomienda (y se valora especialmente) el uso eficiente de numpy. Todos 
#   los datasets se suponen dados como arrays de numpy. 

# * Este archivo (con las implementaciones realizadas), ES LO ÚNICO QUE HAY QUE ENTREGAR.

# * AL FINAL DE ESTE ARCHIVO hay una serie de ejemplos a ejecutar que están comentados, y que
#   será lo que se ejecute durante la presentación del trabajo al profesor.
#   En la versión final a entregar, descomentar esos ejemplos del final y no dejar 
#   ninguna otra ejecución de ejemplos. 



import math
import random
import numpy as np
import pandas as pd


# *****************************************
# CONJUNTOS DE DATOS A USAR EN ESTE TRABAJO
# *****************************************

# Para aplicar las implementaciones que se piden en este trabajo, vamos a usar
# los siguientes conjuntos de datos. Para cargar (casi) todos los conjuntos de datos,
# basta con tener descomprimido el archivo datos-trabajo-aia.zip (en el mismo sitio
# que este archivo) Y CARGARLOS CON LA SIGUIENTE ORDEN:
    
from carga_datos import *    

# Como consecuencia de la línea anterior, se habrán cargado los siguientes 
# conjuntos de datos, que pasamos a describir, junto con los nombres de las 
# variables donde se cargan. Todos son arrays de numpy: 


# * Conjunto de datos de la planta del iris. Se carga en las variables X_iris,
#   y_iris.  

# * Datos sobre pasajeros del Titanic y si sobrevivieron o no. Es una versión 
#   restringida de este conocido dataset, con solo tres caracteristicas:
#   Pclass, IsFemale y Age. Se carga en las variables X_train_titanic, 
#   y_train_titanic, X_test_titanic e y_test_titanic.

# * Datos sobre votos de cada uno de los 435 congresitas de Estados Unidos en
#   17 votaciones realizadas durante 1984. Se trata de clasificar el partido al
#   que pertenece un congresita (0:republicano o 1:demócrata) en función de lo
#   votado durante ese año. Se carga en las variables X_votos, y_votos (ver 
#   descripción en votos.py)


# * Datos de la Universidad de Wisconsin sobre posible imágenes de cáncer de
#   mama, en función de una serie de características calculadas a partir de la
#   imagen del tumor. Se carga en las variables X_cancer, y_cancer. 
#   Ver descripcición en sikit learn.

  
# * Críticas de cine en IMDB, clasificadas como positivas o negativas. El
#   conjunto de datos que usaremos es sólo una parte de los textos del dataset original. 
#   Los textos se han vectorizado usando CountVectorizer de Scikit Learn, con la opción
#   binary=True. Como vocabulario, se han usado las 609 palabras que ocurren
#   más frecuentemente en las distintas críticas. La vectorización binaria
#   convierte cada texto en un vector de 0s y 1s en la que cada componente indica
#   si el correspondiente término del vocabulario ocurre (1) o no ocurre (0)
#   en el texto (ver detalles en el archivo carga_datos.py). Los datos se
#   cargan finalmente en las variables X_train_imdb, X_test_imdb, y_train_imdb,
#   y_test_imdb.    


#  Además, en la carpeta datos/ se tienen los siguientes datasets, que
#  habrán de ser procesado y cargado (es decir, no se caragan directamente con
#  carga_datos.py).   
    
# * Un archivo credito.csv con datos sobre concesión de prestamos en una entidad 
#   bancaria, en función de: tipo de empleo, si ya tiene productos finacieros 
#   contratados, número de propiedades, número de hijos, estado civil y nivel de 
#   ingresos (cargarlo usando pd.read_csv en arrays de numpy X_credito e y_credito,
#   donde X_credito son las seis primeras columnas e y_credito la última).


# * Un archivo adultDataset.csv, con datos de personas para poder predecir si
#   alguien gana más o menos de 50000 dólares anuales, en función de una serie 
#   de características (para más detalles, ver https://archive.ics.uci.edu/dataset/2/adult)  
#   Más adelante se explica cómo cargar y procesar este conjunto de datos. 

# * Un conjunto de imágenes (en formato texto), con una gran cantidad de
#   dígitos (de 0 a 9) escritos a mano por diferentes personas, tomado de la
#   base de datos MNIST. En la carpeta digitdata están todos los datos en archivos de texto. 
#   Para preparar estos datos habrá que escribir funciones que los
#   extraigan de los ficheros de texto (más adelante se dan más detalles). 




# ==================================================
# EJERCICIO 1: SEPARACIÓN EN ENTRENAMIENTO Y PRUEBA 
# ==================================================

# Definir una función 

#           particion_entr_prueba(X,y,test=0.20)

# que recibiendo un conjunto de datos X, y sus correspondientes valores de
# clasificación y, divide ambos en datos de entrenamiento y prueba, en la
# proporción marcada por el argumento test. La división ha de ser ALEATORIA y
# ESTRATIFICADA respecto del valor de clasificación. Por supuesto, en el orden 
# en el que los datos y los valores de clasificación respectivos aparecen en
# cada partición debe ser consistente con el orden original en X e y.   


def particion_entr_prueba(X,y,test=0.20):
    # Inicializamos los conjuntos de datos que vamos a devolver en la particion 
    X_test = []
    y_test = []
    X_train =[]
    y_train = []
    clases = np.unique(y)
    # Iteramos sobre las posibles clases que puede devolver el clasificador 
    for yi in clases:
        X_i = X[y == yi]
        y_i = y[y == yi]
        # Calculamos la proporcion de elementos que va a ir destinada a cada conjunto 
        num_test=int(len(X_i)*test)  
        num_train=int(len(X_i)-num_test)
        # Y reordenamos aleatoriamente los nuevos conjuntos para que la particion sea aleatoria 
        aleatorio=np.arange(len(X_i))
        np.random.shuffle(aleatorio)
        X_train_i=X_i[aleatorio][:num_train]
        X_test_i=X_i[aleatorio][num_train:]
        y_train_i=y_i[aleatorio][:num_train]
        y_test_i=y_i[aleatorio][num_train:]
        # Añadimos los conjuntos obtenidos al resultado final 
        X_train.append(X_train_i)
        X_test.append(X_test_i)
        y_train.append(y_train_i)
        y_test.append(y_test_i)
    # Y, una vez finalizado el bucle, devolvemos los conjuntos como arrays de numpy 
    X_train=np.vstack(X_train)
    X_test=np.vstack(X_test)
    y_train=np.concatenate(y_train)
    y_test=np.concatenate(y_test)
    return X_train, X_test, y_train, y_test


# ------------------------------------------------------------------------------
y_votos[y_votos == "democrata"] = 0
y_votos[y_votos == "republicano"] = 1
y_votos_cod=y_votos.astype(np.float64)
Xe_votos,Xp_votos,ye_votos,yp_votos=particion_entr_prueba(X_votos,y_votos_cod,test=1/3)

# # Como se observa, se han separado 2/3 para entrenamiento y 1/3 para prueba:
# print(y_votos.shape[0],ye_votos.shape[0],yp_votos.shape[0])
# #    (435, 290, 145)
X_train_iris, X_test_iris, y_train_iris, y_test_iris = particion_entr_prueba(X_iris, y_iris, test = 0.2)
# # Las proporciones entre las clases son (aprox) las mismas en los dos conjuntos de
# # datos, y la misma que en el total: 267/168=178/112=89/56

# np.unique(y_votos,return_counts=True)
# #   (array(['democrata', 'republicano'], dtype='<U11'), array([267, 168]))
# print(np.unique(ye_votos,return_counts=True))
#  (array(['democrata', 'republicano'], dtype='<U11'), array([178, 112]))
# print(np.unique(yp_votos,return_counts=True))
# #  (array(['democrata', 'republicano'], dtype='<U11'), array([89, 56]))

# La división en trozos es aleatoria y en el orden en el que
# aparecen los datos en Xe_votos,ye_votos y en Xp_votos,yp_votos, se preserva
# la correspondencia original que hay en X_votos,y_votos.


# Otro ejemplo con los datos del cáncer, en el que se observa que las proporciones
# entre clases se conservan en la partición. 
    
# Xev_cancer,Xp_cancer,yev_cancer,yp_cancer=particion_entr_prueba(X_cancer,y_cancer,test=0.2)

# >>> np.unique(y_cancer,return_counts=True)
# (array([0, 1]), array([212, 357]))

# >>> np.unique(yev_cancer,return_counts=True)
# (array([0, 1]), array([170, 286]))

# >>> np.unique(yp_cancer,return_counts=True)
# (array([0, 1]), array([42, 71]))    


# Podemos ahora separar Xev_cancer, yev_cancer, en datos para entrenamiento y en 
# datos para validación.

# Xe_cancer,Xv_cancer,ye_cancer,yv_cancer=particion_entr_prueba(Xev_cancer,yev_cancer,test=0.2)

# >>> np.unique(ye_cancer,return_counts=True)
#  (array([0, 1]), array([136, 229]))

# >>> np.unique(yv_cancer,return_counts=True)
# (array([0, 1]), array([34, 57]))


# Otro ejemplo con más de dos clases:

# >>> Xe_credito,Xp_credito,ye_credito,yp_credito=particion_entr_prueba(X_credito,y_credito,test=0.4)

# >>> np.unique(y_credito,return_counts=True)
# (array(['conceder', 'estudiar', 'no conceder'], dtype='<U11'),
#  array([202, 228, 220]))

# >>> np.unique(ye_credito,return_counts=True)
# (array(['conceder', 'estudiar', 'no conceder'], dtype='<U11'),
#  array([121, 137, 132]))

# >>> np.unique(yp_credito,return_counts=True)
# (array(['conceder', 'estudiar', 'no conceder'], dtype='<U11'),
#  array([81, 91, 88]))




# # ------------------------------------------------------------------




















# ===============================================
# EJERCICIO 2: IMPLEMENTACIÓN ÁRBOLES DE DECISIÓN
# ===============================================


# En este ejercicio pedimos implementar en python un algoritmo de aprendizaje para árboles 
# de decisión. Los árboles de decisión que trataremos serán árboles binarios, en los que
# en cada nodo interior se pregunta por el valor de un atributo o característica dada, 
# y si ese valor es mayor o menor que un valor umbral dado. Este es el mismo tipo de árbol 
# de decisión que se  manejan en Scikit Learn. 

# Se puede obtener información de este tipo de árboles en la entrada "Decision Trees"
# del manual de Scikit Learn. También en la práctica del Titanic hecha en clase.

# Se propone la implementación de un clasificador basado en árboles de
# de decisión, entrenado usando el algoritmo CART, similar al que implementa 
# la clase DecisonTree de Scikit Learn, pero con ALGUNAS VARIANTES, que indicaremos más
# adelante.

# Los árboles de decisión están formados por nodos. Usar la siguiente clase para la
# implementación de los nodos:
    
class Nodo:
    def __init__(self, atributo=None, umbral=None, izq=None, der=None,distr=None,*,clase=None):
        self.atributo = atributo
        self.umbral = umbral
        self.izq = izq
        self.der = der
        self.distr= distr
        self.clase = clase
        
    def es_hoja(self):
        return self.clase is not None


# Pasamos a describir los distintos atributos de esta clase:

# - atributo: el atributo por el que se pregunta en el nodo. Referenciaremos a cada
#   atributo POR EL ÍNDICE DE SU POSICIÓN (el número de columna).
# - umbral: es el valor umbral por el que se pregunta en el nodo. Si la instancia tiene un
#   valor de atributo menor o igual que el umbral, se sigue por el subárbol izquierdo. En
#   caso contrario, por el subárbol derecho.
# - izq: es el nodo raiz del subárbol izquierdo.
# - der: el nodo raiz del subárbol derecho.
# - distr: es un diccionario cuyas claves son las posibles clases, y cuyos valores son
#   cuántos ejemplos del conjunto de entrenamiento correspondientes al nodo hay de cada
#   clase. Cuando decimos "ejemplos correspondientes al nodo" queremos decir aquellos que
#   cumplen todas las condiciones (desde la raiz) que llevan a ese nodo.
# - clase: Si el nodo es una hoja, es la clase que predice. Si no es una hoja, este valor es None.



# Lo que sigue es una descripción del algoritmo que se pide implementar para la
# construcción de un árbol de decisión. En principio describiremos la versión básica y más
# conocida, y posteriormente indicaremos las peculiaridades y variantes que pedimos
# introducir a esta versión básica.

# Supondremos que recibimos un conjunto de entrenamiento X,y y además dos valores max_prof
# y min_ejemplos_nodo_interior, que nos van a servir como condiciones adicionales para
# dejar de expandir un nodo. El algoritmo se define recursivamente y tiene además un
# argumento adicional prof (inicialmente 0), con la profundidad del nodo actual.  

# CONSTRUYE_ARBOL(X,y,min_ejemplos_nodo_interior,max_prof,prof=0):

    

# 1. SI prof es mayor o igual que max_prof, 
#       o el número de ejemplos de X es menor que min_ejemplos_nodo_interior,
#       o en X todos los ejemplos son de la misma clase:
#       ENTONCES:
#          Devolver un nodo hoja con la distribución de clases en X,
#                    y con la clase mayoritaria en X
# 2. EN OTRO CASO:
#        encontrar el MEJOR atributo A y el mejor umbral u para ese atributo
#        y particionar en dos tanto X como y:
#            * X_izq, y_izq los ejemplos cuyo valor de A es menor o igual que u
#            * X_der, y_der los ejemplos cuyo valor de A es mayor que u
#        Llamadas recursivas:
#            A_izq=CONSTRUYE_ARBOL(X_izq,y_izq,min_ejemplos_nodo_interior,max_prof,prof+1)
#            A_der=CONSTRUYE_ARBOL(X_der,y_der,min_ejemplos_nodo_interior,max_prof,prof+1)
#        Devolver un nodo interior con el atributo y umbral seleccionado,
#                 con la distribución de clases de X, y con A_izq y A_der
#                 como hijos izquierdo y derecho respectivamente.


# Lo anterior es la descripción básica. A continuación indicamos una serie de variantes y
# cuestiones adicionales que se le piden a esta implementación concreta:

# - Consideraremos la posibilidad de restringir los atributos a usar en el árbol a un
#   número de atributos dado n_atrs. Ese subconjunto de atributos se seleccionará
#   aleatoriamente al principio de la construcción del aŕbol y será el mismo para todos
#   los nodos.
#   Por ejemplo, si el dataset tiene 15 atributos y le damos n_atrs=9, al comienzo de la
#   construcción del árbol seleccionamos aleatoriamente 9 atributos, y ya en los nodos del
#   árbol solo podrán aparecer alguno de esos 9 atributos. Nótese que si n_atrs es igual
#   al total de atributos, tendríamos la versión estándar del algoritmo.
#   NOTA: téngase en cuenta que a diferencia de lo que ocurre en la versión clásica de
#   Random Forests, no sorteamos los atributos en cada nodo, sino que hay un único sorteo
#   inicial para todo el árbol.

# - A la hora de elegir el mejor atributo y umbral para la partición de los nodos
#   interiores, usar el criterio de mejor GANANCIA DE INFORMACIÓN (en particular, NO USAR GINI).

# - La principal carga computacional de este algoritmo se debe a la cantidad de candidatos a
#   mejor atributo y mejor umbral que hay que evaluar en cada nodo, para decidir cuál es
#   la mejor partición. El hecho de limitar el número de atributos candidatos (como se ha
#   descrito más arriba), va en esa dirección. 
#   Otra manera es limitar también los posibles valores umbrales a considerar
#   para cada atributo. Para ello, en la implementación que se pide actuaremos en dos
#   sentidos:
#      (a) Considerar solo como candidatos a umbral los puntos medios entre cada par de 
#         valores consecutivos del atributo en los que hay cambio de clase, para los
#         ejemplos correspondientes a ese nodo.
#         Por ejemplo, si ordenados los valores del atributo A en orden creciente, hay un
#         ejemplo con valor v1 de A y clase C1 y a continuación otro ejemplo con valor v2
#         en A y clase C2 distinta de C1, entonces (v1+v2)/2 es un posible valor umbral
#         candidato. El resto de valores NO se considera candidato.

#      (b) En cada nodo, para elegir los umbrales candidatos correspondientes a un atibuto,
#         no considerar todos los ejemplos que corresponden a ese nodo, sino 
#         sólo  una proporción de los mismos, seleccionada aleatoriamente. La proporción a
#         considerar se da en un parámetro prop_umbral.
#         Por ejemplo, si prop_umbral es 0.7 y el conjunto de ejemplos correspondientes al
#         nodo es de 200 ejemplos, entonces aplicaremos el proceso de selección de
#         umbrales candidatos descrito en (a) considerando sólo un suconjunto de 140
#         ejemplos seleccionado aleatoriamente de entre esos 200.  



# Con las descripciones anteriores, ya podemos precisar lo que se pide en eset apartado. 
# Se pide implementar una clase ArbolDecision con el siguiente formato:
def construye_arbol(X,y,min_ejemplos_nodo_interior,max_prof, atributos, prop_umbral, prof=0):
    # En esta primera línea obtenemos las clases y su frecuencia, para su uso en ambas ramas del condicional 
    valores_frecuencia = np.unique(y, return_counts=True)
    # Aquí escribimos el caso base de la funcion, devolviendo una hoja si se cumple alguna condicion que se especifica en el pseudocódigo proporcionado
    if prof >= max_prof or len(X)<min_ejemplos_nodo_interior or len(valores_frecuencia[0]) == 1:
        # Se devuleve la clase mayoritaria y la distribucion con un diccionario qu easocia cada clase al número de elementos que tiene asociada
        c = valores_frecuencia[0][np.argmax(valores_frecuencia[1])]
        return Nodo(distr=dict(zip(valores_frecuencia[0], valores_frecuencia[1])), clase=c)
    else:
        # Si nos encontramos en el caso recursivo, inicializamos la máxima ganancia, la columna con el mejor atributo y el mejor umbral en el nodo a considerar
        max_ganancia = -np.inf
        mejor_atributo = 0
        mejor_umbral = 0
        # Seleccionamos los elementos que vamos a tener en cuenta para elegir umbral y atributo
        num_elementos = int(len(X) * prop_umbral)
        seleccionados = np.random.choice(np.arange(X.shape[0]), num_elementos, replace=False)
        # E iteramos sobre los atributos seleccionados en la primera llamada a la funcion
        for ai in atributos:
            # Calculamos los umbrales disponibles para ese atributo, y posteriormente creamos una funcion parcial que calcule todas las ganancias
            # mediante vectorizacion, para calcularlas con numpy y ganar eficiencia respecto a los bucles for
            umbrales = calcula_umbrales(X[seleccionados], y[seleccionados], ai)
            if len(umbrales) == 0:
                c = valores_frecuencia[0][np.argmax(valores_frecuencia[1])]
                return Nodo(distr=dict(zip(valores_frecuencia[0], valores_frecuencia[1])), clase=c)
            ganancias = np.vectorize(lambda u: ganancia(X[seleccionados], y[seleccionados], u, ai))
            # Elegimos la mayor de todas, y comprobamos que sea mayor que las mas grande obtenida hasta el momento 
            max_ganancia_atributo = np.max(ganancias(umbrales))
            # Alternativa para las ganancias por listas de compresion
            # ganancias = np.array([ganancia(X[seleccionados], y[seleccionados], ui, ai) for ui in umbrales]
            if max_ganancia_atributo > max_ganancia:
                # En caso afirmativo, asignamos esa ganancia a la mejor de todas, igual que el mejor atributo y el mejor umbral
                max_ganancia = max_ganancia_atributo
                mejor_atributo = ai
                mejor_umbral = umbrales[np.argmax(ganancias(umbrales))]
                

        # Dividimos el dataset segun el valor del atributo escogido supere o no el umbral
        X_a = X[:, mejor_atributo]
        X_izq, y_izq = X[X_a <= mejor_umbral], y[X_a <= mejor_umbral]
        X_der, y_der = X[X_a > mejor_umbral], y[X_a > mejor_umbral]
        
        # Y hacemos las llamadas recursivas
        A_izq = construye_arbol(X_izq, y_izq, min_ejemplos_nodo_interior, max_prof, atributos, prop_umbral, prof + 1)
        A_der = construye_arbol(X_der, y_der, min_ejemplos_nodo_interior, max_prof, atributos, prop_umbral, prof + 1)
        
        # Una vez terminadas, devolvemos el nodo con todo lo calculado en la función 
        return Nodo(atributo=mejor_atributo, umbral=mejor_umbral, izq=A_izq, der=A_der, distr=dict(zip(valores_frecuencia[0], valores_frecuencia[1])))



def entropia(y):
    valores = np.unique(y, return_counts=True)
    return -np.sum((valores[1] / len(y)) * np.log2(valores[1] / len(y)))



def ganancia(X,y,u,a):
    return entropia(y) - ((len(y[X[: , a] > u])/len(y)) * entropia(y[X[: , a] > u]) + 
    (len(y[X[:, a] <= u])/len(y)) * entropia(y[X[:, a] <= u]))


def calcula_umbrales(X,y,a):
    ordenados = np.argsort(X[:, a])
    X_ord = X[ordenados]
    y_ord = y[ordenados]
    diferentes = y_ord[:-1] != y_ord[1:]
    umbrales =  (X_ord[:-1, a] + X_ord[1:, a]) / 2
    return umbrales[diferentes]

class ArbolDecision:
    def __init__(self, min_ejemplos_nodo_interior=5, max_prof=10,n_atrs=10,prop_umbral=1.0):
        self.min_ejemplos_nodo_interior = min_ejemplos_nodo_interior
        self.max_prof=max_prof
        self.n_atrs=n_atrs
        self.prop_umbral=prop_umbral   
        self.arbol = Nodo()
   
    def entrena(self, X, y):
        # Elegimos inicialmente los atributos que vamos a considerar de manera aleatoria y llamamos a la funcion escrita anteriormente
        atributos = np.random.choice(np.arange(X.shape[1]),self.n_atrs, replace=False)
        self.arbol = construye_arbol(X, y, self.min_ejemplos_nodo_interior, self.max_prof, atributos, self.prop_umbral)
       
    def clasifica(self, X):
        #Si el clasificador no ha sido entrenado, lanzamos la excepción. En caso contrario llamamos a la funcion auxiliar
        if self.arbol.atributo == None:
            raise ClasificadorNoEntrenado("Se debe entrenar al arbol para clasificar un conjunto de datos")
        else:
            res = np.empty(X.shape[0])
            # Esta función auxiliar toma como parametros el arbol entrenado, un array con los indices que indican cada clasificación y otro que devuelve las clasificaciones
            return  clasifica_aux(self.arbol, X, np.arange(X.shape[0]), res)

    def clasifica_prob(self, x):
        # Idem que la funcion anterior, esta vez al ser un solo elemento a clasificar no necesitamos mas variables auxiliares 
        if self.arbol.atributo == None:
            raise ClasificadorNoEntrenado("Se debe entrenar al arbol para clasificar un conjunto de datos")
        else:
            return clasifica_prob_aux(self.arbol, x)

    def imprime_arbol(self,nombre_atrs,nombre_clase) :
        #Devolvemos la funcion auxiliar que toma como parametros el arbol y el numero de veces que se tabula cada llamada, ademas de los parametros de la funcion original
        return imprime_aux(self.arbol, nombre_atrs, nombre_clase, 0)


def clasifica_aux(arbol, X, indices, res):
    # Si el nodo en el que estamos es una hoja, los elementos cuyos indices hayan cumplido todas las condiciones necesarias para llegar a ese nodo se clafican con su clase 
    if arbol.es_hoja():
        res[indices] = arbol.clase
    else:
        # En caso contrario, se separan los elementos segun si el atributo del arbol supera o no el umbral y se hacen llamadas recursivas con cada grupo obtenido 
        izq_indices = indices[X[:, arbol.atributo] <= arbol.umbral]
        der_indices = indices[X[:, arbol.atributo] > arbol.umbral]
        clasifica_aux(arbol.izq, X[X[:, arbol.atributo] <= arbol.umbral], izq_indices, res)
        clasifica_aux(arbol.der, X[X[:, arbol.atributo] > arbol.umbral], der_indices, res)
    return res

def clasifica_prob_aux(arbol, x):
    # Si el nodo es una hoja, se devuelve la distribucion normalizada para obtener las probabilidades del elemento de pertenecer a cada clase
    if arbol.es_hoja():
        d = arbol.distr
        return {k : v / sum(list(d.values())) for (k, v) in d.items()}
    else:
        # Si no, se hace una llamada recursiva en funcion de si el atributo del nodo supera o no el umbral, como hicimos en la función anterior
        if x[arbol.atributo] <= arbol.umbral:
            return clasifica_prob_aux(arbol.izq, x)
        else:
            return clasifica_prob_aux(arbol.der, x)

def imprime_aux(arbol, nombre_atrs, nombre_clase, tabulador):
    # Si el nodo es hoja, devuelve la clasificacion formateada de esta manera
    if arbol.es_hoja():
            print("\t"*tabulador + nombre_clase + ":"  + str(arbol.clase) + "--" + str(arbol.distr))
    else:
        # Si no, devuelve las ramas formateadas y las llamadas recursivas incrementando el número de tabulaciones
        print("\t"*tabulador + nombre_atrs[arbol.atributo] + "<=" + str(arbol.umbral))
        imprime_aux(arbol.izq, nombre_atrs, nombre_clase, tabulador + 1)
        
        print("\t"*tabulador + nombre_atrs[arbol.atributo] + ">" + str(arbol.umbral))
        imprime_aux(arbol.der, nombre_atrs, nombre_clase, tabulador + 1)

#  El constructor tiene los siguientes argumentos de entrada:

#     + min_ejemplos_nodo_interior: mínimo número de ejemplos del conjunto de 
#       entrenamiento en un nodo del árbol que se aprende, para que se considere 
#       su división.  
#     + max_prof: profundidad máxima del árbol que se aprende.
#     + n_atrs: número de atributos candidatos a considerar en cada partición
#     + prop_umbral: proporción de ejemplos a considerar cuando se buscan los 
#       umbrales candidatos.    
  
#      

# * El método entrena tiene como argumentos de entrada:
#   
#     +  Dos arrays numpy X e y, con los datos del conjunto de entrenamiento 
#        y su clasificación esperada, respectivamente.
#     

# * Método clasifica: recibe UN ARRAY de ejemplos (array numpy) y
#   devuelve el ARRAY de clases que el modelo predice para esos ejemplos. 

# * Método clasifica_prob: recibe UN EJEMPLO y devuelve un diccionario con la predicción
#   de probabilidad de pertenecer a cada clase. Esa probabilidad se calcula como la
#   proporción de ejemplos de clase en la distribución del nodo hoja que da la
#   predicción.

# * Método imprime_arbol: recibe la lista de nombres de cada atributo (columnas) y el
#   nombre del atributo de clasificación, e imprime el árbol de decisión aprendido 
#   (ver ejemplos más abajo) [SUGERENCIA: hacerlo con una función auxiliar recursiva] 


# Si se llama al método de clasificación, o al de impresión, antes de entrenar el modelo,
# se debe devolver (con raise) una excepción:

class ClasificadorNoEntrenado(Exception): pass

        




# Algunos ejemplos (los resultados pueden variar, debido a la aleatoriedad)
# **************************************************************************

# TITANIC
# -------

# clf_titanic = ArbolDecision(max_prof=3,min_ejemplos_nodo_interior=len(X_train_titanic) * 0.1,n_atrs=3)
# clf_titanic.entrena(X_train_titanic, y_train_titanic)
# clf_titanic.imprime_arbol(["Pclass", "Mujer", "Edad"], "Sobrevive")
# print(clf_titanic.clasifica(X_test_titanic))
# for i in range(10, 20):
#     print(clf_titanic.clasifica_prob(X_test_titanic[i]))

# print(res)

 

# Mujer <= 0.000
#      Edad <= 11.000
#           Pclass <= 2.500
#                Partido: 1 -- {1: 10}
#           Pclass > 2.500
#                Partido: 0 -- {0: 13, 1: 8}
#      Edad > 11.000
#           Pclass <= 1.000
#                Partido: 0 -- {0: 62, 1: 30}
#           Pclass > 1.000
#                Partido: 0 -- {0: 270, 1: 32}
# Mujer > 0.000
#      Pclass <= 2.000
#           Edad <= 2.000
#                Partido: 0 -- {0: 1, 1: 1}
#           Edad > 2.000
#                Partido: 1 -- {0: 5, 1: 122}
#      Pclass > 2.000
#           Edad <= 38.500
#                Partido: 1 -- {0: 46, 1: 58}
#           Edad > 38.500
#                Partido: 0 -- {0: 9, 1: 1}

# VOTOS
# -----

# clf_votos = ArbolDecision(min_ejemplos_nodo_interior=3,max_prof=5,n_atrs=16)
# clf_votos.entrena(Xe_votos, ye_votos)
# nombre_atrs_votos=[f"Votación {i}" for i in range(1,17)]
# print(clf_votos.clasifica(Xe_votos), ye_votos)
# clf_votos.imprime_arbol(nombre_atrs_votos,"Partido")

# Votación 4 <= 0.000
#      Votación 3 <= 0.000
#           Votación 11 <= 0.000
#                Votación 13 <= 0.500
#                     Votación 14 <= -0.500
#                          Partido: democrata -- {'democrata': 2}
#                     Votación 14 > -0.500
#                          Partido: republicano -- {'republicano': 3}
#                Votación 13 > 0.500
#                     Votación 7 <= -1.000
#                          Partido: democrata -- {'democrata': 1, 'republicano': 1}
#                     Votación 7 > -1.000
#                          Partido: democrata -- {'democrata': 4}
#           Votación 11 > 0.000
#                Partido: democrata -- {'democrata': 11}
#      Votación 3 > 0.000
#           Partido: democrata -- {'democrata': 149}
# Votación 4 > 0.000
#      Votación 11 <= 0.500
#           Votación 10 <= -1.000
#                Votación 12 <= -1.000
#                     Votación 3 <= -1.000
#                          Partido: democrata -- {'democrata': 1, 'republicano': 1}
#                     Votación 3 > -1.000
#                          Partido: republicano -- {'republicano': 2}
#                Votación 12 > -1.000
#                     Votación 3 <= 0.000
#                          Partido: republicano -- {'republicano': 35}
#                     Votación 3 > 0.000
#                          Partido: republicano -- {'democrata': 1, 'republicano': 2}
#           Votación 10 > -1.000
#                Partido: republicano -- {'republicano': 55}
#      Votación 11 > 0.500
#           Votación 7 <= -1.000
#                Votación 3 <= -1.000
#                     Votación 13 <= 0.000
#                          Partido: democrata -- {'democrata': 1}
#                     Votación 13 > 0.000
#                          Partido: republicano -- {'democrata': 2, 'republicano': 9}
#                Votación 3 > -1.000
#                     Partido: democrata -- {'democrata': 6}
#           Votación 7 > -1.000
#                Partido: republicano -- {'republicano': 4}


# IRIS
# ----

    
# clf_iris = ArbolDecision(max_prof=3,n_atrs=4)
# clf_iris.entrena(X_iris, y_iris)

# clf_iris.imprime_arbol(["Long. Sépalo", "Anch. Sépalo", "Long. Pétalo", "Anch. Pétalo"],"Clase")



#  Long. Pétalo <= 2.450
#       Clase: 0 -- {0: 33}
#  Long. Pétalo > 2.450
#       Long. Pétalo <= 4.900
#            Anch. Pétalo <= 1.650
#                 Clase: 1 -- {1: 32}
#            Anch. Pétalo > 1.650
#                 Clase: 2 -- {1: 1, 2: 3}
#       Long. Pétalo > 4.900
#            Clase: 2 -- {2: 30}


# CÁNCER DE MAMA
# --------------

# clf_cancer = ArbolDecision(min_ejemplos_nodo_interior=3,max_prof=10,n_atrs=15)
# clf_cancer.entrena(Xev_cancer, yev_cancer)
nombre_atrs_cancer=['mean radius', 'mean texture', 'mean perimeter', 'mean area',
       'mean smoothness', 'mean compactness', 'mean concavity',
       'mean concave points', 'mean symmetry', 'mean fractal dimension',
       'radius error', 'texture error', 'perimeter error', 'area error',
       'smoothness error', 'compactness error', 'concavity error',
       'concave points error', 'symmetry error',
       'fractal dimension error', 'worst radius', 'worst texture',
       'worst perimeter', 'worst area', 'worst smoothness',
       'worst compactness', 'worst concavity', 'worst concave points',
       'worst symmetry', 'worst fractal dimension']

# clf_cancer.imprime_arbol(nombre_atrs_cancer,"Es benigno")


#  mean concave points <= 0.051
#       mean area <= 696.050
#            area error <= 34.405
#                 mean area <= 505.550
#                      Es benigno: 1 -- {1: 172}
#                 mean area > 505.550
#                      worst texture <= 30.145
#                           mean concave points <= 0.050
#                                Es benigno: 1 -- {1: 63}
#                           mean concave points > 0.050
#                                Es benigno: 0 -- {0: 1, 1: 1}
#                      worst texture > 30.145
#                           mean texture <= 24.840
#                                compactness error <= 0.013
#                                     Es benigno: 0 -- {0: 3}
#                                compactness error > 0.013
#                                     Es benigno: 1 -- {1: 2}
#                           mean texture > 24.840
#                                Es benigno: 1 -- {1: 11}
#            area error > 34.405
#                 mean concave points <= 0.032
#                      Es benigno: 1 -- {1: 7}
#                 mean concave points > 0.032
#                      mean perimeter <= 89.175
#                           Es benigno: 0 -- {0: 3}
#                      mean perimeter > 89.175
#                           mean texture <= 20.115
#                                Es benigno: 1 -- {1: 3}
#                           mean texture > 20.115
#                                Es benigno: 0 -- {0: 1}
#       mean area > 696.050
#            mean texture <= 16.190
#                 Es benigno: 1 -- {1: 4}
#            mean texture > 16.190
#                 worst fractal dimension <= 0.066
#                      Es benigno: 1 -- {1: 2}
#                 worst fractal dimension > 0.066
#                      Es benigno: 0 -- {0: 6}
#  mean concave points > 0.051
#       mean area <= 790.850
#            worst texture <= 25.655
#                 mean concave points <= 0.079
#                      mean concave points <= 0.052
#                           Es benigno: 0 -- {0: 1}
#                      mean concave points > 0.052
#                           Es benigno: 1 -- {1: 20}
#                 mean concave points > 0.079
#                      Es benigno: 0 -- {0: 6}
#            worst texture > 25.655
#                 perimeter error <= 1.558
#                      Es benigno: 0 -- {0: 1, 1: 1}
#                 perimeter error > 1.558
#                      Es benigno: 0 -- {0: 37}
#       mean area > 790.850
#            Es benigno: 0 -- {0: 111}



# EJEMPLOS DE RENDIMIENTOS OBTENIDOS CON LOS CLASIFICADORES:
# ----------------------------------------------------------

# Usamos la siguiente función para medir el rendimiento (proporción de aciertos) 
# de un clasificador sobre un conjunto de ejemplos:
    
def rendimiento(clasif,X,y):
    return sum(clasif.clasifica(X)==y)/X.shape[0]

    

# Ejemplos (obviamente, el resultado puede variar):

# print("Rendimiento titanic: ")
# print(rendimiento(clf_titanic,X_train_titanic,y_train_titanic))
# 0.8158682634730539
# print(rendimiento(clf_titanic,X_test_titanic,y_test_titanic))
# 0.7982062780269058

# r= rendimiento(clf_votos,Xp_votos,yp_votos)
# print("Rendimiento votos: " + str(r))
# 0.9827586206896551
# rendimiento(clf_votos,Xp_votos,yp_votos)
# 0.9310344827586207

# print(rendimiento(clf_iris,X_iris,y_iris))
#  0.98989898989899
# print(rendimiento(clf_iris,X_test_iris,y_test_iris))
# 0.9607843137254902

# print("Arboles")
# print(rendimiento(clf_cancer,Xev_cancer,yev_cancer))
# # # 0.9956140350877193
# print(rendimiento(clf_cancer,Xp_cancer,yp_cancer))
# 0.9557522123893806































# =============================================
# EJERCICIO 3: IMPLEMENTACIÓN DE RANDOM FORESTS
# =============================================

# Usando la clase ArbolDecision, implementar un clasificador Random Forest. 

# Un clasificador Random Forest aplica dos técnicas que reducen el sobreajuste que 
# pudiéramos tener con un único árbol de decisión:

# - En lugar de aprender un árbol. se aprenden varios árboles y a la hora de clasificar
#   nuevos ejemplos, se devuelve la clasificación mayoritaria.
# - Cada uno de esos árboles no se aprende con el conjunto de entrenamiento original, sino
#   con una muestra de ejemplos, obtenido seleccionado los ejemplos aleatoriamente del 
#   conjunto total, CON REEMPLAZO. Además, durante el aprendizaje y en cada nodo, no se usan todos
#   los atributos sino un sunconjunto de ellos obtenidos aleatoriamente (el mismo para todo el árbol). 

# NOTA IMPORTANTE: En la versión estándar del algoritmo Random Forest, el subconjunto de
# atributos a considerar se sortea EN CADA NODO de los árboles que se aprenden. Sin
# embargo, en nuestro caso, como vamos a usar la clase ArbolDecision del ejercicio
# anterior, se va usar el mismo subconjunto de atributos EN CADA ÁRBOL APRENDIDO.

# Concretando, se pide implementar una clase RandomForest con la siguiente estructura:


class RandomForest:
    def __init__(self, n_arboles=5,prop_muestras=1.0,
                       min_ejemplos_nodo_interior=5, max_prof=10,n_atrs=10,prop_umbral=1.0):
        self.n_arboles = n_arboles
        self.prop_muestras = prop_muestras
        self.min_ejemplos_nodo_interior = min_ejemplos_nodo_interior  
        self.max_prof = max_prof
        self.n_atrs = n_atrs
        self.prop_umbral = prop_umbral
        # Creamos una lista con los arboles que vamos a tener disponibles
        self.arboles_entrenados = []                 

    def entrena(self, X, y):
        num_elementos = int(len(X) * self.prop_muestras)
        # Para cada arbol que se pide
        for _ in range(self.n_arboles):
            # Seleccionamos las muestras que vamos a utilizar en ese arbol, inicializamos, entrenamos y lo añadimos
            muestras = np.random.choice(np.arange(X.shape[0]), num_elementos, replace=True)
            arbol = ArbolDecision(self.min_ejemplos_nodo_interior,self.max_prof, self.n_atrs, self.prop_umbral)
            arbol.entrena(X[muestras], y[muestras])
            self.arboles_entrenados.append(arbol)

    def clasifica(self, X):
        # Apilamos las clasificaciones de cada arbol al conjutno de datos e iniicalizamos el array donde vamos a devolver la clsificacion
        clasificaciones_iniciales = np.stack([a.clasifica(X) for a in self.arboles_entrenados])
        clasificaciones_finales = np.empty(X.shape[0])
        # Iteramos sobre las columnas para obtener las clasificaciones de cada arbol 
        for c in range(clasificaciones_iniciales.shape[1]):
            # Obtenemos la frecuencia de cada clase y añadimos la mayoritaria al array de clasificaciones finales
            unicos, frecuencia = np.unique(clasificaciones_iniciales[:, c], return_counts=True)
            clasificado = unicos[np.argmax(frecuencia)]
            np.append(clasificaciones_finales, clasificado)
        return clasificaciones_finales
    
    
    
# Los argumentos del constructor son:

# - n_arboles: el número de árboles que se van a obtener para el clasificador.
# - n_muestras: el número de ejemplos a muestrear para el aprendizaje de cada árbol.
# - El resto de argumentos son los mismos que en el ejercicio anterior, y se usan en el
#   aprendizaje de cada árbol.


# Ejemplos:
# *********

# VOTOS:
# # # ------

# clf_votos_rf=RandomForest(n_arboles=10,min_ejemplos_nodo_interior=3,max_prof=5,n_atrs=16,prop_umbral=1.0)
# clf_votos_rf.entrena(Xe_votos, ye_votos)
# print(rendimiento(clf_votos_rf,Xe_votos,ye_votos))
# # 0.9517241379310345
# print(rendimiento(clf_votos_rf,Xp_votos,yp_votos))
# 0.9586206896551724


# clf_cancer_rf = RandomForest(n_arboles=15,min_ejemplos_nodo_interior=5,max_prof=10,n_atrs=15)
# clf_cancer_rf.entrena(Xe_cancer, ye_cancer)
# print("Bosques")
# print(rendimiento(clf_cancer_rf, Xe_cancer, ye_cancer))
# # 1.0
# print(rendimiento(clf_cancer_rf, Xp_cancer, yp_cancer))
# 0.9911504424778761


#------------------------------------------------------------------------------
























# =========================================
# EJERCICIO 4: AJUSTANDO LOS CLASIFICADORES
# =========================================

# En este ejercicio vamos a tratar de obtener buenos clasificadores para los 
# los siguientes conjuntos de datos: IMDB, credito, AdultDataset y dígitos.

# ---------------------------
# 4.1 PREPARANDO LOS DATASETS     
# ---------------------------

# Excepto a IMDB, que ya se carga cuando se ejecuta carga_datos.py, el resto 
# tendremos que hacer antes algún preprocesado:
    
# - En X_credito, los atributos son categóricos, así que hay que transformarlos 
#   en numéricos para que se puedan usar con nuestros árboles de decisión. 
#   En el caso de árboles de decisión no es necesario hacer "one hot encoding",
#   sino que basta con codificar los valores de los atributos con números naturales
#   Para ello, SE PIDE USAR el OrdinalEncoder de sklearn.preprocessing (ver manual). 
#   Será necesario también separar en conjunto de prueba y de entrenamiento y
#   validación. 

# - El dataset AdultDataset nos viene es un archivo csv. Cargarlo con 
#   read_csv de pandas, separarlo en entrenamiento y prueba 
#   y aplicarle igualmente OrdinalEncoder, pero sólo a las características desde la 
#   quinta en adelante (ya que las cuatro primeras columnas ya son numéricas). 

# - El dataset de dígitos los podemos obtener a partir de los datos que están en 
#   la carpeta datos/digitdata que se suministra.  Cada imagen viene dada por 28x28
#   píxeles, y cada pixel vendrá representado por un caracter "espacio en
#   blanco" (pixel blanco) o los caracteres "+" (borde del dígito) o "#"
#   (interior del dígito). En nuestro caso trataremos ambos como un pixel negro
#   (es decir, no distinguiremos entre el borde y el interior). En cada
#   conjunto las imágenes vienen todas seguidas en un fichero de texto, y las
#   clasificaciones de cada imagen (es decir, el número que representan) vienen
#   en un fichero aparte, en el mismo orden. Será necesario, por tanto, definir
#   funciones python que lean esos ficheros y obtengan los datos en el mismo
#   formato numpy en el que los necesita el clasificador. 
#   Los datos están ya separados en entrenamiento, validación y prueba. 

from sklearn.preprocessing import OrdinalEncoder
import pandas as pd

#   Se pide incluir aquí las definiciones y órdenes necesarias para definir
#   las siguientes variables, con los datasets anteriores como arrays de numpy.

# Aquí descargamos los arrays directamente con el metodo load
X_train_imdb = np.load("datos/imdb_sentiment/vect_train_text.npy")
X_tests_imdb = np.load("datos/imdb_sentiment/vect_test_text.npy")
y_train_imdb = np.load("datos/imdb_sentiment/y_train_text.npy")
y_test_imdb = np.load("datos/imdb_sentiment/y_test_text.npy")

# * X_train_credito, y_train_credito, X_test_credito, y_test_credito
#   conteniendo el dataset de crédito con los atributos numñericos:

# Creamos un Ordinal Encoder y lo ajustamos al data set de creditos
codificador=OrdinalEncoder()
X_credito_cod=codificador.fit_transform(X_credito)

# Pasamos las clases a valores numéricos a mano por incompatibilidad y hacemos la particion
y_credito[y_credito == "no conceder"] = '-1'
y_credito[y_credito == "estudiar"] = '0'
y_credito[y_credito == "conceder"] = '1'
y_credito_cod = y_credito.astype(np.float64)
X_train_credito,  X_test_credito, y_train_credito, y_test_credito = particion_entr_prueba(X_credito_cod, y_credito_cod, 0.2)





# * X_train_adult, y_train_adult, X_test_adult, y_test_adult
#   conteniendo el AdultDataset con los atributos numéricos:

# Leemos el csv mediante pandas y dividimos en X e y, donde las clases son la última columna del dataframe 
datos_adult=pd.read_csv('datos/adultDataset.csv')
X_adult =datos_adult.iloc[:, :-1].values
y_adult =datos_adult.iloc[:, -1].values
# Pasamos las clases a valores numéricos y creamos el Ordinal Encoder. Como los 4 primeros atributos ya son numéricos, los descartamos a la hora de
# ajustar el data set. Finalmente hacemos la particion 
y_adult[y_adult == "less_than_50K"] = '0'
y_adult[y_adult == "more_than_50K"] = '1'
y_adult_cod = y_adult.astype(np.float32)
codificador=OrdinalEncoder()
X_adult[:, 4:] = codificador.fit_transform(X_adult[:, 4:])
X_adult_cod = X_adult.astype(int)
X_train_adult,  X_test_adult, y_train_adult, y_test_adult = particion_entr_prueba(X_adult_cod, y_adult_cod, 0.2)

# print(X_train_adult[:5], y_train_adult[:5], X_test_adult[:5], y_test_adult[:5])
# print(X_adult_cod.shape[1])







# * X_train_dg, y_train_dg, X_valid_dg, y_valid_dg, X_test_dg, y_test_dg
#   conteniendo el dataset de los dígitos escritos a mano:
# numeros = np.genfromtxt("datos/digitdata/trainingimages")  
# print(numeros[:50])

# Definimos la función de conversión

def convertir_a_numero(x):
    return 0 if x == ' '  else 1

def digito_imagen(ruta):
    lineas = []
    # Leemos el archivo de texto e iteramos sobre sus líneas
    with open(ruta, 'r') as file:
        for linea in file:
            linea= linea.rstrip('\n')  # Eliminamos aquí el salto de línea al final
            if len(linea) < 28:
                linea = linea.ljust(28)  # Rellenamos con espacios si es necesario para que coja la línea completa
            lineas.append([convertir_a_numero(l) for l in linea])

    # Convertimos la lista de lineas en un array de numpy y ajustamos las dimensiones para que sea una secuencia de imagenes.
    imagenes = np.array([lineas])
    n_imagenes = imagenes.size // (28 * 28) 
    return imagenes.reshape((n_imagenes, 28 * 28))

# Seguimos un procedimietno similar para transformar el conjunto de clases
def digito_clase(ruta):
    lineas = []
    with open(ruta, 'r') as file:
        for linea in file:
            l = linea[0]
            lineas.append([int(l)])
    clases = np.array(lineas)
    return clases.flatten() # Devolvemos las clases aplicando flatten para trasponer el array y que sea una fila

X_train_dg = digito_imagen("datos/digitdata/trainingimages")
y_train_dg = digito_clase("datos/digitdata/traininglabels")

X_valid_dg = digito_imagen("datos/digitdata/validationimages")
y_valid_dg = digito_clase("datos/digitdata/validationlabels")

X_test_dg = digito_imagen("datos/digitdata/testimages")
y_test_dg = digito_clase("datos/digitdata/testlabels")

# print(np.concatenate((X_train_dg, X_valid_dg, X_test_dg)))
# print(y_train_dg.flatten())







# -----------------------------
# 4.2 AJUSTE DE HIPERPARÁMETROS     
# -----------------------------

# En nuestra implementación de RandomForest tenemos los siguientes 
# hiperparámetros: 

# n_arboles
# prop_muestras
# min_ejemplos_nodo_interior
# max_prof
# n_atrs
# prop_umbral

# Se trata ahora de encontrar, en cada dataset, una buena combinación de valores para esos 
# hiperparámetros, tratando de obtener un buen rendimiento de los clasificadores. Hacerlo
# usando un conjunto de validación: según se ha visto en la teoría, esto consiste en particionar  
# en entrenamiento, validación y prueba, entrenando por cada combinación de hiperparámetros 
# con el conjunto de entrenamiento y evaluando el rendimiento en validación. El entrenamiento final 
# con la mejor combinación ha de hacerse en la unión de entrenamiento y validación.
    

# NO ES NECESARIO ser demasiado exhaustivo, basta con probar algunas combinaciones, 
# pero sí es importante describir el proceso realizado y las mejores combinaciones 
# encontradas en cada caso. 
# DEJAR ESTE APARTADO COMENTADO, para que no se ejecuten las pruebas realizadas cuando se cargue
# el archivo. 

# ----------------------------

# Para seleccionar los mejores hiperparametros que vamos a asociar a cada clasificador, hemos creado esta pequeña funcion que recibe una lista 
# de posibles combinaciones y calcula el rendimiento obtenido de cada una. Cuando obtiene el rendimiento, lo compara con el mayor obtenido hasta el
# momento, y si lo supera asocia los mejores parametros a la combinacion de valores en la que se esté iterando.Finalemente devuelve los mejores hiperparametros
# y el rendimiento sobre el conjunto test una vez entrenado en la combinacion de entrenamiento y validacion. Para no saturar el ordenador, hemos preferido preferido escribir 
# las combinaciones "a mano" en vez de iterar sobre todas las posibles combinaciones de una serie de valores para cada hiperparametro, como se hizo
# en la practica 5 de evaluacion de modelos. La funcion utilizada es esta:

def ajusta_hiperparametros(X_train, X_valid, X_test, y_train, y_valid, y_test, combinaciones):
    max_rendimiento = 0
    mejores_parametros = {
        "n_arboles" : 0,
        "prop_muestras" : 0,
        "min_ejemplos_nodo_interior" : 0, 
        "max_prof" : 0, 
        "n_atrs" : 0,
        "prop_umbral" : 0
    }

    for comb in combinaciones:
        clf = RandomForest(*comb)
        clf.entrena(X_train, y_train)
        r = rendimiento(clf, X_valid, y_valid)
        if r >= max_rendimiento:
            mejores_parametros = {k : a for (k, a) in zip(mejores_parametros.keys(), comb)}

    clf.entrena(np.concatenate((X_train, X_valid)), np.concatenate((y_train, y_valid)))
    return mejores_parametros, rendimiento(clf, X_test, y_test)


# Aqui separamos los conjuntos de entrenamiento en entrenamiento y validacion 

# X_train_credito,  X_valid_credito, y_train_credito, y_valid_credito = particion_entr_prueba(X_train_credito, y_train_credito, 0.2)
# X_train_imdb,X_valid_imdb,y_train_imdb, y_valid_imdb = particion_entr_prueba(X_train_imdb,y_train_imdb,test = 0.2)
# X_train_adult, X_valid_adult, y_train_adult, y_valid_adult = particion_entr_prueba(X_train_adult, y_train_adult, 0.2)

# Y aqui hacemos las pruebas con varias combinaciones para obtener la mas acertada. No hemos hecho pruebas donde se escojan un numero muy grande de atributos en los conjuntos
# que lo tienen para ahorrar tiempo de computacion.

# print("Hiperparámetros IMDB: " + str(ajusta_hiperparametros(X_train_imdb,X_valid_imdb, X_test_imdb, y_train_imdb, y_valid_imdb, y_test_imdb, [[2,0.5,10,5,100,0.5], [3,0.75,15,6,150,0.75],[5,1.0,20,8,200,0.8]])))
# print("Hiperparámetros crédito: " + str(ajusta_hiperparametros(X_train_credito,X_valid_credito, X_test_credito, y_train_credito, y_valid_credito, y_test_credito, [[10,0.5,10,5,6,0.5], [10,0.75,15,5,4,0.75],[10,0.7,20,8,6,0.7]])))
# print("Hiperparámetros adult: " + str(ajusta_hiperparametros(X_train_adult,X_valid_adult, X_test_adult, y_train_adult, y_valid_adult, y_test_adult, [[1,0.5,10,5,6,0.5], [2,0.75,5,5,6,0.75],[3,0.5,7,5,6,1]])))
# print("Hiperparámetros digitos: " + str(ajusta_hiperparametros(X_train_dg, X_valid_dg, X_test_dg,y_train_dg, y_valid_dg, y_test_dg, [[2,0.5,10,5,100,0.5],[3,0.75,10,5,100,0.75],[5,0.5,10,5,100,0.5]])))

# Despues de ejecutar las pruebas, hemos obtenido que los hiperparametros que ofrecen mayor rendimiento son los de mayor prop_umbral, prop_muestras, n_atributos y n_arboles,
# ya que a mayor número de elementos a considerar y mayor número de arboles que reduzcan el overfitting mejor funcionará el clasificador
  




# ********************************************************************************
# ********************************************************************************
# ********************************************************************************
# ********************************************************************************

# EJEMPLOS DE PRUEBA

# LAS SIGUIENTES LLAMADAS SERÁN EJECUTADAS POR EL PROFESOR EL DÍA DE LA PRESENTACIÓN.
# UNA VEZ IMPLEMENTADAS LAS DEFINICIONES Y FUNCIONES NECESARIAS
# Y REALIZADOS LOS AJUSTES DE HIPERPARÁMETROS, 
# DEJAR COMENTADA CUALQUIER LLAMADA A LAS FUNCIONES QUE SE TENGA EN ESTE ARCHIVO 
# Y DESCOMENTAR LAS QUE VIENEN A CONTINUACIÓN.

# EN EL APARTADO FINAL DE "RENDIMIENTOS FINALES RANDOM FOREST", USAR LA MEJOR COMBINACIÓN DE 
# HIPERPARÁMETROS QUE SE HAYA OBTENIDO EN CADA CASO, EN LA FASE DE AJUSTE DEL EJERCICIO 4

# ESTE ARCHIVO trabajo_aia_23_24_parte_I.py SERÁ CARGADO POR EL PROFESOR, 
# TENIENDO EN LA MISMA CARPETA LOS ARCHIVOS OBTENIDOS
# DESCOMPRIMIENDO datos_trabajo_aia.zip.
# ES IMPORTANTE QUE LO QUE SE ENTREGA SE PUEDA CARGAR SIN ERRORES Y QUE SE EJECUTEN LOS 
# EJEMPLOS QUE VIENEN A CONTINUACIÓN. SI ALGUNO DE LOS EJERCICIOS NO SE HA REALIZADO 
# O DEVUELVE ALGÚN ERROR, DEJAR COMENTADOS LOS CORRESPONDIENTES EJEMPLOS, 
# PARA EViTAR LOS ERRORES EN LA CARGA Y EJECUCIÓN.   



# *********** DESCOMENTAR A PARTIR DE AQUÍ

print("************ PRUEBAS EJERCICIO 1:")
print("**********************************\n")
Xe_votos, Xp_votos, ye_votos, yp_votos=particion_entr_prueba(X_votos,y_votos_cod,test=1/3)

print("Partición votos: ",y_votos.shape[0],ye_votos.shape[0],yp_votos.shape[0])
print("Proporción original en votos: ",np.unique(y_votos,return_counts=True))
print("Estratificación entrenamiento en votos: ",np.unique(ye_votos,return_counts=True))
print("Estratificación prueba en votos: ",np.unique(yp_votos,return_counts=True))
print("\n")

Xev_cancer,Xp_cancer,yev_cancer,yp_cancer=particion_entr_prueba(X_cancer,y_cancer,test=0.2)
print("Proporción original en cáncer: ", np.unique(y_cancer,return_counts=True))
print("Estratificación entr-val en cáncer: ",np.unique(yev_cancer,return_counts=True))
print("Estratificación prueba en cáncer: ",np.unique(yp_cancer,return_counts=True))
Xe_cancer,Xv_cancer,ye_cancer,yv_cancer=particion_entr_prueba(Xev_cancer,yev_cancer,test=0.2)
print("Estratificación entrenamiento cáncer: ", np.unique(ye_cancer,return_counts=True))
print("Estratificación validación cáncer: ",np.unique(yv_cancer,return_counts=True))
print("\n")

Xe_credito,Xp_credito,ye_credito,yp_credito=particion_entr_prueba(X_credito,y_credito,test=0.4)
print("Estratificación entrenamiento crédito: ",np.unique(ye_credito,return_counts=True))
print("Estratificación prueba crédito: ",np.unique(yp_credito,return_counts=True))
print("\n\n\n")




print("************ PRUEBAS EJERCICIO 2:")
print("**********************************\n")

clf_titanic = ArbolDecision(max_prof=3,min_ejemplos_nodo_interior=5,n_atrs=3)
clf_titanic.entrena(X_train_titanic, y_train_titanic)
clf_titanic.imprime_arbol(["Pclass", "Mujer", "Edad"],"Partido")
rend_train_titanic = rendimiento(clf_titanic,X_train_titanic,y_train_titanic)
rend_test_titanic = rendimiento(clf_titanic,X_test_titanic,y_test_titanic)
print(f"****** Rendimiento DT titanic train: {rend_train_titanic}")
print(f"****** Rendimiento DT titanic test: {rend_test_titanic}\n\n\n\n ")




clf_votos = ArbolDecision(min_ejemplos_nodo_interior=3,max_prof=5,n_atrs=16,prop_umbral=1.0)
clf_votos.entrena(Xe_votos, ye_votos)
print(clf_votos.clasifica(Xe_votos), ye_votos)
nombre_atrs_votos=[f"Votación {i}" for i in range(1,17)]
clf_votos.imprime_arbol(nombre_atrs_votos,"Partido")
rend_train_votos = rendimiento(clf_votos,Xe_votos,ye_votos)
rend_test_votos = rendimiento(clf_votos,Xp_votos,yp_votos)
print(f"****** Rendimiento DT votos en train: {rend_train_votos}")
print(f"****** Rendimiento DT votos en test:  {rend_test_votos}\n\n\n\n")



clf_iris = ArbolDecision(max_prof=3,n_atrs=4)
clf_iris.entrena(X_train_iris, y_train_iris)
clf_iris.imprime_arbol(["Long. Sépalo", "Anch. Sépalo", "Long. Pétalo", "Anch. Pétalo"],"Clase")
rend_train_iris = rendimiento(clf_iris,X_train_iris,y_train_iris)
rend_test_iris = rendimiento(clf_iris,X_test_iris,y_test_iris)
print(f"********************* Rendimiento DT iris train: {rend_train_iris}")
print(f"********************* Rendimiento DT iris test: {rend_test_iris}\n\n\n\n ")





clf_cancer = ArbolDecision(min_ejemplos_nodo_interior=3,max_prof=10,n_atrs=15)
clf_cancer.entrena(Xev_cancer, yev_cancer)
nombre_atrs_cancer=['mean radius', 'mean texture', 'mean perimeter', 'mean area',
        'mean smoothness', 'mean compactness', 'mean concavity',
        'mean concave points', 'mean symmetry', 'mean fractal dimension',
        'radius error', 'texture error', 'perimeter error', 'area error',
        'smoothness error', 'compactness error', 'concavity error',
        'concave points error', 'symmetry error',
        'fractal dimension error', 'worst radius', 'worst texture',
        'worst perimeter', 'worst area', 'worst smoothness',
        'worst compactness', 'worst concavity', 'worst concave points',
        'worst symmetry', 'worst fractal dimension']
clf_cancer.imprime_arbol(nombre_atrs_cancer,"Es benigno")
rend_train_cancer = rendimiento(clf_cancer,Xev_cancer,yev_cancer)
rend_test_cancer = rendimiento(clf_cancer,Xp_cancer,yp_cancer)
print(f"***** Rendimiento DT cancer en train: {rend_train_cancer}")
print(f"***** Rendimiento DT cancer en test: {rend_test_cancer}\n\n\n")


print("************ RENDIMIENTOS FINALES RANDOM FOREST")
print("************************************************\n")

# ATENCIÓN: EN CADA CASO, INCORPORAR LA MEJOR COMBINACIÓN DE HIPERPARÁMETROS 
# QUE SE HA OBTENIDO EN EL PROCESO DE AJUSTE



print("==== MEJOR RENDIMIENTO RANDOM FOREST SOBRE IMDB:")
RF_IMDB=RandomForest(*[5,1.0,20,8,200,0.8]) # ATENCIÓN: incorporar aquí los mejores valoeres de los parámetros tras el ajuste
RF_IMDB.entrena(X_train_imdb,y_train_imdb) 
print("Rendimiento RF entrenamiento sobre imdb: ",rendimiento(RF_IMDB,X_train_imdb,y_train_imdb))
print("Rendimiento RF test sobre imdb: ",rendimiento(RF_IMDB,X_test_imdb,y_test_imdb))
print("\n")




print("==== MEJOR RENDIMIENTO RANDOM FOREST SOBRE CRÉDITO:")
RF_CREDITO=RandomForest(n_arboles=10,prop_muestras=0.7,min_ejemplos_nodo_interior=3,max_prof=7,n_atrs=6,prop_umbral=0.7) # ATENCIÓN: incorporar aquí los mejores valores de los parámetros tras el ajuste
RF_CREDITO.entrena(X_train_credito,y_train_credito) 
print("Rendimiento RF entrenamiento sobre crédito: ",rendimiento(RF_CREDITO,X_train_credito,y_train_credito))
print("Rendimiento RF  test sobre crédito: ",rendimiento(RF_CREDITO,X_test_credito,y_test_credito))
print("\n")


print("==== MEJOR RENDIMIENTO RF SOBRE ADULT:")

RF_ADULT=RandomForest(*[3,0.5,7,5,6,0.7]) # ATENCIÓN: incorporar aquí los mejores valores de los parámetros tras el ajuste
RF_ADULT.entrena(X_train_adult,y_train_adult) 
print("Rendimiento RF  entrenamiento sobre adult: ",rendimiento(RF_ADULT,X_train_adult,y_train_adult))
print("Rendimiento RF  test sobre adult: ",rendimiento(RF_ADULT,X_test_adult,y_test_adult))
print("\n")


print("==== MEJOR RENDIMIENTO RL SOBRE DIGITOS:")
RF_DG=RandomForest(*[2,0.7,100,5,100,0.4]) # ATENCIÓN: incorporar aquí los mejores valors de losparámetros tras el ajuste
RF_DG.entrena(X_train_dg,y_train_dg)
print("Rendimiento RF entrenamiento sobre dígitos: ",rendimiento(RF_DG,X_train_dg,y_train_dg))
print("Rendimiento RF validación sobre dígitos: ",rendimiento(RF_DG,X_valid_dg,y_valid_dg))
print("Rendimiento RF test sobre dígitos: ",rendimiento(RF_DG,X_test_dg,y_test_dg))








