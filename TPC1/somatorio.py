import sys
import os
import re

def main():
    acc = 0
    on = True
    inputFileName = input("INSERIR NOME DO FICHEIRO DE INPUT : ")
    if os.path.exists(inputFileName): 
        inputFile = "exists"
        outputFileName = input("INSERIR NOME DO FICHEIRO DE OUTPUT : ")
        if outputFileName == "\n": output = None
        else: output = "exists"
    else: inputFile = None
    
            
    if inputFile: 
        try:
            inputFile = open(inputFileName,"r")
            sys.stdin = inputFile
            if output and outputFileName != "stdout":
                output = open(outputFileName,"w")
                if not output:
                    output = open(outputFileName,"xw")
                sys.stdout = output
        except:
            sys.stderr.write("ERRO : ficheiro invalido")
            sys.stderr.flush()
            return

    try:
        for linha in sys.stdin:
            numbers : list[str] = re.findall(r"\bOn\b|Off|\-?\d+|=",linha,re.IGNORECASE)
            for a in numbers:
                if a.capitalize() == "Off":
                    on = False
                    continue
                if a.capitalize() == "On":
                    on = True
                    continue
                if a.find('=') != -1:
                    sys.stdout.write(f">>{acc}\n")
                    sys.stdout.flush()
                    continue
                if on : 
                    acc = acc + int(a)
            
        sys.stdout.write(f">>{acc}\n\0")
        if inputFile : inputFile.close()
        if output : output.close()
    except:
        sys.stdout.write(f">>{acc}\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()