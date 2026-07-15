# Persepolis: a Linked Open Data Project

**Course:** Information Science and Cultural Heritage, a.y. 2025–2026
**Program:** Digital Humanities and Digital Knowledge (DHDK), University of Bologna
**Topic:** Persepolis, ceremonial capital of the Achaemenid Empire
**Source page:** https://en.wikipedia.org/wiki/Persepolis

## What this is

A small LODLAM (Linked Open Data in Libraries, Archives and Museums) project: 20 entities related
to Persepolis, each reconciled to Wikidata, modeled first as an informal theoretical model and then
as a formal ontology reusing CIDOC-CRM / FOAF / Dublin Core Terms / SKOS, encoded in TEI/XML, and
mechanically transformed into both an HTML report and an RDF/Turtle knowledge graph.

Every Wikidata QID in this project was individually verified against a live Wikidata page before
use — none were generated from memory.

## File list

| File | Purpose |
|---|---|
| `report.html` | Main report — open this first |
| `data.xml` | TEI/XML source: 20 entities, 30 relations, annotated text |
| `style.xsl` | XSLT stylesheet: transforms data.xml → output.html |
| `output.html` | Generated HTML rendering of data.xml |
| `transform.py` | Python script that runs the XSLT transformation |
| `generate_rdf.py` | Python script: parses data.xml, generates knowledge_graph.ttl |
| `knowledge_graph.ttl` | Generated RDF dataset (Turtle syntax) |
| `theoretical_model.svg` | Informal entity-relationship diagram (mind map) |
| `conceptual_model.svg` | Formal ontology diagram (Graffoo notation) |
| `README.md` | This file |

## How to run it

### Requirements
```bash
pip install lxml --break-system-packages
```
(`lxml` is the only dependency; no internet access or additional RDF library like `rdflib` is
required — Turtle is generated as plain, correctly-formatted text.)

### 1. Generate output.html from data.xml
```bash
python3 transform.py
```
This applies `style.xsl` to `data.xml` and writes `output.html`. Re-run this any time `data.xml`
changes.

### 2. Generate knowledge_graph.ttl from data.xml
```bash
python3 generate_rdf.py
```
This parses `data.xml` and writes `knowledge_graph.ttl`, containing the ontology declarations,
20 entity resources, 4 event resources, and 30 relation triples.

### 3. View the results
- Open `output.html` directly in any browser.
- Open `report.html` for the full write-up, with both diagrams embedded.
- Open `knowledge_graph.ttl` in a text editor, or paste it into
  [RDF Grapher](http://www.ldf.fi/service/rdf-grapher) or a triple store (GraphDB, Apache Jena
  Fuseki, Protégé) to visualize/query the graph.

### Validation notes
- `data.xml` was validated for well-formedness with `lxml.etree.parse` — no errors.
- `output.html` was validated by parsing it back with `lxml`'s HTML parser — no errors.
- `knowledge_graph.ttl`'s prefix/triple structure was manually checked for correct Turtle syntax
  (every statement terminated with `.`, every prefixed name resolvable against the declared
  `@prefix` lines).
- All 20 Wikidata QIDs were checked individually against live Wikidata pages before being used
  anywhere in the project.

## Data model summary

- **20 entities**: Persepolis, Darius the Great, Xerxes I, Alexander the Great, Cyrus the Great,
  Ernst Herzfeld, Erich Schmidt, Achaemenid Empire, UNESCO, Institute for the Study of Ancient
  Cultures, Apadana, Gate of All Nations, Tachara, Fars Province, Marvdasht, Pasargadae,
  Naqsh-e Rustam, Zoroastrianism, Old Persian, Persepolis Administrative Archives.
- **30 relations** (see `data.xml`'s `<listRelation>` or `report.html` section 3).
- **4 events**: Foundation (518 BCE), Destruction (330 BCE), Excavation (1931–1939), UNESCO
  Inscription (1979).
- **Reused vocabularies**: CIDOC-CRM, FOAF, Dublin Core Terms, SKOS, OWL/RDFS.
- **19 project-specific properties**, each declared `rdfs:subPropertyOf` an existing Dublin Core
  Terms property (see `generate_rdf.py`'s `ONTOLOGY` block or `report.html` section 4).
