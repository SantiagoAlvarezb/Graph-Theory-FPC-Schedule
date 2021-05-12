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

# algoritmo de coloreo greedy (de network x)
color = nx.coloring.greedy_color(G, strategy="largest_first")
# print(color)

# Como colorear el grafo SIN RESTRICCIONES con la informacion del algoitmo usando anteriormente
color_map = []
for i in color:
    color_map.append(color[i])

# Encontrar el número cromatico
chromatic_number = []
for i in color_map:
    if i not in chromatic_number:
        chromatic_number.append(i)
print("Número de fechas: ", len(chromatic_number))

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

# Cambiar los nodos de Grafo para el nuevo coloreo. Se tuvo que reorganizar el orden de los nodos
new_list_node = list(color_r1.keys())
mapping = dict(zip(G.nodes, new_list_node))
G = nx.relabel_nodes(G, mapping)

color_map_r1 = []
for i in color_r1:
    color_map_r1.append(color_r1[i])

chromatic_number_r1 = []
for i in color_map_r1:
    if i not in chromatic_number_r1:
        chromatic_number_r1.append(i)
print(
    "Número de fechas con la implementacion de la restricción #1: ",
    len(chromatic_number_r1),
)

fig = plt.figure(figsize=(10, 10))
plt.gca().set_title("Grafo con restriccion 1 de 9 equipos coloreado")
pos = nx.circular_layout(G, scale=2)
nx.draw(G, pos, node_color=color_map_r1, with_labels=1, node_size=200, font_size=6)
plt.axis("equal")
plt.show()

print("-----------PARA R1-----------")
for i in range(len(teams)):
    for key, value in color_r1.items():
        if i == value:
            print(i, key)
    print("##")
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

# Cambiar los nodos de Grafo para el nuevo coloreo. Se tuvo que reorganizar el orden de los nodos
new_list_node_2 = list(color_r2.keys())
mapping_2 = dict(zip(G.nodes, new_list_node_2))
G = nx.relabel_nodes(G, mapping_2)

color_map_r2 = []
for i in color_r2:
    color_map_r2.append(color_r2[i])

chromatic_number_r2 = []
for i in color_map_r2:
    if i not in chromatic_number_r2:
        chromatic_number_r2.append(i)
print(
    "Número de fechas con la implementacion de la restricción #2: ",
    len(chromatic_number_r2),
)

fig = plt.figure(figsize=(10, 10))
plt.gca().set_title("Grafo con restriccion 2 de 9 equipos coloreado")
pos = nx.circular_layout(G, scale=2)
nx.draw(G, pos, node_color=color_map_r2, with_labels=1, node_size=200, font_size=6)
plt.axis("equal")
plt.show()

print("-----------Horario parcial con R1 y R2-----------")
for i in range(len(teams)):
    for key, value in color_r1.items():
        if i == value:
            print(i, key)
    print("##")
print("----------------------")

# -------------Fin de Restriccion 2---------------------
# print("----------------------")
# -------------Restriccion 3---------------------
# Tercera restriccion: En lo posible tener una liga donde los equipos son L-V-L-V...

# -------------Fin de Restriccion 3---------------------