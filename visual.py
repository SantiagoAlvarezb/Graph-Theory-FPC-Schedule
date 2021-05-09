import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.Graph()  # Inicializamos el grafo G

node_list = []  # Lista que contendrá los nodos del grafo
teams = list(range(0, 10))  # Número de equipos que toman parte del torneo
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
# 9 = DESCANSO

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
fig = plt.figure(figsize=(40, 40))
plt.gca().set_title("Grafo no restringido 10 equipos")
pos = nx.circular_layout(G, scale=2)
nx.draw(G, pos, with_labels=1, node_size=200, font_size=6)
plt.axis("equal")
plt.show()

# algoritmo de coloreo greedy (de network x)
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
print("Número cromático: ", len(chromatic_number))

fig = plt.figure(figsize=(40, 40))
plt.gca().set_title("Grafo no restringido 10 equipos coloreado")
pos = nx.circular_layout(G, scale=2)
nx.draw(G, pos, node_color=color_map, with_labels=1, node_size=200, font_size=6)
plt.axis("equal")
plt.show()
