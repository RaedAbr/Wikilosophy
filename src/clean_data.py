input_file_path = "data/output_file.csv"
output_file_path = "data/output_clean.csv"


if __name__ == "__main__":
    with open(input_file_path, "r") as f:
        lines = f.readlines()
    x = 0
    with open(output_file_path, "w") as f:
        f.write("src|dest\n")
        for line in lines:
            if "file:" not in line.lower() and "{{" not in line and "|" not in line\
                    and "image:" not in line.lower() and "template:" not in line.lower()\
                    and "wikimedia:" not in line.lower() and "wikipedia:" not in line.lower()\
                    and "wp" not in line.lower():
                line = line.replace("\"", "")
                line = line.replace("'", "")
                line = line.replace("\t", "|")
                if "|" in line:
                    f.write(line.lower())
                    continue
            x += 1
    print(str(x) + " lines deleted")
