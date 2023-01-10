import json
import re
import sys
from pathlib import Path

from rdflib import DCTERMS, FOAF, RDF, BNode, Graph, Namespace, Literal

SDP = Namespace("http://mini.pw.edu.pl/semantic_data_processing/")
DOCO = Namespace("http://purl.org/spar/doco/")
DEO = Namespace("http://purl.org/spar/deo/")
BIBO = Namespace("http://purl.org/ontology/bibo/")
PO = Namespace("http://www.essepuntato.it/2008/12/pattern#")
C4O = Namespace("http://purl.org/spar/c4o")
CO = Namespace("http://purl.org/co/")


def json_to_rdf(filepath):
    filepath = Path(filepath)
    with open(filepath) as f:
        doc_as_json = json.load(f)

    g = Graph()
    g.bind("", SDP)
    for name, obj in [x for x in globals().items() if x[0].isupper() and len(x[0]) >= 2 and x[0] != "SDP"]:
        g.bind(name.lower(), obj)

    g.add((paper := SDP.paper, PO.contains, body_matter := SDP["body-matter"]))
    g.add((paper, PO.contains, back_matter := SDP["back-matter"]))

    g.add((back_matter, RDF.type, DOCO.BackMatter))

    if doc_as_json.get("pdf_parse", {}).get("bib_entries", None):
        bibliography = parse_bibliography(g, doc_as_json)
        g.add((back_matter, PO.contains, bibliography))
        g.add((back_matter, CO.firstItem, bibliography_list_item := BNode()))
        g.add((bibliography_list_item, CO.itemContent, bibliography))

    output_name = re.sub(r"\s+", "", doc_as_json.get("title", "")) + "_sections_biblio_ie"
    output_path = Path(filepath.parent) / f"{output_name}.ttl"
    g.serialize(destination=output_path, format="turtle")
    output_path.chmod(0o666)


def parse_bibliography(g, doc_as_json):
    g.add((bibliography := SDP.bibliography, RDF.type, DOCO.Bibliography))
    g.add((bibliography, CO.firstItem, list_item := BNode()))

    first_iter = True
    for key, data in sorted(doc_as_json.get("pdf_parse", {}).get("bib_entries", {}).items(),
                            key=lambda x: int(x[0][len("BIBREF"):])):
        g.add((bibliography, PO.contains, bib_reference := SDP[key]))
        if not first_iter:
            g.add((list_item, CO.nextItem, next_list_item := BNode()))
            list_item = next_list_item
        g.add((list_item, CO.itemContent, bib_reference))
        g.add((bib_reference, RDF.type, DEO.BibliographicReference))
        # Raw content
        if data.get("raw_text", None):
            g.add((bib_reference, C4O.hasContent, Literal(data["raw_text"])))
        # Authors
        if data.get("authors", None):
            # Range of bibo:authorList is either rdf:List or rdf:Seq
            g.add((bib_reference, BIBO.authorList, author_list := BNode()))
            g.add((author_list, RDF.type, RDF.Seq))
            for i, author_data in enumerate(data["authors"], start=1):
                g.add((author_list, RDF[f"_{i}"], author := BNode()))
                g.add((author, RDF.type, FOAF.Person))
                # BIBO loaded into Protege has foaf:givenname and foaf:family_name in data properties
                # That's why I use them instead of, e.g., foaf:firstName, foaf:surname
                if author_data.get("first", None):
                    g.add((author, FOAF.givenname, Literal(author_data["first"])))
                if author_data.get("last", None):
                    g.add((author, FOAF.family_name, Literal(author_data["last"])))
        # Title
        if data.get("title", None):
            g.add((bib_reference, DCTERMS.title, Literal(data["title"])))
        # Year
        if data.get("year", None):
            g.add((bib_reference, DCTERMS.issued, Literal(int(data["year"]))))
        # Venue
        if data.get("venue", None):
            # The range of dcterms:publisher is dcterms:Agent. However, BIBO assumes
            # that foaf:Agent is equivalent to dcterms:Agent
            g.add((bib_reference, DCTERMS.publisher, publisher := BNode()))
            g.add((publisher, FOAF.name, Literal(data["venue"])))
        # Volume
        if data.get("volume", None):
            g.add((bib_reference, BIBO.volume, Literal(int(data["volume"]))))  # number
        # Issue
        if data.get("issue", None):
            g.add((bib_reference, BIBO.volume, Literal(int(data["issue"]))))  # number
        # Pages
        if data.get("pages", None):
            if m := re.match(r"^(\d+)--(\d+)$", data["pages"]):
                g.add((bib_reference, BIBO.pageStart, Literal(int(m.group(1)))))
                g.add((bib_reference, BIBO.pageEnd, Literal(int(m.group(2)))))
            else:
                g.add((bib_reference, BIBO.pages, Literal(data["pages"])))
        # DOI
        if data.get("other_ids", {}).get("DOI", None):
            g.add((bib_reference, BIBO.doi, Literal(data["other_ids"]["DOI"])))

        first_iter = False

    return bibliography


if __name__ == "__main__":
    input_file = sys.argv[1]
    json_to_rdf(input_file)
