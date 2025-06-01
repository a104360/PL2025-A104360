import os
import sys
from parser.pascal_anasin import rec_Parser
from symbol_table import generalSTable
import traceback


result_folder = "programas_máquina"


def main():
    global result_folder
    generalSTable.reset()
    print("Symbol table initialized.")

    input_path = sys.argv[1]

    if len(sys.argv) == 3:
        result_folder = sys.argv[2]

    try:
        with open(input_path, 'r') as file:
            content = file.read()

        result = rec_Parser(content)

        lines = result.splitlines()
        clean_lines = [line.strip() for line in lines if line.strip()]
        result= '\n'.join(clean_lines)
        print()
        print("-----Tabela de Símbolos final:")
        generalSTable.dump()
        print("---------------")


        print()
        print("==================COMPILAÇÃO TERMINADA==================")
        print()
        print("-----Resultado:")
        print(result)
        print("---------------")
        

        input_filename = os.path.basename(input_path)
        output_filename = os.path.splitext(input_filename)[0] + ".out"
        os.makedirs(result_folder, exist_ok=True)
        output_path = os.path.join(result_folder, output_filename)

        with open(output_path, 'w') as outfile:
            outfile.write(result)

        print(f"Output written to: {output_path}")

    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        # Print full traceback to string
        tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        print("Full traceback:\n", tb_str)

        # Or access structured info
        tb = e.__traceback__
        while tb is not None:
            frame = tb.tb_frame
            lineno = tb.tb_lineno
            filename = frame.f_code.co_filename
            func_name = frame.f_code.co_name
            print(f"Error in file: {filename}, function: {func_name}, line: {lineno}")
            tb = tb.tb_next


if __name__ == "__main__":
    main()


