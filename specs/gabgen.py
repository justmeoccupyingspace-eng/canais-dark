"""Specs v3 do Gabarito do Dia (TikTok/Reels, PT-BR): quiz com mascote. Uso: python3 specs/gabgen.py -> specs/v3/c-3xx-*.json
Sem WhatsApp e sem preço no vídeo (assim todo vídeo pode ser promovido); a venda fica na legenda e na bio."""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v3')
os.makedirs(OUT, exist_ok=True)
TAGS = '#concursotjsp #escreventetjsp #concursopublico #vunesp #concurseiro'


def q(name, label, hook_text, hook_hl, hook_icon, hook_n, question, alts, letter, q_n, ans_text, ans_hl, ans_sub, ans_icon, ans_n, tags, caption, qsize=50, asize=42):
    correct = 'ABCDE'.index(letter)
    spec = {
        'channel': 'gabarito', 'style': 'v3', 'rate': '+4%', 'title': hook_text,
        'publish': {'channel': 'C', 'privacy': 'public'},
        'tiktok': f"{caption} Comenta a letra! Apostila com 182 questões comentadas: amostra grátis no WhatsApp da bio.\n{TAGS} {tags}",
        'scenes': [
            {'type': 'hook', 'kicker': 'Escrevente TJSP · VUNESP', 'text': hook_text, 'hl': hook_hl, 'icon': hook_icon, 'narration': hook_n, 'min_duration': 2.6},
            {'type': 'quiz', 'label': label, 'q': question, 'alts': alts, 'correct': correct, 'narration': q_n, 'extra': 4.6, 'revealFromEnd': 1.6, 'countdown': 3, 'qsize': qsize, 'asize': asize},
            {'type': 'text', 'text': ans_text, 'hl': ans_hl, 'sub': ans_sub, 'icon': ans_icon, 'pose': 'cheer', 'narration': ans_n, 'min_duration': 3.6},
            {'type': 'end', 'text': 'Siga: 1 questão do TJSP por dia', 'hl': '1 questão', 'brand': 'GABARITO DO DIA', 'narration': 'Siga o Gabarito do Dia e treine uma por dia.', 'min_duration': 2.2},
        ],
    }
    json.dump(spec, open(f'{OUT}/{name}.json', 'w'), ensure_ascii=False, indent=1)
    return name


V = []
V.append(q('c-301-sequencia', 'RACIOCÍNIO LÓGICO · SEQUÊNCIAS', 'Qual é o 10º número?', '10º número?', '🔢',
           'Raciocínio lógico do concurso do TJ. Descobre o padrão?',
           'Sequência: 2, 3, 5, 8, 12, 17, ... Mantido o padrão, o 10º termo é:', ['38', '45', '47', '55', '57'], 'C',
           'Dois, três, cinco, oito, doze, dezessete. Qual é o décimo termo?',
           'Letra C: 47', '47', 'as diferenças crescem: +1, +2, +3, +4...', '🧠',
           'Letra C, quarenta e sete. As diferenças crescem de um em um: mais seis, mais sete, mais oito, mais nove. O trinta e oito é só o nono termo.',
           '#raciociniologico', 'Raciocínio Lógico do Escrevente TJSP: qual é o 10º termo?'))
V.append(q('c-302-calendario', 'RACIOCÍNIO LÓGICO · CALENDÁRIO', 'Que dia da semana caiu o dia 20?', 'dia 20?', '📅',
           'Essa questão de calendário derruba muita gente no TJ.',
           'Um mês de 31 dias teve cinco sextas, cinco sábados e cinco domingos. O dia 20 caiu em uma:', ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira'], 'C',
           'Um mês de trinta e um dias teve cinco sextas, cinco sábados e cinco domingos. O dia vinte caiu em que dia?',
           'Letra C: quarta-feira', 'quarta-feira', 'dia 1 = sexta · dia 20 = 19 dias depois', '🗓️',
           'Letra C. Os três dias que se repetem cinco vezes são os dias um, dois e três. Então o dia um foi sexta. Somando dezenove dias, cai numa quarta.',
           '#raciociniologico', 'Raciocínio Lógico do Escrevente TJSP: que dia caiu o dia 20?'))
V.append(q('c-303-juros', 'MATEMÁTICA · JUROS SIMPLES', 'R$ 4.000 a 3% ao mês. Quanto vira?', 'Quanto vira?', '💰',
           'Juros simples no concurso do TJ. Quanto vira esse dinheiro?',
           'R$ 4.000,00 a juros simples de 3% ao mês, por 4 meses. O montante final é:', ['R$ 480,00', 'R$ 4.120,00', 'R$ 4.360,00', 'R$ 4.480,00', 'R$ 4.502,04'], 'D',
           'Quatro mil reais, a juros simples de três por cento ao mês, durante quatro meses. Qual é o montante?',
           'Letra D: R$ 4.480', 'R$ 4.480', 'juros = 4.000 × 0,03 × 4 = 480', '📈',
           'Letra D. Os juros são quatrocentos e oitenta, e o montante soma o capital: quatro mil quatrocentos e oitenta. Quem marcou quatrocentos e oitenta caiu na pegadinha.',
           '#matematica', 'Matemática do Escrevente TJSP: juros simples.'))
V.append(q('c-304-nato', 'CONSTITUCIONAL · ART. 12', 'Só brasileiro nato pode ser...', 'brasileiro nato', '🇧🇷',
           'Qual desses cargos só um brasileiro nato pode ocupar?',
           'Segundo a Constituição Federal, é privativo de brasileiro nato o cargo de:', ['Ministro do STJ', 'Presidente da Câmara dos Deputados', 'Ministro da Justiça', 'Senador da República', 'Procurador-Geral da República'], 'B',
           'Segundo a Constituição, qual destes cargos é privativo de brasileiro nato?',
           'Letra B: Presidente da Câmara', 'Presidente da Câmara', 'CF, art. 12, § 3º', '🏛️',
           'Letra B. O presidente da Câmara está na linha de sucessão da Presidência, por isso precisa ser nato. Senador, ministro do STJ e procurador-geral, não.',
           '#direitoconstitucional', 'Constitucional do Escrevente TJSP: cargo privativo de brasileiro nato.', asize=38))
V.append(q('c-305-regradetres', 'MATEMÁTICA · REGRA DE TRÊS', '8 servidores, 18 dias. E com 12?', 'E com 12?', '👥',
           'Regra de três do concurso do TJ. Cuidado com a pegadinha.',
           '8 servidores digitalizam um arquivo em 18 dias. No mesmo ritmo, 12 servidores levarão:', ['12 dias', '14 dias', '22 dias', '27 dias', '30 dias'], 'A',
           'Oito servidores fazem o serviço em dezoito dias. Com doze servidores, quantos dias?',
           'Letra A: 12 dias', '12 dias', 'mais gente, menos dias: 8 × 18 = 12 × 12', '⚖️',
           'Letra A, doze dias. É inversamente proporcional: oito vezes dezoito dá cento e quarenta e quatro, dividido por doze dá doze. Quem marcou vinte e sete esqueceu de inverter.',
           '#matematica', 'Matemática do Escrevente TJSP: regra de três inversa.'))
V.append(q('c-306-crase', 'PORTUGUÊS · CRASE', 'Só uma tem a crase certa', 'crase certa', '✍️',
           'Português do concurso do TJ. Onde está a crase certa?',
           'Está correto o emprego do sinal indicativo de crase em:', ['Refiro-me àquelas normas e não à estas.', 'Ficaram frente à frente na sala.', 'Sua leitura é semelhante à do relator.', 'Fomos à Brasília para a audiência.', 'O juiz falou à todos sobre a decisão.'], 'C',
           'Em qual dessas frases a crase está correta?',
           'Letra C: semelhante à do relator', 'à do relator', 'semelhante A + A [leitura] do relator', '✅',
           'Letra C. Semelhante pede a preposição a, e tem um artigo escondido: à leitura do relator. Antes de todos, de estas e de Brasília, não tem crase.',
           '#portugues #crase', 'Português do Escrevente TJSP: onde está a crase certa?', asize=38))
V.append(q('c-307-regencia', 'PORTUGUÊS · REGÊNCIA', 'Assistir O filme ou AO filme?', 'AO filme?', '🎬',
           'Regência verbal: essa cai muito na VUNESP.',
           'De acordo com a norma-padrão, a regência verbal está correta em:', ['Prefiro estudar à noite do que de manhã.', 'Ele aspirava o cargo de chefia.', 'Assistiram à palestra sobre o edital.', 'Obedeceram o horário estabelecido.', 'Esqueci dos documentos em casa.'], 'C',
           'Em qual frase a regência verbal está correta?',
           'Letra C: assistiram à palestra', 'assistiram à', 'assistir (ver) pede a preposição A', '🎯',
           'Letra C. Assistir, no sentido de ver, pede a: assistiram à palestra. Aspirar a, obedecer a, e prefiro uma coisa a outra, sem do que.',
           '#portugues', 'Português do Escrevente TJSP: regência verbal.', asize=38))
V.append(q('c-308-atalhos', 'INFORMÁTICA · WINDOWS', 'Qual atalho está certo?', 'atalho', '⌨️',
           'Informática vale nove questões no TJ. Qual desses atalhos está certo?',
           'No Windows 10 ou 11, a combinação de teclas está correta em:', ['Win+L abre as Configurações', 'Alt+Tab fecha a janela ativa', 'Win+E abre a caixa Executar', 'Win+Shift+S abre o histórico do Ctrl+C', 'Ctrl+Shift+Esc abre o Gerenciador de Tarefas'], 'E',
           'No Windows, qual destes atalhos está associado à função certa?',
           'Letra E: Ctrl+Shift+Esc', 'Ctrl+Shift+Esc', 'Win+L bloqueia · Win+E Explorador · Win+R Executar', '🖥️',
           'Letra E. Control, shift e esc abre direto o gerenciador de tarefas. Windows L bloqueia, Windows E abre o explorador e Windows R abre o executar.',
           '#informatica #windows', 'Informática do Escrevente TJSP: atalhos do Windows.', asize=36))
V.append(q('c-309-kits', 'MATEMÁTICA · MDC', 'Quantos itens em cada kit?', 'cada kit?', '📦',
           'MDC no concurso do TJ. Quantos itens vai ter cada kit?',
           '120 cadernos, 168 canetas e 216 pastas em kits idênticos, sem sobra, com o maior número de kits. Cada kit terá:', ['21 itens', '24 itens', '42 itens', '63 itens', '504 itens'], 'A',
           'Cento e vinte cadernos, cento e sessenta e oito canetas e duzentas e dezesseis pastas, no maior número de kits iguais. Quantos itens por kit?',
           'Letra A: 21 itens', '21 itens', 'MDC = 24 kits → 5 + 7 + 9', '🎁',
           'Letra A. O MDC dá vinte e quatro kits, cada um com cinco cadernos, sete canetas e nove pastas: vinte e um itens. Vinte e quatro é o número de kits, não de itens.',
           '#matematica', 'Matemática do Escrevente TJSP: MDC.', qsize=46))
V.append(q('c-310-demorgan', 'RACIOCÍNIO LÓGICO · NEGAÇÃO', 'Como negar uma frase com "ou"?', '"ou"?', '🔀',
           'Negação com ou. A VUNESP adora essa.',
           'A negação de "A sessão foi adiada ou o relator pediu vista" é:', ['Não foi adiada ou o relator não pediu vista.', 'Foi adiada e o relator não pediu vista.', 'Se foi adiada, o relator não pediu vista.', 'Foi adiada ou o relator não pediu vista.', 'Não foi adiada e o relator não pediu vista.'], 'E',
           'Qual é a negação de: a sessão foi adiada ou o relator pediu vista?',
           'Letra E: não... E não...', 'E não', 'negar "p ou q" = "não p e não q"', '🧩',
           'Letra E. Pra negar o ou, você nega as duas partes e troca por e. A letra A seria a negação de uma frase com e.',
           '#raciociniologico', 'Raciocínio Lógico do Escrevente TJSP: negação do "ou".', asize=34))
V.append(q('c-311-torneira', 'MATEMÁTICA · MEDIDAS', 'Quanto tempo pra encher?', 'encher?', '🚰',
           'Questão de medidas do TJ. Quanto tempo essa torneira leva?',
           'Uma torneira despeja 12 litros por minuto num reservatório de 2,4 m³. Para encher tudo, leva:', ['20 minutos', '3 h 20 min', '3 h 33 min', '33 h 20 min', '200 horas'], 'B',
           'Doze litros por minuto, num reservatório de dois vírgula quatro metros cúbicos. Quanto tempo pra encher?',
           'Letra B: 3 h 20 min', '3 h 20 min', '2,4 m³ = 2.400 L → 200 min', '⏱️',
           'Letra B. Dois vírgula quatro metros cúbicos são dois mil e quatrocentos litros. Dividido por doze dá duzentos minutos: três horas e vinte. Três e trinta e três é a pegadinha.',
           '#matematica', 'Matemática do Escrevente TJSP: medidas e tempo.'))
V.append(q('c-312-escada', 'MATEMÁTICA · PITÁGORAS', 'Até que altura a escada chega?', 'altura', '🪜',
           'Pitágoras no concurso do TJ. Até onde essa escada chega?',
           'Escada de 2,5 m apoiada na parede, com o pé a 150 cm da parede. A altura atingida é:', ['1,0 m', '2,0 m', '2,5 m', 'cerca de 2,9 m', '4,0 m'], 'B',
           'Uma escada de dois metros e meio, com o pé a cento e cinquenta centímetros da parede. Que altura ela alcança?',
           'Letra B: 2 metros', '2 metros', '2,5² − 1,5² = 4 → √4 = 2', '📐',
           'Letra B. Pitágoras: dois e meio ao quadrado menos um e meio ao quadrado dá quatro. Raiz de quatro, dois metros. Quem marcou quatro esqueceu a raiz.',
           '#matematica', 'Matemática do Escrevente TJSP: teorema de Pitágoras.'))
print('\n'.join(V))
