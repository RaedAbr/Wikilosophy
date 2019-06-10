import csv

input_file_path = "data/output_clean2.csv"
nodes_file = "data/nodes2.csv"

if __name__ == "__main__":
    data1 = []
    data2 = []
    with open(input_file_path, "r") as f:
        reader = csv.reader(f, delimiter='|')
        next(reader)  # skip header
        for row in reader:
            data1.append(str(row[0]).strip() + "\n")
            data2.append(str(row[1]).strip() + "\n")

    nodes = list(set().union(data1, data2))
    print(nodes[0])
    print(nodes[1])
    print(nodes[2])
    print(len(nodes))
    print(data2.count("philosophy\n"))
    print(data1.count("philosophy\n"))
    with open(nodes_file, "w") as f:
        f.writelines(nodes)
