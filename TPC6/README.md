# TPC 6 : Parser sintático de Expressões aritméticas

## 2025-03-21

### David Filipe Rocha Figueiredo - A104360

![fotoPerfil](../images/DavidFilipeRochaFigueiredoSMALL.png)

Para este TPC, pretende-se que seja implementado um analisador sintático para expressões aritméticas simples, i.g. "2 \* 7 - 5 \* 3".

A solução passa pela implementação de um parser léxico para definir os tokens pertencentes à gramática. Foram identificados:

- NUM : números
- OP  : operações

Despois, os tokens são submetidos a um analisador sintático que reconhece as
frases de acordo com a gramática:

- T = {op,num}
- S = Exp
- N = {Exp, ExpCont}
- P = {
    Exp     -> num ExpCont,
    ExpCont -> (Vazio)
            | op Exp
    }

Por fim, as expressões são enviadas para serem postas numa estrutura, e por fim calcular o valor da expressão, de acordo com prioridades matemáticas.
