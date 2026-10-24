"""Specs v3 do Gabarito do Dia (TikTok/Reels, PT-BR): quiz com mascote. Uso: python3 specs/gabgen.py -> specs/v3/c-3xx-*.json
Sem WhatsApp e sem preço no vídeo (assim todo vídeo pode ser promovido); a venda fica na legenda e na bio."""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v3')
os.makedirs(OUT, exist_ok=True)
TAGS = '#concursotjsp #escreventetjsp #concursopublico #vunesp #concurseiro'


def q(name, label, hook_text, hook_hl, hook_icon, hook_n, question, alts, letter, q_n, ans_text, ans_n, steps, trap, tags, caption, qsize=56, asize=48):
    """steps = (titulo, hl, [linhas], narração, [cues]) · trap = (texto, hl, narração) ou None"""
    correct = 'ABCDE'.index(letter)
    st_text, st_hl, st_rows, st_n, st_cues = steps
    rows = [{**(t if isinstance(t, dict) else {'t': t}), **({'cue': c} if c else {})} for t, c in zip(st_rows, st_cues + [None] * len(st_rows))]
    scenes = [
        {'type': 'hook', 'kicker': 'Escrevente TJSP · VUNESP', 'text': hook_text, 'hl': hook_hl, 'icon': hook_icon, 'narration': hook_n, 'min_duration': 2.0},
        {'type': 'quiz', 'label': label, 'q': question, 'alts': alts, 'correct': correct, 'narration': q_n, 'extra': 4.6, 'revealFromEnd': 1.6, 'countdown': 3, 'qsize': qsize, 'asize': asize},
        {'type': 'text', 'text': ans_text, 'hl': ans_text.split(': ', 1)[-1], 'icon': '✅', 'pose': 'cheer', 'burst': True, 'narration': ans_n, 'min_duration': 1.8},
        {'type': 'steps', 'text': st_text, 'hl': st_hl, 'rows': rows, 'narration': st_n, 'min_duration': 3.0},
    ]
    if trap:
        scenes.append({'type': 'text', 'kicker': 'Pegadinha', 'text': trap[0], 'hl': trap[1], 'icon': '⚠️', 'pose': 'shock', 'narration': trap[2], 'min_duration': 2.2})
    scenes.append({'type': 'end', 'text': 'Siga: 1 questão do TJSP por dia', 'hl': '1 questão', 'brand': 'GABARITO DO DIA', 'narration': 'Segue: uma questão por dia até a prova.', 'min_duration': 2.0})
    spec = {
        'channel': 'gabarito', 'style': 'v3', 'rate': '+5%', 'title': hook_text,
        'publish': {'channel': 'C', 'privacy': 'public'},
        'tiktok': f"{caption} Comenta a letra! Apostila com 182 questões comentadas: amostra grátis no WhatsApp da bio.\n{TAGS} {tags}",
        'scenes': scenes,
    }
    json.dump(spec, open(f'{OUT}/{name}.json', 'w'), ensure_ascii=False, indent=1)
    return name


V = []
V.append(q('c-301-sequencia', 'RACIOCÍNIO LÓGICO · SEQUÊNCIAS', '2, 3, 5, 8, 12, 17... e o 10º?', 'e o 10º?', '🔢',
           'Descobre o padrão dessa sequência?',
           'Sequência: 2, 3, 5, 8, 12, 17, ... Mantido o padrão, o 10º termo é:', ['38', '45', '47', '55', '57'], 'C',
           'Dois, três, cinco, oito, doze, dezessete. Qual é o décimo termo?',
           'Letra C: 47', 'Letra C, quarenta e sete!',
           ('As diferenças crescem', 'crescem', ['+1, +2, +3, +4, +5...', '17, 23, 30, 38...', '38 + 9 = 47'],
            'As diferenças crescem de um em um. Depois do dezessete vem vinte e três, trinta, trinta e oito. Mais nove: quarenta e sete.', ['diferenças', 'depois', 'mais']),
           ('38 é só o 9º termo', '9º termo', 'O trinta e oito é só o nono termo.'),
           '#raciociniologico', 'Raciocínio Lógico do Escrevente TJSP: qual é o 10º termo?'))
V.append(q('c-302-calendario', 'RACIOCÍNIO LÓGICO · CALENDÁRIO', 'Que dia da semana caiu o dia 20?', 'dia 20?', '🗓️',
           'Essa de calendário derruba muita gente.',
           'Um mês de 31 dias teve cinco sextas, cinco sábados e cinco domingos. O dia 20 caiu em uma:', ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira'], 'C',
           'Um mês de trinta e um dias teve cinco sextas, cinco sábados e cinco domingos. O dia vinte caiu em quê?',
           'Letra C: quarta-feira', 'Letra C, quarta-feira!',
           ('31 dias = 4 semanas + 3', '+ 3', ['Dias 1, 2 e 3 aparecem 5 vezes', 'Dia 1 = sexta', 'Dia 20 = sexta + 19 = quarta'],
            'Trinta e um dias são quatro semanas e mais três dias. Os dias um, dois e três se repetem cinco vezes. Então o dia um foi sexta. Mais dezenove dias: quarta.', ['dias', 'então', 'mais']),
           None,
           '#raciociniologico', 'Raciocínio Lógico do Escrevente TJSP: que dia caiu o dia 20?'))
V.append(q('c-303-juros', 'MATEMÁTICA · JUROS SIMPLES', 'R$ 4.000 a 3% ao mês. Quanto vira?', 'Quanto vira?', '💰',
           'Quanto vira esse dinheiro em quatro meses?',
           'R$ 4.000,00 a juros simples de 3% ao mês, por 4 meses. O montante final é:', ['R$ 480,00', 'R$ 4.120,00', 'R$ 4.360,00', 'R$ 4.480,00', 'R$ 4.502,04'], 'D',
           'Quatro mil reais, a juros simples de três por cento ao mês, durante quatro meses. Qual é o montante?',
           'Letra D: R$ 4.480', 'Letra D, quatro mil quatrocentos e oitenta!',
           ('Juros simples', 'simples', ['J = 4.000 × 0,03 × 4', 'J = R$ 480', 'M = 4.000 + 480 = R$ 4.480'],
            'Juros: quatro mil, vezes três por cento, vezes quatro. Dá quatrocentos e oitenta. O montante soma o capital: quatro mil quatrocentos e oitenta.', ['juros', 'dá', 'montante']),
           ('R$ 480 são só os juros', 'só os juros', 'Quem marcou quatrocentos e oitenta caiu na pegadinha.'),
           '#matematica', 'Matemática do Escrevente TJSP: juros simples.'))
V.append(q('c-304-nato', 'CONSTITUCIONAL · ART. 12', 'Só brasileiro nato pode ser...', 'brasileiro nato', '🇧🇷',
           'Só um desses cargos exige brasileiro nato.',
           'Segundo a Constituição Federal, é privativo de brasileiro nato o cargo de:', ['Ministro do STJ', 'Presidente da Câmara dos Deputados', 'Ministro da Justiça', 'Senador da República', 'Procurador-Geral da República'], 'B',
           'Segundo a Constituição, qual destes cargos é privativo de brasileiro nato?',
           'Letra B: Presidente da Câmara', 'Letra B, presidente da Câmara!',
           ('Só nato (art. 12, § 3º)', 'Só nato', ['Presidente e vice', 'Pres. da Câmara e do Senado', 'Ministro do STF', 'Diplomata, oficial militar, Min. da Defesa'],
            'A lista é curta: presidente e vice, presidentes da Câmara e do Senado, ministros do Supremo, diplomatas, oficiais das Forças Armadas e o ministro da Defesa.', ['presidente', 'presidentes', 'ministros', 'diplomatas']),
           ('Senador e ministro do STJ podem ser naturalizados', 'naturalizados', 'Senador e ministro do STJ podem ser naturalizados.'),
           '#direitoconstitucional', 'Constitucional do Escrevente TJSP: cargo privativo de brasileiro nato.', asize=42))
V.append(q('c-305-regradetres', 'MATEMÁTICA · REGRA DE TRÊS', '8 servidores, 18 dias. E com 12?', 'E com 12?', '👥',
           'Regra de três com pegadinha. Acerta?',
           '8 servidores digitalizam um arquivo em 18 dias. No mesmo ritmo, 12 servidores levarão:', ['12 dias', '14 dias', '22 dias', '27 dias', '30 dias'], 'A',
           'Oito servidores fazem o serviço em dezoito dias. Com doze servidores, quantos dias?',
           'Letra A: 12 dias', 'Letra A, doze dias!',
           ('Mais gente, menos dias', 'menos dias', ['Inversamente proporcional', '8 × 18 = 144', '144 ÷ 12 = 12 dias'],
            'É inversamente proporcional. Oito vezes dezoito dá cento e quarenta e quatro. Dividido por doze: doze dias.', ['inversamente', 'oito', 'dividido']),
           ('27 dias? Esqueceu de inverter', 'inverter', 'Quem marcou vinte e sete esqueceu de inverter.'),
           '#matematica', 'Matemática do Escrevente TJSP: regra de três inversa.'))
V.append(q('c-306-crase', 'PORTUGUÊS · CRASE', 'Só uma tem a crase certa', 'crase certa', '✍️',
           'Só uma dessas crases está certa.',
           'Está correto o emprego do sinal indicativo de crase em:', ['Refiro-me àquelas normas e não à estas.', 'Ficaram frente à frente na sala.', 'Sua leitura é semelhante à do relator.', 'Fomos à Brasília para a audiência.', 'O juiz falou à todos sobre a decisão.'], 'C',
           'Em qual dessas frases a crase está correta?',
           'Letra C: semelhante à do relator', 'Letra C!',
           ('Por que tem crase?', 'crase?', ['Semelhante pede A (preposição)', '+ a leitura (artigo escondido)', 'a + a = à do relator'],
            'Semelhante pede a preposição a. E tem um artigo escondido: a leitura do relator. A mais a: crase.', ['semelhante', 'artigo', 'mais']),
           ('Antes de todos, estas e Brasília: sem crase', 'sem crase', 'Antes de todos, de estas e de Brasília, não tem crase.'),
           '#portugues #crase', 'Português do Escrevente TJSP: onde está a crase certa?', asize=42))
V.append(q('c-307-regencia', 'PORTUGUÊS · REGÊNCIA', 'Assistir O filme ou AO filme?', 'AO filme?', '🎬',
           'Assistir o filme ou assistir ao filme?',
           'De acordo com a norma-padrão, a regência verbal está correta em:', ['Prefiro estudar à noite do que de manhã.', 'Ele aspirava o cargo de chefia.', 'Assistiram à palestra sobre o edital.', 'Obedeceram o horário estabelecido.', 'Esqueci dos documentos em casa.'], 'C',
           'Em qual frase a regência verbal está correta?',
           'Letra C: assistiram à palestra', 'Letra C!',
           ('Quem pede A', 'pede A', ['Assistir (ver) A', 'Aspirar (desejar) A', 'Obedecer A', 'Preferir X A Y, sem "do que"'],
            'Assistir, no sentido de ver, pede a. Aspirar, no sentido de desejar, também. Obedecer a. E prefere-se uma coisa a outra, sem do que.', ['assistir', 'aspirar', 'obedecer', 'prefere']),
           None,
           '#portugues', 'Português do Escrevente TJSP: regência verbal.', asize=42))
V.append(q('c-308-atalhos', 'INFORMÁTICA · WINDOWS', 'Qual atalho está certo?', 'atalho', '⌨️',
           'Só um desses atalhos está certo.',
           'No Windows 10 ou 11, a combinação de teclas está correta em:', ['Win+L abre as Configurações', 'Alt+Tab fecha a janela ativa', 'Win+E abre a caixa Executar', 'Win+Shift+S abre o histórico do Ctrl+C', 'Ctrl+Shift+Esc abre o Gerenciador de Tarefas'], 'E',
           'No Windows, qual destes atalhos está associado à função certa?',
           'Letra E: Ctrl+Shift+Esc', 'Letra E!',
           ('Decora esses', 'Decora', [{'t': 'Ctrl+Shift+Esc: Gerenciador', 'hi': True}, 'Win+L: bloqueia a tela', 'Win+E: Explorador', 'Win+R: Executar', 'Win+V: histórico do Ctrl+C'],
            'Control shift esc abre o gerenciador de tarefas. Windows L bloqueia. Windows E, explorador. Windows R, executar. E Windows V, o histórico do control C.', ['control', 'windows', 'windows', 'windows', 'e']),
           None,
           '#informatica #windows', 'Informática do Escrevente TJSP: atalhos do Windows.', asize=40))
V.append(q('c-309-kits', 'MATEMÁTICA · MDC', 'Quantos itens em cada kit?', 'cada kit?', '📦',
           'Quantos itens vai ter cada kit?',
           '120 cadernos, 168 canetas e 216 pastas em kits idênticos, sem sobra, com o maior número de kits. Cada kit terá:', ['21 itens', '24 itens', '42 itens', '63 itens', '504 itens'], 'A',
           'Cento e vinte cadernos, cento e sessenta e oito canetas e duzentas e dezesseis pastas, no maior número de kits iguais. Quantos itens por kit?',
           'Letra A: 21 itens', 'Letra A, vinte e um itens!',
           ('Maior número de kits = MDC', 'MDC', ['MDC(120, 168, 216) = 24 kits', '5 cadernos + 7 canetas + 9 pastas', '5 + 7 + 9 = 21 itens'],
            'O MDC dá vinte e quatro kits. Cada kit leva cinco cadernos, sete canetas e nove pastas: vinte e um itens.', ['mdc', 'cada', 'vinte']),
           ('24 é o número de kits, não de itens', 'kits', 'Vinte e quatro é o número de kits, não de itens.'),
           '#matematica', 'Matemática do Escrevente TJSP: MDC.', qsize=50))
V.append(q('c-310-demorgan', 'RACIOCÍNIO LÓGICO · NEGAÇÃO', 'Como negar uma frase com "ou"?', '"ou"?', '🔀',
           'Como negar uma frase com ou?',
           'A negação de "A sessão foi adiada ou o relator pediu vista" é:', ['Não foi adiada ou o relator não pediu vista.', 'Foi adiada e o relator não pediu vista.', 'Se foi adiada, o relator não pediu vista.', 'Foi adiada ou o relator não pediu vista.', 'Não foi adiada e o relator não pediu vista.'], 'E',
           'Qual é a negação de: a sessão foi adiada ou o relator pediu vista?',
           'Letra E: não... E não...', 'Letra E!',
           ('Negar o "ou"', 'Negar', ['Nega as duas partes', 'Troca OU por E', 'não adiada E não pediu vista'],
            'Pra negar o ou: nega as duas partes e troca por e. Não foi adiada e não pediu vista.', ['nega', 'troca', 'não']),
           ('A letra A nega uma frase com "e"', 'com "e"', 'A letra A seria a negação de uma frase com e.'),
           '#raciociniologico', 'Raciocínio Lógico do Escrevente TJSP: negação do "ou".', asize=38))
V.append(q('c-311-torneira', 'MATEMÁTICA · MEDIDAS', 'Quanto tempo pra encher?', 'encher?', '🚰',
           'Quanto tempo essa torneira leva?',
           'Uma torneira despeja 12 litros por minuto num reservatório de 2,4 m³. Para encher tudo, leva:', ['20 minutos', '3 h 20 min', '3 h 33 min', '33 h 20 min', '200 horas'], 'B',
           'Doze litros por minuto, num reservatório de dois vírgula quatro metros cúbicos. Quanto tempo pra encher?',
           'Letra B: 3 h 20 min', 'Letra B, três horas e vinte!',
           ('Converte primeiro', 'Converte', ['1 m³ = 1.000 litros', '2,4 m³ = 2.400 litros', '2.400 ÷ 12 = 200 min', '200 min = 3 h 20 min'],
            'Um metro cúbico tem mil litros. Então são dois mil e quatrocentos. Dividido por doze: duzentos minutos. Ou seja, três horas e vinte.', ['um', 'então', 'dividido', 'ou']),
           ('3 h 33? Hora tem 60 minutos', '60 minutos', 'Três e trinta e três é a pegadinha: hora tem sessenta minutos.'),
           '#matematica', 'Matemática do Escrevente TJSP: medidas e tempo.'))
V.append(q('c-312-escada', 'MATEMÁTICA · PITÁGORAS', 'Até que altura a escada chega?', 'altura', '🪜',
           'Até que altura essa escada chega?',
           'Escada de 2,5 m apoiada na parede, com o pé a 150 cm da parede. A altura atingida é:', ['1,0 m', '2,0 m', '2,5 m', 'cerca de 2,9 m', '4,0 m'], 'B',
           'Uma escada de dois metros e meio, com o pé a cento e cinquenta centímetros da parede. Que altura ela alcança?',
           'Letra B: 2 metros', 'Letra B, dois metros!',
           ('Pitágoras', 'Pitágoras', ['2,5² = h² + 1,5²', '6,25 − 2,25 = 4', 'h = √4 = 2 m'],
            'Pitágoras: a escada é a hipotenusa. Seis e vinte e cinco menos dois e vinte e cinco dá quatro. Raiz de quatro: dois metros.', ['pitágoras', 'seis', 'raiz']),
           ('4,0 m? Esqueceu a raiz', 'raiz', 'Quem marcou quatro esqueceu a raiz.'),
           '#matematica', 'Matemática do Escrevente TJSP: teorema de Pitágoras.'))

V.append(q('c-314-excel', 'INFORMÁTICA · EXCEL', 'Qual erro do Excel é esse?', 'Excel', '📊',
           'Quatro erros do Excel. Só um está certo.',
           'Associa corretamente a mensagem de erro do Excel à sua causa mais comum:', ['#NOME?: célula excluída', '#REF!: nome de função errado', '#DIV/0!: divisão por zero ou célula vazia', '#VALOR!: PROCV não achou o valor', '#N/D: somar célula com texto'], 'C',
           'Qual alternativa associa certo o erro do Excel à causa?',
           'Letra C: #DIV/0!', 'Letra C!',
           ('Decora esses', 'Decora', [{'t': '#DIV/0!: divisão por zero', 'hi': True}, '#NOME?: função escrita errada', '#REF!: célula excluída', '#N/D: PROCV não achou'],
            'Divisão por zero dá div zero. Nome de função errado dá nome. Célula excluída dá ref. E PROCV que não acha dá N D.', ['divisão', 'nome', 'célula', 'procv']),
           None,
           '#informatica #excel', 'Informática do Escrevente TJSP: erros do Excel.', asize=40))
V.append(q('c-315-pronome', 'PORTUGUÊS · COLOCAÇÃO PRONOMINAL', 'Me entregaram ou Entregaram-me?', 'Entregaram-me?', '✍️',
           'Colocação pronominal: a VUNESP adora.',
           'A colocação do pronome átono está de acordo com a norma-padrão em:', ['Me entregaram o processo ontem.', 'O servidor tinha entregado-lhe o documento.', 'Nunca esqueceram-se do prazo final.', 'Disseram que entregariam-me o parecer.', 'Entregar-lhe-emos os documentos amanhã.'], 'E',
           'Em qual frase o pronome está bem colocado?',
           'Letra E: Entregar-lhe-emos', 'Letra E!',
           ('As regras que caem', 'caem', ['Não começa frase com pronome', 'Nunca depois do particípio', '"Nunca" e "que" puxam o pronome', 'Futuro no início: mesóclise'],
            'Não se começa frase com pronome. Nunca depois do particípio. Palavras como nunca e que puxam o pronome pra antes. E com futuro no início, mesóclise.', ['não', 'nunca', 'palavras', 'futuro']),
           ('Mesóclise ainda cai na prova', 'Mesóclise', 'Parece antigo, mas a mesóclise ainda cai na prova.'),
           '#portugues', 'Português do Escrevente TJSP: colocação pronominal.', asize=42))
V.append(q('c-316-mmc', 'MATEMÁTICA · MMC', '6, 8 e 10 dias. Quando coincidem?', 'Quando coincidem?', '⚙️',
           'Três máquinas. Quando elas coincidem de novo?',
           'Manutenção a cada 6, 8 e 10 dias. As três coincidiram numa segunda-feira. A próxima coincidência será numa:', ['quinta-feira, em 24 dias', 'quarta-feira, em 30 dias', 'sábado, em 40 dias', 'terça-feira, em 120 dias', 'sexta-feira, em 480 dias'], 'D',
           'Manutenção a cada seis, oito e dez dias. Coincidiram numa segunda. Quando coincidem de novo?',
           'Letra D: terça, em 120 dias', 'Letra D!',
           ('Coincidir = MMC', 'MMC', ['MMC(6, 8, 10) = 120 dias', '120 = 17 semanas + 1 dia', 'Segunda + 1 = terça'],
            'Coincidir é MMC: cento e vinte dias. Isso dá dezessete semanas e mais um dia. Segunda mais um: terça.', ['coincidir', 'isso', 'segunda']),
           ('480 = 6 × 8 × 10 (produto, não MMC)', 'não MMC', 'Quem marcou quatrocentos e oitenta multiplicou tudo, e isso não é MMC.'),
           '#matematica', 'Matemática do Escrevente TJSP: MMC.', asize=42))
V.append(q('c-317-inafiancavel', 'CONSTITUCIONAL · ART. 5º', 'Inafiançável E imprescritível', 'imprescritível', '⚖️',
           'Essa pegadinha da Constituição derruba muita gente.',
           'Segundo a Constituição Federal, são crimes inafiançáveis e imprescritíveis:', ['racismo e ação de grupos armados contra o Estado Democrático', 'tortura, tráfico de drogas e terrorismo', 'terrorismo, tráfico de drogas e hediondos', 'racismo, terrorismo e hediondos', 'ação de grupos armados e hediondos'], 'A',
           'Quais crimes são inafiançáveis e imprescritíveis?',
           'Letra A: racismo e grupos armados', 'Letra A!',
           ('Só dois são imprescritíveis', 'dois', ['Racismo (art. 5º, XLII)', 'Grupos armados (art. 5º, XLIV)', 'Tortura, tráfico, terrorismo e hediondos: inafiançáveis, mas prescrevem'],
            'Só dois são imprescritíveis: racismo e ação de grupos armados. Tortura, tráfico, terrorismo e hediondos são inafiançáveis, mas prescrevem.', ['racismo', 'grupos', 'tortura']),
           None,
           '#direitoconstitucional', 'Constitucional do Escrevente TJSP: crimes imprescritíveis.', asize=40))

# notícia: abertura das inscrições (28/10)
spec = {'channel': 'gabarito', 'style': 'v3', 'rate': '+4%', 'title': 'Inscrições abertas: Escrevente TJSP',
        'publish': {'channel': 'C', 'privacy': 'public'},
        'tiktok': f"Inscrições do Escrevente TJSP abertas até 10/12: taxa de R$ 81 e prova em 14/03/2027. Vagas no interior e no litoral de SP. Amostra grátis da apostila no WhatsApp da bio.\n{TAGS} #edital #inscricoesabertas",
        'scenes': [
            {'type': 'hook', 'kicker': 'Começou hoje', 'text': 'Inscrições abertas: Escrevente TJSP', 'hl': 'abertas:', 'icon': '📝', 'narration': 'Abriram as inscrições do Escrevente do TJ de São Paulo!', 'min_duration': 2.6},
            {'type': 'big', 'text': 'Salário inicial', 'hl': 'Salário', 'big': 'R$ 6.782', 'label': 'com ensino médio, 40 h semanais', 'narration': 'Salário inicial de seis mil setecentos e oitenta e dois reais.', 'min_duration': 3.0},
            {'type': 'steps', 'text': 'Anota as datas', 'hl': 'datas', 'rows': [{'t': 'Inscrições: até 10/12', 'icon': '📝', 'cue': 'inscrições'}, {'t': 'Taxa: R$ 81', 'icon': '💳', 'cue': 'taxa'}, {'t': 'Site da VUNESP', 'icon': '🌐', 'cue': 'site'}], 'result': False, 'narration': 'As inscrições vão até dez de dezembro. A taxa é de oitenta e um reais, no site da VUNESP.', 'min_duration': 3.2},
            {'type': 'text', 'text': 'Vagas no interior e no litoral de SP', 'hl': 'interior e no litoral', 'icon': '📍', 'pose': 'shrug', 'narration': 'As vagas são do interior e do litoral. A capital ficou de fora.', 'min_duration': 3.0},
            {'type': 'big', 'text': 'A prova é em', 'hl': 'prova', 'big': '14/03', 'label': 'faltam 137 dias', 'narration': 'A prova é em catorze de março. Faltam cento e trinta e sete dias.', 'min_duration': 3},
            {'type': 'end', 'text': 'Siga: 1 questão do TJSP por dia', 'hl': '1 questão', 'brand': 'GABARITO DO DIA', 'narration': 'Segue: uma questão por dia até a prova.', 'min_duration': 2.0},
        ]}
json.dump(spec, open(f'{OUT}/c-313-inscricoes.json', 'w'), ensure_ascii=False, indent=1)
V.append('c-313-inscricoes')
print('\n'.join(V))
