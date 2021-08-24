"""
-----------------------LIBRERÍAS Y MÓDULOS-------------------------------------------------------------------------------
"""
#Para trabajar con los ficheros temporales que se crean
import os
import os.path

#Básicos para trabajar con los arrays y operar
import numpy as np
import pandas as pd
import math

#Módulos para crear la aplicación visual, la interfaz de usuario
import tkinter as tk
from tkinter import *
from tkinter import filedialog as FileDialog
from tkinter import messagebox as MessageBox

#Para dibujar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#Para el error cuadratico medio
from sklearn.metrics import mean_squared_error

#Estos para la regresión con statsmodels, para los ajustes lineales
import statsmodels.api as sm
import statsmodels.formula.api as smf

#Para los warnings
import warnings

#Para los ajustes no lineales.
from scipy.optimize import leastsq

"""
------------------------CONFIGURACIÓN WARNINGS-------------------------------------------------------------
"""
warnings.filterwarnings('ignore')

"""
---------------------------FUNCIONES---------------------------------------------------------------------------
Las funciones creadas en la aplicación son para asociar a cada botón de la interfaz a una funcionalidad concreta
"""

"""
#Función que no está asociada a ninguna pestaña, es solo para limpiar cuando pulses en una pestaña
"""
def windowClear():
    #Para los que están con pack
    list = principalRoot.pack_slaves() 
    for l in list: 
        l.destroy()
    #Para los que están con grid
    list1 = principalRoot.grid_slaves()
    for l1 in list1:
        l1.destroy()
    #Para los que están con place
    list2 = principalRoot.place_slaves()
    for l2 in list2:
        l2.destroy()  
    #Esto para devolver el root a su tamaño original.
    principalRoot.config(width = 480, height = 320)

"""
#Función para definir la configuración inicial de la interfaz
"""
def initialConfiguration():
    #Variables con el nombre de la APP
    global texto2
    texto2 = ("APP PARA ANÁLISIS DE DATOS O-C "
    "\n DE MÍNIMOS DE BINARIAS ECLIPSANTES")
    #Crearemos un marco en el que escribiremos el nombre de la APP
    tittleLabel = Label(principalRoot, bg = "Grey", text = texto2)
    #Cambiamos el tamaño de la letra
    tittleLabel.config(font=('Arial', 15))
    #Con este método place no se cambia el tamaño del contenedor.
    tittleLabel.place(x = 20, y= 80) 

    #Variables con el nombre
    global texto3
    texto3 = ("Toribio Gutiérrez González")
    #Crearemos un marco en el que escribiremos el nombre
    nameLabel = Label(principalRoot, bg = "Grey", text = texto3)
    #Con este método place no se cambia el tamaño del contenedor.
    nameLabel.place(x = 130, y= 200) 

    #Variables con el correo
    global texto4
    texto4 = ("toribiogg@gmail.com")
    #Crearemos un marco en el que escribiremos el correo
    mailLabel = Label(principalRoot, bg = "Grey", text = texto4)
    #Con este método place no se cambia el tamaño del contenedor.
    mailLabel.place(x = 139, y= 225) 

"""
-------------Funciones para cerrar y resetear la aplicación---------------------------
"""
def cerrar():
    #Vemos si existen los fichero temporales para eliminarlos
    if (os.path.isfile('temporal.txt')): 
        os.remove('temporal.txt')
    if (os.path.isfile('temporal_efemerides.txt')):
        os.remove('temporal_efemerides.txt')
    principalRoot.quit() 
    principalRoot.destroy() 
    #Para terminar por completo la ejecución del programa
    exit(0)

"""
Función para resetear, que lo que hace es eliminar los ficheros temporales sin cerrar el programa
"""
def reseteo():
    #Para limpiar los wdigets que haya
    windowClear()
    #Para volver a la configuración inicial
    initialConfiguration()
    
    #Vemos si existen los fichero temporales para eliminarlos 
    if (os.path.isfile('temporal.txt')): 
        os.remove('temporal.txt')
    if (os.path.isfile('temporal_efemerides.txt')):
        os.remove('temporal_efemerides.txt')
    MessageBox.showinfo("RESET", "Introduce tus nuevos datos de entradas para realizar los ajustes")

"""
----------------Funciones para leer los valores de entrada---------------------------------------
"""
"""
Función para leer las efemérides de referencia
"""
def efemerides():
    #Para limpiar los wdigets que haya
    windowClear()
    
    #Función "interna" para cuando el usuario pulse el botón aceptar
    def botonEfemerides():
        #Para controlar que el usuario meta valores numéricos y separados por puntos, 
        #hay que usar StringVar(), y capturar la excepción
        try:
            x = float(epoch.get())
            y = float(period.get())

            ephemerides = pd.DataFrame([float(x), float(y)])  
            #Las guardamos en un fichero temporal      
            ephemerides.to_csv("temporal_efemerides.txt", sep = " ", header = None, index = None) 
            #Esto para que cuando le de aceptar se elimina el marco que pide los valores
            ephemeridesFrame.destroy()
            #Esto para devolver el root a su tamaño original.
            principalRoot.config(width = 480, height = 320)

            #Para nostrar la configuración inicial
            initialConfiguration()
        except:
            MessageBox.showwarning("TIPOS NO VÁLIDOS", "Introduce unos valores correctos, han de ser numéricos, separados por punto")
            #Para nostrar la configuración inicial
            initialConfiguration()

    #Se define el cuadro que saldrá en la interfaz para pedir los valores de referencia
    #Primero se crea el marco
    ephemeridesFrame = Frame(principalRoot)  
    #Lo empaquetamos en la raíz, en el cuadro de interfaz principal.
    ephemeridesFrame.pack(fill="both")      
    #Configuración del marco
    #color
    ephemeridesFrame.config(bg = "CadetBlue")     
    #Tamaño
    ephemeridesFrame.config(width = 750, height = 750) 
    #Tipo de cursor
    ephemeridesFrame.config(cursor = "star")
    #Tamaño borde
    ephemeridesFrame.config(bd = 24)
    #Tipo de Borde 
    ephemeridesFrame.config(relief ="sunken")
    
    #Etiqueta para el título
    tittleLabel = Label(ephemeridesFrame, text = "EFEMÉRIDES DE REFERENCIA")
    tittleLabel.grid(row = 0, column = 0, columnspan=2)
    
    #Variables para trabajar con ella desde las funciones
    epoch = StringVar()
    period = StringVar()
    
    #Nombre para pedir la primera variable
    epochLabel = Label(ephemeridesFrame, bg = "CadetBlue", text = "Época inicial: ")
    epochLabel.grid(row = 1, column = 0)
    #Entrada para la primera variable
    epochEntry = Entry(ephemeridesFrame, textvariable = epoch)
    epochEntry.grid(row = 1, column = 1)
    
    #Nombre para pedir la segunda variable
    periodLabel = Label(ephemeridesFrame, bg = "CadetBlue", text = "Periodo de referencia: ")
    periodLabel.grid(row = 2, column = 0)
    #Entrada para la segunda variable
    periodEntry = Entry(ephemeridesFrame, textvariable = period)
    periodEntry.grid(row = 2, column = 1)
        
    #Le añado el botón que trabajará con las variables que le hemos pasado, este llamará a la función "interna",
    Button(ephemeridesFrame, text = "Aceptar", command = botonEfemerides).grid(row = 3, column = 0, columnspan=2)

"""    
Función que lee el ficheor de los valores de entrada, y realiza el cálculo de los mínimos, guardandolos en un ficheor 
temporal, para trabajar con ellos en las diferentes partes de la aplicación
"""
def ruta():
    #Para limpiar los wdigets que haya
    windowClear()

    #Para volver a la configuración inicial
    initialConfiguration()

    #Para que se pueda ejecutar todo esto, tienen que haberse introducido las efemérides de referencia, 
    #y, por tanto exixtir el fichero, de modo que se añade esta comprobación devolviéndose un mensaje de advertencia
    if (os.path.isfile('temporal_efemerides.txt')):
        #Para pedir la ruta del fichero en el que están contenidos los datos
        ruta_fichero = FileDialog.askopenfilename(filetypes = (("Ficheros de texto", "*.txt"),("Todos los ficheros","*.*")),title = "Selección de archivo con datos de entrada", )
        archivo = np.loadtxt(ruta_fichero, usecols = [0,1])
        #También leo la columna del tipo de mínimo para saber como hacer el cálculo
        tipoMin = np.loadtxt(ruta_fichero, usecols = [2], dtype = str)
        #Cargamos el archivo con los valores de referencia
        efemerides = np.loadtxt('temporal_efemerides.txt')

        C = np.zeros(len(archivo))
        OC = np.zeros(len(archivo))
        M = np.zeros(len(archivo))
        epoch = np.zeros(len(archivo))

        #Valores de referencia para utilizar en los cálculos
        E = efemerides[0]
        P = efemerides[1] 

        #Primero hago el cáclculo de los M, que luego se guardaran en la época
        for i in range(len(archivo)):
            if (tipoMin[i] == 'p') or (tipoMin[i] == 'I'): 
                M[i] = int((archivo[i,0] - E)/P)

            elif (tipoMin[i] == 's') or (tipoMin[i] == 'II'):
                if (archivo[i,0] > E):
                    M[i] = int((archivo[i,0] - E)/P) + 0.5
                elif (archivo[i,0] < E):
                    M[i] = int((archivo[i,0] - E)/P) - 0.5

        #Ahora hacemos el cáclculo de los mínimos , los O-C, y le época que hay que guardar en función de los M
        for i in range(len(archivo)):
            if (tipoMin[i] == 'p') or (tipoMin[i] == 'I'):
                if (archivo[i,0] >= E):
                    c1 = E + P * M[i]
                    c2 = E + P * (M[i] + 1)
                elif (archivo[i,0] < E):
                    c1 = E + P * M[i]
                    c2 = E + P * (M[i] - 1)

                #Ahora se calcula los OC intermedios
                oc1 = archivo[i,0] - c1
                oc2 = archivo[i,0] - c2
                #Su valor absoluto
                ABSoc1 = abs(oc1)
                ABSoc2 = abs(oc2)

                #En función de que valor absoluto sea mayor guardamos uno u otro
                if(ABSoc2 > ABSoc1):
                    C[i] = c1
                    OC[i] = oc1
                elif(ABSoc1 > ABSoc2):
                    C[i] = c2
                    OC[i] = oc2

                #Ahora para ver cual sera el valor de la época que guardaremos
                if (archivo[i,0] > E):
                    epoch[i] = M[i] + 1
                elif (archivo[i,0] < E):
                    epoch[i] = M[i] - 1

            elif (tipoMin[i] == 's') or (tipoMin[i] == 'II'):
                C[i] = E + P * M[i]
                OC[i] = archivo[i,0] - C[i]
                epoch[i] = M[i]

            #Creo el array con todas estas variables
            temporalData = np.zeros((len(archivo), 5))
            for i in range(len(archivo)):
                temporalData[i,0] = archivo[i,0] #el valor observado
                temporalData[i,1] = archivo[i,1] #el error del valor observado
                temporalData[i,2] = C[i] #El calculado
                temporalData[i,3] = OC[i] #la diferencia entre ambos (O - C)
                temporalData[i,4] = epoch[i] #La época (eje x)

        #Ahora lo paso a DataFrame
        final1 = pd.DataFrame(temporalData, columns = ['Observados', 'Error', 'Calculados', 'O - C', 'Época'])
        #En el que tenemos el tipo de minimo
        final2 = pd.DataFrame(tipoMin, columns = ['Tipo Mínimo'])

        #Los Juntamos 
        final = pd.concat([final1, final2], axis=1)
        #Lo guardo en un fichero temporal
        final.to_csv("temporal.txt", sep = " ", index = None) 
        #Enviamos un mensaje al usuario para que sepa que los mensajes se han cargado correctamenter
        MessageBox.showinfo("CARGA COMPLETA", "Tus datos se han cargado correctamente")
        
    else:
        MessageBox.showwarning("ERROR DE FLUJO", "Introduce primero los valores de las efemérides de referencia en la pestaña correspondiente")
    
"""
--------------Funciones para la salida de los datos----------------------
"""

"""
Función que guarda los cálculos en un fichero de salida
"""
def salida():
    #Para limpiar los wdigets que haya
    windowClear()

    #Para volver a la configuración inicial
    initialConfiguration()

    #Para controlar el flujo y que se introduzcan primero los datos de entrada.
    if (os.path.isfile('temporal.txt')):
        ruta_salida = FileDialog.asksaveasfile(title = "Fichero de guardado", defaultextension = ".txt")
        archivoSalida = pd.read_csv('temporal.txt', sep = ' ')    
        archivoSalida.to_csv(ruta_salida.name, sep = "\t", index = False)
        
    else:
        MessageBox.showwarning("ERROR DE FLUJO", "Introduce primero los datos de entrada (efemérides de referencia y mínimos observados)")

"""   
Función para realizar el diagrama O-C
"""
def diagrama():
    #Para limpiar los wdigets que haya
    windowClear()

    #Para volver a la configuración inicial
    initialConfiguration()

    #Control de Flujo, que primero estén los datos de entrada
    if (os.path.isfile('temporal.txt')):
        #primero tiene que leer los valores del fichero de salida
        archivoRepresentar = np.loadtxt('temporal.txt', usecols = [3,4], skiprows = 1) #Ya que el OC y la época están en la cuarta y la quinta columna respectivamwente
        #Para la barra de error
        error = np.loadtxt('temporal.txt', usecols = [1], skiprows = 1) #El error está en la columna 1
        #Ahora habría que crear la gráfica para que salte en una ventana tkinter

        #Creamos un root diferente
        RaizGrafica = tk.Tk()
        RaizGrafica.wm_title('Diagrama O-C')

        #Realizamos la gráfica
        figDiagrama = plt.figure(figsize = (7, 5), dpi=100)

        plot_figDiagrama = figDiagrama.add_subplot(111)
        plot_figDiagrama.set_xlabel("E")
        plot_figDiagrama.set_ylabel("O - C [dias]")
        plot_figDiagrama.set_title("Diagrama O-C")
        diagrama, = plot_figDiagrama.plot(archivoRepresentar[:,1], archivoRepresentar[:,0], 'o', label = "Datos")
        #Para la barra de error
        plot_figDiagrama.errorbar(archivoRepresentar[:,1], archivoRepresentar[:,0], yerr = error, fmt = 'o', color = "blue")

        plot_figDiagrama.legend(loc = 'best')

        #con Canvas se crea el área de dibujo
        canvasDiagrama = FigureCanvasTkAgg(figDiagrama, master = RaizGrafica)
        canvasDiagrama.draw()
        canvasDiagrama.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

        #ahora añadimos la barra de herramientas
        toolbarDiagrama = NavigationToolbar2Tk(canvasDiagrama, RaizGrafica)
        toolbarDiagrama.update()
        canvasDiagrama.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

        RaizGrafica.mainloop()
    
    else:
        MessageBox.showwarning("ERROR DE FLUJO", "Introduce primero los datos de entrada (efmérides de referencia y mínimos observados)")

"""
---------------Funciones que implementan los ajustes de los modelos----------------
"""
"""
Función para hacer el ajuste lineal
"""
def lineal():
    #Para limpiar los wdigets que haya
    windowClear()

    #Para volver a la configuración inicial
    initialConfiguration()

    #Control de Flujo, que primero estén los datos de entrada
    if (os.path.isfile('temporal.txt')):
        #Pedimos al usuario donde va a querer guardar tanto el resumen como los paramétros del ajuste
        MessageBox.showinfo("Resumen Ajuste", "Introduce la ruta del fichero donde guardar el resumen del ajuste")
        ruta_resumen_lineal = FileDialog.asksaveasfile(title = "Resumen del ajuste lineal", defaultextension = ".txt")
        MessageBox.showinfo("Parámetros ajuste", "Introduce la ruta del fichero donde guardar los parámetros del ajuste")
        ruta_parametros_lineal = FileDialog.asksaveasfile(title = "Parámetros del ajuste lineal", defaultextension = ".txt")
        
        #Primero se leen los datos que estarán en el archivo temporal
        dataAjuste = np.loadtxt('temporal.txt', usecols = [3,4], skiprows = 1) #Nos interesan la cuarta y quinta columnas

        #Para la barra de error
        error = np.loadtxt('temporal.txt', usecols = [1], skiprows = 1) #El error está en la columna 1
        #Creamos el array con los pesos de los errores, uno/error^2
        pesoError = np.zeros(len(error))
        for i in range (len(error)):
            #Aquí pasa que podemos tener un error de cero y esto pues tiende a infinito
            if (error[i] == 0.0):
                #pesoError[i] = 1/(0.00000000001**2)
                #Se pone como un valor alto del error, el ajuste es más parecido a los ejemplos, esto quiere decir que los
                #valores sin error de los artículos realmente tienen un error elevado, no muy cercano a cero
                pesoError[i] = 1/(0.1**2)
            else:
                pesoError[i] = 1/(error[i]**2)
        #Guardo los datos en un Dataframe, de modo que estén ordenados, primero la X y luego la Y
        DFX = pd.DataFrame(dataAjuste[:,1], columns = ['epoch'])
        DFY = pd.DataFrame(dataAjuste[:,0], columns = ['OC'])
        DFAjuste = pd.concat([DFX, DFY], axis=1)

        #Se hace el ajuste a nuestro modelo, primero se crea una instancia al modelo lineal, el ajuste con pesos ponderados
        modLineal = smf.wls(formula = 'OC ~ epoch', data = DFAjuste, weights = pesoError).fit()

        #Este es el ajuste son pesos, sin que sea ponderado
        #modLineal = smf.ols(formula = 'OC ~ epoch', data = DFAjuste).fit()

        #Guardamos el resumen del ajuste en el ficheor que nos ha proporcionado el usuario
        f1 = open(ruta_resumen_lineal.name, "w")
        f1.write(modLineal.summary().as_text())
        f1.close()

        #Predicciones que son necesarias tanto para pintar como para sacar el RMSE
        prediccionesLineal = modLineal.get_prediction().summary_frame(alpha=0.05)
        #Calculamos el RMSE
        rmse = mean_squared_error(
            y_true  = dataAjuste[:,0],
            y_pred  = prediccionesLineal.iloc[:,0],
            squared = False
           )

        #Guardamos los parámetros en el fichero que le hemos preguntado al usuario
        f2 = open(ruta_parametros_lineal.name, "w")
        f2.write("----------------------------Modelo de ajuste Lienal-----------------------\n")
        f2.write("--------------------------------- f = a  + b * x---------------------------\n")
        f2.write("\n")
        f2.write(f"Modelo: f = {modLineal.params[0]} + {modLineal.params[1]} x\n")
        f2.write(f"Coficientes: a = {modLineal.params[0]}, b = {modLineal.params[1]}\n")
        f2.write(f"Desviación estándar coeficientes: std(a) = {modLineal.bse[0]}, std(b) = {modLineal.bse[1]}\n")
        f2.write(f"R^2: {modLineal.rsquared}\n")
        f2.write(f"Error cuadrático medio (rmse): {rmse}\n")
        f2.close()

        #Pintamos el gráfico
        prediccionesLineal['x'] = DFAjuste.iloc[:,0]
        prediccionesLineal['y'] = DFAjuste.iloc[:,1]
        prediccionesLineal = prediccionesLineal.sort_values('x')

        #Sacar el gráfico por una entana (root) emergente.
        #Primero la ventana
        RaizLineal = tk.Tk()
        RaizLineal.wm_title('Ajuste lineal')
        #Segundo la gráfica
        figLineal = plt.figure(figsize = (7, 5), dpi=100)
        #se añade el subplot
        plot_figLineal = figLineal.add_subplot(111)
        plot_figLineal.set_xlabel("E")
        plot_figLineal.set_ylabel("O - C [dias]")
        plot_figLineal.set_title("Ajuste Lineal")
        DiagramaLineal, = plot_figLineal.plot(prediccionesLineal['x'], prediccionesLineal['y'], 'o', color = "Blue", label = "Datos")

        #Para agregar la barra de error
        plot_figLineal.errorbar(prediccionesLineal['x'], prediccionesLineal['y'], yerr = error, fmt = 'o', color = "blue")

        DiagramaLineal, = plot_figLineal.plot(prediccionesLineal['x'], prediccionesLineal["mean"], linestyle='-', color = 'red', label="Ajuste")
        DiagramaLineal, = plot_figLineal.plot(prediccionesLineal['x'], prediccionesLineal["mean_ci_lower"], linestyle='--', color='green', label="95% CI")
        DiagramaLineal, = plot_figLineal.plot(prediccionesLineal['x'], prediccionesLineal["mean_ci_upper"], linestyle='--', color='green')
        #DaigramaLineal, = plot_fig2.fill_between(prediccionesLineal['x'], prediccionesLineal["mean_ci_lower"], prediccionesLineal["mean_ci_upper"], alpha=0.1
        plot_figLineal.legend(loc = "best")

        #con Canvas se crea el área de dibujo
        canvasLineal = FigureCanvasTkAgg(figLineal, master = RaizLineal)
        canvasLineal.draw()
        canvasLineal.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
        #ahora añadimos la barra de herramientas
        toolbarLineal = NavigationToolbar2Tk(canvasLineal, RaizLineal)
        toolbarLineal.update()
        canvasLineal.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

        RaizLineal.mainloop()
        
    else: 
        MessageBox.showwarning("ERROR DE FLUJO", "Introduce primero los datos de entrada (efmérides de referencia y mínimos observados)")

"""    
#Función del ajuste parabolico
"""
def parabolico():
    #Para limpiar los wdigets que haya
    windowClear()

    #Para volver a la configuración inicial
    initialConfiguration()

    #Control de Flujo, que primero estén los datos de entrada
    if (os.path.isfile('temporal.txt')):
        #Pedimos al usuario donde va a querer guardar tanto el resumen como los paramétros del ajuste
        MessageBox.showinfo("Resumen Ajuste", "Introduce la ruta del fichero donde guardar el resumen del ajuste")
        ruta_resumen_parabolico = FileDialog.asksaveasfile(title = "Resumen del ajuste parabolico", defaultextension = ".txt")
        MessageBox.showinfo("Parámetros ajuste", "Introduce la ruta del fichero donde guardar los parámetros del ajuste")
        ruta_parametros_parabolico = FileDialog.asksaveasfile(title = "Parámetros del ajuste parabolico", defaultextension = ".txt")
        #primero se leen los datos que estarán en el archivo temporal
        dataAjusteParabolico = np.loadtxt('temporal.txt', usecols = [3,4], skiprows = 1)

        #Para la barra de error
        error = np.loadtxt('temporal.txt', usecols = [1], skiprows = 1) #El error está en la columna 1
        #Creamos el arrya con los pesos de los errores, uno/error^2
        pesoError = np.zeros(len(error))
        for i in range (len(error)):
            #Aquí pasa que podemos tener un error de cero y tendería a infinito en la función.
            if (error[i] == 0.0):
                #pesoError[i] = 1/(0.00000000001**2)
                pesoError[i] = 1/(0.1**2)
            else:
                pesoError[i] = 1/(error[i]**2)

        #Los guardo en un DataFrame, ordenado (X, Y)
        DFXParabolico = pd.DataFrame(dataAjusteParabolico[:,1], columns = ['epoch'])
        DFYParabolico = pd.DataFrame(dataAjusteParabolico[:,0], columns = ['OC'])
        DFAjusteParabolico = pd.concat([DFXParabolico, DFYParabolico], axis=1)

        #Se hace el ajuste a nuestro modelo, creando una instancia al mismo, utilizamos mínimos cuadrados ponderados
        modParabolico = smf.wls(formula = 'OC ~  epoch + np.power(epoch, 2)', data = DFAjusteParabolico, weights = pesoError).fit()

        #Ajuste sin pesos, minimos cuadrados ordinarios
        #modParabolico = smf.ols(formula = 'OC ~  epoch + np.power(epoch, 2)', data = DFAjusteParabolico).fit()

        #Guardamos el resumen del ajuste en el ficheor que nos ha proporcionado el usuario
        f3 = open(ruta_resumen_parabolico.name, "w")
        f3.write(modParabolico.summary().as_text())
        f3.close()

        #Predicciones que son necesarias tanto para pintar como para sacar el RMSE
        prediccionesParabolico = modParabolico.get_prediction().summary_frame(alpha=0.05)

        #Calculamos el RMSE
        rmse1 = mean_squared_error(
            y_true  = dataAjusteParabolico[:,0],
            y_pred  = prediccionesParabolico.iloc[:,0],
            squared = False
           )

        #Guardamos los parámetros en el fichero que le hemos preguntado al usuario
        f4 = open(ruta_parametros_parabolico.name, "w")
        f4.write("----------------------------Modelo de ajuste Parabolico-----------------------\n")
        f4.write("----------------------------- f = a + b * x + c * x^2------------------------\n")
        f4.write("\n")
        f4.write(f"Modelo: f = {modParabolico.params[0]} + {modParabolico.params[1]} x + {modParabolico.params[2]} x^2\n")
        f4.write(f"Coficientes: a = {modParabolico.params[0]}, b = {modParabolico.params[1]}\, c = {modParabolico.params[2]}\n")
        f4.write(f"Desviación estándar coeficientes: std(a) = {modParabolico.bse[0]}, std(b) = {modParabolico.bse[1]}, std(c) = {modParabolico.bse[2]}\n")
        f4.write(f"R^2: {modParabolico.rsquared}\n")
        f4.write(f"Erro cuadrático medio (rmse): {rmse1}\n")
        f4.close()

        #Pintamos la gráfica
        prediccionesParabolico['x'] = DFAjusteParabolico.iloc[:,0] 
        prediccionesParabolico['y'] = DFAjusteParabolico.iloc[:,1]
        prediccionesParabolico = prediccionesParabolico.sort_values('x')


        #Pintamos la gráfica y la mostramos por una ventana emergente.
        #Primero la ventana
        RaizParabolico = tk.Tk()
        RaizParabolico.wm_title('Ajuste Parabólico')
        #Segundo la gráfica
        figParabolico = plt.figure(figsize = (7, 5), dpi = 100)
        #se añade el subplot
        plot_figParabolico = figParabolico.add_subplot(111)
        plot_figParabolico.set_xlabel("E")
        plot_figParabolico.set_ylabel("O - C [dias]")
        plot_figParabolico.set_title("Ajuste Parabólico")
        DaigramaParabolico, = plot_figParabolico.plot(prediccionesParabolico['x'], prediccionesParabolico['y'], 'o', color = "Blue", label = "Datos")

        #Agregamos la barra de error
        plot_figParabolico.errorbar(prediccionesParabolico['x'], prediccionesParabolico['y'], yerr = error, fmt = 'o', color = "Blue")

        DaigramaParabolico, = plot_figParabolico.plot(prediccionesParabolico['x'], prediccionesParabolico["mean"], linestyle='-', color = 'red', label="Ajuste")
        DaigramaParabolico, = plot_figParabolico.plot(prediccionesParabolico['x'], prediccionesParabolico["mean_ci_lower"], linestyle='--', color='green', label="95% CI")
        DaigramaParabolico, = plot_figParabolico.plot(prediccionesParabolico['x'], prediccionesParabolico["mean_ci_upper"], linestyle='--', color='green')
        plot_figParabolico.legend(loc = "best")

        #con Canvas se crea el área de dibujo
        canvasParabolico = FigureCanvasTkAgg(figParabolico, master = RaizParabolico)
        canvasParabolico.draw()
        canvasParabolico.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
        #ahora añadimos la barra de herramientas
        toolbarParabolico = NavigationToolbar2Tk(canvasParabolico, RaizParabolico)
        toolbarParabolico.update()
        canvasParabolico.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

        RaizParabolico.mainloop()
    
    else:
        MessageBox.showwarning("ERROR DE FLUJO", "Introduce primero los datos de entrada (efmérides de referencia y mínimos observados)") 

"""    
#Función para hacer el ajuste senoidal con tendencia lineal y excentricidad = 0
"""
def linealSenoidalCero():
    #Para limpiar los wdigets que haya
    windowClear()

    #Control de Flujo, que primero estén los datos de entrada
    if (os.path.isfile('temporal.txt')):
        #Necesitamos los valores de las efemérides de referencia P, E, se leen de los ficheros, 
        #para emplearlos en los modelos de ajuste.
        efemerides = np.loadtxt('temporal_efemerides.txt')
        E = efemerides[0]
        P = efemerides[1]

        #Pedimos al usuario donde va a querer guardar los parámetros del ajuste
        MessageBox.showinfo("Parámetros Ajuste", "Introduce la ruta del fichero donde guardar los parámetros del ajuste")
        ruta_resumen_senoidalLineal = FileDialog.asksaveasfile(title = "Parámetros del ajuste senoidal-lineal (e=0)", defaultextension = ".txt")
        
        #Primero la función boton para pulsarla cuando se le pasen los valores de entrada y realizar el ajuste
        def LinealCeroBoton():
            #Primero las funciones de los residuos para que trabaje la librería
            
            #Funcion del modelo
            def LinealSenoCero(p, x):
                return p[0] + p[1] * x + p[2] * np.sin((2 * math.pi * x )/p[3] + p[4])

            #Funcion con los residuos
            def ResiduosLinealSenoCero(p, y, x):
                y_modelo = LinealSenoCero(p, x)
                return y_modelo - y

            #Genero el array con los parámetros inciales, con el .get() para poder obtener el valor de la variable
            parametrosIniciales = np.array([float(a.get()), float(b.get()), float(A.get()), float(Pm.get()), float(fase.get())])

            #primero se leen los datos que estarán en el archivo temporal
            dataAjusteLinealCero = np.loadtxt('temporal.txt', usecols = [3,4], skiprows = 1)

            #Para la barra de error
            error = np.loadtxt('temporal.txt', usecols = [1], skiprows = 1) #El error está en la columna 1
            #Para cuando haya errores cero
            for i in range (len(error)):
                if (error[i] == 0.0):
                    #Suponiendo que si es cero, es porque los valores son muy pequeños
                    error[i] = 0.00000000001

            #Array para hacer la representación, 250 valores entre el máximo y el mínimo de la época
            maximo = np.amax(dataAjusteLinealCero[:,1])
            minimo = np.amin(dataAjusteLinealCero[:,1])
            salto = (maximo - minimo) / 250 #Quiereo 250 tramos
            #Se genera el array de las épocas (ejeX) para hacer la representación
            xRepresentar = np.zeros(250)
            valor = minimo
            for i in range (250):    
                xRepresentar[i] = valor
                valor += salto

            #Ajustamos al modelo
            X = dataAjusteLinealCero[:,1]
            Y = dataAjusteLinealCero[:,0]
            parametrosFinales, pcov, infodict, errmsg, success = leastsq(ResiduosLinealSenoCero, parametrosIniciales, args=(Y, X), full_output = True)
            """
            Método de control por si no se encuentra el resultado, si la función de ajuste no converge.
            """
            if (success == 0) or (success == 1) or (success == 2) or (success == 3) or (success == 4):
                
                """
                Calculamos los errores para mostrarlos en la información del modelo
                """
                #Primero los parámetros obtenidos con sus errores
                if (len(dataAjusteLinealCero[:,0]) > len(parametrosIniciales)) and pcov is not None:
                    s_sq = (ResiduosLinealSenoCero(parametrosFinales, dataAjusteLinealCero[:,0], dataAjusteLinealCero[:,1])**2).sum()/(len(dataAjusteLinealCero[:,0])-len(parametrosIniciales))
                    pcov = pcov * s_sq
                else:
                    pcov = np.inf

                errorLineal = [] 
                for i in range(len(parametrosFinales)):
                    try:
                        errorLineal.append(np.absolute(pcov[i][i])**0.5)
                    except:
                        errorLineal.append( 0.00 )
            
                erroresParametros = np.array(errorLineal) 

                #Forma alternativa del cálculo de los errores de los coeficientes
                """
                pstd = np.sqrt(np.diag(pcov))
                #Calculamos los errores de cada coeficientes
                erroresParametros = np.zeros(len(parametrosFinales))
                for i in range (len(parametrosFinales)):
                    erroresParametros[i] = pstd[i]/2
                """
                """
                #-------------R2---------
                """
                #Son necesarias las predicciones en base al modelo obtenido
                Y_predict = np.zeros(len(X))
                for i in range (len(X)):
                    Y_predict[i] = LinealSenoCero(parametrosFinales, X[i])

                #Valor medio 
                valuemed = np.mean(Y) 

                num = 0.0
                den = 0.0
                for i in range (len(Y_predict)):
                    #num += (Y[i] - valuemed)**2
                    #den += (Y_predict[i] - valuemed)**2
                    num += (Y_predict[i] - Y[i])**2
                    den += (Y[i] - valuemed)**2
                
                
                #rsquared2 = num/den
                rsquared2 = 1 - num/den
                """
                #-----RMSE----
                """
                #RMSE 
                inter = 0.0
                for i in range (len(Y_predict)):
                    inter += (Y_predict[i] - Y[i])**2

                rmse2 = inter/len(Y_predict)
                rmse2 = math.sqrt(rmse2)

                """
                #Lo guardamos en el ficheor que nos pasa el usuario
                """
                f5 = open(ruta_resumen_senoidalLineal.name, "w")
                f5.write("--------------------Modelo de ajuste Lineal Senoidal (e=0)--------------------\n")
                f5.write("---------------- f = a + b * x + A * sin((2 * pi * x)/Pm + w) ----------------\n")
                f5.write("\n")
                f5.write(f"Parámetros inciales: a = {parametrosIniciales[0]}, b = {parametrosIniciales[1]}, A = {parametrosIniciales[2]}\n")
                f5.write(f"                     Pm = {parametrosIniciales[3]}, fase = {parametrosIniciales[4]}\n")
                f5.write("\n")
                f5.write(f"Modelo: f = {parametrosFinales[0]} + {parametrosFinales[1]} * x + {parametrosFinales[2]} * sin((2 * pi * x )/{parametrosFinales[3]} + {parametrosFinales[4]})\n")
                f5.write(f"Parámetros finales: a = {parametrosFinales[0]}, b = {parametrosFinales[1]}, A = {parametrosFinales[2]}\n")
                f5.write(f"                    Pm = {parametrosFinales[3]}, fase = {parametrosFinales[4]}\n") 
                f5.write("\n")
                f5.write(f"Errores de los parámetros: E(a) = {erroresParametros[0]}, E(b) = {erroresParametros[1]}, E(A) = {erroresParametros[2]}\n")
                f5.write(f"                           E(Pm) = {erroresParametros[3]}, E(fase) = {erroresParametros[4]}\n") 
                f5.write("\n")
                f5.write(f"R^2: {rsquared2}\n")
                f5.write(f"Error cuadratico medio(rmse): {rmse2}\n")
                f5.close()

                
                #Generamos la curva obtenida por el modelo
                yAjuste = np.zeros(len(xRepresentar))
                for i in range (len(xRepresentar)):
                    yAjuste[i] = LinealSenoCero(parametrosFinales, xRepresentar[i])

                #Representamos como hicimos antes
                #primero ventana
                RaizLinealSenoidalCero = tk.Tk()
                RaizLinealSenoidalCero.wm_title('Ajuste Lineal-Senoidal (e=0)')
                figLinealCero = plt.figure(figsize = (7, 5), dpi = 100)
                #se añade el subplot
                plot_figLinealCero = figLinealCero.add_subplot(111)
                plot_figLinealCero.set_xlabel("E")
                plot_figLinealCero.set_ylabel("O - C [dias]")
                plot_figLinealCero.set_title("Ajuste Senoidal_lineal (e=0)")
                DiagramaLinealSenoidalCero, = plot_figLinealCero.plot(dataAjusteLinealCero[:,1], dataAjusteLinealCero[:,0], 'o', color = 'Blue', label = "Datos")

                #Barra de error
                plot_figLinealCero.errorbar(dataAjusteLinealCero[:,1], dataAjusteLinealCero[:,0], yerr = error, fmt = 'o', color = "Blue")
                
                DiagramaLinealSenoidalCero, = plot_figLinealCero.plot(xRepresentar, yAjuste, linestyle='-', color = 'red', label="Ajuste")
                plot_figLinealCero.legend(loc = "best")

                #con Canvas se crea el área de dibujo
                canvasLinealCero = FigureCanvasTkAgg(figLinealCero, master = RaizLinealSenoidalCero)
                canvasLinealCero.draw()
                canvasLinealCero.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
                #ahora añadimos la barra de herramientas
                toolbarLinealCero=NavigationToolbar2Tk(canvasLinealCero, RaizLinealSenoidalCero)
                toolbarLinealCero.update()
                canvasLinealCero.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

                InitialDataLinealCeroFrame.destroy()
                principalRoot.config(width = 480, height = 320)
                #Para volver a la configuración inicial
                initialConfiguration()
                RaizLinealSenoidalCero.mainloop()
            else:
                #Limpiamos 
                windowClear()

                #Agremamos configuración inicial de la ventana raíz
                initialConfiguration()

                MessageBox.showwarning("ERROR PROCESO", "El método de ajuste ha dado error, mensaje de error de la función:\n" + errmsg)
        #Primero se crea el marco
        InitialDataLinealCeroFrame = Frame(principalRoot)  

        #Lo empaquetamos en la raíz del programa
        InitialDataLinealCeroFrame.pack()      

        #Configuración del marco
        #Color
        InitialDataLinealCeroFrame.config(bg = "CadetBlue")     
        #Tamaño
        InitialDataLinealCeroFrame.config(width = 750, height = 750) 
        #Cursor
        InitialDataLinealCeroFrame.config(cursor = "star")
        #Tamaño borde
        InitialDataLinealCeroFrame.config(bd = 24)
        #Tipo de Borde 
        InitialDataLinealCeroFrame.config(relief ="sunken")
    

        #Etiqueta para el título
        tittleLabel = Label(InitialDataLinealCeroFrame, text = "Valores ajuste senoidal-lineal (e = 0)")
        tittleLabel.grid(row = 0, column = 0, columnspan = 2)

        #Variables para trabajar con ella desde las funciones
        a = DoubleVar()
        b = DoubleVar()
        A = DoubleVar()
        Pm = DoubleVar()
        fase = DoubleVar()

        #Nombre para pedir la primera variable
        var1Label = Label(InitialDataLinealCeroFrame, bg = "CadetBlue", text = "a")
        var1Label.grid(row = 1, column = 0)
        #Entrada para la primera variable
        var1Entry = Entry(InitialDataLinealCeroFrame, textvariable = a)
        var1Entry.grid(row = 1, column = 1)

        #Nombre para pedir la segunda variable
        var2Label = Label(InitialDataLinealCeroFrame, bg = "CadetBlue", text = "b")
        var2Label.grid(row = 2, column = 0)
        #Entrada para la segunda variable
        var2Entry = Entry(InitialDataLinealCeroFrame, textvariable = b)
        var2Entry.grid(row = 2, column = 1)

        #Nombre para pedir la tercera variable
        var3Label = Label(InitialDataLinealCeroFrame, bg = "CadetBlue", text = "Amplitud(A) [dias]")
        var3Label.grid(row = 3, column = 0)
        #Entrada para la tercera variable
        var3Entry = Entry(InitialDataLinealCeroFrame, textvariable = A)
        var3Entry.grid(row = 3, column = 1)

        #Nombre para pedir la cuarta variable
        var4Label = Label(InitialDataLinealCeroFrame, bg = "CadetBlue", text = "Pm [dias]")
        var4Label.grid(row = 4, column = 0)
        #Entrada para la cuarta variable
        var4Entry = Entry(InitialDataLinealCeroFrame, textvariable = Pm)
        var4Entry.grid(row = 4, column = 1)

        #Nombre para pedir la quinta variable
        var5Label = Label(InitialDataLinealCeroFrame, bg = "CadetBlue", text = "fase [radianes]")
        var5Label.grid(row = 5, column = 0)
        #Entrada para la quinta variable
        var5Entry = Entry(InitialDataLinealCeroFrame, textvariable = fase)
        var5Entry.grid(row = 5, column = 1)

        #Le añado el botón que trabajará las variables que le hemos pasado,no se si guardarlas en el archivo temporal
        Button(InitialDataLinealCeroFrame, text = "Ajuste", command = LinealCeroBoton).grid(row = 7, column = 0, columnspan = 2)
    else:
        #Limpiamos 
        windowClear()

        #Agremamos configuración inicial de la ventana raíz
        initialConfiguration()

        MessageBox.showwarning("ERROR DE FLUJO", "Introduce primero los datos de entrada (efmérides de referencia y mínimos observados)")

"""   
#Función para hacer el ajuste senoidal con tendencia parabolica y excentricidad = 0
"""
def parabolicoSenoidalCero():
    #Para limpiar los wdigets que haya
    windowClear()

    #Control de Flujo, que primero estén los datos de entrada
    if (os.path.isfile('temporal.txt')):
        #Necesitamos los valores de las efemérides de referencia P, E, se leen de los ficheros
        efemerides = np.loadtxt('temporal_efemerides.txt')
        E = efemerides[0]
        P = efemerides[1]

        #Pedimos al usuario donde va a querer guardar los parámetros del ajuste
        MessageBox.showinfo("Parámetros Ajuste", "Introduce la ruta del fichero donde guardar los parámetros del ajuste")
        ruta_resumen_senoidalParabolico = FileDialog.asksaveasfile(title = "Parámetros del ajuste senoidal-parabólico (e=0)", defaultextension = ".txt")
        #Función interna que realiza el ajuste una vez que se le pasan los valores iniciales, asociada al botón
        def SenoidalCeroBoton():
            #Primero las funciones de los residuos para que trabaje la librería
            #Funcion del modelo
            def ParabolicoSenoCero(p, x):
                return p[0] + p[1] * x + p[2] * (x ** 2) + p[3] * np.sin((2 * math.pi * x )/p[4] + p[5])

            #Funcion con los residuos
            def ResiduosParabolicoSenoCero(p, y, x):
                y_modelo = ParabolicoSenoCero(p, x)
                return y_modelo - y

            #Genero el array con los parámetros inciales
            parametrosIniciales1 = np.array([float(a.get()), float(b.get()), float(c.get()),float(A.get()), float(Pm.get()), float(fase.get())])

            #primero se leen los datos que estarán en el archivo temporal
            dataAjusteParabolicoCero = np.loadtxt('temporal.txt', usecols = [3,4],skiprows = 1)

            #Para la barra de error
            error = np.loadtxt('temporal.txt', usecols = [1], skiprows = 1) #El error está en la columna 1
            #Para cuando haya errores cero
            for i in range (len(error)):
                if (error[i] == 0.0):
                    error[i] = 0.00000000001

            #Array para hacer la representación, 250 valores entre el máximo y el mínimo de la época
            maximo = np.amax(dataAjusteParabolicoCero[:,1])
            minimo = np.amin(dataAjusteParabolicoCero[:,1])
            salto = (maximo - minimo) / 250 #Quiereo 250 tramos
            xRepresentar = np.zeros(250)
            valor = minimo
            for i in range (250):    
                xRepresentar[i] = valor
                valor += salto

            #Ajustamos al modelo
            X1 = dataAjusteParabolicoCero[:,1]
            Y1 = dataAjusteParabolicoCero[:,0]

            parametrosFinales1, pcov1, infodict1, errmsg1, success1 = leastsq(ResiduosParabolicoSenoCero, parametrosIniciales1, args=(Y1, X1), full_output = True)
            
            if (success1 == 0) or (success1 == 1) or (success1 == 2) or (success1 == 3) or (success1 == 4):
                """
                Calculamos los errores para mostrarlos en la información del modelo
                """
                #Primero los parámetros obtenidos con sus errores
                if (len(dataAjusteParabolicoCero[:,0]) > len(parametrosIniciales1)) and pcov1 is not None:
                    s_sq1 = (ResiduosParabolicoSenoCero(parametrosFinales1, dataAjusteParabolicoCero[:,0], dataAjusteParabolicoCero[:,1])**2).sum()/(len(dataAjusteParabolicoCero[:,0])-len(parametrosIniciales1))
                    pcov1 = pcov1 * s_sq1
                else:
                    pcov1 = np.inf

                errorParabolico= [] 
                for i in range(len(parametrosFinales1)):
                    try:
                        errorParabolico.append(np.absolute(pcov1[i][i])**0.5)
                    except:
                        errorParabolico.append( 0.00 )
            
                erroresParametros1 = np.array(errorParabolico) 

                #Método alternativo para el cálculo del error.
                """
                pstd2 = np.sqrt(np.diag(pcov1))
                #Calculamos los errores de cada coeficientes
                erroresParametros1 = np.zeros(len(parametrosFinales1))
                for i in range (len(parametrosFinales1)):
                    erroresParametros1[i] = pstd2[i]/2
                """
                """
                -------------R2---------
                """
                #Son necesarias las predicciones en base al modelo obtenido
                Y_predict1 = np.zeros(len(X1))
                for i in range (len(X1)):
                    Y_predict1[i] = ParabolicoSenoCero(parametrosFinales1, X1[i])

                #Valor medio 
                valuemed1 = np.mean(Y1) 

                num1 = 0.0
                den1 = 0.0
                for i in range (len(Y_predict1)):
                    #num1 += (Y1[i] - valuemed1)**2
                    #den1 += (Y_predict1[i] - valuemed1)**2
                    num1 += (Y_predict1[i] - Y1[i])**2
                    den1 += (Y1[i] - valuemed1)**2


                rsquared3 = 1 - num1/den1
                """
                -----RMSE----
                """
                #RMSE 
                inter1 = 0.0
                for i in range (len(Y_predict1)):
                    inter1 += (Y_predict1[i] - Y1[i])**2

                rmse3 = inter1/len(Y_predict1)
                rmse3 = math.sqrt(rmse3)


                """
                Lo guardamos en el ficheor que nos pasa el usuario
                """
                
                f6 = open(ruta_resumen_senoidalParabolico.name, "w")
                f6.write("--------------------Modelo de ajuste Parabolico Senoidal (e=0)-----------------------\n")
                f6.write("--------------- f = a + b * x + c * x^2 + A * sin((2 * pi * x )/Pm + fase) ----------\n")
                f6.write("\n")
                f6.write(f"Parámetros iniciales: a = {parametrosIniciales1[0]}, b = {parametrosIniciales1[1]}, c = {parametrosIniciales1[2]}\n")
                f6.write(f"                      A = {parametrosIniciales1[3]}, Pm = {parametrosIniciales1[4]}, fase = {parametrosIniciales1[5]}\n")
                f6.write("\n")
                f6.write(f"Modelo: f = {parametrosFinales1[0]} + {parametrosFinales1[1]} * x + {parametrosFinales1[2]} * x^2  + {parametrosFinales1[3]} * sin((2 * pi * x )/{parametrosFinales1[4]} + {parametrosFinales1[5]})\n")
                f6.write(f"Parámetros finales: a = {parametrosFinales1[0]}, b = {parametrosFinales1[1]}, c = {parametrosFinales1[2]}\n")
                f6.write(f"                    A = {parametrosFinales1[3]}, Pm = {parametrosFinales1[4]}, fase = {parametrosFinales1[5]}\n")
                f6.write("\n")
                f6.write(f"Errores de los parámetros: E(a) = {erroresParametros1[0]}, E(b) = {erroresParametros1[1]}, E(c) = {erroresParametros1[2]}\n")
                f6.write(f"                           E(A) = {erroresParametros1[3]}, E(Pm) = {erroresParametros1[4]}, E(fase) = {erroresParametros1[5]}\n") 
                f6.write("\n")
                f6.write(f"R^2: {rsquared3}\n")
                f6.write(f"Error cuadratico medio(rmse): {rmse3}\n")
                f6.close()

                #Generamos la curva obtenida por el modelo
                yAjusteParabolico = np.zeros(len(xRepresentar))
                for i in range (len(xRepresentar)):
                    yAjusteParabolico[i] = ParabolicoSenoCero(parametrosFinales1, xRepresentar[i])
                #Representación en un ventana emergente
                #Primero la ventana
                RaizParabolicoSenoidalCero = tk.Tk()
                RaizParabolicoSenoidalCero.wm_title('Ajuste Parabolico-Senoidal (e=0)')
                figSenoidalCero = plt.figure(figsize = (7, 5), dpi = 100)
                #Se añade el subplot
                plot_figSenoidalCero = figSenoidalCero.add_subplot(111)
                plot_figSenoidalCero.set_xlabel("E")
                plot_figSenoidalCero.set_ylabel("O - C [dias]")
                plot_figSenoidalCero.set_title("Ajuste Senoidal-Parabolico (e=0)")
                DiagramaParabolicoSenoidadCero, = plot_figSenoidalCero.plot(dataAjusteParabolicoCero[:,1], dataAjusteParabolicoCero[:,0], 'o', color = "Blue", label = "Datos")

                #Barra de error
                plot_figSenoidalCero.errorbar(dataAjusteParabolicoCero[:,1], dataAjusteParabolicoCero[:,0], yerr = error, fmt = 'o', color = "Blue")

                DiagramaParabolicoSenoidadCero, = plot_figSenoidalCero.plot(xRepresentar, yAjusteParabolico, linestyle='-', color = 'red', label="Ajuste")
                plot_figSenoidalCero.legend(loc = "best")

                #con Canvas se crea el área de dibujo
                canvasSenoidalCero = FigureCanvasTkAgg(figSenoidalCero, master = RaizParabolicoSenoidalCero)
                canvasSenoidalCero.draw()
                canvasSenoidalCero.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
                #ahora añadimos la barra de herramientas
                toolbarSenoidalCero=NavigationToolbar2Tk(canvasSenoidalCero, RaizParabolicoSenoidalCero)
                toolbarSenoidalCero.update()
                canvasSenoidalCero.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

                InitialDataSenoidalCeroFrame.destroy()
                principalRoot.config(width = 480, height = 320)

                #Para volver a la configuración inicial
                initialConfiguration()
                RaizParabolicoSenoidalCero.mainloop()
            else:
                #Limpiamos 
                windowClear()

                #Agremamos configuración inicial de la ventana raíz
                initialConfiguration()

                MessageBox.showwarning("ERROR PROCESO", "El método de ajuste ha dado error, mensaje de error de la función:\n" + errmsg1)
        #Primero se crea el marco
        InitialDataSenoidalCeroFrame = Frame(principalRoot)  

        #Lo empaquetamos en la raíz del programa
        InitialDataSenoidalCeroFrame.pack()      

        #Configuración del marco
        #Color
        InitialDataSenoidalCeroFrame.config(bg = "CadetBlue")     
        #Tamaño
        InitialDataSenoidalCeroFrame.config(width = 750, height = 750) 
        #Cursor
        InitialDataSenoidalCeroFrame.config(cursor = "star")
        #Tamaño borde
        InitialDataSenoidalCeroFrame.config(bd = 24)
        #Tipo de Borde 
        InitialDataSenoidalCeroFrame.config(relief ="sunken")
    

        #Etiqueta para el título
        tittleLabel = Label(InitialDataSenoidalCeroFrame, text = "Valores ajuste senoidal-parabolico (e = 0)")
        tittleLabel.grid(row = 0, column = 0, columnspan = 2)

        #Variables para trabajar con ella desde las funciones
        a = DoubleVar()
        b = DoubleVar()
        c = DoubleVar()
        A = DoubleVar()
        Pm = DoubleVar()
        fase = DoubleVar()

        #Nombre para pedir la primera variable
        var1Label = Label(InitialDataSenoidalCeroFrame, bg = "CadetBlue", text = "a")
        var1Label.grid(row = 1, column = 0)
        #Entrada para la primera variable
        var1Entry = Entry(InitialDataSenoidalCeroFrame, textvariable = a)
        var1Entry.grid(row = 1, column = 1)

        #Nombre para pedir la segunda variable
        var2Label = Label(InitialDataSenoidalCeroFrame, bg = "CadetBlue", text = "b")
        var2Label.grid(row = 2, column = 0)
        #Entrada para la segunda variable
        var2Entry = Entry(InitialDataSenoidalCeroFrame, textvariable = b)
        var2Entry.grid(row = 2, column = 1)

        #Nombre para pedir la tercera variable
        var3Label = Label(InitialDataSenoidalCeroFrame, bg = "CadetBlue", text = "c")
        var3Label.grid(row = 3, column = 0)
        #Entrada para la tercera variable
        var3Entry = Entry(InitialDataSenoidalCeroFrame, textvariable = c)
        var3Entry.grid(row = 3, column = 1)

        #Nombre para pedir la cuarta variable
        var4Label = Label(InitialDataSenoidalCeroFrame, bg = "CadetBlue", text = "Amplitud [dias]")
        var4Label.grid(row = 4, column = 0)
        #Entrada para la cuarta variable
        var4Entry = Entry(InitialDataSenoidalCeroFrame, textvariable = A)
        var4Entry.grid(row = 4, column = 1)

        #Nombre para pedir la quinta variable
        var5Label = Label(InitialDataSenoidalCeroFrame, bg = "CadetBlue", text = "Pm [dias]")
        var5Label.grid(row = 5, column = 0)
        #Entrada para la quinta variable
        var5Entry = Entry(InitialDataSenoidalCeroFrame, textvariable = Pm)
        var5Entry.grid(row = 5, column = 1)

        #Nombre para pedir la sexta variable
        var6Label = Label(InitialDataSenoidalCeroFrame, bg = "CadetBlue", text = "fase [radianes]")
        var6Label.grid(row = 6, column = 0)
        #Entrada para la sexta variable
        var6Entry = Entry(InitialDataSenoidalCeroFrame, textvariable = fase)
        var6Entry.grid(row = 6, column = 1)

        #Le añado el botón que trabajará las variables que le hemos pasado,no se si guardarlas en el archivo temporal
        Button(InitialDataSenoidalCeroFrame, text = "Ajuste", command = SenoidalCeroBoton).grid(row= 8, column = 0, columnspan = 2)
        
    else:
        #Limpiamos 
        windowClear()

        #Agremamos configuración inicial de la ventana raíz
        initialConfiguration()

        MessageBox.showwarning("ERROR DE FLUJO", "Introduce primero los datos de entrada (efmérides de referencia y mínimos observados)")

"""   
#Función para hacer el ajuste senoidal con tendencia parabolica y excentricidad distinta de cero
"""
def linealSenoidalNoCero():
    #Para limpiar los wdigets que haya
    windowClear()

    #Control de Flujo, que primero estén los datos de entrada
    if (os.path.isfile('temporal.txt')):
        #Necesitamos los valores de las efemérides de referencia P, E, se leen de los ficheros
        efemerides = np.loadtxt('temporal_efemerides.txt')
        E = efemerides[0]
        P = efemerides[1]

        #Pedimos al usuario donde va a querer guardar los parámetros del ajuste
        MessageBox.showinfo("Parámetros Ajuste", "Introduce la ruta del fichero donde guardar los parámetros del ajuste")
        ruta_resumen_senoidalParabolico = FileDialog.asksaveasfile(title = "Parámetros del ajuste senoidal-lineal", defaultextension = ".txt")
        #Función interna que realiza el ajuste una vez que se le pasan los valores iniciales, asociada al botón
        def LinealNoCeroBoton():
            #Primero las funciones de los residuos para que trabaje la librería
            #Con el desarrollo en serie que viene  con los coeficientes del apéndice del libro
            
            #Función del modelo.
            def LinealSenoNoceroRepresentar(p, x):
                teta = (2 * math.pi * ((E + P * x) - p[4]))/p[5]
                S = np.sin(teta)
                C = np.cos(teta)
                a1 = S
                a2 = S * C
                a3 = C**2 * S - 0.5 * S**3
                a4 = C**3 * S - (5/3.) * C * S**3
                a5 = C**4 * S - (11/3.) * C**2 * S**3 + (13/24.) * S**5
                a6 = C**5 * S - (20/3.) * C**3 * S**3 + (47/15.) * S**5
                a7 = C**6 * S - (65/6.) * C**4 * S**3 + (1291/120.) * C**2 * S**5 - (541/720.) * S**7
                a8 = C**7 * S - (49/3.) * C**5 * S**3 + (427/15.) * C**3 * S**5 - (1957/315.) * S**7
                a9 = C**8 * S - (70/3.) * C**6 * S**3 + (1281/20.) * C**4 * S**5 - (36619/1260.) * C**2 * S**7 + (9509/8064.) * S**9
                a10 = C**9 * S - 32 * C**7 * S**3 + (644/5.) * C**5 * S**5 - (6368/63.) * C**3 * S**7 + (5141/405.) * S**9        

                delta = teta + a1 * p[3] + a2 * p[3]**2 + a3 * p[3]**3 + a4 * p[3]**4 + a5 * p[3]**5 + a6 * p[3]**6 + a7 * p[3]**7 + a8 * p[3]**8 + a9 * p[3]**9 + a10 * p[3]**10

                inter = np.tan(delta/2.)
                raiz = np.sqrt((1 + p[3])/(1 - p[3])) * inter
                nu = (np.cos(raiz) / np.sin(raiz)) * 2.
                devolver = p[0] + p[1] * x + p[2] * (((1 - p[3]**2)/(1 + p[3] * np.cos(nu))) * np.sin(nu + p[6]) + p[3] * np.sin(p[6]))

                return devolver

            def ResiduosLinealSenoNoCero (p, y, x):
                y_modelo = LinealSenoNoceroRepresentar(p, x)
                return y_modelo - y

            
            #Genero el array con los parámetros inciales
            parametrosIniciales2 = np.array([float(a.get()), float(b.get()), float(amplitud.get()),float(e.get()), float(T0.get()), float(Pm.get()), float(omega.get())])

            #primero se leen los datos que estarán en el archivo temporal
            dataAjusteLinealNoCero = np.loadtxt('temporal.txt', usecols = [3,4],skiprows = 1)

            #Para la barra de error
            error = np.loadtxt('temporal.txt', usecols = [1], skiprows = 1) #El error está en la columna 1
            #Para cuando haya errores cero
            for i in range (len(error)):
                if (error[i] == 0.0):
                    error[i] = 0.00000001

            #Array para hacer la representación, 100 valores entre el máximo y el mínimo de la época
            maximo = np.amax(dataAjusteLinealNoCero[:,1])
            minimo = np.amin(dataAjusteLinealNoCero[:,1])
            salto = (maximo - minimo) / 100 #Quiereo quinientos tramos para que no me salga tan feo, que se redondee algo mas
            xRepresentar = np.zeros(100)
            valor = minimo
            for i in range (100):    
                xRepresentar[i] = valor
                valor += salto

            #Ajustamos al modelo
            X2 = dataAjusteLinealNoCero[:,1]
            Y2 = dataAjusteLinealNoCero[:,0]

            parametrosFinales2, pcov2, infodict2, errmsg2, success2 = leastsq(ResiduosLinealSenoNoCero, parametrosIniciales2, args=(Y2, X2), full_output = True)

            if (success2 == 0) or (success2 == 1) or (success2 == 2) or (success2 == 3) or (success2 == 4):
                """
                Calculamos los errores para mostrarlos en la información del modelo
                """
                #Primero los parámetros obtenidos con sus errores
                if (len(dataAjusteLinealNoCero[:,0]) > len(parametrosIniciales2)) and pcov2 is not None:
                    s_sq2 = (ResiduosLinealSenoNoCero(parametrosFinales2, dataAjusteLinealNoCero[:,0], dataAjusteLinealNoCero[:,1])**2).sum()/(len(dataAjusteLinealNoCero[:,0])-len(parametrosIniciales2))
                    pcov2 = pcov2 * s_sq2
                else:
                    pcov2 = np.inf

                errorLinealNoCero = [] 
                for i in range(len(parametrosFinales2)):
                    try:
                        errorLinealNoCero.append(np.absolute(pcov2[i][i])**0.5)
                    except:
                        errorLinealNoCero.append( 0.00 )
            
                erroresParametros2 = np.array(errorLinealNoCero)
                
                #Método alternativo para calcular el error
                """
                pstd2 = np.sqrt(np.diag(pcov2))
                #Calculamos los errores de cada coeficientes
                erroresParametros2 = np.zeros(len(parametrosFinales2))
                for i in range (len(parametrosFinales2)):
                    erroresParametros2[i] = pstd2[i]/2
                """
                """
                -------------R2---------
                """
                #Son necesarias las predicciones en base al modelo obtenido
                Y_predict2 = np.zeros(len(X2))
                for i in range (len(X2)):
                    Y_predict2[i] = LinealSenoNoceroRepresentar(parametrosFinales2, X2[i])

                #Valor medio 
                valuemed2= np.mean(Y2) 

                num2 = 0.0
                den2 = 0.0
                for i in range (len(Y_predict2)):
                    #num2 += (Y2[i] - valuemed2)**2
                    #den2 += (Y_predict2[i] - valuemed2)**2
                    num2 += (Y_predict2[i] - Y2[i])**2
                    den2 += (Y2[i] - valuemed2)**2


                rsquared4 = 1 - num2/den2

                
                """
                -----RMSE----
                """
                #RMSE 
                inter2 = 0.0
                for i in range (len(Y_predict2)):
                    inter2 += (Y_predict2[i] - Y2[i])**2

                rmse4 = inter2/len(Y_predict2)
                rmse4 = math.sqrt(rmse4)

                """
                Lo guardamos en el ficheor que nos pasa el usuario
                """
                f7 = open(ruta_resumen_senoidalParabolico.name, "w")
                f7.write("-----------------------------Modelo de ajuste Lineal Senoidal -------------------------------------\n")
                f7.write("-------- f = a + b * x + A * [((1 - e**2)/(1 + e * cos(nu))) * sin(nu + omega) + e * sin(omega)] --\n")
                f7.write("\n")
                f7.write(f"Parámetros iniciales: a = {parametrosIniciales2[0]}, b = {parametrosIniciales2[1]}, A = {parametrosIniciales2[2]}\n")
                f7.write(f"                      e = {parametrosIniciales2[3]}, T0 = {parametrosIniciales2[4]}, Pm = {parametrosIniciales2[5]}\n")
                f7.write(f"                      omega = {parametrosIniciales2[6]}\n")
                f7.write("\n")
                f7.write(f"Parámetros finales: a = {parametrosFinales2[0]}, b = {parametrosFinales2[1]}, A = {parametrosFinales2[2]}\n")
                f7.write(f"                    e = {parametrosFinales2[3]}, T0 = {parametrosFinales2[4]}, Pm = {parametrosFinales2[5]}\n")
                f7.write(f"                    omega = {parametrosFinales2[6]}\n")
                f7.write("\n")
                f7.write(f"Errores de los parámetros: E(a) = {erroresParametros2[0]}, E(b) = {erroresParametros2[1]}, E(A) = {erroresParametros2[2]}\n")
                f7.write(f"                           E(e) = {erroresParametros2[3]}, E(T0) = {erroresParametros2[4]}, E(Pm) = {erroresParametros2[5]}\n") 
                f7.write(f"                           E(Omega) = {erroresParametros2[6]}\n")
                f7.write("\n")
                f7.write(f"R^2: {rsquared4}\n")
                f7.write(f"Error cuadratico medio(rmse): {rmse4}\n")
                f7.close()

                #Generamos la curva obtenida por el modelo
                yAjustelinealNocero = np.zeros(len(xRepresentar))
                for i in range (len(xRepresentar)):
                    yAjustelinealNocero[i] = LinealSenoNoceroRepresentar(parametrosFinales2, xRepresentar[i])

                #Representamos mostrand en una ventana emergente.
                #Primero la ventana
                RaizLinealSenoidalNoCero = tk.Tk()
                RaizLinealSenoidalNoCero.wm_title('Ajuste Lineal-Senoidal')
                figLinealNoCero = plt.figure(figsize = (7, 5), dpi = 100)
                #Se añade el subplot
                plot_figLinealNoCero= figLinealNoCero.add_subplot(111)
                plot_figLinealNoCero.set_xlabel("E")
                plot_figLinealNoCero.set_ylabel("O - C [dias]")
                plot_figLinealNoCero.set_title("Ajuste Lineal-Senoidal")
                DiagramaLinealSenoidalNoCero, = plot_figLinealNoCero.plot(dataAjusteLinealNoCero[:,1], dataAjusteLinealNoCero[:,0], 'o', label = "Datos")


                #Barra de error
                plot_figLinealNoCero.errorbar(dataAjusteLinealNoCero[:,1], dataAjusteLinealNoCero[:,0], yerr = error, fmt = 'o', color = "Blue")

                DiagramaLinealSenoidalCero, = plot_figLinealNoCero.plot(xRepresentar, yAjustelinealNocero, linestyle='-', color = 'red', label="Ajuste")
                plot_figLinealNoCero.legend(loc = "best")

                #Con Canvas se crea el área de dibujo
                canvasLinealNoCero = FigureCanvasTkAgg(figLinealNoCero, master = RaizLinealSenoidalNoCero)
                canvasLinealNoCero.draw()
                canvasLinealNoCero.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
                #Ahora añadimos la barra de herramientas
                toolbarLinealNoCero=NavigationToolbar2Tk(canvasLinealNoCero, RaizLinealSenoidalNoCero)
                toolbarLinealNoCero.update()
                canvasLinealNoCero.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

                InitialDataLinealNoCeroFrame.destroy()
                principalRoot.config(width = 480, height = 320)

                #Para volver a la configuración inicial
                initialConfiguration()

                RaizLinealSenoidalNoCero.mainloop()
            else:
                #Limpiamos 
                windowClear()

                #Agremamos configuración inicial de la ventana raíz
                initialConfiguration()

                MessageBox.showwarning("ERROR PROCESO", "El método de ajuste ha dado error, mensaje de error de la función:\n" + errmsg2)

        #Primero se crea el marco
        InitialDataLinealNoCeroFrame = Frame(principalRoot)  

        #Lo empaquetamos en la raíz del programa
        InitialDataLinealNoCeroFrame.pack()      

        #Configuración del marco
        #Color
        InitialDataLinealNoCeroFrame.config(bg = "CadetBlue")     
        #Tamaño
        InitialDataLinealNoCeroFrame.config(width = 750, height = 750) 
        #Cursor
        InitialDataLinealNoCeroFrame.config(cursor = "star")
        #Tamaño borde
        InitialDataLinealNoCeroFrame.config(bd = 24)
        #Tipo de Borde 
        InitialDataLinealNoCeroFrame.config(relief ="sunken")
    

        #Etiqueta para el título
        tittleLabel = Label(InitialDataLinealNoCeroFrame, text = "Valores ajuste senoidal-lineal")
        tittleLabel.grid(row = 0, column = 0, columnspan = 2)

        #Variables para trabajar con ella desde las funciones
        a = DoubleVar()
        b = DoubleVar()
        amplitud = DoubleVar()
        e = DoubleVar()
        T0 = DoubleVar()
        Pm = DoubleVar()
        omega = DoubleVar()

        #Nombre para pedir la primera variable
        var1Label = Label(InitialDataLinealNoCeroFrame, bg = "CadetBlue", text = "a: ")
        var1Label.grid(row = 1, column = 0)
        #Entrada para la primera variable
        var1Entry = Entry(InitialDataLinealNoCeroFrame, textvariable = a)
        var1Entry.grid(row = 1, column = 1)

        #Nombre para pedir la segunda variable
        var2Label = Label(InitialDataLinealNoCeroFrame, bg = "CadetBlue", text = "b: ")
        var2Label.grid(row = 2, column = 0)
        #Entrada para la segunda variable
        var2Entry = Entry(InitialDataLinealNoCeroFrame, textvariable = b)
        var2Entry.grid(row = 2, column = 1)

        #Nombre para pedir la tercera variable
        var3Label = Label(InitialDataLinealNoCeroFrame, bg = "CadetBlue", text = "Amplitud(A): ")
        var3Label.grid(row = 3, column = 0)
        #Entrada para la tercera variable
        var3Entry = Entry(InitialDataLinealNoCeroFrame, textvariable = amplitud)
        var3Entry.grid(row = 3, column = 1)

        #Nombre para pedir la cuarta variable
        var4Label = Label(InitialDataLinealNoCeroFrame, bg = "CadetBlue", text = "Excentricidad (e): ")
        var4Label.grid(row = 4, column = 0)
        #Entrada para la cuarta variable
        var4Entry = Entry(InitialDataLinealNoCeroFrame, textvariable = e)
        var4Entry.grid(row = 4, column = 1)

        #Nombre para pedir la sexta variable
        var5Label = Label(InitialDataLinealNoCeroFrame, bg = "CadetBlue", text = "T0: ")
        var5Label.grid(row = 6, column = 0)
        #Entrada para la sexta variable
        var5Entry = Entry(InitialDataLinealNoCeroFrame, textvariable = T0)
        var5Entry.grid(row = 6, column = 1)
        
        #Nombre para pedir la quinta variable
        var6Label = Label(InitialDataLinealNoCeroFrame, bg = "CadetBlue", text = "Pm: ")
        var6Label.grid(row = 5, column = 0)
        #Entrada para la quinta variable
        var6Entry = Entry(InitialDataLinealNoCeroFrame, textvariable = Pm)
        var6Entry.grid(row = 5, column = 1)

        #Nombre para pedir la septima variable
        var7Label = Label(InitialDataLinealNoCeroFrame, bg = "CadetBlue", text = "omega(w): ")
        var7Label.grid(row = 7, column = 0)
        #Entrada para la sptima variable
        var7Entry = Entry(InitialDataLinealNoCeroFrame, textvariable = omega)
        var7Entry.grid(row = 7, column = 1)

        #Le añado el botón que trabajará las variables que le hemos pasado,no se si guardarlas en el archivo temporal
        Button(InitialDataLinealNoCeroFrame, text = "Ajuste", command = LinealNoCeroBoton).grid(row = 8, column = 0, columnspan = 2)
        
    else: 
        #Limpiamos 
        windowClear()

        #Agremamos configuración inicial de la ventana raíz
        initialConfiguration()

        MessageBox.showwarning("ERROR DE FLUJO", "Introduce primero los datos de entrada (efmérides de referencia y mínimos observados)")

"""   
#Función para hacer el ajuste senoidal con tendencia parabolica y excentricidad distinta de cero
"""
def parabolicoSenoidalNoCero():
    #Para limpiar los wdigets que haya
    windowClear()

    #Control de Flujo, que primero estén los datos de entrada
    if (os.path.isfile('temporal.txt')):
        #Voy a necesitar los valores de las efemérides de referencia P, E, se leen de los ficheros
        efemerides = np.loadtxt('temporal_efemerides.txt')
        E = efemerides[0]
        P = efemerides[1]

        #Pedimos al usuario donde va a querer guardar los parámetros del ajuste
        MessageBox.showinfo("Parámetros Ajuste", "Introduce la ruta del fichero donde guardar los parámetros del ajuste")
        ruta_resumen_senoidalParabolico = FileDialog.asksaveasfile(title = "Parámetros del ajuste senoidal-lineal", defaultextension = ".txt")
        #Función interna que realiza el ajuste una vez que se le pasan los valores iniciales, asociada al botón
        def ParabolicoNoCeroBoton():
            #Primero las funciones de los residuos para que trabaje la librería        
            #Con el desarrollo en serie que viene  con los coeficientes del apéndice del libro
            
            #Función del modelo.
            def ParabolicoSenoNocero(p, x):
                teta = (2 * math.pi * ((E + P * x) - p[5]))/p[6]
                S = np.sin(teta)
                C = np.cos(teta)
                a1 = S
                a2 = S * C
                a3 = C**2 * S - 0.5 * S**3
                a4 = C**3 * S - (5/3.) * C * S**3
                a5 = C**4 * S - (11/3.) * C**2 * S**3 + (13/24.) * S**5
                a6 = C**5 * S - (20/3.) * C**3 * S**3 + (47/15.) * S**5
                a7 = C**6 * S - (65/6.) * C**4 * S**3 + (1291/120.) * C**2 * S**5 - (541/720.) * S**7
                a8 = C**7 * S - (49/3.) * C**5 * S**3 + (427/15.) * C**3 * S**5 - (1957/315.) * S**7
                a9 = C**8 * S - (70/3.) * C**6 * S**3 + (1281/20.) * C**4 * S**5 - (36619/1260.) * C**2 * S**7 + (9509/8064.) * S**9
                a10 = C**9 * S - 32 * C**7 * S**3 + (644/5.) * C**5 * S**5 - (6368/63.) * C**3 * S**7 + (5141/405.) * S**9        

                delta = teta + a1 * p[4] + a2 * p[4]**2 + a3 * p[4]**3 + a4 * p[4]**4 + a5 * p[4]**5 + a6 * p[4]**6 + a7 * p[4]**7 + a8 * p[4]**8 + a9 * p[4]**9 + a10 * p[4]**10

                inter = np.tan(delta/2.)
                raiz = np.sqrt((1 + p[4])/(1 - p[4])) * inter
                nu = (np.cos(raiz) / np.sin(raiz)) * 2.
                devolver = p[0] + p[1] * x + p[2] * (x**2) + p[3] * (((1 - p[4]**2)/(1 + p[4] * np.cos(nu))) * np.sin(nu + p[7]) + p[4] * np.sin(p[7]))

                return devolver

            def ResiduosParabolicoSenoNoCero (p, y, x):
                y_modelo = ParabolicoSenoNocero(p, x)
                return y_modelo - y

            #Genero el array con los parámetros inciales
            parametrosIniciales3 = np.array([float(a.get()), float(b.get()), float(c.get()), float(amplitud.get()),float(e.get()), float(T0.get()), float(Pm.get()), float(omega.get())])

            #primero se leen los datos que estarán en el archivo temporal
            dataAjusteParabolicoNoCero = np.loadtxt('temporal.txt', usecols = [3,4],skiprows = 1)

            #Para la barra de error
            error = np.loadtxt('temporal.txt', usecols = [1], skiprows = 1) #El error está en la columna 1
            #Para cuando haya errores cero
            for i in range (len(error)):
                if (error[i] == 0.0):
                    error[i] = 0.00000000001

            #Array para hacer la representación, 100 valores entre el máximo y el mínimo de la época
            maximo = np.amax(dataAjusteParabolicoNoCero[:,1])
            minimo = np.amin(dataAjusteParabolicoNoCero[:,1])
            salto = (maximo - minimo) / 100 #Quiereo 100 tramos para que salga más suave al representar
            xRepresentar = np.zeros(100)
            valor = minimo
            for i in range (100):    
                xRepresentar[i] = valor
                valor += salto

            #Ajustamos al modelo
            X3 = dataAjusteParabolicoNoCero[:,1]
            Y3 = dataAjusteParabolicoNoCero[:,0]
            parametrosFinales3, pcov3, infodict3, errmsg3, success3 = leastsq(ResiduosParabolicoSenoNoCero, parametrosIniciales3, args=(Y3, X3), full_output = True)


            if (success3 == 0) or (success3 == 1) or (success3 == 2) or (success3 == 3) or (success3 == 4):
                """
                Calculamos los errores para mostrarlos en la información del modelo
                """

                #Primero los parámetros obtenidos con sus errores
                if (len(dataAjusteParabolicoNoCero[:,0]) > len(parametrosFinales3)) and pcov3 is not None:
                    s_sq3 = (ResiduosParabolicoSenoNoCero(parametrosFinales3, dataAjusteParabolicoNoCero[:,0], dataAjusteParabolicoNoCero[:,1])**2).sum()/(len(dataAjusteParabolicoNoCero[:,0])-len(parametrosFinales3))
                    pcov3 = pcov3 * s_sq3
                else:
                    pcov2 = np.inf

                errorParabolicoNoCero = [] 
                for i in range(len(parametrosFinales3)):
                    try:
                        errorParabolicoNoCero.append(np.absolute(pcov3[i][i])**0.5)
                    except:
                        errorParabolicoNoCero.append( 0.00 )
            
                erroresParametros3 = np.array(errorParabolicoNoCero)
                
                #Método alternativo para calcular el error
                """
                pstd3 = np.sqrt(np.diag(pcov3))
                #Calculamos los errores de cada coeficientes
                erroresParametros3 = np.zeros(len(parametrosFinales3))
                for i in range (len(parametrosFinales3)):
                    erroresParametros3[i] = pstd3[i]/2
                """
                """
                -------------R2---------
                """
                #Son necesarias las predicciones en base al modelo obtenido
                Y_predict3 = np.zeros(len(X3))
                for i in range (len(X3)):
                    Y_predict3[i] = ParabolicoSenoNocero(parametrosFinales3, X3[i])

                #Valor medio 
                valuemed3= np.mean(Y3) 

                num3 = 0.0
                den3 = 0.0
                for i in range (len(Y_predict3)):
                    #num3 += (Y3[i] - valuemed3)**2
                    #den3 += (Y_predict3[i] - valuemed3)**2
                    num3 += (Y_predict3[i] - Y3[i])**2
                    den3 += (Y3[i] - valuemed3)**2


                rsquared5 = num3/den3
                """
                -----RMSE----
                """
                #RMSE 
                inter3 = 0.0
                for i in range (len(Y_predict3)):
                    inter3 += (Y_predict3[i] - Y3[i])**2

                rmse5 = inter3/len(Y_predict3)
                rmse5 = math.sqrt(rmse5)

                """
                Lo guardamos en el ficheor que nos pasa el usuario
                """
                f8 = open(ruta_resumen_senoidalParabolico.name, "w")
                f8.write("------------------------Modelo de ajuste Parabolico Senoidal -----------------------------------------\n")
                f8.write("- f = a + b * c + c * x**2 + A * [((1 - e**2)/(1 + e * cos(nu))) * sin(nu + omega) + e * sin(omega)] -\n")
                f8.write("\n")
                f8.write(f"Parámetros iniciales: a = {parametrosIniciales3[0]}, b = {parametrosIniciales3[1]}, c = {parametrosIniciales3[2]}\n")
                f8.write(f"                      A = {parametrosIniciales3[3]}, e = {parametrosIniciales3[4]}, T0 = {parametrosIniciales3[5]}\n")
                f8.write(f"                      Pm = {parametrosIniciales3[6]}, omega = {parametrosIniciales3[7]}\n")
                f8.write("\n")
                f8.write(f"Parámetros finales: a = {parametrosFinales3[0]}, b = {parametrosFinales3[1]}, c = {parametrosFinales3[2]}\n")
                f8.write(f"                    A = {parametrosFinales3[3]}, e = {parametrosFinales3[4]}, T0 = {parametrosFinales3[5]}\n")
                f8.write(f"                    Pm = {parametrosFinales3[6]}, omega = {parametrosFinales3[7]}\n")
                f8.write("\n")
                f8.write(f"Errores de los parámetros: E(a) = {erroresParametros3[0]}, E(b) = {erroresParametros3[1]}, E(c) = {erroresParametros3[2]}\n")
                f8.write(f"                           E(A) = {erroresParametros3[3]}, E(e) = {erroresParametros3[4]}, E(T0) = {erroresParametros3[5]}\n") 
                f8.write(f"                           E(Pm) = {erroresParametros3[6]}, E(omega) = {erroresParametros3[7]}\n")
                f8.write("\n")
                f8.write(f"R^2: {rsquared5}\n")
                f8.write(f"Error cuadratico medio(rmse): {rmse5}\n")
                f8.close()

                #Generamos la curva obtenida por el modelo
                yAjusteParabolicoNocero = np.zeros(len(xRepresentar))
                for i in range (len(xRepresentar)):
                    yAjusteParabolicoNocero[i] = ParabolicoSenoNocero(parametrosFinales3, xRepresentar[i])

                #Representamos en una ventana emergente
                #Primero ventana
                RaizParabolicoSenoidalNoCero = tk.Tk()
                RaizParabolicoSenoidalNoCero.wm_title('Ajuste Parabolico-Senoidal')
                figParabolicoNoCero = plt.figure(figsize = (7, 5), dpi = 100)
                #Se añade el subplot
                plot_figParabolicoNoCero = figParabolicoNoCero.add_subplot(111)
                plot_figParabolicoNoCero.set_xlabel("E")
                plot_figParabolicoNoCero.set_ylabel("O - C [dias]")
                plot_figParabolicoNoCero.set_title("Ajuste Parabolico-Senoidal")
                DiagramaParabolicoSenoidalNoCero, = plot_figParabolicoNoCero.plot(dataAjusteParabolicoNoCero[:,1], dataAjusteParabolicoNoCero[:,0], 'o', label = "Datos")


                #Barra de error
                plot_figParabolicoNoCero.errorbar(dataAjusteParabolicoNoCero[:,1], dataAjusteParabolicoNoCero[:,0], yerr = error, fmt = 'o', color = "Blue")

                DiagramaParabolicoSenoidalCero, = plot_figParabolicoNoCero.plot(xRepresentar, yAjusteParabolicoNocero, linestyle='-', color = 'red', label="Ajuste")
                plot_figParabolicoNoCero.legend(loc = "best")

                #con Canvas se crea el área de dibujo
                canvasParabolicoNoCero = FigureCanvasTkAgg(figParabolicoNoCero, master = RaizParabolicoSenoidalNoCero)
                canvasParabolicoNoCero.draw()
                canvasParabolicoNoCero.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)
                #ahora añadimos la barra de herramientas
                toolbarParabolicoNoCero=NavigationToolbar2Tk(canvasParabolicoNoCero, RaizParabolicoSenoidalNoCero)
                toolbarParabolicoNoCero.update()
                canvasParabolicoNoCero.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = 1)

                InitialDataParabolicoNoCeroFrame.destroy()
                principalRoot.config(width = 480, height = 320)

                #Para volver a la configuración inicial
                initialConfiguration()

                RaizParabolicoSenoidalNoCero.mainloop()
            else:
                #Limpiamos 
                windowClear()

                #Agremamos configuración inicial de la ventana raíz
                initialConfiguration()

                MessageBox.showwarning("ERROR PROCESO", "El método de ajuste ha dado error, mensaje de error de la función:\n" + errmsg3)
        #Primero se crea el marco
        InitialDataParabolicoNoCeroFrame = Frame(principalRoot)  

        #Lo empaquetamos en la raíz del programa
        InitialDataParabolicoNoCeroFrame.pack()      

        #Configuración del marco
        #Color
        InitialDataParabolicoNoCeroFrame.config(bg = "CadetBlue")     
        #Tamaño
        InitialDataParabolicoNoCeroFrame.config(width = 750, height = 750) 
        #Cursor
        InitialDataParabolicoNoCeroFrame.config(cursor = "star")
        #Tamaño borde
        InitialDataParabolicoNoCeroFrame.config(bd = 24)
        #Tipo de Borde 
        InitialDataParabolicoNoCeroFrame.config(relief ="sunken")


        #Etiqueta para el título
        tittleLabel = Label(InitialDataParabolicoNoCeroFrame, text = "Valores ajuste senoidal-lineal")
        tittleLabel.grid(row = 0, column = 0, columnspan = 2)

        #Variables para trabajar con ella desde las funciones
        a = DoubleVar()
        b = DoubleVar()
        c = DoubleVar()
        amplitud = DoubleVar()
        e = DoubleVar()
        T0 = DoubleVar()
        Pm = DoubleVar()
        omega = DoubleVar()

        #Nombre para pedir la primera variable
        var1Label = Label(InitialDataParabolicoNoCeroFrame, bg = "CadetBlue", text = "a: ")
        var1Label.grid(row = 1, column = 0)
        #Entrada para la primera variable
        var1Entry = Entry(InitialDataParabolicoNoCeroFrame, textvariable = a)
        var1Entry.grid(row = 1, column = 1)

        #Nombre para pedir la segunda variable
        var2Label = Label(InitialDataParabolicoNoCeroFrame, bg = "CadetBlue", text = "b: ")
        var2Label.grid(row = 2, column = 0)
        #Entrada para la segunda variable
        var2Entry = Entry(InitialDataParabolicoNoCeroFrame, textvariable = b)
        var2Entry.grid(row = 2, column = 1)

        #Nombre para pedir la tercera variable
        var3Label = Label(InitialDataParabolicoNoCeroFrame, bg = "CadetBlue", text = "c: ")
        var3Label.grid(row = 3, column = 0)
        #Entrada para la tercera variable
        var3Entry = Entry(InitialDataParabolicoNoCeroFrame, textvariable = c)
        var3Entry.grid(row = 3, column = 1)

        #Nombre para pedir la cuarta variable
        var4Label = Label(InitialDataParabolicoNoCeroFrame, bg = "CadetBlue", text = "Amplitud(A): ")
        var4Label.grid(row = 4, column = 0)
        #Entrada para la cuarta variable
        var4Entry = Entry(InitialDataParabolicoNoCeroFrame, textvariable = amplitud)
        var4Entry.grid(row = 4, column = 1)

        #Nombre para pedir la quinta variable
        var5Label = Label(InitialDataParabolicoNoCeroFrame, bg = "CadetBlue", text = "Excentricidad (e): ")
        var5Label.grid(row = 5, column = 0)
        #Entrada para la quinta variable
        var5Entry = Entry(InitialDataParabolicoNoCeroFrame, textvariable = e)
        var5Entry.grid(row = 5, column = 1)

        #Nombre para pedir la septima variable
        var6Label = Label(InitialDataParabolicoNoCeroFrame, bg = "CadetBlue", text = "T0: ")
        var6Label.grid(row = 7, column = 0)
        #Entrada para la septima variable
        var6Entry = Entry(InitialDataParabolicoNoCeroFrame, textvariable = T0)
        var6Entry.grid(row = 7, column = 1)

        #Nombre para pedir la sexta variable
        var7Label = Label(InitialDataParabolicoNoCeroFrame, bg = "CadetBlue", text = "Pm: ")
        var7Label.grid(row = 6, column = 0)
        #Entrada para la sexta variable
        var7Entry = Entry(InitialDataParabolicoNoCeroFrame, textvariable = Pm)
        var7Entry.grid(row = 6, column = 1)

        #Nombre para pedir la octava variable
        var8Label = Label(InitialDataParabolicoNoCeroFrame, bg = "CadetBlue", text = "omega(w): ")
        var8Label.grid(row = 8, column = 0)
        #Entrada para la octava variable
        var8Entry = Entry(InitialDataParabolicoNoCeroFrame, textvariable = omega)
        var8Entry.grid(row = 8, column = 1)

        #Le añado el botón que trabajará las variables que le hemos pasado,no se si guardarlas en el archivo temporal
        Button(InitialDataParabolicoNoCeroFrame, text = "Ajuste", command = ParabolicoNoCeroBoton).grid(row = 9, column = 0, columnspan = 2)

    else:
        #Limpiamos 
        windowClear()

        #Agremamos configuración inicial de la ventana raíz
        initialConfiguration()

        MessageBox.showwarning("ERROR DE FLUJO", "Introduce primero los datos de entrada (efmérides de referencia y mínimos observados)")


"""
-----------------Funciones para la ayuda------------------------------------------------------
"""
"""
#Función con el texto para la ayuda del usuario
"""
def flujo():
    #Para limpiar los wdigets que haya
    windowClear()

    #Crearemos un marco en el que escribiremos la ayuda al usuario
    flujoFrame = Frame(principalRoot)
    flujoFrame.pack()

    #Configuración del marco
    #Color
    flujoFrame.config(bg = "Grey")     
    #Tamaño
    flujoFrame.config(width = 750, height = 750) 
    #Cursor
    flujoFrame.config(cursor = "star")
    #Tamaño borde
    flujoFrame.config(bd = 24)
    #Tipo de Borde 
    flujoFrame.config(relief ="sunken")

    #Variables con el texto
    global texto
    #De esta manera, con el paréntesis se puede escribir un comando en varias líneas, en este caso el texto
    texto = (" Para el correcto funcionamiento de la aplicación algunas pestañas han de haberse utilizado antes de poder utilizar el resto," 
    "\n estas son las correspondientes a la lectura de los datos externos."
    "\n Orden de flujo:"
    "\n"
    "\n 1. Cuando nos encontremos en la pantalla inicial al abrir la aplicación lo primero es proporcionar la efemérides de referencia"
    "\n (Datos de entrada -> Efemérides de referencia)."
    "\n 2. Una vez proporcionada estas, se le ha de proporcionar el fichero de entrada con los datos de mínimos de brillo"
    "\n (Datos de entrada -> Fichero entrada)."
    "\n 3. Una vez que se han hecho estos dos pasos, se puede hacer uso de cualquiera de las pestañas, y sus suspetañas."
    "\n"
    "\n NOTA 1: La pestaña de Ayuda está excluida de estas condiciones, puede utilizarse en cualquier momento."
    "\n NOTA 2: En caso de que no se siga este orden, la aplicación devolverá un mensaje de error."
    "\n NOTA 3: La pestaña de inicio también está excluida de este orden, el caso de la subpestaña RESET altera el flujo," 
    "\n ya que elimina los datos de entrada proporcionados, si haces uso de ella, tendrás que volver al punto 1 del flujo")
    #Etiqueta que contendrá todo el texto
    #El justify que todas las líneas de texto aparezcan alineadas a la izquierda.
    textoLabel = Label(flujoFrame, bg = "Grey", justify = LEFT, 
                        text = texto)
    textoLabel.pack()

"""
#Función para explicar ue hace cada una de las pestañas
"""
def explicacion():
    #Para limpiar los wdigets que haya
    windowClear()

    #Crearemos un marco en el que escribiremos la ayuda al usuario
    explicationFrame = Frame(principalRoot)
    explicationFrame.pack()

    #Configuración del marco
    #Color
    explicationFrame.config(bg = "Grey")     
    #Tamaño
    explicationFrame.config(width = 750, height = 750) 
    #Cursor
    explicationFrame.config(cursor = "star")
    #Tamaño borde
    explicationFrame.config(bd = 24)
    #Tipo de Borde 
    explicationFrame.config(relief ="sunken")

    #Variables con el texto
    global texto1
    #De esta manera, con el paréntesis se puede escribir un comando en varias líneas, en este caso el texto
    texto1 = (" A continuación se da una breve explicación, a modo de ayuda para el usuario," 
    "\n para cada una de las pestañas que podemos ver en la aplicación:"
    "\n 1. Inicio."
    "\n 1.a RESET: Para resetear la aplicación, eliminando todos los datos de entrada que se le hayan proporcionado previamente."
    "\n 1.b Salir: Para cerrar la apliación."
    "\n"
    "\n 2. Datos de entrada."
    "\n 2.a Efemérides de referencia: Aparecerá una ventana en la que introducir los valores de la efemérides de referencia,"
    "\n con un botón para que la aplicación los lea y almacene."
    "\n 2.b Fichero entrada: Ventana para navegar por el equipo y proporcionar al programa el fichero con los datos de mínimos de entrada."
    "\n"
    "\n 3. Datos de salida."
    "\n 3.a Datos de salida: Ventana para solicitar al usuario la ruta en la que guardar el fichero con los datos O-C," 
    "\n los observados, calculados y el error de los mismos."
    "\n"
    "\n 4. Diagramas O-C."
    "\n 4.a Representación: Representación gráfica de los O-C calculados a partir de los valores de entrada proporcionados."
    "\n"
    "\n 5. Modelos de Ajustes."
    "\n 5.a Lineal: Has de proporcionarle dos rutas en las que guardar información del modelo, tras esto hace la representación gráfica" 
    "\n del modelo lineal a los datos."
    "\n 5.b Parabólico: Has de proporcionarle dos rutas en las que guardar información del modelo, tras esto hace la representación gráfica"
    "\n del modelo parabólico a los datos."
    "\n 5.c Lineal-senoidal (e = 0): Has de proporcionarle la ruta en la que guardar la información del modelo, después," 
    "\n mediante una ventana te pide los datos iniciales de los coeficientes, con un botón, la aplicación los lee y almacena," 
    "\n tras esto hace la representación gráfica del modelo a los datos."
    "\n 5.d Lineal-senoidal: Has de proporcionarle la ruta en la que guardar la información del modelo, después," 
    "\n mediante una ventana te pide los datos iniciales de los coeficientes, con un botón, la aplicación los lee y almacena," 
    "\n tras esto hace la representación gráfica del modelo a los datos."
    "\n 5.e Parabólico-senoidal (e = 0): Has de proporcionarle la ruta en la que guardar la información del modelo, después," 
    "\n mediante una ventana te pide los datos iniciales de los coeficientes, con un botón, la aplicación los lee y almacena, "
    "\n tras esto hace la representación gráfica del modelo a los datos,"
    "\n 5.f Parabólico-senoidal: Has de proporcionarle la ruta en la que guardar la información del modelo, después," 
    "\n mediante una ventana te pide los datos iniciales de los coeficientes, con un botón, la aplicación los lee y almacena," 
    "\n tras esto hace la representación gráfica del modelo a los datos.")

    #Etiqueta que contendrá todo el texto
    #El justify que todas las líneas de texto aparezcan alineadas a la izquierda.
    textoLabel = Label(explicationFrame, bg = "Grey", justify = LEFT, 
                        text = texto1)
    textoLabel.pack()

"""
--------------------------------------------------------------------------------------------------------------------------
--------------------------------------------CUERPO DE LA APLICACIÓN-------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------
"""
#Creamos lo que será la raíz del programa
principalRoot = tk.Tk()
#Le ponemos un título
principalRoot.title("Mínimos O-C")

#Configuramos la raiz
principalRoot.config(bg = "grey")          # Color de fondo, background
principalRoot.config(cursor = "star")      # Tipo de cursor
principalRoot.config(relief = "sunken")    # Relieve de la ventana
principalRoot.config(bd = 24)              # Tamaño del borde en píxeles
principalRoot.config(width = 480, height = 320)     #Tamañoamaño de la raíz

#Ahora vamos a añadir la barra de menú
barramenus = tk.Menu(principalRoot) #aquí le decimos que que lo haga en el marco principal
principalRoot.config(menu = barramenus) 

#Creamos los submenuses y las diferentes pestañas que contendrá cada uno de ellos
filemenu = tk.Menu(barramenus, tearoff = 0) #Con tearoff = 0 se le quita el elemento que sale por defecto

#PESTAÑAS

#Añado una pestaña de reseteo que lo que hace es eliminar los ficheros temporales que se crean
filemenu.add_command(label = "RESET", command = reseteo)
filemenu.add_separator()
filemenu.add_command(label = "Salir", command = cerrar)

#este sería el menú para leer el archico con los datos
entradamenu = tk.Menu(barramenus, tearoff = 0)
entradamenu.add_command(label = "Efemérides de referencia", command = efemerides)
entradamenu.add_command(label = "Fichero entrada", command = ruta)

#Aquí el menú que da el archivo de salida
salidamenu = tk.Menu(barramenus, tearoff = 0)
salidamenu.add_command(label = "Datos de salida", command = salida)

#Aquí el que representaría los diagramas O-C:
OCmenu = tk.Menu(barramenus, tearoff = 0)
OCmenu.add_command(label = "Representación", command = diagrama)

#Aquí el que realiza los ajustes
ajustemenu = tk.Menu(barramenus, tearoff = 0)
ajustemenu.add_command(label = "Lineal", command = lineal)
ajustemenu.add_command(label = "Parabólico", command = parabolico)
#Añado las pestañas de los ajustes no lineales, los de e = 0 y los de e != 0
ajustemenu.add_command(label = "Lineal-senoidal (e = 0)", command = linealSenoidalCero)
ajustemenu.add_command(label = "Lineal-senoidal", command = linealSenoidalNoCero)
ajustemenu.add_command(label = "Parabólico-senoidal (e = 0)", command = parabolicoSenoidalCero)
ajustemenu.add_command(label = "Parabólico-senoidal", command = parabolicoSenoidalNoCero)

#Finalmente el menú de ayuda
helpmenu = tk.Menu(barramenus, tearoff = 0)
helpmenu.add_command(label = "Flujo Aplicacion", command = flujo)
helpmenu.add_separator()
helpmenu.add_command(label = "Acerca de...", command = explicacion)

barramenus.add_cascade(label = "Inicio", menu = filemenu)
barramenus.add_cascade(label = "Datos de entrada", menu = entradamenu)
barramenus.add_cascade(label = "Datos de salida", menu = salidamenu)
barramenus.add_cascade(label = "Diagramas O-C", menu = OCmenu)
barramenus.add_cascade(label = "Modelos de Ajustes", menu = ajustemenu)
barramenus.add_cascade(label = "Ayuda", menu = helpmenu)

initialConfiguration()

principalRoot.mainloop()
