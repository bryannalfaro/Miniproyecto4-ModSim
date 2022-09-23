import math
import random

#Based on Sheldon Ross, Simulation, 5th Edition.

#Un servidor
capacity_server_mountain = 100
clients_per_second_mountain = 2400/60

#Se utiliza distribucion Poisson para llegadas
def poisson_generation(t , lambda_value):
    u = random.random()
    return t - (1/lambda_value) * math.log(u)

#Inicializacion de variables
t = na = nd = n = 0
T0 = poisson_generation(t, clients_per_second_mountain)
ta = T0
arrival_time = {}
departure_time = {}

#Variable para almacenar el tiempo ocupado
occupied_time = 0
occupied_time_list = []

td = math.inf

T = 3600 #Una hora de ejecucion
while t <= T or n>0:
    if ta <= td and ta <= T: #Caso 1 , representando una llegada
        t = ta
        na += 1
        n += 1
        ta = poisson_generation(t, clients_per_second_mountain) #Se genera la proxima llegada
        arrival_time[na] = t
        if n == 1:
            Y = random.expovariate(capacity_server_mountain) #se genera el tiempo de servicio
            td = t + Y #Se mueve en el tiempo
            occupied_time_list.append(Y) #Se agrega tiempo de servicio
            occupied_time += Y #Se suma el tiempo de servicio

    elif td < ta and td <= T: #Caso 2 , representando una salida
        t = td
        nd += 1
        n -= 1
        if n == 0: #Si no hay clientes en el sistema
            td = math.inf
        else:
            Y = random.expovariate(capacity_server_mountain) #se genera el tiempo de servicio
            td = t + Y #Se mueve en el tiempo
            occupied_time += Y #Se suma el tiempo de servicio
            occupied_time_list.append(Y) #Se agrega tiempo de servicio
        departure_time[nd]=t
    elif min(ta,td) > T and n>0: #Caso 3 , hay clientes y se paso el tiempo
        t = td
        n -= 1
        nd += 1
        if n >  0: #Si hay clientes en el sistema
            Y = random.expovariate(capacity_server_mountain) #se genera el tiempo de servicio
            td = t + Y #Se mueve en el tiempo
            occupied_time += Y #Se suma el tiempo de servicio
            occupied_time_list.append(Y) #Se agrega tiempo de servicio
        departure_time[nd]= t
    elif min(ta,td) > T and n==0: #Caso 4 , no hay clientes y se paso el tiempo
        tp = max(t-T,0) #Tiempo extra
        break



#Total de procesos
print('Solicitudes',nd)

#Tiempo servidor ocupado
print('Tiempo servidor ocupado', occupied_time)

#Tiempo servidor desocupado
print('Tiempo servidor desocupado', T-occupied_time)

cola = len(arrival_time)
contador = 0
arrivals = list(arrival_time.values())
departures = list(departure_time.values())

#Se calcula para cada solicitud el tiempo de salida - tiempo de llegada y se quita
#el tiempo ocupado, lo que dara el tiempo en cola para cada solicitud
for i in range(cola):
    contador += (departures[i] - arrivals[i]) - occupied_time_list[i]

print('Tiempo en cola', contador)

#Tiempo promedio en cola
print('Tiempo promedio en cola', contador/len(arrival_time))


#Se calcula el tiempo en cola de cada solicitud y se cuentan
#las solicitudes que estuvieron en cola
contador = 0
for i in range(cola):
    queue = (departures[i] - arrivals[i]) - occupied_time_list[i]
    if queue != 0: #Si estuvo en cola esta solicitud
        contador += 1

#Tiempo promedio de solicitudes por segundos
print('Tiempo promedio de solicitudes por segundos',contador/T)

#Obtener el ultimo valor almacenado en nd de la lista
print('Salida ultima solicitud', departure_time[nd])
