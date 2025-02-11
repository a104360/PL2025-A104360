import sys
import re
import os

def main():
    acc = 0
    on = True
    os.system("clear")

    for linha in sys.stdin:
        numbers : list[str] = re.findall(r"\bOn\b|Off|\-?\d+|=",linha,re.IGNORECASE)
        for a in numbers:
            if a.capitalize() == "Off":
                on = False
                continue
            if a.capitalize() == "On":
                on = True
                continue
            if a == "=":
                print(acc)
                continue
            if on : 
                acc = acc + int(a)


if __name__ == "__main__":
    main()