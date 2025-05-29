import sys
from parser import parse

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file>")
        return

    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line:
            try:
                result = parse(line)
                print(result)
            except Exception as e:
                print(f"Error parsing line '{line}': {e}")

if __name__ == "__main__":
    main()
