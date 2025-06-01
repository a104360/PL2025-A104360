from symbol_table import generalSTable
from symbol_table import SymbolTable

# ====== Produções de Função e Procedimento ======

cool_funcy_name = ""

def p_funcao(p):
    '''
    Dfuncao : FuncDec BufferVar BEGIN LocalInstsList END ';'
    '''

    global generalSTable
    func_name = p[1]

    local_insts = p[4]
    global_insts = p[2]

    
    code = f"\n{func_name}:"
    code += global_insts + "\n"
    code += local_insts
    
    ret_val = generalSTable.get_func_return_code(func_name)

    if ret_val == "":
        return

    code += ret_val

    code += "\nRETURN\n"
    
    generalSTable.set_state("global")
    
    p[0] = code
    

def p_funky_town(p):
    '''
    BufferVar : BufferVar Dvariaveis
              |
    '''

    if len(p) == 3:

        p[0] = p[1] + p[2]
    else:
        p[0] = "\n"


def p_func_dec(p):
    '''
    FuncDec : Cabeca ArgumentosSetter ':' Tipo ';'
    '''

    func_name = p[1]
    func_return_type = p[4]
    arg_types = p[2]
    
    generalSTable.set_state("global")
    generalSTable.add_function(func_name, func_return_type, arg_types)
    generalSTable.set_state(func_name)


    
    p[0] = p[1]





def p_cabeca(p):
    '''
    Cabeca : FUNCTION ID
    '''
    global cool_funcy_name
    cool_funcy_name = p[2]
    p[0] = p[2]

def p_procedimento(p):
    '''
    Dprocedimento : PROCEDURE ID ArgumentosProcedimentoOpc ';' GlobalInsts BEGIN LocalInstsList END ';'
    '''
    print(f"Procedimento reconhecido: {p[2]}")


def p_argumentos_procedimento_opc(p):
    '''
    ArgumentosProcedimentoOpc : ArgumentosSetter
                              | 
    '''
    if len(p) == 2:
        print("Argumentos do procedimento reconhecidos")
        p[0] = p[1]

    

    else:
        print("Procedimento sem argumentos")


# ====== Produções de Argumentos (Chamadas e Definições) ======

def p_argumentos_getter(p):
    '''
    ArgumentosGetter : '(' ArgumentosGetterInit ')'
    '''
    #print("Reconhecida chamada de função com argumentos")

    p[0] = p[2]


def p_argumentos_getter_init(p):
    '''
    ArgumentosGetterInit : ArgumentosGetterBuffer Expressao
                           | 
    '''
    if len(p) == 3:
        print("Mais um argumento passado na chamada")
        p[0] = p[1] + [p[2]]
    elif len(p) == 1:
        p[0] = []
    else:
        print("Nenhum argumento passado")

def p_argumentos_getter_buffer(p):
    '''
    ArgumentosGetterBuffer : ArgumentosGetterBuffer Expressao ','
                           | 
    '''
    if len(p) == 4:
        print("Mais um argumento passado na chamada")
        p[0] = p[1] + [p[2]]
    else:
        print("Nenhum argumento passado")
        p[0] = []


def p_argumentos_setter(p):
    '''
    ArgumentosSetter : '(' ArgumentosSetterBuffer ')'
    '''

    generalSTable.set_state(cool_funcy_name)


    argumentos = p[2]

    arg_types = []
    amount = 0
    for tipo, nomes in argumentos:
        for nome in nomes:
            if generalSTable.has_variable(nome):
                raise ValueError(f"Variável '{nome}' já declarada no contexto atual.")
            amount+=1

        arg_types.extend([tipo] * len(nomes))

    amount *= -1

    for tipo, nomes in argumentos:
        for nome in nomes:
            generalSTable.add_variable(nome, tipo, amount)
            amount +=1

    p[0] = arg_types


def p_argumentos_setter_buffer(p):
    '''
    ArgumentosSetterBuffer : ArgumentosSetterBuffer ',' Argumento
                           | Argumento
                           | 
    '''
    if len(p) == 4:
        t = (p[3][0],p[3][1:])
        p[0] = p[1] + [t]


    elif len(p) == 2:
        p[0] = [(p[1][0],p[1][1:])]

    else:
        print("Nenhum argumento declarado")
        p[0] = []

def p_argumento(p):
    '''
    Argumento : OutrosArgumentos ID ':' Tipo
    '''

    nomes = p[1] + [p[2]]
    tipo = p[4].lower()

    p[0] = [tipo] + nomes
    

def p_outros_argumentos(p):
    '''
    OutrosArgumentos : OutrosArgumentos ID ','
                     | 
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[2]]

    else:
        p[0] = []

    
# ====== Produção para Chamadas de Função ======

def p_ChamadaFuncao(p):
    '''
    ChamadaFuncao : ID ArgumentosGetter
    '''
    # print(f"Chamada de função reconhecida: {p[1]}{p[2]}")


    func_name = p[1]
    arguments = p[2]


    if func_name.lower() == "writeln" or func_name.lower() == "write":
        #generalSTable.add_function("write", "None", "string")
        #generalSTable.add_function("writeln", "None", "string")

        p[0] = ""
        for x in arguments:
            if x[2] != "":
                p[0] = p[0] + x[2]
                match(x[1]):
                    case "string":
                        p[0] = p[0] + (f"\nWRITES")
                    case "integer":
                        p[0] = p[0] + (f"\nWRITEI")
                    case "real":
                        p[0] = p[0] + (f"\nWRITER")
                    case "boolean":
                        if x[0] == "TRUE":
                            p[0] = p[0] + (f"\nWRITEI")
                        else:
                            p[0] = p[0] + (f"\nWRITEI")

            else:
                match(x[1]):
                    case "string":
                        p[0] = p[0] + (f"\nPUSHS \"{x[0][1:-1]}\"")
                        p[0] = p[0] + (f"\nWRITES\n")
                    case "integer":
                        p[0] = p[0] + (f"PUSHI {x[0]}")
                        p[0] = p[0] + (f"\nWRITEI")
                    case "real":
                        p[0] = p[0] + (f"PUSHR {x[0]}")
                        p[0] = p[0] + (f"\nWRITER")
                    case "boolean":
                        if x[0] == "TRUE":
                            p[0] = p[0] + (f"PUSHI 1")
                            p[0] = p[0] + (f"\nWRITEI")
                        else:
                            p[0] = p[0] + (f"PUSHI 0")
                            p[0] = p[0] + (f"\nWRITEI")

        if func_name.lower() == "writeln":
            p[0] = p[0] + "\nWRITELN"

    elif func_name.lower() == "readln" or func_name.lower() == "read":
        p[0] = ""
        for arg in arguments:
            var_name = arg[0]
            var_type = generalSTable.get_type(var_name)
            var_pos = generalSTable.get_position(var_name)

            # Instruções de leitura e conversão
            p[0] += f"READ"
            match arg[1]:
                case "integer":
                    p[0] += f"\nATOI"
                case "real":
                    p[0] += f"\nATOF"

            # Verifica se é array
            if generalSTable.is_array(var_name):
                print("Sou array")
                array_name, base_type, index_code = arg

                # Remove o LOADN se estiver presente
                lines = index_code.split("\n")
                lines = [line for line in lines if "LOADN" not in line]
                cleaned_index_code = "\n".join(lines)

                # Gera o código final sem o LOADN
                p[0] = cleaned_index_code + "\n" + p[0] + "\nSTOREN"
            else:
                if var_pos != -1:
                    p[0] += f"\nSTOREG {var_pos}"
                    
                else:
                    x = generalSTable.get_getter(var_name)
                    p[0] += f"\nSTOREL {x}"
                # Variável simples

        if func_name.lower() == "readln":
            p[0] = p[0] + "\nWRITELN"


    elif func_name.lower() == "length":
        # generalSTable.add_function("length", "integer", "string")

        code = '\n' + p[2][0][2] + "\nSTRLEN"

        x = "length(" + p[2][0][0] + ")"

        p[0] = (x,'integer',code)

    else:

        if generalSTable.get_func_return(func_name) != "None": code = f"\nPUSHI 0"
        
        buffer = ""
        for x in arguments:
            val, type, code = x
            #if tipo != expected_argument_types[i]:
                # print(f"A função {func_name} esperava tipo [{expected_argument_types[i]}], recebeu [{tipo}]")
            if code == "":
                if type == "integer":
                    buffer += f"\nPUSHI {val}\n"
                elif type == "real":
                    buffer += f"\nPUSHF {val}\n"
                elif type == "string":
                    buffer += f'\nPUSHS {val}\n'
                elif type == "boolean":
                    buffer += f"\nPUSHI {1 if val else 0}\n"
                else:
                    print(f"Tipo desconhecido '{type}'")
                    p[0] = ""
                    return
            else:
                buffer += f"\n{code}\n"
         
        buffer = buffer + '\n'.join([
            f"PUSHA {func_name}",
            "CALL",
        ])

        p[0] = (func_name, generalSTable.get_func_return(func_name), buffer)

        


def p_ArgumentosGetter(p):
    '''
    ArgumentosGetter : '(' ListaArgumentos ')'
                     | '(' ')'
    '''

    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = []

def p_ListaArgumentos(p):
    '''
    ListaArgumentos : ListaArgumentos ',' Expressao
                    | Expressao
    '''

    if len(p) == 2:
        p[0] = [p[1]]

    else:
        p[0] = p[1] + [p[3]]

    # Implementar conforme necessário
