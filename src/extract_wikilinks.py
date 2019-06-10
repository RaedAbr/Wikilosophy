from bz2 import BZ2File
from xml.etree import ElementTree
import mwparserfromhell as wikiparser
import os

index_file_path = "data/simplewiki-20190520-pages-articles-multistream-index.txt.bz2"
multistream_file_path = "data/simplewiki-20190520-pages-articles-multistream.xml.bz2"
temp_file = "data/temp.xml.bz2"
output_file_path = "data/output_simple.csv"
SHIFT = 100


def show_xml(elem, indent=0):
    """
    Print the XML structure of elem on the standard output

    :param elem:    XML content to print
    :type elem:     XML object
    :param indent:  Numbre of spaces before the current tag
    """
    if elem.text:
        print(' ' * indent + elem.tag + ": " + elem.text[0:100] + "...")
    else:
        print(' ' * indent + elem.tag)
    for child in elem.findall('*'):
        show_xml(child, indent + 1)


def is_wikilink_not_to_file(node):
    """
    Check if the given node is an instance of mwparserfromhell.wikicode.Wikilink
    and if it doesn't point to a file or an image

    :param node:    The node to check
    :type node:     mwparserfromhell.wikicode.node
    :return:        True or False
    :rtype:         bool
    """
    return isinstance(node, wikiparser.wikicode.Wikilink) and not str(node).startswith("[[File:") \
        and not str(node).startswith("[[Image:")


def is_text_with_parenthesis(node):
    """
    Check if the given node is an instance of mwparserfromhell.wikicode.Text
    and if there are parenthesis in it

    :param node:    The node to check
    :type node:     mwparserfromhell.wikicode.node
    :return:        True or False
    :rtype:         bool
    """
    return isinstance(node, wikiparser.wikicode.Text) and ("(" in str(node) or ")" in str(node))


if __name__ == '__main__':
    # Read bz2 index file
    index_bz2_file = BZ2File(index_file_path)
    index_content = index_bz2_file.readlines()
    index_bz2_file.close()
    print(len(index_content))

    # Create output file, write data on it (100 lines in each iteration)
    output_file_path = open(output_file_path, "w")
    current_shift = SHIFT
    while current_shift < len(index_content):
        # Calculate the start offset, end offset and the amount of bytes to be extracted
        # from the wiki articles bz2 file
        start_offset = index_content[current_shift - 1].decode("utf-8").split(":")[0]
        end_offset = index_content[current_shift].decode("utf-8").split(":")[0]
        bytes_count = int(end_offset) - int(start_offset)

        print(start_offset)
        print(end_offset)

        # Create a partition of the bz2 articles file according to the offset using dd line command
        bash_command = "dd bs=1 skip=" + start_offset + " count=" + str(bytes_count) + " < "\
                       + multistream_file_path + "> " + temp_file
        os.system(bash_command)

        # Read the content of the partition, and parse it to XML object
        pagesBz2File = BZ2File(temp_file)
        xmlObject = ElementTree.fromstringlist(["<pages>", pagesBz2File.read(), "</pages>"])
        pagesBz2File.close()

        # For each page (article), get the id (not used for the moment), the title and the content text
        for page in xmlObject.findall("*"):
            if page.find("redirect") is not None:
                continue

            page_id = page.find("id").text
            page_title = page.find("title").text

            page_text = str(page.find("revision/text").text).replace("'''", "")  # to remove tags from the text
            parsed = wikiparser.parse(page_text)

            text_and_wikilinks_nodes = [
                node for node in parsed.nodes if
                is_wikilink_not_to_file(node)
                or
                is_text_with_parenthesis(node)
            ]

            # Get the first wikilink, not in italic, and not within parenthesis
            opening_parenthesis = False
            closing_parenthesis = False
            for node in text_and_wikilinks_nodes:
                node_value = str(node)
                if isinstance(node, wikiparser.wikicode.Text) and node_value is not '\n':
                    while "(" in node_value and ")" in node_value:
                        node_value = node_value.replace("(", "", 1).replace(")", "", 1)
                    if "(" in node_value:
                        opening_parenthesis = True
                        continue
                    if ")" in node_value:
                        closing_parenthesis = True
                        continue

                if opening_parenthesis and not closing_parenthesis:
                    continue

                if opening_parenthesis and closing_parenthesis:
                    opening_parenthesis, closing_parenthesis = False, False

                if isinstance(node, wikiparser.wikicode.Wikilink):
                    next_page = str(node.title)
                    output_file_path.write(page_title + "\t" + next_page + "\n")
                    # print(page_title + " => " + next_page)
                    break

        current_shift = current_shift + SHIFT

    output_file_path.close()
