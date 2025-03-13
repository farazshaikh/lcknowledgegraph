import json
import os
import csv
import networkx as nx








def generate_cytoscape_json(G):
    elements = {"nodes": [], "edges": []}
    for node in G.nodes:
        print(f"Adding node  Cytoscape{node}")
        elements['nodes'].append({ "data": { "id": node, "label": node} })

    for edge in G.edges:
        edge_id = f"{edge[0]}__to__{edge[1]}"
        elements['edges'].append({ "data": { "id": edge_id, "source": edge[0], "target": edge[1] } })

    with open("./output/graph.json", "w") as f:
        json.dump(elements, f)

    print("Cytoscape.js elements JSON generated at output/graph.json")



def generate_graph(concept_map):
    G = nx.DiGraph()
    # req, (id, [prereq])

    # create a id to concept name mapping
    id_to_concept = dict();
    for req, v in concept_map.items():
        id_to_concept[v[0]] = req
        print(f"Adding node {req} with id {v[0]}")
        G.add_node(req, id=v[0])

    for req, v in concept_map.items():
        for prereq in v[1]:
            print(f"Adding edge {req} -> {id_to_concept[prereq]}")
            G.add_edge(req, id_to_concept[prereq])

    # Return the graph object
    return G


def save_graph_to_file(G, filename):
    nx.write_graphml(G, filename)



def process_concept_streams(problems):
    # Extract concept streams from problems
    concept_map = {}
    for problem in problems:
        problem_id = problem['id']
        concepts_streams = problem.get('concepts', [])

        #"cc->data_structures->arrays->linkedlist->linkedlist_addition",
        #"cc->mathematics->addition->carry"
        for concept_stream in concepts_streams:
            concept_stream = concept_stream.split('->')[::-1]

            for concept in concept_stream:
                if concept not in concept_map:
                    # Initialize concept in map with empty list of dependent IDs
                    concept_map[concept] = (len(concept_map), set([]))

            for i in range(len(concept_stream) - 1):
                req = concept_stream[i]
                prereq = concept_stream[i + 1]
                concept_map[req][1].add(concept_map[prereq][0])

    print(concept_map)
    return concept_map


def load_latest_problems_json():
    # Find the highest version of problems_v{n}.json
    version = 0
    while os.path.exists(f'data/problems_v{version+1}.json'):
        version += 1

    # Load the highest version file
    problems_path = f'data/problems_v{version}.json'
    with open(problems_path, 'r') as f:
        problems = json.load(f)

    print(f"Loaded {len(problems)} problems from {problems_path}")
    return problems


def load_graph():
    # Load the latest problems JSON file
    problems = load_latest_problems_json()
    # Process concept streams
    concept_map = process_concept_streams(problems)
    return concept_map

if __name__ == "__main__":
    concept_map = load_graph()
    g = generate_graph(concept_map)
    save_graph_to_file(g, "./output/graph.graphml")
    generate_cytoscape_json(g)