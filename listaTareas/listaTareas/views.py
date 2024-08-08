from listaTareas.logica import ListaTareas
#importo para el proyecto los elementos de la lógica.
from django.shortcuts import render, redirect
#Render permite generar una vista html desde un dict{} a través de Django
from django.http import JsonResponse #respuesta tipo json para errores de carga del archivo
import json #Para usar json
from django.views.decorators.csrf import csrf_protect #esto se usa para que no hayan errores
#en el cruce de información cuando se usan POST (No lo entiendo del todo)
from django.utils.decorators import method_decorator #Lo mismo de arriba, pero cuando el problema es de otro tipo.
import arrow #Lo uso para 

@csrf_protect
def crear(request):
    #Tuve problemas con el atruibuto request así que puse estos debugs de seguimiento.
    if not request:
        print("DEBUG - No se recibió 'request' correctamente")
    print("DEBUG - Entrando a la vista 'crear'")
    print("DEBUG - Método de la solicitud:", request.method)
    #Carga este codigo solo si el formulario de esta misma vista
    #ha enviado una solicitud del tipo POST
    if request.method == 'POST':
        try:
    #Descompongo la información acorde a la estructura que necesito.
            title = request.POST.get('title')
            note = request.POST.get('note')
            date = request.POST.get('date')        
            if title and note and date:
                # Guardar los datos en formato JSON
                #Siempre que se crea una tarea el status es False porque nunca se han completado al momento de crearse
                post_data = {'title': title, 'note': note, 'date':date, 'status':'Pendiente'}
                try:
                #Usar with, entiendo, ayuda a que el archivo se abra y cierre, evitando sobreescrituras ideseadas.
                    with open('datos.json', 'r') as f:
                        #Cargamos los datos que ya tenemos
                        datos_existentes = json.load(f)
                except FileNotFoundError:
                        #Si no existe aun nuestro archivo, asumimos vacía la lista
                        datos_existentes = []
                datos_existentes.append(post_data)
                with open('datos.json','w') as f:
                        json.dump(datos_existentes, f, indent=4)
                        f.write('\n')  # Agrega una nueva línea para cada objeto JSON

                return render(request, 'createsucces.html')
            else:
                return JsonResponse({'status': 'error', 'message': 'falta información'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        #Uso arrow aquí para limitar las fechas posibles en el form html
        #a las del día de acceso o futuro, no anteriores.
        #Así, el formulario html siempre tiene en cuenta el tiempo del usuario.
        userTime = arrow.now().format('YYYY-MM-DD')
        contexto = {'userTime': userTime}
        return render(request, 'crear.html', contexto)

def mostrar(request):
#Si se postea, osea, que se marca una tarea como completada se ejecuta lo siguiente.
    if request.method =='POST':
        try:
        #Se recibe la información del formulario html.
        #Para ello en el form "Name" es la id. o K y value el valor v.
            for k,v in request.POST.items():
                print("Esto es K:", k,v)
                #El formulario siempre trae una linea de más con un código que no nos interesa.
                #Por eso añadimos el prefijo id. para solo tomar lo que es informació válida
                #para nuesro trabajo.
                if k.startswith('id'):
                    print("Así se ve lo recibo", k, "|", v)
                    #removemos el prefijo.
                    title = k.replace('id.','')
                    print("DEBUG-- Title:", title)
                    print("DEBUG-- Status:", v)
                    #Esta linea de acciones solo tiene sentido si hay un cambio de status a TRUE
                    if v == 'Completado':
                        with open('datos.json', 'r') as loCargado:
                            datos_existentes = json.load(loCargado)
                            print("Se cargaron datos")
                            for item in datos_existentes:
                                print("Superado")
                                #Buscamos en nuestra lista por nombre la tarea
                                #Al encontrar una coincidencia cambiamos su status.                            
                                if item.get('title') == title:
                                    print("Estamos cambiando status",title,v)
                                    item['status'] = v
                                    with open('datos.json','w') as loCargado:
                                        #Sobreescrimos todo el archivo, con los datos modificados.
                                        json.dump(datos_existentes,loCargado )
            #Mostramos feedback de que se ha completado correctamente la actualización de estado.
            return render(request, 'completarsucces.html')                              
                # else:
                #     return JsonResponse({'status':'falla algo en el segundo IF'})    
        except Exception as algo:
            return JsonResponse({'status':'error', 'message':str(algo)}, status=500) 
    #Va a mostrar un render con la lista de tareas que llega en formato diccionario.
    #Se mete en el dict Contexto y se manda a renderizar    
    else:
        #Accedemos al archivo
        try: 
            with open('datos.json', 'r') as f:
                #Creamos un objeto lista de tareas con el atributo filename=datos.jason
                miLista = ListaTareas('datos.json')
                #Asignamos el diccionario que nos ofrece la funcion get_dict a la variable a para mayor abstracción.
                a = miLista.get_dic()
                print("a=",a)
                if a:
                    #Si a no está vacía renderizamos, de lo contrario mandamos una pantalla que nos dice
                    #Que no tenemos tareas pendientes.
                    contexto = {'lista' : a}                   
                    return render(request, 'mostrar.html', contexto)  
                elif (a == "empty"):
                    return render(request,'empty.html')
                else:
                    return render(request,'empty.html')
                   
        except FileNotFoundError:
            return render(request,'empty.html')
        #JsonResponse({'status':'No existe archivo'}, status=404)
        #Esto se lanza cuando no hay archivo, pero corta la interacción con el usuario.
        #Es mucho más apropiado decirle que no hay ninguna tarea, para que así
        #Cree su primera tarea y con ello el archivo.
        

def historial(request):
#Similar a la vista anterior pero sin el formulario, sin interacción solo para mostrar las tareas ya realizadas
        try: 
            with open('datos.json', 'r') as f:
                #Creamos un objeto lista de tareas con el atributo filename=datos.jason
                miLista = ListaTareas('datos.json')
                #Asignamos el diccionario que nos ofrece la funcion get_dict a la variable a para mayor abstracción.
                a = miLista.get_historial()
                print("a=",a)
                if a:
                    #Si a no está vacía renderizamos, de lo contrario mandamos una pantalla que nos dice
                    #Que no tenemos tareas pendientes.
                    contexto = {'lista' : a}                   
                    return render(request, 'historial.html', contexto)  
                elif (a == "empty"):
                    return render(request,'empty.html')
                else:
                    return render(request,'empty.html')
                   
        except FileNotFoundError:
            return render(request,'empty.html')
        #JsonResponse({'status':'No existe archivo'}, status=404)