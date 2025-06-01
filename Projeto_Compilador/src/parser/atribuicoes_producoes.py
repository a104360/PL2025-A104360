from symbol_table import generalSTable
import re

# ====== Produções de Atribuições ======

def p_atribuicao(p):
    '''
    Atribuicao : Atribuido ASSIGN Expressao
    '''
    destino = p[1]

    # ===============================
    # CASO: EXPRESSÃO DO TIPO strlen
    # ===============================


    if isinstance(p[3], str):
        if re.search('strlen', p[3].lower()):
            expr_code = p[3]
            if isinstance(destino, str):  # variável simples
                pos = generalSTable.get_position(destino)

                if pos != -1:
                    p[0] = expr_code + f"\nSTOREG {pos}"
                
                else:
                    x = generalSTable.get_getter(destino)

                    p[0] = expr_code + f"\nSTOREL {x}"
                
                return
            elif isinstance(destino, tuple) and destino[0] == "array":
                _, _, _, index_code = destino
                p[0] = index_code + "\n" + expr_code + "\nSTOREN"
                return

    # ===============================
    # EXPRESSÃO NORMAL
    # ===============================
    expr_val, expr_type, expr_code = p[3]


    # --------------------------------
    # CASO 1: VARIÁVEL SIMPLES
    # --------------------------------
    if isinstance(destino, str):
        var_name = destino

        if not generalSTable.has_variable(var_name):
            print(f"Erro: variável '{var_name}' não declarada.")
            p[0] = ""
            return
        
        expected_type = generalSTable.get_type(var_name)

        
        if expected_type == "Func":
            func_return = generalSTable.get_func_return(var_name)
            if func_return == expr_type:
                if generalSTable.current_state == var_name:
                    if len(generalSTable.get_func_return_code(var_name)) == 0:
                            # Constant folding

                        generalSTable.set_func_return_code(var_name,expr_code)
                        p[0] = "\n"
                        
        else:    

            if expr_type != expected_type and expected_type not in ("integer", "real"):
                print(f"Erro: tipos incompatíveis: variável '{var_name}' é '{expected_type}', expressão é '{expr_type}'")
                p[0] = ""
                return
        
            elif expr_code == "":
                # Constant folding
                if expr_type == "integer":
                    expr_code = f"\nPUSHI {expr_val}"
                elif expr_type == "real":
                    expr_code = f"\nPUSHF {expr_val}"
                elif expr_type == "string":
                    expr_code = f'\nPUSHS "{expr_val}"'
                elif expr_type == "boolean":
                    expr_code = f"\nPUSHI {1 if expr_val else 0}"
                else:
                    print(f"Tipo desconhecido '{expr_type}'")
                    p[0] = ""
                    return
            
            pos = generalSTable.get_position(var_name)

            if pos != -1:
                p[0] = expr_code + f"\nSTOREG {pos}"

            else:
                x = generalSTable.get_getter(destino)
                p[0] = expr_code + f"\nSTOREL {x}"
            return

    # --------------------------------
    # CASO 2: ARRAY
    # destino = ("array", base_type, array_name, index_code)
    # --------------------------------
    elif isinstance(destino, tuple) and destino[0] == "array":
        _, base_type, array_name, index_code = destino

        if expr_type != base_type:
            print(f"Erro: tipo incompatível em atribuição ao array '{array_name}'")
            p[0] = ""
            return

        if expr_code == "":
            if expr_type == "integer":
                expr_code = f"\nPUSHI {expr_val}"
            elif expr_type == "real":
                expr_code = f"\nPUSHF {expr_val}"
            elif expr_type == "string":
                expr_code = f'\nPUSHS "{expr_val}"'
            elif expr_type == "boolean":
                expr_code = f"\nPUSHI {1 if expr_val else 0}"
            else:
                print(f"Tipo desconhecido '{expr_type}'")
                p[0] = ""
                return

        p[0] = index_code + "\n" + expr_code + "\nSTOREN"
        return

    else:
        print("Erro: destino de atribuição inválido")
        p[0] = ""



def p_atribuido(p):
    '''
    Atribuido : ID
              | Acesso_array
    '''
    p[0] = p[1]







