import sys
import os
from parser import parse

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file>")
        return

    source_path = os.path.join(os.path.dirname(__file__), "..", sys.argv[1])
    source_path = os.path.abspath(source_path)

    try:
        with open(source_path, 'r') as file:
            source = file.read()
        parse(source)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
