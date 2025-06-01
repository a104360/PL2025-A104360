from loops_table import counter

# ====== Produções IF/THEN/ELSE ======

def p_instrucao_condicional(p):
    '''
    InstrucaoCondicional : IF Condicao THEN BlocoCondicional ParteElse
    '''
    print("Reconhecida instrução condicional IF-THEN[-ELSE]")
    
    counter.inc_if()

    false_label = f'ELSE{counter.get_if()}'
    end_if = f'ENDIF{counter.get_if()}'
    check_cond = f'JZ {false_label}'
    end_true_body = f'JUMP {end_if}'

    p[0] = "\n".join([p[2],
                      check_cond,
                      p[4],
                      end_true_body,
                      false_label+':',
                      p[5],
                      end_if+ ':'])


def p_bloco_condicional(p):
    '''
    BlocoCondicional : Instrucao
    '''
    print("Reconhecido bloco do THEN")
    p[0] = p[1]

def p_parte_else(p):
    '''
    ParteElse : ELSE Instrucao
              | 
    '''
    if len(p) > 1:
        p[0] = f"{p[1]} {p[2]}"
        print("Reconhecido bloco ELSE")
        p[0] = p[2]
    else:
        print("Não há bloco Else")
        p[0] = '\n'
