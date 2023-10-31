from rdflib import Graph
import os


def merge_ttl(ttl_file_1, ttl_file_2):
    g1 = Graph()
    g2 = Graph()

    g1.parse(ttl_file_1, format="ttl")
    g2.parse(ttl_file_2, format="ttl")

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
                    try:
                        final_out_path = os.path.join(output_path, archive, dir)
                        final_output_ttl = ttl_file
                        for out_ttl in os.listdir(final_out_path):
                            if ttl_file.lower() == out_ttl.lower():
                                final_out_path = out_ttl

                        g = merge_ttl(
                            ttl_file_1=os.path.join(dir_path, ttl_file),
                            ttl_file_2=os.path.join(
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
                            f"Can not scrape more information from {ttl_file} file, final turtle in this step file will be created based only on input information for this pipeline step"
                        )
