import math
import numpy as np
import random

#Based on Sheldon Ross, Simulation, 5th Edition.

#Un servidor
capacity_server_pizzita = 10
clients_per_second_pizzita = 2400/60
servers_amount_pizzita = 17

#Se utiliza distribucion Poisson para llegadas
def poisson_generation(t , lambda_value):
    u = random.random()
    return t - (1/lambda_value) * math.log(u)

#Inicializacion de variables
t = na = nd = n = 0
T0 = poisson_generation(t, clients_per_second_pizzita)
ta = T0
arrival_time = {}
departure_time = {}

#Variable para almacenar el tiempo ocupado
occupied_time_list = []
#Fill occupied_time
for i in range(servers_amount_pizzita):
    occupied_time_list.append(0)


td = math.inf

#Customers en un servidor especifico
system_customers_servers = np.zeros(servers_amount_pizzita)

#Cantidad de clientes servidos por servidor
served_customers_servers = np.zeros(servers_amount_pizzita)

#Completition time by server
completition_time_departures = []
#Fill array with inf
for i in range(servers_amount_pizzita):
    completition_time_departures.append(math.inf)

#Tiempos en cola por cliente
queue_time = {}
#Salidas de cola por cliente
queue_departures = {}

T = 3600 #Una hora de ejecucion
while t <= T or n>0:
    #Caso 1
    if ta <= min(completition_time_departures) and ta <= T:

        #Movernos en el tiempo
        t = ta
        na += 1
        n += 1
        ta = poisson_generation(t, clients_per_second_pizzita) #Se genera la proxima llegada

        #Verificar en cada servidor cual esta libre
        flag = False
        for i in range(servers_amount_pizzita):
            if system_customers_servers[i] == 0:
                system_customers_servers[i] = na

                #Generar tiempo de servicio
                Y = random.expovariate(capacity_server_pizzita)
                completition_time_departures[i] = t + Y
                occupied_time_list[i] += Y
                flag = True
                break

        if flag == False:
            #Si no hay servidores libres
            #Se encola el cliente
            queue_time[na] = t

    #Caso 2
    else:
        #Obtener el indice que tiene el minimo valor de la siguiente salida
        index = completition_time_departures.index(min(completition_time_departures))

        #Movernos en el tiempo
        t = completition_time_departures[index]
        nd += 1
        n -= 1

        #Se aumenta la cantidad de clientes servidos por este servidor (index)
        served_customers_servers[index] += 1

        #Guardar la salida
        departure_time[nd] = t

        #Verificar si hay clientes en cola
        if n >= servers_amount_pizzita:
            m_val = max(system_customers_servers)
            system_customers_servers[index] = m_val + 1

            #Generar tiempo de servicio
            Y = random.expovariate(capacity_server_pizzita)
            completition_time_departures[index] = t + Y
            occupied_time_list[index] += Y

            #Tiempo en que sale de cola por cliente
            queue_departures[system_customers_servers[index]] = t
        else:
            completition_time_departures[index] = math.inf
            system_customers_servers[index] = 0

#Cuestionamientos

print('Cantidad de solicitudes atendidas' , nd)

print('Cantidad de solicitudes por cada servidor')
for i in range(servers_amount_pizzita):
    print('Servidor', i+1, 'atendio', served_customers_servers[i])

print('Tiempo ocupado de cada servidor')
for i in range(servers_amount_pizzita):
    print('Servidor', i+1, occupied_time_list[i])

print('Tiempo desocupado de cada servidor')
for i in range(servers_amount_pizzita):
    print('Servidor', i+1, T - occupied_time_list[i])


value_total= 0
for i in queue_time:
    value_total += (queue_departures[i] - queue_time[i])
print('Tiempo total de solicitudes en cola> ',value_total)

average_queue = 0
if len(queue_time) == 0:
    average_queue = 0
else:
    average_queue = value_total / len(queue_time)

print('Tiempo promedio de solicitudes en cola> ',average_queue)

value_total= 0
for i in queue_time:
    queue =  (queue_departures[i] - queue_time[i])
    if queue > 0:
        value_total += 1

print('Cantidad de solicitudes en cola cada segundo> ',value_total/T)

print('Salida de la ultima solicitud', departure_time[nd])


#Task 2
print(len(queue_time))