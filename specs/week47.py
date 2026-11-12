"""Semana 47 (16–22/11) do Gabarito do Dia (TikTok/Reels, PT-BR): 14 vídeos, 12:00 e 19:00 BRT (paleta clara).
PLANO.md (07/11), caminho 3 do TikTok: conteúdo que a busca interna pede (inscrição, planilha 2027, prazo) + questões VUNESP de Português e Direito.
Fatos do edital: Edital de Abertura nº 02/2026 (DJE 19/10/2026) — R$ 6.782,54, inscrições 28/10 a 10/12/2026 no site da VUNESP, taxa R$ 81,
prova 14/03/2027 à tarde (5 h), 70 questões em 3 blocos, redação 0–40 (mín. 24), cadastro de reserva, 50 circunscrições da 2ª à 10ª RAJ, sem troca.
Isca "PLANILHA": planilha de estudos de 18 semanas (09/11 → 14/03/2027) enviada pelo WhatsApp (gera lista). Uso: python3 specs/week47.py -> specs/v3/c-3xx-*.json"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v3')
os.makedirs(OUT, exist_ok=True)
TAGS = '#concursotjsp #escreventetjsp #concursopublico #vunesp #concurseiro'
SELL = 'Apostila com 182 questões comentadas: amostra grátis no WhatsApp da bio.'
END = {'type': 'end', 'text': 'Siga: 1 questão do TJSP por dia', 'hl': '1 questão', 'brand': 'GABARITO DO DIA', 'narration': 'Segue: uma questão por dia até a prova.', 'min_duration': 2.0}
V = []


def save(name, spec):
    spec['palette'] = 'gabaritoclaro'  # desde 31/10: só a paleta clara tem alcance; escuro zerou
    json.dump(spec, open(f'{OUT}/{name}-claro.json', 'w'), ensure_ascii=False, indent=1)
    V.append(name + '-claro')


def q(name, at, label, hook_text, hook_hl, hook_icon, hook_n, question, alts, letter, q_n, ans_text, ans_n, steps, trap, tags, caption, qsize=56, asize=48):
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
    scenes.append(END)
    save(name, {'channel': 'gabarito', 'style': 'v3', 'rate': '+5%', 'title': hook_text, 'publish': {'channel': 'C', 'privacy': 'public', 'tiktok_at': at},
                'tiktok': f"{caption} Comenta a letra! {SELL}\n{TAGS} {tags}", 'scenes': scenes})


def info(name, at, title, caption, tags, scenes, sell=SELL):
    save(name, {'channel': 'gabarito', 'style': 'v3', 'rate': '+4%', 'title': title, 'publish': {'channel': 'C', 'privacy': 'public', 'tiktok_at': at},
                'tiktok': f"{caption} {sell}\n{TAGS} {tags}", 'scenes': scenes + [END]})



# ---------------- 16/11 ----------------
info('c-346-prova', '2026-11-16 12:00', 'Como é a prova do TJSP 2027',
     'Prova do Escrevente TJSP: 14/03/2027, à tarde, 5 horas, 70 questões em 3 blocos e redação de 0 a 40 (mínimo 24) no mesmo dia.',
     '#prova #edital #tjsp', [
         {'type': 'hook', 'kicker': 'Edital 2026', 'text': 'Como é a prova do TJSP 2027', 'hl': 'prova', 'icon': '📋', 'narration': 'Como é a prova do escrevente do TJ de São Paulo, em vinte segundos.', 'min_duration': 2.4},
         {'type': 'big', 'text': 'Data', 'hl': 'Data', 'big': '14/03', 'label': 'domingo à tarde · 5 horas de prova', 'narration': 'É dia quatorze de março, à tarde, com cinco horas de prova.', 'min_duration': 2.6},
         {'type': 'steps', 'text': 'O que tem no dia', 'hl': 'no dia', 'rows': [{'t': '70 questões objetivas', 'icon': '✅', 'cue': 'setenta'}, {'t': 'Divididas em 3 blocos', 'icon': '🧩', 'cue': 'blocos'}, {'t': 'Redação: nota de 0 a 40', 'icon': '📝', 'cue': 'redação'}, {'t': 'Mínimo 24 na redação', 'icon': '🎯', 'cue': 'mínimo'}], 'result': False,
          'narration': 'São setenta questões objetivas, divididas em três blocos. E tem redação no mesmo dia, valendo de zero a quarenta, com mínimo de vinte e quatro.', 'min_duration': 4.0},
         {'type': 'text', 'kicker': 'Dica', 'text': 'Treine prova inteira no tempo', 'hl': 'no tempo', 'icon': '⏱️', 'pose': 'pointUp', 'narration': 'Dica: treina pelo menos uma prova inteira no tempo, com a redação junto.', 'min_duration': 2.8},
     ])
q('c-347-haver', '2026-11-16 19:00', 'PORTUGUÊS · CONCORDÂNCIA VERBAL', '"Houveram problemas" está certo?', 'Houveram', '✍️',
  'Houveram muitos problemas. Tá certo isso? A VUNESP adora.',
  'A concordância verbal está de acordo com a norma-padrão em:', ['Haviam muitas pessoas na sala.', 'Fazem dez anos que estudo.', 'Houve muitas reclamações no fórum.', 'Devem haver soluções para o caso.', 'Existe muitas dúvidas sobre o edital.'], 'C',
  'Em qual frase a concordância está certa?',
  'Letra C: houve muitas reclamações', 'Letra C!',
  ('Verbos que não vão ao plural', 'plural', ['Haver = existir: houve, havia (singular)', 'Fazer = tempo: faz dez anos', 'Auxiliar também fica: deve haver', 'Existir concorda: existem dúvidas'],
   'Haver no sentido de existir não tem sujeito: houve, havia, sempre no singular. Fazer indicando tempo também: faz dez anos. O auxiliar acompanha: deve haver. Mas existir concorda normal: existem dúvidas.', ['existir', 'tempo', 'auxiliar', 'concorda']),
  ('"Existem" vai ao plural; "há" não', 'plural', 'Pegadinha: troque por existir. Existem muitas dúvidas, no plural. Há muitas dúvidas, no singular.'),
  '#portugues #concordancia', 'Português do Escrevente TJSP: haver e fazer impessoais.', asize=44)

# ---------------- 17/11 ----------------
q('c-348-malmau', '2026-11-17 12:00', 'PORTUGUÊS · MAL OU MAU', 'Mal ou mau?', 'mau?', '✍️',
  'Mal ou mau? Tem um truque que resolve na hora.',
  'O emprego de "mal" ou "mau" está correto em:', ['Foi um mal exemplo para todos.', 'Ele agiu mau na reunião.', 'Ele se comportou mal na audiência.', 'Estava de mal humor no fórum.', 'O doce em excesso faz mau.'], 'C',
  'Em qual frase está certo?',
  'Letra C: comportou-se mal', 'Letra C!',
  ('O truque', 'truque', ['Mal: oposto de BEM (agiu mal)', 'Mau: oposto de BOM (mau exemplo)', 'Mau humor, mau exemplo', 'Faz mal (faz bem)'],
   'O truque: mal é o contrário de bem. Agiu bem, agiu mal. Mau é o contrário de bom: bom exemplo, mau exemplo. Então é mau humor, mau exemplo, e faz mal, porque o contrário é faz bem.', ['bem', 'bom', 'humor', 'faz']),
  ('"Mal cheguei, ele saiu": mal = assim que', 'assim que', 'Pegadinha: mal também é conjunção. Mal cheguei, ele saiu, quer dizer assim que eu cheguei.'),
  '#portugues #ortografia', 'Português do Escrevente TJSP: mal ou mau.', asize=44)
q('c-349-poderes', '2026-11-17 19:00', 'DIREITO ADMINISTRATIVO · PODERES', 'Multa da vigilância sanitária: qual poder?', 'qual poder?', '⚖️',
  'A prefeitura multa um restaurante por descumprir regra sanitária. Qual é o poder?',
  'A aplicação de multa a estabelecimento comercial por descumprimento de norma sanitária é manifestação do poder:', ['Hierárquico', 'Disciplinar', 'Regulamentar', 'De polícia', 'Vinculado'], 'D',
  'Qual é o poder?',
  'Letra D: poder de polícia', 'Letra D!',
  ('Cada poder no seu lugar', 'seu lugar', ['Polícia: limita direitos do particular', 'Disciplinar: pune servidor', 'Hierárquico: ordena e revisa', 'Regulamentar: decreto para executar lei'],
   'Poder de polícia limita a liberdade e a propriedade do particular em nome do interesse público. Disciplinar pune o servidor. Hierárquico organiza, dá ordens e revisa. Regulamentar edita decreto para executar a lei.', ['polícia', 'Disciplinar', 'Hierárquico', 'Regulamentar']),
  ('Multa a SERVIDOR é disciplinar', 'SERVIDOR', 'Pegadinha: se a punição for para um servidor, por falta funcional, aí é poder disciplinar, não de polícia.'),
  '#direitoadministrativo #poderdepolicia', 'Direito Administrativo para o Escrevente TJSP: poder de polícia x disciplinar.', asize=46)

# ---------------- 18/11 ----------------
q('c-350-porques', '2026-11-18 12:00', 'PORTUGUÊS · PORQUÊS', 'Por que, porque, por quê ou porquê?', 'porquê?', '✍️',
  'Por que, porque, por quê ou porquê? Quatro jeitos, e a prova cobra todos.',
  'Preenche corretamente as lacunas: "___ você faltou? Quero entender o ___."', ['Porque / por quê', 'Por que / porquê', 'Por quê / porque', 'Porquê / por que', 'Porque / porquê'], 'B',
  'Qual alternativa preenche certo?',
  'Letra B: por que / porquê', 'Letra B!',
  ('Os quatro porquês', 'quatro', ['Por que: pergunta (por que faltou?)', 'Por quê: no fim da frase', 'Porque: resposta, explicação', 'Porquê: substantivo (o porquê)'],
   'Por que, separado, é pergunta: por que você faltou? Por quê, separado e com acento, vai no fim: faltou por quê? Porque, junto, é resposta. E porquê, junto e com acento, é substantivo: o porquê.', ['pergunta', 'fim', 'resposta', 'substantivo']),
  ('Com artigo antes, é porquê', 'artigo', 'Pegadinha: se tem artigo antes, o porquê, vira substantivo. Junto e com acento.'),
  '#portugues #ortografia', 'Português do Escrevente TJSP: os quatro porquês.', asize=44)
info('c-351-salario', '2026-11-18 19:00', 'Escrevente TJSP: R$ 6.782,54',
     'Escrevente Técnico Judiciário do TJSP: R$ 6.782,54, nível médio, 50 circunscrições e cadastro de reserva. Inscrições até 10/12 no site da VUNESP.',
     '#salario #edital #tjsp', [
         {'type': 'hook', 'kicker': 'Edital 2026', 'text': 'Quanto ganha o escrevente do TJSP', 'hl': 'Quanto ganha', 'icon': '💰', 'narration': 'Quanto ganha o escrevente do TJ de São Paulo?', 'min_duration': 2.2},
         {'type': 'big', 'text': 'Salário', 'hl': 'Salário', 'big': 'R$ 6.782', 'label': 'R$ 6.782,54 segundo o edital de 2026', 'narration': 'Seis mil setecentos e oitenta e dois reais, segundo o edital.', 'min_duration': 2.6},
         {'type': 'steps', 'text': 'O que mais o edital diz', 'hl': 'edital', 'rows': [{'t': 'Nível médio', 'icon': '🎓', 'cue': 'médio'}, {'t': '50 circunscrições no estado', 'icon': '📍', 'cue': 'circunscrições'}, {'t': 'Cadastro de reserva', 'icon': '📋', 'cue': 'reserva'}, {'t': 'Inscrição até 10/12', 'icon': '⏳', 'cue': 'dezembro'}], 'result': False,
          'narration': 'O cargo é de nível médio. São cinquenta circunscrições no estado, com cadastro de reserva. E a inscrição vai até dez de dezembro.', 'min_duration': 3.8},
         {'type': 'text', 'kicker': 'Atenção', 'text': 'Escolha a circunscrição com cuidado', 'hl': 'circunscrição', 'icon': '⚠️', 'pose': 'shock', 'narration': 'Atenção: a circunscrição não troca depois. Escolhe onde você consegue trabalhar.', 'min_duration': 2.6},
     ])

# ---------------- 19/11 ----------------
q('c-352-condescendencia', '2026-11-19 12:00', 'DIREITO PENAL · CRIMES CONTRA A ADM.', 'Chefe que "deixa passar" comete crime?', 'deixa passar', '⚖️',
  'O chefe vê o subordinado cometer infração e, por pena, deixa passar. É crime?',
  'O funcionário que, por indulgência, deixa de responsabilizar subordinado que cometeu infração no exercício do cargo comete:', ['Prevaricação', 'Condescendência criminosa', 'Advocacia administrativa', 'Concussão', 'Peculato culposo'], 'B',
  'Qual é o crime?',
  'Letra B: condescendência criminosa', 'Letra B!',
  ('Não confunda', 'confunda', ['Condescendência (320): indulgência', 'Prevaricação (319): interesse pessoal', 'Advocacia adm. (321): interesse privado', 'Peculato culposo: facilita por culpa'],
   'Condescendência criminosa, artigo trezentos e vinte: deixa de responsabilizar por indulgência. Prevaricação, trezentos e dezenove: deixa de agir por interesse ou sentimento pessoal. Advocacia administrativa: patrocina interesse privado perante a administração. Peculato culposo: concorre por culpa para o crime de outro.', ['indulgência', 'Prevaricação', 'Advocacia', 'culpa']),
  ('Indulgência = condescendência', 'condescendência', 'O macete: se a palavra é indulgência, pena, tolerância, é condescendência. Se é interesse pessoal, é prevaricação.'),
  '#direitopenal #crimescontraaadministracao', 'Direito Penal para o Escrevente TJSP: condescendência criminosa x prevaricação.', qsize=50, asize=44)
q('c-353-virgula', '2026-11-19 19:00', 'PORTUGUÊS · VÍRGULA', 'Vírgula entre sujeito e verbo pode?', 'pode?', '✍️',
  'Vírgula entre sujeito e verbo. Pode ou não pode?',
  'A pontuação está de acordo com a norma-padrão em:', ['Os candidatos aprovados, tomarão posse em março.', 'O juiz, após a audiência, proferiu a sentença.', 'O escrevente entregou, o processo ao juiz.', 'Os servidores do fórum, chegaram cedo.', 'Amanhã, haverá, sessão no tribunal.'], 'B',
  'Em qual frase a vírgula está certa?',
  'Letra B: o juiz, após a audiência, proferiu', 'Letra B!',
  ('Regras da vírgula', 'vírgula', ['Nunca entre sujeito e verbo', 'Nunca entre verbo e complemento', 'Isola expressão intercalada', 'Adjunto deslocado: pode isolar'],
   'Nunca separa o sujeito do verbo, nem o verbo do complemento. Mas uma expressão intercalada, no meio da frase, vai entre vírgulas: o juiz, após a audiência, proferiu a sentença. E o adjunto deslocado pode ser isolado.', ['sujeito', 'complemento', 'intercalada', 'deslocado']),
  ('Sujeito longo também não leva vírgula', 'longo', 'Pegadinha: mesmo com sujeito longo, como os servidores do fórum, não vai vírgula antes do verbo.'),
  '#portugues #pontuacao', 'Português do Escrevente TJSP: vírgula entre sujeito e verbo.', qsize=52, asize=40)

# ---------------- 20/11 ----------------
q('c-354-nato', '2026-11-20 12:00', 'DIREITO CONSTITUCIONAL · NACIONALIDADE', 'Naturalizado pode ser ministro do STF?', 'ministro do STF?', '⚖️',
  'Um brasileiro naturalizado pode ser ministro do Supremo?',
  'Segundo o art. 12, § 3º, da Constituição, é cargo privativo de brasileiro nato:', ['Senador da República', 'Deputado federal', 'Ministro do Supremo Tribunal Federal', 'Governador de Estado', 'Ministro da Fazenda'], 'C',
  'Qual cargo é privativo de brasileiro nato?',
  'Letra C: ministro do STF', 'Letra C!',
  ('Só brasileiro nato', 'nato', ['Presidente e vice-presidente', 'Presidentes da Câmara e do Senado', 'Ministro do STF', 'Diplomata, oficial, ministro da Defesa'],
   'Só brasileiro nato: presidente e vice-presidente da República. Presidentes da Câmara e do Senado. Ministro do Supremo. Carreira diplomática, oficial das Forças Armadas e ministro da Defesa.', ['presidente', 'Câmara', 'Supremo', 'diplomática']),
  ('Senador pode ser naturalizado; presidente do Senado, não', 'presidente do Senado', 'Pegadinha: deputado e senador podem ser naturalizados. Só a presidência da Câmara e do Senado exige brasileiro nato.'),
  '#direitoconstitucional #nacionalidade', 'Direito Constitucional para o Escrevente TJSP: cargos privativos de brasileiro nato.', asize=44)
q('c-355-colocacao', '2026-11-20 19:00', 'PORTUGUÊS · COLOCAÇÃO PRONOMINAL', '"Me disseram" no começo da frase pode?', 'Me disseram', '✍️',
  'Me disseram que a prova mudou. Começar frase com me pode, na prova?',
  'A colocação pronominal está de acordo com a norma-padrão em:', ['Me disseram que a prova mudou.', 'Não disseram-me nada sobre o prazo.', 'Ninguém me avisou do prazo.', 'Se encontraram no fórum ontem.', 'Quando entregaram-me o processo, saí.'], 'C',
  'Em qual frase a colocação está certa?',
  'Letra C: ninguém me avisou', 'Letra C!',
  ('Quando o pronome vem antes', 'antes', ['Não começa frase com me, te, se', 'Negação puxa: não me disseram', 'Ninguém, nada, nunca puxam', 'Quando, que, se: quando me entregaram'],
   'Na norma-padrão, frase não começa com me, te ou se. Palavra negativa puxa o pronome para antes: não me disseram. Ninguém, nada e nunca também puxam. E conjunção como quando, que e se: quando me entregaram.', ['começa', 'negativa', 'Ninguém', 'conjunção']),
  ('Na fala vale; na prova, não', 'na prova', 'Pegadinha: me disseram é normal na fala do Brasil. Mas a prova cobra a norma-padrão.'),
  '#portugues #colocacaopronominal', 'Português do Escrevente TJSP: colocação pronominal (próclise).', asize=42)

# ---------------- 21/11 ----------------
q('c-356-ondeaonde', '2026-11-21 12:00', 'PORTUGUÊS · ONDE OU AONDE', 'Onde ou aonde?', 'aonde?', '✍️',
  'Aonde você mora? Errado. Mas por quê?',
  'O emprego de "onde" ou "aonde" está correto em:', ['Aonde fica o fórum central?', 'Onde você vai depois da prova?', 'Aonde você vai depois da prova?', 'Não sei aonde deixei a chave.', 'A cidade aonde moro é pequena.'], 'C',
  'Em qual frase está certo?',
  'Letra C: aonde você vai', 'Letra C!',
  ('O truque', 'truque', ['Aonde = a + onde', 'Verbo de movimento: ir A algum lugar', 'Onde: lugar em que algo está', 'Morar, ficar, estar: onde'],
   'Aonde é a mais onde. Usa com verbo de movimento, que pede a: ir a algum lugar, aonde você vai? Onde é o lugar em que algo está: onde você mora, onde fica, onde está.', ['movimento', 'ir', 'lugar', 'mora']),
  ('Chegar também pede a: aonde ele chegou', 'chegar', 'Pegadinha: chegar também é movimento e pede a. Aonde ele chegou, com a.'),
  '#portugues', 'Português do Escrevente TJSP: onde ou aonde.', asize=44)
q('c-357-direitossociais', '2026-11-21 19:00', 'DIREITO CONSTITUCIONAL · ART. 6º', 'Qual NÃO é direito social do art. 6º?', 'NÃO é', '⚖️',
  'Educação, saúde, moradia, transporte. Qual desses não está no artigo sexto?',
  'NÃO está entre os direitos sociais do art. 6º da Constituição:', ['Moradia', 'Transporte', 'Lazer', 'Propriedade', 'Alimentação'], 'D',
  'Qual não é direito social do artigo sexto?',
  'Letra D: propriedade', 'Letra D!',
  ('Os direitos sociais do art. 6º', 'art. 6º', ['Educação, saúde, alimentação, trabalho', 'Moradia, transporte, lazer, segurança', 'Previdência social', 'Maternidade, infância, desamparados'],
   'O artigo sexto lista: educação, saúde, alimentação, trabalho, moradia, transporte, lazer, segurança, previdência social, proteção à maternidade e à infância, e assistência aos desamparados.', ['educação', 'transporte', 'previdência', 'maternidade']),
  ('Propriedade está no art. 5º', 'art. 5º', 'Pegadinha: propriedade é direito garantido, mas está no artigo quinto, entre os direitos individuais.'),
  '#direitoconstitucional #direitossociais', 'Direito Constitucional para o Escrevente TJSP: direitos sociais do art. 6º.', asize=46)

# ---------------- 22/11 ----------------
q('c-358-acentuacao', '2026-11-22 12:00', 'PORTUGUÊS · ACENTUAÇÃO', 'Ideia tem acento?', 'acento?', '✍️',
  'Ideia tem acento? E voo? E pôde? O acordo ortográfico mudou isso.',
  'A acentuação está de acordo com a norma vigente em:', ['A idéia foi aprovada pelo juiz.', 'Ele não pôde vir ontem.', 'O vôo atrasou duas horas.', 'Pára de falar durante a sessão.', 'Teve uma atitude heróica.'], 'B',
  'Em qual frase a acentuação está certa?',
  'Letra B: ele não pôde', 'Letra B!',
  ('O que mudou com o acordo', 'acordo', ['Ideia, heroico: sem acento', 'Voo, enjoo: sem acento', 'Para (verbo): sem acento', 'Pôde (passado): continua com acento'],
   'Com o acordo ortográfico, ideia e heroico perderam o acento. Voo e enjoo também. Para, do verbo parar, ficou sem acento. Mas pôde, no passado, continua com acento, para diferenciar de pode.', ['ideia', 'Voo', 'parar', 'passado']),
  ('Pôr (verbo) também continua com acento', 'Pôr', 'Pegadinha: pôr, o verbo, também manteve o acento, para não confundir com por, preposição.'),
  '#portugues #acentuacao', 'Português do Escrevente TJSP: acentuação depois do acordo ortográfico.', asize=44)
info('c-359-apostila', '2026-11-22 19:00', '182 questões comentadas: amostra grátis',
     'Apostila do Escrevente TJSP com 182 questões comentadas, no estilo das questões desta semana. Amostra grátis no WhatsApp da bio: manda APOSTILA.',
     '#apostila #questoes #tjsp', [
         {'type': 'hook', 'kicker': 'Escrevente TJSP', 'text': '182 questões comentadas', 'hl': '182', 'icon': '📚', 'narration': 'Gostou das questões da semana? Tem cento e oitenta e duas, todas comentadas.', 'min_duration': 2.6},
         {'type': 'steps', 'text': 'Nesta semana caiu', 'hl': 'semana', 'rows': [{'t': 'Haver, mal ou mau, porquês', 'icon': '✍️', 'cue': 'haver'}, {'t': 'Vírgula, onde e aonde, acentos', 'icon': '✍️', 'cue': 'Vírgula'}, {'t': 'Poder de polícia, condescendência', 'icon': '⚖️', 'cue': 'polícia'}, {'t': 'Brasileiro nato, direitos sociais', 'icon': '⚖️', 'cue': 'nato'}], 'result': False,
          'narration': 'Nesta semana caiu: haver, mal ou mau, e os porquês. Vírgula, onde e aonde, e acentos. Poder de polícia e condescendência criminosa. Brasileiro nato e direitos sociais.', 'min_duration': 4.2},
         {'type': 'text', 'kicker': 'Como pegar', 'text': 'Manda APOSTILA no WhatsApp da bio', 'hl': 'APOSTILA', 'icon': '📲', 'pose': 'pointUp', 'narration': 'Manda apostila no WhatsApp da bio, que eu te mando uma amostra grátis.', 'min_duration': 3.0},
     ], sell='Amostra grátis no WhatsApp da bio.')

print(len(V), 'vídeos:', ', '.join(V))
