# Revisão independente (substitui a aprovação humana)

Quem escreve o roteiro NÃO revisa. Um agente separado, sem ter visto o processo de escrita, lê o spec e responde APROVADO ou REPROVADO com motivos. Só vai para `specs/queue/` o que foi APROVADO.

## Reprovar se houver qualquer um destes
1. **Fato sem fonte**: número, data ou afirmação que não vem de um dado carregado automaticamente (FRED etc.) ou de uma fonte citada na descrição. Em canais de explicação (B), toda afirmação técnica precisa ser conferível em fonte primária ou livro-texto; na dúvida, cortar a frase.
2. **Opinião de política, eleição, religião, saúde ou investimento** apresentada como fato ou recomendação. Nunca dar conselho financeiro ou médico.
3. **Alegação enganosa**: causa afirmada onde só há correlação; escala de gráfico que distorce; dado nominal tratado como real sem aviso.
4. **Diretrizes do YouTube**: violência gráfica, assédio, desinformação médica/eleitoral, conteúdo para menores, marcas registradas de terceiros, música ou imagens sem licença.
5. **Conteúdo repetitivo/genérico**: mesma estrutura e mesmas frases de um vídeo recente do canal sem dado ou ângulo novo. Cada vídeo precisa de um dado ou explicação própria.
6. **Metadados**: título clickbait que a entrega não cumpre; descrição sem fonte; falta de aviso de narração sintética.
7. **Afiliado (canal C)**: sem aviso de link de afiliado; preço ou especificação sem fonte e data; comparação de produto que o texto não sustenta.

## Formato da resposta do revisor
`APROVADO` ou `REPROVADO`, seguido de lista numerada de problemas com a frase exata e a correção.
