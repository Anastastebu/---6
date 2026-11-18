import re
from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef

def convert_mermaid_to_owl(mmd_path: str, ttl_output_path: str):
    g = Graph()
    EX = Namespace("http://example.org/it_infrastructure#")
    g.bind("ex", EX)
    g.bind("owl", OWL)

    with open(mmd_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Словник концептів: ID -> Label
    concepts = {}
    
    # 1. Парсинг концептів
    for line in lines:
        match = re.search(r'(\w+)\["([^"]+)"\]', line)
        if match:
            c_id, c_label = match.groups()
            concepts[c_id] = c_label
            c_uri = EX[c_id]
            g.add((c_uri, RDF.type, OWL.Class))
            g.add((c_uri, RDFS.label, Literal(c_label, lang="uk")))

    # 2. Парсинг зв'язків
    for line in lines:
        rel_match = re.search(r'(\w+)\s*-->\|"([^"]+)"\|\s*(\w+)', line)
        if rel_match:
            source, relation, target = rel_match.groups()
            if source in concepts and target in concepts:
                # Нормалізація предикату
                pred_id = re.sub(r'\W+', '_', relation.strip().lower())
                pred_uri = EX[pred_id]
                
                g.add((pred_uri, RDF.type, OWL.ObjectProperty))
                g.add((pred_uri, RDFS.label, Literal(relation, lang="uk")))
                
                # Потрійка RDF (Subject - Predicate - Object)
                g.add((EX[source], pred_uri, EX[target]))

    g.serialize(destination=ttl_output_path, format="turtle")
    print(f"Успішно згенеровано OWL/RDF файл: {ttl_output_path}")

if __name__ == "__main__":
    convert_mermaid_to_owl("models/concept_map.mmd", "models/concept_map.ttl")