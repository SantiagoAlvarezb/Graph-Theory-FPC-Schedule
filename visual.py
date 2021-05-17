import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.Graph()  # Inicializamos el grafo G

node_list = []  # Lista que contendrá los nodos del grafo
teams = list(range(0, 9))  # Número de equipos que toman parte del torneo
# Los siguientes numeros representan los siguientes equipos
# 0 = Santa Fe
# 1 = Millonarios
# 2 = Atlético Nacional
# 3 = Deportivo Independiente Medellín
# 4 = Deportivo Cali
# 5 = América de Cali
# 6 = Boyacá Chicó
# 7 = Patriotas
# 8 = Junior

# Función que genera los nodos. Se generan de forma que cada equipo juego con el otro una sola voz
def creating_node_list(teams):
    for j in teams:
        for k in teams:
            if j == k:
                pass
            if k <= j:
                pass
            else:
                node_list.append((j, k))
    return node_list


# Se agregan los nodos al grafo G
def add_nodes(list1):
    G.add_nodes_from(list1)


# Función que generalas aristas del grafo. Donde solo existe arista entre nodos con equipos semejantes
def add_edges():
    for i in range(len(node_list)):
        for j in range(i + 1, len(node_list)):
            if (
                node_list[i][0] == node_list[j][0]
                or node_list[i][1] == node_list[j][1]
                or node_list[i][0] == node_list[j][1]
                or node_list[i][1] == node_list[j][0]
            ):
                G.add_edge(node_list[i], node_list[j])


node_list = creating_node_list(teams)
# intercalar partidos para evitar que equipos tengan unicamente partidos como locales o como visitantes
for i in node_list[::2]:
    node_list.remove(i)
    i = (i[1], i[0])
    node_list.append(i)

add_nodes(node_list)
add_edges()
# print(nx.info(G))  # Informacion importante sobre el grafo se muestra en la terminal

# Para la visualización del grafo
fig = plt.figure(figsize=(10, 10))
plt.gca().set_title("Grafo no restringido 9 equipos")
pos = nx.circular_layout(G, scale=2)
nx.draw(G, pos, with_labels=1, node_size=200, font_size=6)
plt.axis("equal")
plt.show()

# algoritmo de coloreo greedy/voraz (de network x)
color = nx.coloring.greedy_color(G, strategy="largest_first")

# Como colorear el grafo SIN RESTRICCIONES con la informacion del algoitmo usando anteriormente
color_map = []
for i in color:
    color_map.append(color[i])

# Encontrar el número cromatico
chromatic_number = []
for i in color_map:
    if i not in chromatic_number:
        chromatic_number.append(i)

fig = plt.figure(figsize=(10, 10))
plt.gca().set_title("Grafo no restringido 9 equipos coloreado")
pos = nx.circular_layout(G, scale=2)
nx.draw(G, pos, node_color=color_map, with_labels=1, node_size=200, font_size=6)
plt.axis("equal")
plt.show()


# -------------Restriccion 1---------------------
# Primera restriccion: Equipos que comparten estadio no pueden jugar en la misma jornada como locales
shared = []
# Se crea lista con partidos donde los equipos locales son aquellos que comparten estadio (equipos: 0, 1, 2, 3) y se agregan aristas entre ellos
for i in G.nodes():
    if i[0] == 0 or i[0] == 1 or i[0] == 2 or i[0] == 3:
        shared.append(i)

for i in range(len(shared)):
    for j in range(i + 1, len(shared)):
        if (shared[i][0] == 0 and shared[j][0] == 1) or (
            shared[i][0] == 1 and shared[j][0] == 0
        ):
            G.add_edge(shared[i], shared[j])
        elif (shared[i][0] == 2 and shared[j][0] == 3) or (
            shared[i][0] == 3 and shared[j][0] == 2
        ):
            G.add_edge(shared[i], shared[j])

# Para la visualización del grafo con la implementación de la primera restriccion sin coloreo
fig = plt.figure(figsize=(10, 10))
plt.gca().set_title("Grafo con restriccion 1 de 9 equipos")
pos = nx.circular_layout(G, scale=2)
nx.draw(G, pos, with_labels=1, node_size=200, font_size=6)
plt.axis("equal")
plt.show()

# Aplicar algoritmo de color para el nuevo grafos
color_r1 = nx.coloring.greedy_color(G, strategy="largest_first")

sorted_dict = dict()
sorted_list = list((i, color_r1.get(i)) for i in G.nodes)
for i in sorted_list:
    sorted_dict.setdefault(i[0], i[1])
color_r1 = sorted_dict

color_map_r1 = []
for i in color_r1:
    color_map_r1.append(color_r1[i])

chromatic_number_r1 = []
for i in color_map_r1:
    if i not in chromatic_number_r1:
        chromatic_number_r1.append(i)

fig = plt.figure(figsize=(10, 10))
plt.gca().set_title("Grafo con restriccion 1 de 9 equipos coloreado")
pos = nx.circular_layout(G, scale=2)
nx.draw(G, pos, node_color=color_map_r1, with_labels=1, node_size=200, font_size=6)
plt.axis("equal")
plt.show()

print("----------------------")
print(
    "A continuacion les presentamos el horario parcial obtenido con la implementación de R1"
)
for i in range(len(chromatic_number_r1)):
    print("Fecha:", i + 1)
    for key, value in color_r1.items():
        if i == value:
            print(key)
print("----------------------")
# -------------Fin de Restriccion 1---------------------

# -------------Restriccion 2---------------------
# Segunda restriccion: NO existe una fecha de clasicos
clasicos = []
# Se crea lista con los partidos denominados clásicos y agregar aristas entre ellas para que esten en fechas diferentes
for i in G.nodes():
    if (
        (i[0] == 1 and i[1] == 0)
        or (i[0] == 2 and i[1] == 3)
        or (i[0] == 5 and i[1] == 4)
        or (i[0] == 6 and i[1] == 7)
    ):
        clasicos.append(i)

for i in range(len(clasicos)):
    for j in range(i + 1, len(clasicos)):
        G.add_edge(clasicos[i], clasicos[j])

# Para la visualización del grafo con la implementación de la primera restriccion sin coloreo
fig = plt.figure(figsize=(10, 10))
plt.gca().set_title("Grafo con restriccion 2 de 9 equipos")
pos = nx.circular_layout(G, scale=2)
nx.draw(G, pos, with_labels=1, node_size=200, font_size=6)
plt.axis("equal")
plt.show()

# Aplicar algoritmo de color para el nuevo grafos
color_r2 = nx.coloring.greedy_color(G, strategy="largest_first")

sorted_dict_2 = dict()
sorted_list_2 = list((i, color_r2.get(i)) for i in G.nodes)
for i in sorted_list_2:
    sorted_dict_2.setdefault(i[0], i[1])
color_r2 = sorted_dict_2


color_map_r2 = []
for i in color_r2:
    color_map_r2.append(color_r2[i])

chromatic_number_r2 = []
for i in color_map_r2:
    if i not in chromatic_number_r2:
        chromatic_number_r2.append(i)

fig = plt.figure(figsize=(10, 10))
plt.gca().set_title("Grafo con restriccion 2 de 9 equipos coloreado")
pos = nx.circular_layout(G, scale=2)
nx.draw(G, pos, node_color=color_map_r2, with_labels=1, node_size=200, font_size=6)
plt.axis("equal")
plt.show()

print("----------------------")
print(
    "A continuacion les presentamos el horario parcial obtenido con la implementación de R1 y R2"
)
for i in range(len(chromatic_number_r2)):
    print("Fecha:", i + 1)
    for key, value in color_r2.items():
        if i == value:
            print(i, key)
print("----------------------")
# -------------Fin de Restriccion 2---------------------

# -------------Restriccion 3---------------------
# Tercera restriccion: En lo posible tener una liga donde los equipos son L-V-L-V...
# Se crea cada fecha como una lista y esta se inserta dentro de una lista llamada fechas (se vuelve una lista de listas)
fechas = []
f1 = []
f2 = []
f3 = []
f4 = []
f5 = []
f6 = []
f7 = []
f8 = []
f9 = []
f10 = []
f11 = []
for i in range(len(chromatic_number_r2)):
    for key, value in color_r2.items():
        if i == value:
            if value == 0:
                f1.append(key)
            if value == 1:
                f2.append(key)
            if value == 2:
                f3.append(key)
            if value == 3:
                f4.append(key)
            if value == 4:
                f5.append(key)
            if value == 5:
                f6.append(key)
            if value == 6:
                f7.append(key)
            if value == 7:
                f8.append(key)
            if value == 8:
                f9.append(key)
            if value == 9:
                f10.append(key)
            if value == 10:
                f11.append(key)
fechas.append(f1)
fechas.append(f2)
fechas.append(f3)
fechas.append(f4)
fechas.append(f5)
fechas.append(f6)
fechas.append(f7)
fechas.append(f8)
fechas.append(f9)
fechas.append(f10)
fechas.append(f11)

# Se escoge la primera fecha como nuestra base (cabe mencionar que se podria escoger otras fechas como base)
horario = (
    []
)  # se crea la lista horario, donde al finalizar se tendrá el horario final #

# Agregamos nuestra fecha base a horario y la quitamos de fechas
horario.append(fechas[0])
fechas.remove(fechas[0])

# we are going to go through ALL the matchdays and compare with the our base
# we are going to count the number of breaks that the two consecutive matchdays would have and the one with the minimum is the next one to be appended from fechas to horario (and deleted in fechas)

# En esta sección del codigo se comparamos la ultima fecha agregada a la lista horario con cada una de las fechas en la lista fechas
# Se cuentan el numero de equipos que juegan de local la ultima fecha agregada a lista y que juegan de visitante en las fechas de la lista fechas
# Se escoge la fecha con el numero maximo y se agrega a horario y se elimina de fechas
# Se vuelve y se repite el proceso hasta que la lista horario este llena
base = 0
rango = 10
while len(horario) != 11:
    comunes = []
    for x in range(rango):
        test = []
        for i in horario[base]:
            test.append(i[0])
        test2 = []
        for i in fechas[x]:
            test2.append(i[1])
        if len(fechas[x]) % 2 != 0:
            test2.append(99)
        elif len(fechas[x]) == 2:
            test2.append(99)
            test2.append(99)
        else:
            pass
        # encontramos el numero de equipos que juegan de local una fecha y la proxima jugarian de visitante
        mismos = len(set(test) & set(test2))
        comunes.append(mismos)

    # se encuentra la fecha con numero maximo
    valor_max = max(comunes)
    max_index = comunes.index(valor_max)

    # Se agrega esta fecha encontrada a horarios y se quita de fechas
    horario.append(fechas[max_index])
    fechas.remove(fechas[max_index])
    base += 1
    rango -= 1

# -------------Fin de Restriccion 3---------------------
print("----------------------")
print(
    "A continuacion les presentamos el horario final obtenido con la implementación de las 3 restricciones"
)
count = 0
for i in horario:
    print("Fecha:", count + 1)
    for j in i:
        print(j)
    count += 1
print("----------------------")