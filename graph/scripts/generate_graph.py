import json
import os
import argparse
import networkx as nx
from collections import defaultdict
from typing import Dict, Tuple, Set, List, NamedTuple
from enum import Enum


class ConceptType(Enum):
    CONCEPT = "concept"
    PROBLEM = "problem"

class ConceptInfo(NamedTuple):
    id: int # id of the concept
    type: ConceptType # type of the concept
    prereqs: Set[int] # ids of the concepts that are prereqs for this concept


def generate_cytoscape_json(G, web_dir: str):
    elements = {"nodes": [], "edges": []}
    # Add nodes
    for node in G.nodes:
        print(f"Adding node to Cytoscape: {node}")
        elements['nodes'].append({
            "data": {
                "id": str(node),  # Ensure ID is a string
                "label": str(node),
                "type": node.type.value
            }
        })

    # Add edges
    for i, edge in enumerate(G.edges):
        source, target = edge
        edge_id = f"e{i}"
        elements['edges'].append({
            "data": {
                "id": edge_id,
                "source": str(source),  # Ensure source is a string
                "target": str(target)   # Ensure target is a string
            }
        })

    # Create web directory if it doesn't exist
    os.makedirs(web_dir, exist_ok=True)
    # Write to file
    with open(os.path.join(web_dir, "graph.json"), "w") as f:
        json.dump(elements, f, indent=2)

    print("Cytoscape.js elements JSON generated at web/graph.json")



def generate_graph(concept_map: Dict[str, ConceptInfo]) -> nx.DiGraph:
    G = nx.DiGraph()
    # req, (id, [prereq])

    # create a id to concept name mapping
    id_to_concept: Dict[int, str] = defaultdict(lambda: "")
    for req, concept_info in concept_map.items():
        id_to_concept[concept_info.id] = req
        print(f"Adding node {req} with id {concept_info.id}")
        G.add_node(req, info=concept_info)

    for req, concept_info in concept_map.items():
        for prereq in concept_info.prereqs:
            print(f"Adding edge {req} -> {id_to_concept[prereq]}")
            G.add_edge(req, id_to_concept[prereq])

    # Return the graph object
    return G


def save_graph_to_file(G, filename):
    nx.write_graphml(G, filename)



def process_concept_streams(problems, add_problem_ids: bool = False) -> Dict[str, ConceptInfo]:
    # Extract concept streams from problems
    concept_map: Dict[str, ConceptInfo] = defaultdict(lambda: ConceptInfo(len(concept_map), ConceptType.CONCEPT, set([])))
    for problem in problems:
        problem_id: int = problem['id']
        concepts_streams: List[str] = problem.get('concepts', [])

        #"cc->data_structures->arrays->linkedlist->linkedlist_addition",
        #"cc->mathematics->addition->carry"
        for concept_stream in concepts_streams:
            concept_stream = concept_stream.split('->')[::-1]

            for concept in concept_stream:
                if concept not in concept_map:
                    # Initialize concept in map with empty list of dependent IDs
                    concept_map[concept] = ConceptInfo(len(concept_map), ConceptType.CONCEPT, set([]))

            for i in range(len(concept_stream) - 1):
                req = concept_stream[i]
                prereq = concept_stream[i + 1]
                concept_map[req].prereqs.add(concept_map[prereq].id)

            # Add problem ID to the first concept in the stream
            if add_problem_ids:
                problem_id_str = "LC_" + str(problem_id)
                if problem_id_str not in concept_map:
                    concept_map[problem_id_str] = ConceptInfo (len(concept_map), ConceptType.PROBLEM, set([]))
                # add tail of the concept stream as a prereq to the problem
                concept_map[problem_id_str].prereqs.add(concept_map[concept_stream[0]].id)

    #print(concept_map)
    return concept_map


def load_latest_problems_json(data_dir: str):
    # Find the highest version of problems_v{n}.json
    version = 0
    while os.path.exists(f'{data_dir}/problems_v{version+1}.json'):
        version += 1

    # Load the highest version file
    problems_path = f'{data_dir}/problems_v{version}.json'
    with open(problems_path, 'r') as f:
        problems = json.load(f)

    print(f"Loaded {len(problems)} problems from {problems_path}")
    return problems


def load_graph(data_dir: str):
    # Load the latest problems JSON file
    problems = load_latest_problems_json(data_dir)
    # Process concept streams
    concept_map = process_concept_streams(problems, add_problem_ids=True)
    return concept_map

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate knowledge graph')
    parser.add_argument('--data_dir', type=str, help='Directory for the data file')
    parser.add_argument('--out-dir', type=str, help='Directory for the output files')
    args = parser.parse_args()

    concept_map = load_graph(args.data_dir)
    g = generate_graph(concept_map)
   # save_graph_to_file(g, args.out_dir + "/graph.graphml")
    generate_cytoscape_json(g, args.out_dir)