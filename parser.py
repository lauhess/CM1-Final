def parse_graph(lines):
    num_vert = int(lines[0])
    vert = lines[1:num_vert+1]
    aristas = [tuple(e.split(" ")) for e in lines[num_vert+1:] ]
    return (vert, aristas)

def read_graph(file_path):
    try:
        with open(file_path) as f:
            data = f.read()
            lines = data.split("\n")
    except FileNotFoundError:
        error_quit(f"El archivo {file_path} no existe.")

    return parse_graph(lines)
