import xml.etree.ElementTree as ET


def main():
    tree = ET.parse('country_data.xml')
    root = tree.getroot()


if __name__ == "__main__":
    main()
