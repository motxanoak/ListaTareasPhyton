import arrow #Arrow es una librería para manejar fechas.
import operator #La uso para ordenar listas de objetos.
import json #Uso Json en vez de bases de datos sql.
#Creamos la clase de objetos que operamos en nuestra lista, por ejemplo las tareas
#lo mínimo sería usar titulo, descripcion y el estado (realizado o no)
#Yo quise agregar fecha y un tiempo limite porque ya lo estaba usando (con arrow) en otro proyecto que iba a entregar como final
#hasta que vi que el documento que explicaba lo que pedía el curso.
#Aquí el enlace para que puedan usarlo https://arrow.readthedocs.io/en/latest/
#Importo operador porque quiero que la lista se ordene acorde al deadline de la tarea

## También modifiqué algo de la configuración en settings para usar templates y estilos 'static'
class Tarea:
#La clase tarea tiene estos atributos.
    def __init__(self, title, note ,date ,status):
        self.title = title
        self.note = note
        self._date = date
        self.status = status
    def set_title(self, title):
        self.title=title
    def get_title(self):
        return self.title
    def set_note(self,note):
        self.note=note
    def get_note(self):
        return self.note
    def set_status(self,status):
        self.status=status
    def get_status(self):
        return self.status
    def get_date(self):
        return self._date
    def get_deadline(self):
        userTime = arrow.now()
        future = arrow.get(self._date)
        return future.humanize(userTime)
    
#Al crear la lista como una clase es más fácil manipular la información en ella
#Tiene 4 atributos:
#Lista de tareas
#Diccionario para renderizar en Django
#Filename va a ser un atributo desde la creación del objeto para ordenar el archivo con el que se guarda la info. 
#Al crearse me di cuenta que, para evitar un error, lo mejor era cargar la información del archivo y que está ya estuviera lista 
#para ser usada desde la lista[]
class ListaTareas:
    def __init__(self, filename):
        self.tareas = []
        self.dic = {}
        self.filename = filename
        self.cargar()       
        
#Cargar toma un diccionario desde el Json y lo vuelve una lista[] de objetos
    def cargar(self):
        try:
            with open(self.filename, 'r') as file:
                datos = json.load(file)  # Cargar datos desde el archivo JSON
                self.tareas = []  # Lista para almacenar las tareas cargadas
                for item in (datos):
                    title = item['title']
                    note = item['note']
                    date = item['date']
                    status = item['status']  
                    tarea = Tarea(title,note,date,status)
                    self.tareas.append(tarea)
                    print("DEBUG - Tareas cargadas:", self.tareas)
                return self.tareas #Aquí retorna la lista para que pueda usarse de forma global
        except FileNotFoundError:
            print(f"El archivo '{self.filename}' no fue encontrado.")
            return ['El archivo' + self.filename +'no fue encontrado']
        except json.JSONDecodeError:
            print(f"El archivo '{self.filename}' no tiene un formato JSON válido.")      

#DJANGO  renderiza desde diccionarios, al menos hasta lo que aprendí para este proyecto.
#Por lo tanto se crea esta función que toma los atributos de los objetos Tareas() y los transcribe 
#a un Diccionario{} de strings que pueda renderizarse en <html>.
    def get_dic(self):
        #Este devuelve las pendientes.
        #Verifico que la lista no esté vacía, para que pueda darse un feedback acorde. 
        if not self.tareas:
           return "empty" #Esto requiere un template independiente
        else:
        #Aquí uso operator para poder sustraer el atributo _date y usarlo para organizar la lista en
        #un orden de inminencia de cada tarea.
        #Es el único filtro. Seguro '_date' pueda cambiarse por una variable que se comunicase con la interfaz de usuario para
        #Organizar la información de otra forma.
            self.tareasOrdenadas=sorted(self.tareas,key=operator.attrgetter('_date'))
            #El diccionario necesita indexarse. Extraemos de la lista ordenada, e introducimos los
            #datos de cada objeto en en el dict{}
            for indice,item in enumerate(self.tareasOrdenadas):
                if (item.get_status() == "Pendiente"):
                    self.dic[indice] = {'serie': indice,'title':item.get_title(),
                    'note':item.get_note(), 
                    'date':item.get_date(),
                    #Hay que poner una excepción aquí por el deadline
                    'deadline':item.get_deadline(),
                    'status':item.get_status(),
                    }
        return  self.dic #la información con la que trabajamos las views. ----- Vamos a views.py ----->         
        
    def get_historial(self):
   #Historial devulve las completadas
        #Verifico que la lista no esté vacía, para que pueda darse un feedback acorde. 
        if not self.tareas:
           return "empty" #Esto requiere un template independiente
        else:
        #Aquí uso operator para poder sustraer el atributo _date y usarlo para organizar la lista en
        #un orden de inminencia de cada tarea.
        #Es el único filtro. Seguro '_date' pueda cambiarse por una variable que se comunicase con la interfaz de usuario para
        #Organizar la información de otra forma.
            self.tareasOrdenadas=sorted(self.tareas,key=operator.attrgetter('_date'))
            #El diccionario necesita indexarse. Extraemos de la lista ordenada, e introducimos los
            #datos de cada objeto en en el dict{}
            for indice,item in enumerate(self.tareasOrdenadas):
                if (item.get_status() == "Completado"):
                    self.dic[indice] = {'serie': indice,'title':item.get_title(),
                    'note':item.get_note(), 
                    'date':item.get_date(),
                    #Hay que poner una excepción aquí por el deadline
                    'deadline':item.get_deadline(),
                    'status':item.get_status(),
                    }
        return  self.dic #la información con la que trabajamos las views. ----- Vamos a views.py ----->