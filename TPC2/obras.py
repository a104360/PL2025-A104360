import re
import sys


def alphaComposers(entries : dict[int,list[str]]):
    lista = dict()
    for a in entries.values():
        lista[a[4]] = None
    
    lista = sorted(lista.keys())
    return lista

def periods(entries : dict[int,list[str]]):
    periods = dict()
    for a in entries.values():
        if periods.get(a[3]):
            periods[a[3]] = periods[a[3]] + 1
        else: periods[a[3]] = 1
    return periods

def periodComposers(db : dict[int,list[str]]) -> dict[str,list[str]]:
    period : dict[str,list[str]] = dict()
    plain = db.values()
    for a in plain:
        if period.get(a[3]) == None:
            period[a[3]] = [a[4]]
        else : 
            period[a[3]].append(a[4])
            period[a[3]] = sorted(period[a[3]])
    return period
    
    

def main() -> dict[int,list[str]]:
    file = open("obras.csv")
    sys.stdin = file

    result : dict[int,list[str]] = dict()

    i = 0
    # Leitura feita para ignorar a primeira linha com o nome dos valores dos campos
    sys.stdin.readline()


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

            # Continuação da leitura das linhas na tentativa de encontrar o resto dos campos 
            for b in sys.stdin:

                # Para cada linha seguinte, verificamos se é uma linha completa
                rTemp = re.search(r'(.*(?=;\d{4}));(\d{4});(.*?(?=;));(.*?(?=;));(\d{2}:\d{2}:\d{2});(O\d+)',b)

                # Caso não seja
                if rTemp == None:

                    # Continuamos a capturar a descrição 
                    rTemp = re.search(r'(.*\n)',b) 

                    # Caso não seja uma continuação, mas o resto dos campos
                    if rTemp == None:
                        rTemp = re.search(r'(.*(?=;\d{4}));(\d{4});(.*?(?=;));(.*?(?=;));(\d{2}:\d{2}:\d{2});(O\d+)',b)

                        result[i][1] = result[i][1] + (rTemp.group(1))
                        result[i][1] = re.sub(r'\n|\t|         ',' ',result[i][1])
                        result[i].append(rTemp.group(2))
                        result[i].append(rTemp.group(3))
                        result[i].append(rTemp.group(4))
                        result[i].append(rTemp.group(5))
                        result[i].append(rTemp.group(6))
                        break

                    result[i][1] = result[i][1] + rTemp.group(1)

                    
                else:
                    result[i][1] = result[i][1] + rTemp.group(1)
                    result[i][1] = re.sub(r'\n|\t|         ',' ',result[i][1])
                    result[i].append(rTemp.group(2))
                    result[i].append(rTemp.group(3))
                    result[i].append(rTemp.group(4))
                    result[i].append(rTemp.group(5))
                    result[i].append(rTemp.group(6))
                    break
        else : 
            result[i] = list()
            result[i].append(r.group(1))
            result[i].append(r.group(2))
            result[i][1] = re.sub(r'\n|\t|         ',' ',result[i][1])
            result[i].append(r.group(3))
            result[i].append(r.group(4))
            result[i].append(r.group(5))
            result[i].append(r.group(6))
        i = i + 1
    return result
    
if __name__ == '__main__':
    # Parse do 
    db = main()

    # Lista ordenada alfabeticamente dos compositores musicais
    file = open("results/result1.txt","w")
    sys.stdout = file
    for a in alphaComposers(db):
        print(a)

    file.close()
    # Distribuição por período : quantas obras por período
    file = open("results/result2.txt", "w")
    sys.stdout = file
    mapper = periods(db)
    for a in mapper:
        sys.stdout.write(f'{a} - {mapper[a]}\n')
        sys.stdout.flush
    file.close()
    # Dicionário [periodo,lista alfabetica dos títulos das obras]
    file = open("results/result3.txt", "w")
    sys.stdout = file
    composers = periodComposers(db)
    for a in composers:
        sys.stdout.write(f'{a} - {composers[a]}\n')
        sys.stdout.flush()
    file.close()
