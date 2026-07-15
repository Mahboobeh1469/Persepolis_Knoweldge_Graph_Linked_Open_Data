"""
generate_rdf.py
Parses data.xml (TEI) and produces knowledge_graph.ttl: an RDF/Turtle dataset
instantiating the project's conceptual model (ontology), reusing CIDOC-CRM,
FOAF, Dublin Core Terms and SKOS, plus a small set of project-specific
properties (ex:) declared as sub-properties of existing ones.

Course project: Information Science and Cultural Heritage, a.y. 2025-2026, DHDK.
No external RDF library is used (rdflib could not be installed - no network
access in the sandbox); triples are assembled and serialized as plain Turtle
strings, which is valid and sufficient for a dataset of this size.
"""
from lxml import etree

TEI_NS = "{http://www.tei-c.org/ns/1.0}"
XML_NS = "{http://www.w3.org/XML/1998/namespace}"
tree = etree.parse("data.xml")
root = tree.getroot()

RES = "https://w3id.org/persepolis-project/resource/"
ONT = "https://w3id.org/persepolis-project/ontology#"

PREFIXES = f"""@prefix crm:     <http://www.cidoc-crm.org/cidoc-crm/current/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix foaf:    <http://xmlns.com/foaf/0.1/> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix res:     <{RES}> .
@prefix ex:      <{ONT}> .

"""

# ---------------------------------------------------------------------------
# 1. Conceptual model (ontology)
# ---------------------------------------------------------------------------
ONTOLOGY = """# ==================== CONCEPTUAL MODEL (ontology) ====================

crm:E27_Site rdfs:subClassOf crm:E18_Physical_Thing .
crm:E22_Human-Made_Object rdfs:subClassOf crm:E18_Physical_Thing .

ex:builtBy a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:creator ;
    rdfs:label "built by"@en ;
    rdfs:comment "Original construction. Cardinality 1..1 on the site/monument side in this dataset."@en ;
    rdfs:domain crm:E18_Physical_Thing ;
    rdfs:range foaf:Person .

ex:expandedBy a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:contributor ;
    rdfs:label "expanded by"@en ;
    rdfs:comment "Later continuation of construction by a successor, distinct from builtBy. Cardinality 0..*."@en ;
    rdfs:domain crm:E18_Physical_Thing ;
    rdfs:range foaf:Person .

ex:completedBy a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:contributor ;
    rdfs:label "completed by"@en ;
    rdfs:domain crm:E22_Human-Made_Object ;
    rdfs:range foaf:Person .

ex:destroyedBy a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:relation ;
    rdfs:label "destroyed by"@en ;
    rdfs:domain crm:E18_Physical_Thing ;
    rdfs:range foaf:Person .

ex:capitalOf a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:relation ;
    rdfs:label "capital of"@en ;
    rdfs:domain crm:E27_Site ;
    rdfs:range crm:E4_Period .

ex:succeeds a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:replaces ;
    rdfs:label "succeeds (as capital)"@en ;
    rdfs:domain crm:E27_Site ;
    rdfs:range crm:E27_Site .

ex:locatedNear a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:relation ;
    rdfs:label "located near"@en ;
    rdfs:domain crm:E27_Site ;
    rdfs:range crm:E27_Site, crm:E53_Place .

ex:recognizes a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:relation ;
    rdfs:label "recognizes"@en ;
    rdfs:comment "Agent-first direction (organization -> site), matching standard RDF practice."@en ;
    rdfs:domain foaf:Organization ;
    rdfs:range crm:E27_Site .

ex:foundedBy a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:creator ;
    rdfs:label "founded by"@en ;
    rdfs:domain crm:E4_Period ;
    rdfs:range foaf:Person .

ex:containsTomb a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:relation ;
    rdfs:label "contains tomb of"@en ;
    rdfs:domain crm:E27_Site ;
    rdfs:range foaf:Person .

ex:excavatedBy a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:contributor ;
    rdfs:label "excavated by"@en ;
    rdfs:domain crm:E27_Site ;
    rdfs:range foaf:Person .

ex:succeededExcavationOf a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:replaces ;
    rdfs:label "succeeded (as excavation director)"@en ;
    rdfs:domain foaf:Person ;
    rdfs:range foaf:Person .

ex:conductedExcavationAt a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:relation ;
    rdfs:label "conducted excavation at"@en ;
    rdfs:domain foaf:Organization ;
    rdfs:range crm:E27_Site .

ex:associatedWithReligion a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:subject ;
    rdfs:label "associated with religion"@en ;
    rdfs:domain crm:E27_Site ;
    rdfs:range skos:Concept .

ex:hasLanguage a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:language ;
    rdfs:label "has language (of inscriptions)"@en ;
    rdfs:domain crm:E27_Site ;
    rdfs:range crm:E56_Language .

ex:yieldedArchive a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:relation ;
    rdfs:label "yielded archive"@en ;
    rdfs:domain crm:E27_Site ;
    rdfs:range crm:E31_Document .

ex:discoveredBy a owl:ObjectProperty ;
    rdfs:subPropertyOf dcterms:contributor ;
    rdfs:label "discovered by"@en ;
    rdfs:domain crm:E31_Document ;
    rdfs:range foaf:Person .

# dcterms:spatial and dcterms:hasPart are reused directly (no local definition needed)

"""

# ---------------------------------------------------------------------------
# 2. Read entities from the TEI standOff
# ---------------------------------------------------------------------------
entities = {}

def add(eid, label, cls, wikidata=None, wikipedia=None, desc=None):
    entities[eid] = dict(label=label, cls=cls, wikidata=wikidata,
                          wikipedia=wikipedia, desc=desc)

for place in root.findall(f".//{TEI_NS}listPlace/{TEI_NS}place"):
    eid = place.get(f"{XML_NS}id")
    label = place.find(f"{TEI_NS}placeName").text
    wikidata = place.find(f"{TEI_NS}idno[@type='wikidata']").text
    wikipedia = place.find(f"{TEI_NS}idno[@type='wikipedia']").text
    desc = place.find(f"{TEI_NS}desc").text
    cls = "crm:E27_Site" if eid in ("persepolis", "pasargadae", "naqshe_rustam") else "crm:E53_Place"
    add(eid, label, cls, wikidata, wikipedia, desc)

for person in root.findall(f".//{TEI_NS}listPerson/{TEI_NS}person"):
    eid = person.get(f"{XML_NS}id")
    label = person.find(f"{TEI_NS}persName").text
    wikidata = person.find(f"{TEI_NS}idno[@type='wikidata']").text
    wikipedia = person.find(f"{TEI_NS}idno[@type='wikipedia']").text
    desc = person.find(f"{TEI_NS}desc").text
    add(eid, label, "foaf:Person", wikidata, wikipedia, desc)

for org in root.findall(f".//{TEI_NS}listOrg/{TEI_NS}org"):
    eid = org.get(f"{XML_NS}id")
    label = org.find(f"{TEI_NS}orgName").text
    wikidata = org.find(f"{TEI_NS}idno[@type='wikidata']").text
    wikipedia = org.find(f"{TEI_NS}idno[@type='wikipedia']").text
    desc = org.find(f"{TEI_NS}desc").text
    cls = "crm:E4_Period" if org.get("type") == "empire" else "foaf:Organization"
    add(eid, label, cls, wikidata, wikipedia, desc)

for item in root.findall(f".//{TEI_NS}list[@type='monuments']/{TEI_NS}item"):
    eid = item.get(f"{XML_NS}id")
    label = item.find(f"{TEI_NS}name").text
    monument_type = item.get("type")
    wikidata = item.find(f"{TEI_NS}idno[@type='wikidata']").text
    wikipedia = item.find(f"{TEI_NS}idno[@type='wikipedia']").text
    desc = item.find(f"{TEI_NS}desc").text
    add(eid, label, "crm:E22_Human-Made_Object", wikidata, wikipedia, desc)
    if monument_type:
        entities[eid]["monument_type"] = monument_type

for item in root.findall(f".//{TEI_NS}list[@type='concepts']/{TEI_NS}item"):
    eid = item.get(f"{XML_NS}id")
    label = item.find(f"{TEI_NS}name").text
    wikidata = item.find(f"{TEI_NS}idno[@type='wikidata']").text
    wikipedia = item.find(f"{TEI_NS}idno[@type='wikipedia']").text
    desc = item.find(f"{TEI_NS}desc").text
    cls = "crm:E56_Language" if eid == "old_persian" else "skos:Concept"
    add(eid, label, cls, wikidata, wikipedia, desc)

archive = root.find(f".//{TEI_NS}listBibl/{TEI_NS}bibl[@{XML_NS}id='fortification_archive']")
eid = archive.get(f"{XML_NS}id")
label = archive.find(f"{TEI_NS}title").text
wikidata = archive.find(f"{TEI_NS}idno[@type='wikidata']").text
desc = archive.find(f"{TEI_NS}desc").text
add(eid, label, "crm:E31_Document", wikidata, None, desc)

# ---------------------------------------------------------------------------
# 3. Read events
# ---------------------------------------------------------------------------
events = {}
for ev in root.findall(f".//{TEI_NS}listEvent/{TEI_NS}event"):
    eid = ev.get(f"{XML_NS}id")
    who_attr = ev.get("who") or ""
    who = [w.lstrip("#") for w in who_attr.split()] if who_attr else []
    events[eid] = dict(label=ev.find(f"{TEI_NS}label").text, when=ev.get("when"), who=who)

EVENT_SUBCLASS = {
    "foundation": "crm:E63_Beginning_of_Existence",
    "destruction": "crm:E6_Destruction",
    "excavation": "crm:E7_Activity",
    "inscription": "crm:E5_Event",
}

# ---------------------------------------------------------------------------
# 4. Serialize entity descriptions
# ---------------------------------------------------------------------------
def esc(s):
    return s.replace('"', '\\"') if s else ""

lines = [PREFIXES, ONTOLOGY, "# ==================== ENTITIES (instance data, 20 total) ====================\n"]

for eid, e in entities.items():
    triples = [f"res:{eid} a {e['cls']} ;",
               f'    rdfs:label "{esc(e["label"])}"@en ;']
    if e["desc"]:
        triples.append(f'    dcterms:description "{esc(e["desc"])}"@en ;')
    if e.get("monument_type"):
        triples.append(f'    dcterms:type "{esc(e["monument_type"])}"@en ;')
    if e["wikidata"]:
        triples.append(f"    owl:sameAs <{e['wikidata']}> ;")
    if e["wikipedia"]:
        triples.append(f"    foaf:isPrimaryTopicOf <{e['wikipedia']}> ;")
    triples[-1] = triples[-1][:-1] + "."
    lines.append("\n".join(triples) + "\n")

# ---------------------------------------------------------------------------
# 5. Serialize events as first-class RDF resources
# ---------------------------------------------------------------------------
lines.append("# ==================== EVENTS (instances of crm:E5_Event) ====================\n")
for eid, ev in events.items():
    subclass = EVENT_SUBCLASS.get(eid, "crm:E5_Event")
    triples = [f"res:{eid}_event a {subclass} ;",
               f'    rdfs:label "{esc(ev["label"])}"@en ;',
               f'    dcterms:date "{esc(ev["when"])}" ;']
    for wid in ev.get("who", []):
        triples.append(f"    crm:P11_had_participant res:{wid} ;")
    triples[-1] = triples[-1][:-1] + "."
    lines.append("\n".join(triples) + "\n")

# ---------------------------------------------------------------------------
# 6. Serialize relations
# ---------------------------------------------------------------------------
PROP_MAP = {
    "builtBy": "ex:builtBy",
    "expandedBy": "ex:expandedBy",
    "completedBy": "ex:completedBy",
    "destroyedBy": "ex:destroyedBy",
    "capitalOf": "ex:capitalOf",
    "succeeds": "ex:succeeds",
    "locatedIn": "dcterms:spatial",
    "locatedNear": "ex:locatedNear",
    "hasComponent": "dcterms:hasPart",
    "recognizes": "ex:recognizes",
    "foundedBy": "ex:foundedBy",
    "containsTomb": "ex:containsTomb",
    "excavatedBy": "ex:excavatedBy",
    "succeededExcavationOf": "ex:succeededExcavationOf",
    "conductedExcavationAt": "ex:conductedExcavationAt",
    "associatedWithReligion": "ex:associatedWithReligion",
    "hasLanguage": "ex:hasLanguage",
    "yieldedArchive": "ex:yieldedArchive",
    "discoveredBy": "ex:discoveredBy",
}

lines.append("# ==================== RELATIONS (from listRelation, 30 total) ====================\n")
n_rel = 0
for rel in root.findall(f".//{TEI_NS}listRelation/{TEI_NS}relation"):
    name = rel.get("name")
    active = rel.get("active").lstrip("#")
    passive = rel.get("passive").lstrip("#")
    prop = PROP_MAP[name]
    ref = rel.get("ref")
    comment = ""
    if ref:
        ev = events[ref.lstrip("#")]
        comment = f'    # {ev["label"]} ({ev["when"]})\n'
    lines.append(f"res:{active} {prop} res:{passive} .\n{comment}")
    n_rel += 1

with open("knowledge_graph.ttl", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote knowledge_graph.ttl with {len(entities)} entities, {len(events)} events, "
      f"{n_rel} relations.")
