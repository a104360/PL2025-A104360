# TPC3 : Conversor de MarkDown para HTML

## Data : 2025-02-27

## Autor

- David Filipe Rocha Figueiredo
- A104360

<img src="../images/DavidFilipeRochaFigueiredo.png" width="200px" alt="fotoPerfil">

## Resumo

- Pretende-se construir um analisador léxico para uma liguagem de query com a
qual se podem escrever frases do género:

```code
# DBPedia: obras de Chuck Berry 
select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000
```

- Para a resolução do exercício, recorreu-se ao módulo python ply.lex, que permite
a criação de tokens e regras de separação, tratemento de erro e caracteres ilegais.

### Lista de Resultados

- [Ficheiro com resultados para análise léxica](result1.txt)
