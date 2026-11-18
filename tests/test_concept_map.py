import pytest
from rdflib import Graph, RDF, OWL, RDFS, Namespace

@pytest.fixture
def map_graph():
    g = Graph()
    g.parse("models/concept_map.ttl", format="turtle")
    return g

def test_graph_not_empty(map_graph):
    """C1: Граф валідний та містить триплети"""
    assert len(map_graph) > 0

def test_concept_count(map_graph):
    """C2: Перевірка кількості концептів (>= 15)"""
    classes = list(map_graph.subjects(RDF.type, OWL.Class))
    assert len(classes) >= 15

def test_no_generic_relations(map_graph):
    """C3: Перевірка відсутності неспецифічних предикатів (наприклад, 'related_to')"""
    EX = Namespace("http://example.org/it_infrastructure#")
    bad_pred = EX["related_to"]
    triples = list(map_graph.triples((None, bad_pred, None)))
    assert len(triples) == 0, "Виявлено заборонений загальний зв'язок 'related_to'"

def test_cross_links_exist(map_graph):
    """C4: Наявність міжгілкових крос-зв'язків"""
    EX = Namespace("http://example.org/it_infrastructure#")
    # Перевірка зв'язку між Security/Firewall та Server/Network
    firewall_protects = list(map_graph.triples((EX["Firewall"], EX["захищає"], EX["Server"])))
    assert len(firewall_protects) > 0