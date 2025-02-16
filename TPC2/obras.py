import re
import sys

# first line : nome;desc;anoCriacao;periodo;compositor;duracao;_id

# prototype 1 : ^((.*?)?;(\"(?:[^\"\\]|\\.|\n|\"\"|[^\"]|\n)+\")?;(\d+)?;(\S+)?;(.*?)?;(\d{2}:\d{2}:\d{2})?;(O\d+)?)
# prototype 2 : ((.*)?;(\"[^;]+\")?;(\d+)?;(\S+)?;(.*?);(\d{2}:\d{2}:\d{2})?;(O\d+))
# prototype 3 : (^\S([^;])+?;(\"[^;]+\")?;(\d+)?;(\S+)?;(.*?);(\d{2}:\d{2}:\d{2})?;(O\d+))
# prototype 4 : ((^\S(?:[^;])+);(\"[^;]+\"))

# kinda working prototype : ((^\S(?:[^;])+);((?:[^\"]|\"(?!;))*\");(\d+);([^;]+);([^;]+);(\d{2}:\d{2}:\d{2});(O\d+))

# ((?:[^\"]|\"(?!;))*\");


# MOST RECENT WHOLE REGEX : ((^\S(?:[^;])+);(\"?.*(?=;\d{4}));(\d{4});(.*?(?=;));(.*?(?=;));(\d{2}:\d{2}:\d{2});(O\d+))

# Receber nome/descr
nameDesc = r"^(^\S(?:[^;])+);(\"?.*)"

# Receber resto


def main():
    file = open("obras.csv")
    sys.stdin = file

    result : dict[int,list[str]] = dict()

    i = 0
    # Iteração por entrada no csv
    for a in sys.stdin:
        # Tentativa de manipular para aparecer a entrada para os casos de descrição pequena
        r = re.search(r'(^\S(?:[^;])+);(\"?.*(?=;\d{4}));(\d{4});(.*?(?=;));(.*?(?=;));(\d{2}:\d{2}:\d{2});(O\d+)',a,re.MULTILINE)
        # Caso a descrição tenha uma mudança de linha
        if r == None:
            # Capturamos nome e decrição até à mudança de linha
            r = re.search(r'(^\S(?:[^;])+);(\"?.*)',a)
            result[i] = list()
            result[i].append(r.group(1))
            result[i].append(r.group(2))
            #print(result[i])
            for b in sys.stdin:
                #print(b)
                # Para cada linha seguinte, verificamos se é uma linha completa
                rTemp = re.search(r'(.*(?=;\d{4}));(\d{4});(.*?(?=;));(.*?(?=;));(\d{2}:\d{2}:\d{2});(O\d+)',b)
                if b == '         show piece.";1745;Barroco;Krebs, Johann Ludwig;01:00:26;O2':
                    print(f'group 1 : {rTemp.group(1)}')
                    print(f'group 2 : {rTemp.group(2)}')
                    print(f'group 3 : {rTemp.group(3)}')
                    print(f'group 4 : {rTemp.group(4)}')
                    print(f'group 5 : {rTemp.group(5)}')
                    print(f'group 6 : {rTemp.group(6)}')
                # Caso não seja
                if rTemp == None:
                    # Continuamos a capturar a descrição 
                    rTemp = re.search(r'(.*\n)',b) 
                    # Caso não seja uma continuação, mas a continuação da linha
                    if rTemp == None:
                        print("Encontrou um não")
                        rTemp = re.search(r'(.*(?=;\d{4}));(\d{4});(.*?(?=;));(.*?(?=;));(\d{2}:\d{2}:\d{2});(O\d+)',b)
                        #print(b)
                        result[i][1] = result[i][1] + (rTemp.group(1))
                        result[i][1] = re.sub(r'\n|\t|         ',' ',result[i][1])
                        result[i].append(rTemp.group(2))
                        result[i].append(rTemp.group(3))
                        result[i].append(rTemp.group(4))
                        result[i].append(rTemp.group(5))
                        result[i].append(rTemp.group(6))
                        #print(rTemp.group(6))
                        break

                    result[i][1] = result[i][1] + rTemp.group(1)
                    #print(descTemp)

                    
                else:
                    #print(result[i])
                    result[i][1] = result[i][1] + rTemp.group(1)
                    result[i][1] = re.sub(r'\n|\t|         ',' ',result[i][1])
                    result[i].append(rTemp.group(2))
                    result[i].append(rTemp.group(3))
                    result[i].append(rTemp.group(4))
                    result[i].append(rTemp.group(5))
                    result[i].append(rTemp.group(6))
                    break
                #print(rTemp)
        else : 
            #print("passou no else ")
            result[i] = list()
            result[i].append(r.group(1))
            result[i].append(r.group(2))
            result[i][1] = re.sub(r'\n|\t|         ',' ',result[i][1])
            result[i].append(r.group(3))
            result[i].append(r.group(4))
            result[i].append(r.group(5))
            result[i].append(r.group(6))
        i = i + 1
        #result[i] = list(r[0])
        #result[i].append(r[1])

    i = 0
    for a in result:
        print(f'{i} : {result[i][0]}\n')
        i = i + 1
    
    
if __name__ == '__main__':
    main()