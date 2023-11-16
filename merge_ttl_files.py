from rdflib import Graph, RDF, Namespace, URIRef, BNode, Literal
import os
import re
from rapidfuzz import fuzz


def merge_ttl(ttl_file_org, ttl_file_add):
    g1 = Graph()
    g2 = Graph()

    g1.parse(ttl_file_org, format="ttl")
    g2.parse(ttl_file_add, format="ttl")

    fabio = Namespace("http://purl.org/spar/fabio/")
    bn = Namespace("https://w3id.org/ocs/ont/papers/")
    g1.bind("fabio", fabio)
    g1.bind("bn", bn)
    g2.bind("fabio", fabio)
    g2.bind("", bn)

    paper_org = g1.value(predicate=RDF.type, object=fabio.ResearchPaper)
    paper_add = URIRef(bn + "paper")

    id_ = re.search(r"[a-zA-Z0-9]{9}$", str(paper_org)).group(0)

    for s, p, o in g2.triples((None, None, None)):
        new_s = s
        new_o = o

        if s == paper_add:
            new_s = paper_org

        elif not isinstance(s, BNode):
            sub = str(s)
            sub = sub + "_" + id_
            new_s = URIRef(sub)

        if not isinstance(o, (Literal, BNode)):
            obj = str(o)
            obj = obj + "_" + id_
            new_o = URIRef(obj)

        if p == RDF.type:
            new_o = o

        g2.remove((s, p, o))
        g2.add((new_s, p, new_o))

    for prefix, namespace in g2.namespaces():
        g1.namespace_manager.bind(prefix, namespace)

    g1 += g2

    return g1.serialize(format="turtle")


if __name__ == "__main__":
    archives = ["csis", "scpe"]
    input_path = "/home/input_ttl_files"
    output_path = "/home/output_ttl_files"
    for archive in archives:
        root_dir = os.path.join(input_path, archive)
        for dir in os.listdir(root_dir):
            dir_path = os.path.join(root_dir, dir)
            if os.path.isdir(dir_path):
                for ttl_file in os.listdir(dir_path):
                    final_out_path = os.path.join(output_path, archive, dir)
                    final_output_ttl = ttl_file
                    mod_ttl_file = "".join(
                        [char for char in ttl_file.lower() if char.isalpha()]
                    )
                    for out_ttl in os.listdir(final_out_path):
                        mod_out_ttl = "".join(
                            [char for char in out_ttl.lower() if char.isalpha()]
                        )
                        if fuzz.ratio(mod_ttl_file, mod_out_ttl) > 95:
                            final_out_path = out_ttl
                            break

                    try:
                        g = merge_ttl(
                            ttl_file_org=os.path.join(dir_path, ttl_file),
                            ttl_file_add=os.path.join(
                                output_path, archive, dir, final_out_path
                            ),
                        )
                        with open(os.path.join(dir_path, ttl_file), "wb") as file:
                            if isinstance(g, str):
                                g = g.encode()
                            file.write(g)
                        print(f"File {ttl_file} merged")
                    except:
                        print(
                            f"Cannot scrape more information from {ttl_file} file, final ttl will be creating based on input file"
                        )
