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

## 10. Rodada ampla (25/11, 10:30Z) — o que mudou
Mercado: Escrevente 2026 = cadastro de reserva, interior + RMSP (2ª–10ª RAJ), taxa R$ 81, inscrições até 10/12, prova 14/03/2027, Vunesp, salário R$ 6.782 (B, Estratégia). Inscritos: 103.554 em 2023 (A via Direção, Vunesp); ~132 mil em 2025 (B). Mercado grande; não é falta de comprador.
Preço da concorrência (lido nas páginas): Opção digital R$ 42,53 (338 p.); Nova Concursos R$ 81 (454 p.); apostilatjsp R$ 34/54; Hotmart apostila 730 p. (preço não exibido); NEAF combo R$ 998; Qconcursos grátis com 10 questões. O nosso a R$ 27–37 é o mais barato: preço não é a barreira, confiança e marca são.
Afiliado comparado: Nova Concursos paga 20% (R$ 16 por venda de R$ 81) e só cita divulgação grátis. Pior que produto próprio (R$ 31 líquido a R$ 37). Afiliado descartado.
CPM revisado: infoproduto/educação R$ 8–35 (C, VT Group), R$ 18–32 no feed (C, Trafius), R$ 18–28 no 1º tri (C, Maximizy). Abaixo dos R$ 38 que usei. Sazonalidade (C, Trafius): Black Friday até +70%, dezembro +40–60%, fevereiro é o mais barato do ano.
Conversão de página de infoproduto: 1,5–2% (C, VT); 2–5% low ticket (C, sem fonte).
Conta refeita a CPM R$ 25 (dez cobra mais): R$ 263,55 → ~10.500 impressões → 105–210 cliques → 2–4 vendas → R$ 70–140 líquidos. Empate segue pedindo 8–9 vendas. Chance ~10–15%.
Conta nova na Meta: limite inicial relatado de US$ 50–150/dia (R$ 280–850) e verificação de identidade para alguns objetivos (C, afiliados); não trava teste de R$ 26/dia.
Conector oficial: exige permissões ads_mcp_management + ads_management; não há restrição de país documentada (A, Meta).
MUDANÇA DE JANELA (decisão minha, conta acima): 01–10/12 pega CPM de dezembro (+40–60%). Inscrito confirmado continua comprando material até a prova. Janela melhor: 05/01–14/02/2027, com CPM mais baixo e comprador já inscrito (comprometido). Dezembro só se ele quiser velocidade.
Google Pesquisa: maior intenção; volume e CPC não verificados (Planejador exige conta). Segundo teste, se o primeiro der sinal.

## 11. O método completo do autor (25/11, 10:45Z): 10 posts lidos + site da agência + regras oficiais
Quem ele é: dono de agência de tráfego com automação de WhatsApp e CRM. O site diz que cobra R$ 1.500–5.000/mês por cliente, pede verba mínima de R$ 1.500/mês, tem 94 clientes e R$ 1,25 mi em mídia gerida (números do próprio site, C). Vende também a mentoria "Método SVA" (preço não público). Os posts "Visão tropa" são topo de funil da mentoria e da agência. O dinheiro dele vem de cliente e de aluno.

### O que cada linha dos posts quer dizer
| Linha do post | O que é na prática | Nós |
|---|---|---|
| "Campanha 1-1-1 full adv" | 1 campanha, 1 conjunto, 1 anúncio, tudo Advantage+ (público e posicionamento automáticos). Vários 1-1-1 no orçamento mínimo para testar criativo sem a Meta concentrar a verba num só | Adotar |
| "Não manja? começa com 10zão" / "200 por produto já brinca" | R$ 10/dia; R$ 200 por produto testado. Mínimo técnico da Meta: mensagens R$ 6/dia, conversão R$ 6–10/dia (C, Trafius) | Bate com o teto de R$ 300 |
| "Criativo low ticket é imagem" / "imagem com preço qualifica melhor" / "vídeo: clique mais caro, lead melhor" | Começar por imagem estática com o preço escrito; vídeo depois | Adotar |
| "Analisa os campeões na biblioteca; bota o Claude pra analisar os seus e dos concorrentes" | Biblioteca de Anúncios + análise dos que rodam há meses | Já fazemos |
| "Tá duro é wpp" / "lead chegou? manda áudio, conversa" / "vendeu? reinveste" | Anúncio de clique para o WhatsApp e fechamento por conversa humana; receita volta para o anúncio | Nova forma do T3 (D1) |
| "Tem caixa é site, VSL, funil interativo" | Página, vídeo de vendas e quiz com pixel; precisa de mais verba para a Meta aprender | Nossa forma antiga (Kiwify), fica para depois |
| "Sem pixel você me quebra" / "instala Clarity e analytics" | Pixel + Microsoft Clarity (grátis: mapa de calor e gravação de sessão) | Adotar quando houver página |
| "19,90 não paga nem os anúncios" / "Black tá osso" | Ticket baixo não paga o clique; CPM sobe até 70% na Black Friday | Confirma a nossa conta |
| "Acertou? Leva pra outro país" | Repetir o vencedor em outro mercado. CPM mediano de e-commerce: Brasil US$ 2,63 (R$ 14,86), México US$ 3,92, Colômbia US$ 2,00 (Lebesgue via Pace, jul/2026) | Só produto universal; o caderno do TJSP não viaja |
| "Oferta: Etsy + biblioteca de anúncios" | Produto digital que já vende lá fora (selo de mais vendido, avaliações) + conferir se já roda anúncio dele no Brasil | Fila |
| "Conteúdo infinito... monetiza com view ou produto" / "Canal dark deixa rico mas demora" | Vídeo de IA em massa em 4 redes | Já testamos: ~500 vídeos em 4 meses, R$ 0. O YouTube desmonetiza conteúdo "inautêntico" feito em massa desde 15/07/2025 (B) |
| "Vender serviço entregar com IA" / "pack pra empresa no zap" / "site com Lovable" / "arte com GPT" | Vender serviço | Exige vender; ver forma 4 |
| "Claude é no opus low" | Modelo forte com pouco raciocínio para economizar limite | Para a rotina de anúncio, Sonnet basta |

### O que fica de fora (regra 7 de DINHEIRO.md), com o motivo
- Comprar conta Veo na G2G / abrir e-mails para ganhar crédito grátis: viola os termos do Google, e conta comprada pode ser roubada ou derrubada. Desnecessário: o Google AI Ultra dá 10.000–25.000 créditos/mês no Flow; no Ultra, o Veo 3.1 Fast custa 10 créditos, o que dá 1.000+ vídeos/mês (C, WaveSpeed resumindo o Google; o Fast e o Quality saem do Flow em 05/12/2026).
- Chip virtual (HeroSMS, a partir de US$ 0,01) e vários WhatsApp em perfis de Android: número virtual vem de pool compartilhado; o WhatsApp bane, e o histórico some sem aviso. 6,8 milhões de contas banidas no 1º semestre de 2025; bloqueio maior a ferramentas não autorizadas desde 15/01/2026 (B, Estado de Minas, 02/2026).
- Comprar BM verificada / "3 contas de anúncios" para fugir de bloqueio: a Meta notificou parceiros por "aluguel de acesso a contas confiáveis" que ajudavam a burlar a fiscalização (A, Meta, 02/2026). Um banimento derruba tudo o que está ligado ao perfil do operador.
- Usar no anúncio o vídeo viral de outra pessoa: viola direito autoral e a política de anúncios da Meta (A).
- Robô (Playwright) no Gerenciador de Anúncios: automação de interface é violação. Caso público de 2026: portfólio inteiro banido sem recurso cerca de 1 semana depois de um agente com permissão de escrita (B, Porter e Supermetrics). Limite da Meta desde maio/2026: 4 mudanças de orçamento por conjunto por hora e 10 mudanças de limite de gasto por dia (B). Playwright só para leitura (Biblioteca, TikTok), nunca no Gerenciador.
- Uazapi: a documentação confirma conexão por QR Code ou código de pareamento e disparo de campanha com intervalo configurável (A, docs.uazapi.com). É API não oficial: fora do número de venda.
- GGMAX/G2G (conta e item de jogo): viola os termos dos jogos; há queixas de saldo retido e de banimento no Reclame Aqui.

### WhatsApp: regras oficiais e números
- Oficial (A, Meta): conversa iniciada por anúncio de clique para o WhatsApp abre janela de 72 h em que toda mensagem é grátis; mensagem de atendimento (sem modelo) é grátis. O app WhatsApp Business, que é grátis, cria o anúncio em Ferramentas → Anunciar, com saudação, mensagem de ausência e catálogo.
- IA no WhatsApp: IA de uso geral proibida na API desde 15/01/2026; IA do próprio negócio (qualificar, agendar, vender) é permitida (B, respond.io).
- Custo por conversa (C, salvo indicação): educação R$ 5–15 (MessageCentral, sem fonte); clínicas mediana ~R$ 10, metade das contas entre R$ 8 e R$ 12, máximo R$ 25 (dezenas de contas, abr–jul/2026, B-, Eduardo Stopa); caso da agência do autor R$ 2,33.
- Conversa → venda: educação 8–18% e beleza 25–40% (C, MessageCentral); 9% em média em 2021 (C, OmniChat, sem método). Velocidade de resposta decide: responder em 2 min converte muito mais que em 2 h (B-).

### As formas de aplicação, por chance de se pagar (R$ 300 = R$ 263,55 de entrega)
| Forma | Conta | Chance de se pagar | Quem paga o pedágio |
|---|---|---|---|
| D1. Caderno TJSP por WhatsApp: 3 × 1-1-1 de imagem com preço → conversa → Pix direto (sem taxa da Kiwify) | R$ 5–12 por conversa → 22–53 conversas → 8–18% fecham → 2–9 vendas a R$ 37 → R$ 65–350. No meio: ~4 vendas, R$ 146. Empatar pede 9 vendas | ~15% (10–20%), estimativa minha | Operador responde em minutos, 20–40 min/dia, com roteiro e áudios que eu escrevo |
| D2. Negócio local de serviço que o operador possa usar como caso (agendamento por WhatsApp, raio de 3–5 km, imagem com preço) | R$ 3–8 por conversa → 33–88 conversas → 15–30% agendam → 5–26 clientes. Exemplo de ticket em beleza: alongamento em gel R$ 120–250, manutenção R$ 80–160 a cada 20–30 dias (Catraca Livre, valores de 2025) | Alta (~60%; entradas C) | Quem toca o negócio atende e precisa ter agenda livre |
| D3. Página na Kiwify (forma antiga) | 2–4 vendas, R$ 70–140 | ~10–15% | Menos tempo do operador |
| 4. Serviço de tráfego para negócio local (o que o autor vende) | Iniciante cobra R$ 500–1.500/mês por cliente (C). Agências: 44% fecham até 5 clientes recorrentes por ano e 14% nenhum; 28% dos clientes vêm de indicação e 20% de prospecção (RD Station 2026, n = 349/713) | Depende de ter caso | Vender; D2 gera o caso |

Desenho do D1: 3 conjuntos 1-1-1 (Engajamento → WhatsApp → maximizar conversas) a R$ 8,70/dia cada; 3 imagens com preço (questões Vunesp comentadas; plano de 15 semanas até a prova; preço contra o concorrente); Advantage+ no estado de SP. WhatsApp Business num número próprio (chip real, usado normalmente por 1 semana antes); saudação + catálogo + respostas rápidas; 2–3 áudios gravados uma vez pelo operador; Pix direto; PDF entregue na conversa; planilha de conversas e vendas. Programação de horário só existe com orçamento total: usar orçamento total com veiculação nos horários em que ele responde. Regras: com R$ 80 de entrega, pausar conjunto com custo por conversa acima de R$ 15; com R$ 130 e até 2 vendas, parar tudo; continuar só se vendas × preço ≥ depósito usado. Janela: 05/01–14/02/2027.
Veredito: o autor ganha com serviço e mentoria. A parte replicável do método é 1-1-1 + imagem com preço + WhatsApp com fechamento humano + reinvestir. D1 melhora a chance do caderno de ~10% para ~15%, mas ainda não deve pagar os primeiros R$ 300. D2 é a única forma com chance alta de se pagar, e gera o caso que a forma 4 exige.
