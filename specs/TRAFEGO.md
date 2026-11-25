# TRÁFEGO PAGO — estudo de 25/11/2026

Meta do operador: entender por completo o que o vídeo "Visão sobre Claude" descreve e responder "aplicar tráfego pago de tal forma? Como é, de qual forma".
Ler junto com specs/DINHEIRO.md (prompt da máquina). Graus de fonte: A = oficial/primária, B = imprensa ou praticante com método, C = vendedor ou estimativa sem método. Câmbio: R$ 5,65 por US$.

## 0. Resposta curta
- Como é: quem ganha com "Claude + Meta Ads" compra público no leilão da Meta e usa IA para baratear o que era caro (pesquisa de concorrente, página, criativo em volume, leitura diária dos números). A IA não cria comprador nem melhora a conta: oferta e ticket médio decidem.
- De qual forma cabe aqui: produto próprio, venda direta, como teste medido de R$ 300 (forma 1 da seção 5). A forma em que perfis como o do vídeo ganham é serviço (gerir anúncio dos outros), que exige conseguir cliente e ter resultado para mostrar; hoje não temos nenhum dos dois.
- Chance de os primeiros R$ 300 se pagarem: cerca de 10% (faixa 5–15%, estimativa minha; conta na seção 4). Retorno esperado desses R$ 300: R$ 50–130. O que eles compram com certeza é medição real do nosso nicho e a máquina montada.

## 1. O vídeo, item por item
| Item do vídeo | Para que serve numa operação de anúncio | Custo verificado | Já temos? |
|---|---|---|---|
| "Plano de 110" | Quase certo que é o Claude Pro: lançado no Brasil a R$ 110/mês em ago/2024 (B, SSD Nodes); hoje US$ 20 (R$ 113). Acima: Max US$ 100 (R$ 565) e Ultra US$ 200 (R$ 1.130) (A, página de preços do Claude). O recado do vídeo é "o plano barato dá conta", por isso o "Opus no low" | R$ 110–113/mês | O operador já usa Claude |
| Antigravity (Google) | Ambiente de agentes com navegador e subagentes; os planos pagos do Google AI incluem modelos Claude (A, página de preços do Antigravity). Cota semanal; foi reduzida várias vezes entre dez/2025 e mar/2026 (B) | Incluso no plano Google AI | Disponível ao operador |
| Playwright / "controla o navegador" | Operar telas como humano | Grátis | Sim (navegador do operador, de dia) |
| Obsidian | Memória em arquivos de texto | Grátis | Sim (este repositório) |
| Imagem da OpenAI por API | Criativo estático em volume. Tabela lida: US$ 0,009–0,133 por imagem (C; a versão "2.6" citada no vídeo não foi confirmada) | até ~R$ 0,75 por imagem | Motor próprio de vídeo + geração do Google AI |
| Higgsfield / Segmind por API | Vídeo de IA sem assinatura. Higgsfield: Kling 3.0 720p a US$ 0,084/s, ~US$ 0,67 (R$ 3,79) por clipe de 8 s; assinaturas do site de US$ 15 a 129/mês (A, blog da Higgsfield). Segmind: pré-pago a partir de US$ 10 (A) | ~R$ 4 por clipe | Não precisa para começar |
| Uazapi | WhatsApp por API (chave + ID de instância) para atender e recuperar venda. Não achei fonte primária dizendo se é a API oficial da Meta; o modelo "instância" é o das APIs que conectam o número por sessão. Tratar como NÃO oficial (risco de banimento do número) até prova em contrário | não verificado | Não usar |
| ScrapingDog / Apify | Raspar a Biblioteca de Anúncios para achar o que roda há meses. Apify: US$ 0,70–0,75 por 1.000 anúncios; plano grátis dá US$ 5/mês (A) | Grátis no nosso volume | Leitura pelo navegador já resolveu (23/11) |
| "Opus no low" | Gastar menos limite em tarefa simples | — | Rotina de anúncio roda em Sonnet |
| "Treina com muitos dados" | Dar contexto (anúncios vencedores, números da conta). Não é treino de modelo | — | Sim |

Leitura: o vídeo lista ferramentas, não um modelo de negócio. Quase tudo já existe aqui. Falta o que nenhuma ferramenta dá: conta de anúncio com saldo, oferta que converte e conta que fecha.

## 2. Como o tráfego pago funciona (Meta, Brasil, 2026)
- Leilão: vence o maior valor total = lance × taxa estimada de ação + qualidade do anúncio (A, Meta). Criativo melhor paga menos pelo mesmo público.
- Andromeda (A, blog de engenharia da Meta, 02/12/2024): o sistema recupera e escolhe o anúncio pelo próprio criativo; segmentação manual perdeu peso. Prática atual (C): 1 campanha, poucos conjuntos, público aberto, 4–8 criativos realmente diferentes em ângulo e formato.
- Fase de aprendizado (B, Lebesgue citando a Meta): ~50 eventos de otimização em 7 dias por conjunto; mudar orçamento em mais de 20%, público ou criativo reinicia. Regra prática: verba diária ≈ custo por compra × 50 ÷ 7. Com R$ 26/dia o conjunto fica em "aprendizado limitado" o teste inteiro. Serve para ler sinal, não para otimizar.
- Imposto (A, comunicado oficial da Meta): desde 01/01/2026 a Meta repassa PIS/Cofins 9,25% + ISS 2,9% = 12,15%. Pré-pago (Pix/boleto): sai do saldo; R$ 1.000 depositados viram R$ 878,50 de entrega. Cartão: R$ 1.000 de entrega custam R$ 1.138,30. O Gerenciador mostra valores sem imposto.
- Rastreamento: pixel + API de Conversões. Kiwify (A, central de ajuda): até 50 pixels por produto; InitiateCheckout dispara ao abrir o checkout; Purchase dispara na compra aprovada por cartão; o artigo (2024) não diz o que acontece no Pix. Até 5 ofertas extras no checkout por produto (A). Meta: quem usa a API de Conversões na web teve custo por resultado 17,8% menor (A, 15/04/2026).
- Referências de custo: não existe benchmark oficial do Brasil. Global 2025 (B, Triple Whale via Influee, ~35 mil contas): CPM US$ 14,19, CTR 2,19%, conversão 1,60%, custo por compra US$ 38,19. Brasil, infoprodutos (C, Trafius, sem método): CPM R$ 38 (28–60), CPC R$ 3,20–8,00. Verba de teste sugerida por praticantes (C): R$ 30–60/dia com 2–4 criativos.
- Calendário: CPM costuma subir no 4º trimestre e ter pico na semana da Black Friday (27/11/2026) (C, padrão de mercado, sem número local).

## 3. Como os operadores juntam IA e anúncio
1. Pesquisa: Biblioteca de Anúncios. O que roda há meses é o que se paga.
2. Oferta e página: IA escreve; humano decide preço e promessa.
3. Criativo em volume: imagem e vídeo por API, ângulos diferentes.
4. Subida da campanha pelo conector oficial: conectores de IA da Meta em beta aberto desde 29/04/2026, para Claude e ChatGPT (B, PPC Land); servidor em https://mcp.facebook.com/ads (A, blog de desenvolvedores da Meta, 16/07/2026). No Claude: Personalizar → Conectores → adicionar conector personalizado com essa URL → login do Facebook → escolher os portfólios. ~29 ferramentas: relatórios, anomalias, comparativos, erros de entrega, saúde do pixel; criar e editar campanha, conjunto e anúncio. O que o conector cria nasce PAUSADO e é ativado no Gerenciador (B, Jon Loomer).
5. Rotina: puxar 7 dias de dados, marcar criativo cansado (CTR mais de 15% abaixo do pico, frequência acima de 3,5), pausar e trocar. Praticantes rodam isso por script de hora em hora com regra de pausa por custo por compra (C, Vini Ensina; sem caso identificado).
6. Recuperação: e-mail/WhatsApp para Pix gerado e não pago.
Outras rotas: conectores de terceiros só de leitura (Porter, Reportei, Windsor, Supermetrics); servidor comunitário da Pipeboard (US$ 49/mês hospedado ou grátis local com token; 25 ferramentas; não é da Meta) (C). Agente Manus dentro do Gerenciador desde 17/02/2026 (C, Porter; não conferido na Meta).
Riscos documentados: relatos de contas derrubadas ligadas a integrações de IA não aprovadas e erros de escrita (B, Jon Loomer). O risco vem de escrita em escala, rajadas de chamadas, mudança rápida de orçamento e robô operando a tela do Gerenciador; leitura é segura (C, Porter). API não oficial de WhatsApp leva a banimento do número.
Resultado alegado: 90% menos tempo operacional e +15% de ROAS (caso de cliente da Anthropic citado por terceiro; método não descrito). O resto são exemplos sem fonte. Ninguém mostra IA transformando oferta fraca em lucro.

## 4. A conta que decide
Tráfego se paga quando: líquido por pedido × conversão do clique > custo do clique × 1,1383.
- Kiwify (B, guia HeroSpark conferido nas páginas oficiais em 06–07/07/2026): 8,99% + R$ 2,49 por venda aprovada, em qualquer meio; saque R$ 3,67. Líquido: R$ 27 → R$ 22,08; R$ 37 → R$ 31,18; R$ 47 → R$ 40,28.
- Custo máximo por venda mostrado no Gerenciador (líquido × 0,8785): R$ 19,40 a R$ 27; R$ 27,39 a R$ 37; R$ 35,39 a R$ 47.
- R$ 300 por Pix → R$ 263,55 de entrega. A CPM de R$ 38: ~6.900 impressões. Cliques: 70–140 se o clique no link ficar em 1–2%; 33–82 se o CPC for o da estimativa brasileira (R$ 3,20–8,00).
- Vendas esperadas a 1,6–3% de conversão: 1–4 (zero é possível). Receita líquida esperada: R$ 50–130.
- Para empatar os R$ 300: 14 vendas a R$ 27, 10 a R$ 37 ou 8 a R$ 47. Isso pede 6–20% dos cliques comprando; a mediana global é 1,6%.
- Chance de empatar no primeiro lote: ~10% (5–15%), estimativa minha. Em 23/11 eu disse 20–30%; estava alto.
- Quem roda há meses no nicho (710 anúncios ativos em 23/11) cobra R$ 34–895 e empilha oferta extra. O lucro está no ticket médio e na recompra, não na primeira venda.

## 5. As três formas de aplicar
| Forma | Quem arrisca a verba | O que exige | Leitura |
|---|---|---|---|
| 1. Produto próprio, venda direta | O operador | Oferta forte + capital para testar | Única que cabe sem conversa de venda. R$ 300 = medição |
| 2. Afiliado com anúncio | O operador | Igual, com produto de terceiro | Mesma conta, comissão menor que o preço, zero controle da página |
| 3. Gestão de tráfego para terceiros | O cliente | Conseguir cliente e ter resultado para mostrar | Onde o autor do vídeo e parecidos ganham. Honorário (C, três tabelas sem método): R$ 500–1.500 por cliente para iniciante; R$ 1.500–2.500 para conta de até R$ 5 mil de verba. 5 clientes a R$ 2.000 = R$ 10 mil. Sem caso próprio, não vende |

## 6. Plano para o nosso caso (teste T3, só com o "sim" do operador)
Prazo do produto: inscrições do Escrevente TJSP até 10/12/2026; prova em 14/03/2027. Depois da prova o caderno vale zero. Janela útil: ~15 semanas.
Montagem (R$ 0, 25–30/11):
- Operador (~1 h, uma vez): conta Kiwify; página do Facebook, portfólio empresarial e conta de anúncios pré-paga; pixel e token da API de Conversões colados na Kiwify por ele; conector da Meta adicionado no Claude; depósito de R$ 300 por Pix; ativar a campanha pausada.
- Eu: auditar o PDF contra o Edital 02/2026; reforçar a oferta até encostar no concorrente (700 questões + 3 simulados por R$ 34–54) com preço de R$ 37 e 1 oferta extra de R$ 17–19; página; 6 criativos (3 ângulos × vídeo e imagem); campanha criada pausada; relatório diário com números.
Teste (01–10/12, pega o fim das inscrições): 1 campanha de vendas, 1 conjunto, estado de SP, 18–45 anos, público aberto, otimização para compra, R$ 26/dia de entrega.
Regras escritas antes:
- Não mexer nos 3 primeiros dias.
- Pausar criativo com 1.500 impressões ou mais e clique no link abaixo de 0,8%.
- Com R$ 130 de entrega e 0–2 vendas: parar no mesmo dia; o saldo restante fica na conta.
- Continuar só se o custo por venda no Gerenciador ficar em até 88% do líquido médio por pedido; a partir daí só reinveste receita.
Mede: CPM, clique no link, custo por clique, clique → checkout, checkout → compra, Pix gerado × pago, aceite da oferta extra.
Limites meus: não digito cartão, Pix nem CPF; não ativo gasto; pauso por regra só com o "sim" dele para este teste; não opero a tela do Gerenciador por robô; não uso WhatsApp não oficial nem disparo em massa; nada de "aprovação garantida".

## 7. O que ficou sem verificar (resolve na montagem ou no teste)
Depósito mínimo por Pix; se a Kiwify dispara a compra no Pix gerado ou no pago; se o conector da Meta está liberado na conta dele; limite diário e análise de identidade de conta de anúncios nova; preço e natureza da Uazapi; CPM, clique e conversão reais do nosso nicho; devolução de saldo pré-pago não usado.

## 8. Fontes
- Imposto: https://www.reformatributaria.com/wp-content/uploads/2025/09/Comunicado-oficial-Meta.pdf · https://viniensina.com.br/?p=3172
- Conector oficial: https://developers.facebook.com/blog/post/2026/07/16/meta-ads-mcp-server/ · https://ppc.land/meta-opens-its-ad-system-to-claude-and-chatgpt-with-new-ai-connectors/ · https://www.jonloomer.com/meta-ads-ai-connectors/amp/
- Andromeda: https://engineering.fb.com/2024/12/02/production-engineering/meta-andromeda-advantage-automation-next-gen-personalized-ads-retrieval-engine/
- Aprendizado: https://lebesgue.io/blog/facebook-ads-learning-phase/
- Benchmarks: https://influee.co/br/blog/facebook-ads-benchmarks · https://trafius.com.br/blog/orcamento-minimo-diario-meta-ads-brasil-2026 · https://viniensina.com.br/orcamento-minimo-meta-ads-2026/
- Kiwify: https://help.kiwify.com/en/article/how-to-set-up-the-facebook-pixel-1oxa7i0/ · https://herospark.com/guias/taxas-e-margem
- IA + anúncio: https://viniensina.com.br/gestor-de-trafego-com-ia-automatizar-meta-ads/ · https://portermetrics.com/pt/tutorial/claude/chat-meta-ads/ · https://dev.to/rupa_tiwari_dd308948d710f/how-to-automate-meta-ads-with-claude-ai-and-mcp-real-workflows-real-results-m9o
- Honorários: https://www.freelasemcrise.com.br/quanto-cobrar/gestao-trafego-pago-meta · https://trafius.com.br/blog/preco-de-gestor-de-trafego-em-2026-tabela-por-porte
- Ferramentas: https://www.ssdnodes.com/learn/lang/pt/claude-pro-in-brazil-what-you-pay · https://higgsfield.ai/blog/ai-video-api-pricing-vs-subscriptions · https://apify.com/curious_coder/facebook-ads-library-scraper/pricing · https://market.lobehub.com/s/plugins/pabloweyne-uazapi-mcp

## 9. Comparação ampla e automação total (25/11, 10Z)
| Caminho | Automação | Comparado ao nosso | Veredito |
|---|---|---|---|
| Stack do vídeo (Claude + APIs + navegador) | Alta na execução | Igual ao que temos | Nada a comprar |
| IA nativa da Meta (Advantage+, Creative Studio, agente MAIBA) | Segmentação, criativo e verba já automáticos; criação conversacional "em breve" | Faz de graça parte do que o vídeo vende; ganho declarado ~5% mais conversões (A, Meta, out/2026) | Usar: Advantage+ de vendas como padrão do T3 |
| Conector oficial (MCP) | Cria/edita, tudo pausado | Meta diz que mira grandes anunciantes e agências | Tentar; se não liberar, eu preparo e ele sobe pelo Gerenciador |
| Google Pesquisa | Manual/semiautomático | Captura quem já busca "apostila escrevente tjsp" (intenção maior); CPC não verificado | Candidato melhor que Meta para concurso; testar só depois, não dividir R$ 300 |
| Ferramentas pagas de terceiros (Pipeboard etc.) | Alta | Redundante | Não |
Sincero: automação total do trabalho é possível (eu faço pesquisa, produto, página, criativos, campanha pausada, relatório e regra de corte). Automação total do dinheiro não existe: conta, depósito e ativação são dele, e o resultado depende de oferta. Quanto mais a Meta automatiza, menos a ferramenta diferencia; só oferta e criativo diferenciam.
