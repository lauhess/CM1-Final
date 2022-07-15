import sys

def parse_graph(lines):
    num_vert = int(lines[0])
    vert = lines[1:num_vert+1]
    aristas = [tuple(e.split(" ")) for e in lines[num_vert+1:] ]
    return (vert, aristas)

def read_graph(file_path):
    try:
        with open(file_path) as f:
            data = f.read()
            lines = data.strip().split("\n")
    except FileNotFoundError:
        print(f"El archivo {file_path} no existe.")
        sys.exit(1)

    return parse_graph(lines)
