# TPC3 : Conversor de MarkDown para HTML

## 2025-02-27

### David Filipe Rocha Figueiredo - A104360

![fotoPerfil](../images/DavidFilipeRochaFigueiredoSMALL.png)

## Resumo

- Pretende-se que o programa converta um ficheiro MarkDown para um ficheiro HTML.
- Foram utilizadas expressões regulares para a resolução do problema.
- As conversões implementadas foram referentes a tags de negrito, itálico,
headers, lsitas numeradas, listas não numeradas, imagens e links textuais.
- A implementação passa por uma leitura total do ficheiro, seguida por uma
série de substituições para cada conversão, excepto para as listas, que passam por
uma separação do texto com o caractér '\n', e construção iterativa das listas em
HTML.

### Lista de Resultados

- [Ficheiro markdown](results/index.md)
- [Ficheiro convertido em HTML](results/index.html)
