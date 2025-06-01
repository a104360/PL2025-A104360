from symbol_table import generalSTable

def p_dvariaveis(p):
    'Dvariaveis : VAR Listavariaveis'
    print("Declaração de variáveis encontrada")
    p[0] = p[2]


def p_listavariaveis(p):
    '''
    Listavariaveis : Listavariaveis Variaveis ':' Tipo ';'
                   | 
    '''
    if len(p) > 1:
        tipo = p[4]

        declarations = []

        if isinstance(tipo, tuple) and tipo[0] == "array":
            base_type = tipo[1]
            lower, upper = int(tipo[2]), int(tipo[3])
            size = upper - lower + 1
            for var_name in p[2]:
                try:
                    generalSTable.add_array(var_name, base_type, lower, upper)
                    declarations.append(f"PUSHN {size}")
                except ValueError as e:
                    print(f"Erro: {e}")
        else:
            tipo = tipo.lower()
            if tipo == "integer" or tipo == "boolean":
                code = "PUSHI 0"
            elif tipo == "string":
                code = 'PUSHS ""'
            elif tipo == "real":
                code = "PUSHF 0"
            else:
                code = f"; tipo não reconhecido: {tipo}"

            for var_name in p[2]:
                try:
                    generalSTable.add_variable(var_name, tipo)
                    declarations.append(code)
                except ValueError as e:
                    print(f"Erro: {e}")

        joined_code = "\n".join(declarations)
        p[0] = p[1] + "\n" + joined_code if p[1] else joined_code

        print(f"Variáveis declaradas: {p[2]} do tipo {tipo}")
    else:
        p[0] = ""



def p_variaveis(p):
    '''
    Variaveis : Variaveis ',' ID
              | ID
    '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


def p_tipo(p):
    '''
    Tipo : Datatype
         | ARRAY '[' Intervalo ']' OF Datatype
         | ID
    '''
    if len(p) == 2:
        p[0] = p[1]  # tipo simples
    elif len(p) == 7:
        intervalo = p[3]
        tipo_base = p[6].lower()
        lower, upper = intervalo
        p[0] = ("array", tipo_base, lower, upper)
    else:
        p[0] = p[1]



def p_intervalo(p):
    '''
    Intervalo : INTEGER '.' '.' INTEGER
    '''
    p[0] = (p[1], p[4])


def p_datatype(p):
    '''
    Datatype : REAL_TYPE
             | INTEGER_TYPE
             | STRING_TYPE
             | BOOLEAN_TYPE
             | CHAR_TYPE
    '''
    p[0] = p[1]