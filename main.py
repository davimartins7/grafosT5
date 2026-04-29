import sys
from graph_lib import Graph

def dsatur(graph):
    n = graph.V
    colors = [-1] * n
    order = []
    
    max_deg = -1
    start_v = -1
    for v in range(n):
        deg = graph.degree(v)
        if deg > max_deg:
            max_deg = deg
            start_v = v
            
    colors[start_v] = 0
    order.append(start_v)
    
    remaining = set(range(n))
    remaining.remove(start_v)
    
    while remaining:
        max_sat = -1
        candidates = []
        
        for v in remaining:
            neighbor_colors = {colors[neighbor] for neighbor in graph.adj[v] if colors[neighbor] != -1}
            sat_deg = len(neighbor_colors)
            
            if sat_deg > max_sat:
                max_sat = sat_deg
                candidates = [v]
            elif sat_deg == max_sat:
                candidates.append(v)
        
        best_v = -1
        max_deg = -1
        for v in candidates:
            deg = graph.degree(v)
            if deg > max_deg:
                max_deg = deg
                best_v = v
        
        neighbor_colors = {colors[neighbor] for neighbor in graph.adj[best_v] if colors[neighbor] != -1}
        color = 0
        while color in neighbor_colors:
            color += 1
            
        colors[best_v] = color
        order.append(best_v)
        remaining.remove(best_v)
        
    return colors, order

def validate_coloring(graph, colors):
    for v in range(graph.V):
        if colors[v] == -1: return False, f"Vértice {v} não colorido."
        for neighbor in graph.adj[v]:
            if colors[v] == colors[neighbor]:
                return False, f"Conflito entre {v} e {neighbor}."
    return True, "Coloração válida."

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_do_arquivo>")
        return

    input_file = sys.argv[1]
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
            v_count = int(lines[0].strip())
            e_count = int(lines[1].strip())
            g = Graph(v_count)
            for i in range(2, 2 + e_count):
                v, w = lines[i].split()
                g.add_edge(v, w)
    except Exception as e:
        print(f"Erro: {e}")
        return

    print("--- Lista de Adjacência ---")
    print(g)
    print()

    colors, order = dsatur(g)
    states = ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]
    
    print("--- Ordem de Coloração ---")
    print(" -> ".join([states[v] for v in order]))
    print()

        # Definição dos nomes das cores
    nomes_cores = ["Amarelo", "Azul", "Verde", "Vermelho", "Laranja", "Roxo", "Rosa"]
    
    print("--- Cores Atribuídas ---")
    for v in range(g.V):
        # Usamos o índice da cor para buscar o nome na lista
        cor_nome = nomes_cores[colors[v]] if colors[v] < len(nomes_cores) else f"Cor {colors[v]}"
        print(f"{states[v]} ({v}): {cor_nome}")
    print()


    print(f"Total de cores utilizadas: {len(set(colors))}")
    is_valid, message = validate_coloring(g, colors)
    print(f"Validação: {message}")

if __name__ == "__main__":
    main()
