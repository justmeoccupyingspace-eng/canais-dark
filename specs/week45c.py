"""Semana 45 (02–08/11) do Gabarito do Dia (TikTok/Reels, PT-BR): 14 vídeos, 12:30 e 19:30 BRT.
Foco (análise da semana 44): questões de Português da VUNESP + salário/edital, com palavras-chave na legenda.
Fatos do edital: Edital de Abertura nº 02/2026 (DJE 19/10/2026) — R$ 6.782,54 (ref. mar/2026), inscrições 28/10 a 10/12/2026,
taxa R$ 81, prova 14/03/2027 à tarde (5 h), 70 questões em 3 blocos, redação 0–40 (mín. 24), cadastro de reserva,
50 circunscrições da 2ª à 10ª RAJ (capital fora), sem troca de circunscrição depois. Uso: python3 specs/week45c.py -> specs/v3/c-3xx-*.json"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v3')
os.makedirs(OUT, exist_ok=True)
TAGS = '#concursotjsp #escreventetjsp #concursopublico #vunesp #concurseiro'
SELL = 'Apostila com 182 questões comentadas: amostra grátis no WhatsApp da bio.'
END = {'type': 'end', 'text': 'Siga: 1 questão do TJSP por dia', 'hl': '1 questão', 'brand': 'GABARITO DO DIA', 'narration': 'Segue: uma questão por dia até a prova.', 'min_duration': 2.0}
V = []


def save(name, spec):
    json.dump(spec, open(f'{OUT}/{name}.json', 'w'), ensure_ascii=False, indent=1)
    V.append(name)


def q(name, at, label, hook_text, hook_hl, hook_icon, hook_n, question, alts, letter, q_n, ans_text, ans_n, steps, trap, tags, caption, qsize=56, asize=48):
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
    scenes.append(END)
    save(name, {'channel': 'gabarito', 'style': 'v3', 'rate': '+5%', 'title': hook_text, 'publish': {'channel': 'C', 'privacy': 'public', 'tiktok_at': at},
                'tiktok': f"{caption} Comenta a letra! {SELL}\n{TAGS} {tags}", 'scenes': scenes})


def info(name, at, title, caption, tags, scenes):
    save(name, {'channel': 'gabarito', 'style': 'v3', 'rate': '+4%', 'title': title, 'publish': {'channel': 'C', 'privacy': 'public', 'tiktok_at': at},
                'tiktok': f"{caption} {SELL}\n{TAGS} {tags}", 'scenes': scenes + [END]})


# ---------------- 02/11 ----------------
info('c-318-salario', '2026-11-02 12:30', 'Quanto ganha um Escrevente do TJSP?',
     'Salário do Escrevente TJSP 2026: R$ 6.782,54 iniciais, com ensino médio e 40 h semanais, mais auxílios. Edital é de cadastro de reserva.',
     '#salario #edital #tjsp', [
         {'type': 'hook', 'kicker': 'Edital 2026', 'text': 'Quanto ganha um Escrevente do TJSP?', 'hl': 'Quanto ganha', 'icon': '💰', 'narration': 'Quanto ganha um escrevente do TJ de São Paulo?', 'min_duration': 2.4},
         {'type': 'big', 'text': 'Salário inicial', 'hl': 'Salário', 'big': 'R$ 6.782', 'label': 'só com ensino médio · 40 h semanais', 'narration': 'Salário inicial de seis mil setecentos e oitenta e dois reais. Só com ensino médio.', 'min_duration': 3.0},
         {'type': 'steps', 'text': 'E ainda tem', 'hl': 'ainda tem', 'rows': [{'t': 'Auxílio-alimentação', 'icon': '🍽️', 'cue': 'alimentação'}, {'t': 'Auxílio-saúde', 'icon': '🏥', 'cue': 'saúde'}, {'t': 'Auxílio-transporte', 'icon': '🚌', 'cue': 'transporte'}], 'result': False,
          'narration': 'E ainda tem auxílio para alimentação, para saúde e para transporte.', 'min_duration': 3.0},
         {'type': 'text', 'kicker': 'Atenção', 'text': 'O edital é de cadastro de reserva', 'hl': 'cadastro de reserva', 'icon': '📋', 'pose': 'shrug', 'narration': 'Atenção: o edital é de cadastro de reserva. Quem passa entra na fila de convocação.', 'min_duration': 3.0},
         {'type': 'big', 'text': 'Inscrições até', 'hl': 'Inscrições', 'big': '10/12', 'label': 'taxa de R$ 81 · site da VUNESP', 'narration': 'As inscrições vão até dez de dezembro, no site da VUNESP.', 'min_duration': 2.6},
     ])
q('c-319-concordancia', '2026-11-02 19:30', 'PORTUGUÊS · CONCORDÂNCIA', 'Haviam ou havia candidatos?', 'havia', '✍️',
  'Haviam ou havia muitos candidatos? Essa a VUNESP adora.',
  'Está de acordo com a norma-padrão a concordância verbal em:', ['Fazem dois anos que o edital não sai.', 'Haviam muitos candidatos na sala.', 'Devem haver novas vagas no ano que vem.', 'Existem muitas dúvidas sobre o edital.', 'Houveram problemas na inscrição.'], 'D',
  'Em qual frase a concordância está certa?',
  'Letra D: existem muitas dúvidas', 'Letra D!',
  ('Os impessoais', 'impessoais', ['Haver (= existir): sempre singular', 'Fazer (tempo): sempre singular', 'Existir concorda: existem dúvidas'],
   'Haver, no sentido de existir, fica sempre no singular. Fazer, indicando tempo, também. Já existir concorda normalmente: existem dúvidas.', ['haver', 'fazer', 'existir']),
  ('"Deve haver": o auxiliar também fica no singular', 'singular', 'E cuidado: deve haver. O auxiliar também fica no singular.'),
  '#portugues #concordancia', 'Português do Escrevente TJSP: concordância com haver e fazer.', asize=42)

# ---------------- 03/11 ----------------
q('c-320-acentuacao', '2026-11-03 12:30', 'PORTUGUÊS · ACENTUAÇÃO', 'Ideia ou idéia? Voo ou vôo?', 'Voo ou vôo?', '✍️',
  'Ideia com acento ou sem? O acordo ortográfico ainda pega muita gente.',
  'De acordo com o Acordo Ortográfico vigente, está correta a grafia em:', ['Tive uma idéia para o recurso.', 'O vôo atrasou duas horas.', 'Foi um esforço heróico.', 'Eles têm direito à vaga.', 'Ele sempre pára no sinal.'], 'D',
  'Qual grafia está certa pelo acordo ortográfico?',
  'Letra D: eles têm', 'Letra D!',
  ('O que caiu com o acordo', 'caiu', ['Ideia, heroico: sem acento', 'Voo, leem: sem acento', 'Para (verbo): sem acento', 'Têm (plural): continua'],
   'Ideia e heroico perderam o acento. Voo e leem também. O para, do verbo parar, também. Mas o têm, no plural, continua com acento.', ['ideia', 'voo', 'para', 'mas']),
  ('Herói e papéis mantêm o acento', 'mantêm', 'Pegadinha: herói e papéis continuam com acento, porque são oxítonas.'),
  '#portugues #acordoortografico', 'Português do Escrevente TJSP: acentuação pelo acordo ortográfico.', asize=44)
q('c-321-concussao', '2026-11-03 19:30', 'DIREITO PENAL · CRIMES CONTRA A ADM.', 'Exigir propina é qual crime?', 'qual crime?', '⚖️',
  'O funcionário exigiu propina. Qual é o crime?',
  'O funcionário público que exige, para si, vantagem indevida, em razão da função, comete o crime de:', ['peculato', 'concussão', 'corrupção passiva', 'prevaricação', 'condescendência criminosa'], 'B',
  'O funcionário público que exige vantagem indevida em razão da função comete qual crime?',
  'Letra B: concussão', 'Letra B, concussão!',
  ('O verbo decide', 'verbo', ['Exigir: concussão (art. 316)', 'Solicitar ou receber: corrupção passiva (art. 317)', 'Apropriar-se: peculato (art. 312)'],
   'Quem decide é o verbo. Exigir é concussão. Solicitar ou receber é corrupção passiva. E se apropriar do que tem em razão do cargo é peculato.', ['quem', 'exigir', 'solicitar', 'e']),
  ('Solicitar não é exigir', 'não é exigir', 'A pegadinha clássica: solicitar não é exigir.'),
  '#direitopenal', 'Direito Penal do Escrevente TJSP: concussão ou corrupção passiva?', asize=46)

# ---------------- 04/11 ----------------
info('c-322-prova', '2026-11-04 12:30', 'Como é a prova do Escrevente TJSP?',
     'Prova do Escrevente TJSP 2027: 70 questões em 3 blocos e redação. Precisa acertar metade de Português e de Direito e tirar 24 de 40 na redação.',
     '#edital #provatjsp #redacao', [
         {'type': 'hook', 'kicker': 'Edital 2026', 'text': 'Como é a prova do Escrevente TJSP?', 'hl': 'Como é a prova', 'icon': '📝', 'narration': 'Como é a prova do escrevente do TJ de São Paulo?', 'min_duration': 2.4},
         {'type': 'big', 'text': 'Prova objetiva', 'hl': 'objetiva', 'big': '70', 'label': 'questões de múltipla escolha · 5 horas', 'narration': 'São setenta questões de múltipla escolha, em até cinco horas.', 'min_duration': 2.8},
         {'type': 'steps', 'text': 'Três blocos', 'hl': 'Três', 'rows': [{'t': 'Português: elimina', 'icon': '✍️', 'cue': 'português'}, {'t': 'Direito: elimina', 'icon': '⚖️', 'cue': 'direito'}, {'t': 'Conhecimentos Gerais: só classifica', 'icon': '🧠', 'cue': 'conhecimentos'}], 'result': False,
          'narration': 'Três blocos: português e direito eliminam. Conhecimentos gerais só classifica.', 'min_duration': 3.2},
         {'type': 'text', 'kicker': 'Pra não ser eliminado', 'text': 'Acerte metade de Português e de Direito', 'hl': 'metade', 'icon': '🎯', 'pose': 'pointUp', 'narration': 'Pra não ser eliminado, acerte pelo menos metade de português e de direito.', 'min_duration': 2.8},
         {'type': 'big', 'text': 'Redação', 'hl': 'Redação', 'big': '24/40', 'label': 'nota mínima · no mesmo dia, 14/03/2027', 'narration': 'E tem redação, no mesmo dia: precisa de vinte e quatro de quarenta pontos.', 'min_duration': 3.0},
     ])
q('c-323-porques', '2026-11-04 19:30', 'PORTUGUÊS · PORQUÊS', 'Por que, porque, porquê ou por quê?', 'porquê', '✍️',
  'Os quatro porquês. Acerta essa?',
  'O emprego do "porquê" está correto em:', ['Não sei porque ele faltou à prova.', 'Ele faltou por que estava doente.', 'Ninguém entendeu o porquê da decisão.', 'Você faltou porquê?', 'Por quê você não veio ontem?'], 'C',
  'Em qual frase o porquê está certo?',
  'Letra C: o porquê da decisão', 'Letra C!',
  ('Cada um no seu lugar', 'seu lugar', ['Por que: pergunta (por qual motivo)', 'Porque: resposta (pois)', 'Porquê: com artigo (o motivo)', 'Por quê: no fim da frase'],
   'Por que, separado, é pergunta. Porque, junto, é resposta. Porquê com acento vem com artigo: o porquê. E por quê, separado e com acento, no fim da frase.', ['separado', 'junto', 'acento', 'fim']),
  ('"Não sei por que": pergunta escondida', 'pergunta escondida', 'Não sei por que ele faltou: é uma pergunta escondida, então é separado.'),
  '#portugues', 'Português do Escrevente TJSP: os quatro porquês.', asize=44)

# ---------------- 05/11 ----------------
q('c-324-malmau', '2026-11-05 12:30', 'PORTUGUÊS · MAL OU MAU', 'Mal humor ou mau humor?', 'mau humor?', '✍️',
  'Mal ou mau? Tem um truque que nunca falha.',
  'Está correto o emprego de "mal" ou "mau" em:', ['O servidor agiu mau com o colega.', 'Ele é um mal exemplo para os novatos.', 'Mau chegou, já foi chamado.', 'O réu estava de mau humor na audiência.', 'Aquele foi um ano mal para o comércio.'], 'D',
  'Em qual frase o mal ou mau está certo?',
  'Letra D: de mau humor', 'Letra D!',
  ('O truque do contrário', 'contrário', ['Mau: contrário de bom', 'Mal: contrário de bem', 'Mal também = assim que'],
   'O truque é o contrário. Mau é o contrário de bom: bom humor, mau humor. Mal é o contrário de bem. E mal também pode ser assim que.', ['truque', 'mau', 'mal', 'e']),
  None,
  '#portugues', 'Português do Escrevente TJSP: mal ou mau?', asize=44)
q('c-325-ondeaonde', '2026-11-05 19:30', 'PORTUGUÊS · ONDE OU AONDE', 'Onde ou aonde você vai?', 'aonde', '✍️',
  'Onde você vai ou aonde você vai?',
  'De acordo com a norma-padrão, está correto o emprego de "onde" ou "aonde" em:', ['Aonde você estuda para o concurso?', 'Onde você vai depois da prova?', 'Aonde fica o fórum da cidade?', 'Aonde você quer chegar com isso?', 'A cidade aonde moro é pequena.'], 'D',
  'Em qual frase o onde ou aonde está certo?',
  'Letra D: aonde quer chegar', 'Letra D!',
  ('Tem movimento?', 'movimento?', ['Aonde: verbo com A (ir, chegar)', 'Onde: lugar parado (estar, ficar, morar)'],
   'A pergunta é: tem movimento? Aonde vem com verbos que pedem a, como ir e chegar. Onde é lugar parado: estar, ficar, morar.', ['aonde', 'onde']),
  ('"Onde você vai?" é o erro mais comum', 'mais comum', 'Onde você vai é o erro mais comum. O certo é aonde.'),
  '#portugues', 'Português do Escrevente TJSP: onde ou aonde?', asize=44)

# ---------------- 06/11 ----------------
info('c-326-circunscricao', '2026-11-06 12:30', 'Escolheu a circunscrição errada?',
     'Escrevente TJSP 2026: 50 circunscrições no interior e no litoral (capital fora), e não dá pra trocar depois da inscrição. Inscrições até 10/12.',
     '#edital #circunscricao #tjsp', [
         {'type': 'hook', 'kicker': 'Antes de se inscrever', 'text': 'Escolheu a circunscrição errada?', 'hl': 'errada?', 'icon': '📍', 'narration': 'Cuidado na hora de escolher a circunscrição do escrevente TJSP.', 'min_duration': 2.4},
         {'type': 'text', 'kicker': 'Regra do edital', 'text': 'Não dá pra trocar depois', 'hl': 'trocar depois', 'icon': '🔒', 'pose': 'shock', 'narration': 'Pelo edital, não dá pra trocar depois da inscrição.', 'min_duration': 2.4},
         {'type': 'big', 'text': 'São', 'hl': 'São', 'big': '50', 'label': 'circunscrições · da 2ª à 10ª região', 'narration': 'São cinquenta circunscrições, da segunda à décima região administrativa.', 'min_duration': 2.6},
         {'type': 'steps', 'text': 'Algumas delas', 'hl': 'Algumas', 'rows': [{'t': 'Campinas e Sorocaba', 'icon': '📍', 'cue': 'campinas'}, {'t': 'Santos e São José dos Campos', 'icon': '📍', 'cue': 'santos'}, {'t': 'Ribeirão Preto e Bauru', 'icon': '📍', 'cue': 'ribeirão'}], 'result': False,
          'narration': 'Tem Campinas e Sorocaba, Santos e São José dos Campos, Ribeirão Preto e Bauru, entre outras.', 'min_duration': 3.2},
         {'type': 'text', 'kicker': 'Atenção', 'text': 'A capital ficou de fora', 'hl': 'capital', 'icon': '🏙️', 'pose': 'shrug', 'narration': 'E a capital ficou de fora deste edital.', 'min_duration': 2.2},
     ])
q('c-327-haa', '2026-11-06 19:30', 'PORTUGUÊS · HÁ OU A', 'Há dois anos ou a dois anos?', 'Há', '✍️',
  'Há dois anos ou a dois anos? Tem um teste rápido.',
  'Está correto o emprego de "há" ou "a" em:', ['Daqui há dois meses começa a prova.', 'Estudo para o concurso a dois anos.', 'O relator saiu há pouco.', 'O fórum fica há dois quarteirões.', 'Há partir de hoje, vou estudar.'], 'C',
  'Em qual frase o há ou a está certo?',
  'Letra C: saiu há pouco', 'Letra C!',
  ('Troca por faz', 'faz', ['Deu certo com "faz"? É HÁ', 'Futuro ou distância: A', 'Daqui a, a partir de'],
   'Troca por faz. Saiu faz pouco? Funcionou: é há. Futuro ou distância é a sem h: daqui a dois meses, a dois quarteirões, a partir de hoje.', ['troca', 'futuro', 'daqui']),
  None,
  '#portugues', 'Português do Escrevente TJSP: há ou a?', asize=44)

# ---------------- 07/11 ----------------
q('c-328-virgula', '2026-11-07 12:30', 'PORTUGUÊS · PONTUAÇÃO', 'Essa vírgula está errada?', 'vírgula', '✍️',
  'A vírgula que mais reprova na VUNESP.',
  'A vírgula está empregada de acordo com a norma-padrão em:', ['Os candidatos aprovados, serão convocados.', 'O juiz, analisou o processo com cuidado.', 'Em março, os candidatos farão a prova.', 'O edital prevê, cadastro de reserva.', 'Quem estudou, vai passar.'], 'C',
  'Em qual frase a vírgula está certa?',
  'Letra C: Em março, os candidatos...', 'Letra C!',
  ('A regra de ouro', 'ouro', ['Nunca separe sujeito e verbo', 'Nunca separe verbo e complemento', 'Pode: termo deslocado no início'],
   'A regra de ouro: nunca separe sujeito e verbo. Nem verbo e complemento. Pode usar vírgula num termo deslocado pro início, como em março.', ['regra', 'nem', 'pode']),
  ('"Quem estudou" é o sujeito: sem vírgula', 'sem vírgula', 'Pegadinha: quem estudou é o sujeito inteiro. Então, sem vírgula.'),
  '#portugues #pontuacao', 'Português do Escrevente TJSP: vírgula entre sujeito e verbo.', asize=42)
q('c-329-vendese', '2026-11-07 19:30', 'PORTUGUÊS · VOZ PASSIVA', 'Vende-se casas ou vendem-se?', 'vendem-se?', '✍️',
  'Vende-se casas ou vendem-se casas?',
  'A concordância está de acordo com a norma-padrão em:', ['Aluga-se salas comerciais.', 'Precisam-se de escreventes.', 'Consertam-se computadores.', 'Fez-se vários reparos no prédio.', 'Vende-se apartamentos no centro.'], 'C',
  'Em qual frase a concordância com se está certa?',
  'Letra C: consertam-se computadores', 'Letra C!',
  ('Tem preposição?', 'preposição?', ['Sem preposição: concorda (vendem-se casas)', 'Com preposição: singular (precisa-se de)'],
   'Olha se tem preposição. Sem preposição, o verbo concorda: vendem-se casas, consertam-se computadores. Com preposição, fica no singular: precisa-se de escreventes.', ['sem', 'com']),
  ('"Precisam-se de" está errado', 'errado', 'Precisam-se de está errado: com de, fica precisa-se.'),
  '#portugues #concordancia', 'Português do Escrevente TJSP: vende-se ou vendem-se?', asize=44)

# ---------------- 08/11 ----------------
q('c-330-crasehora', '2026-11-08 12:30', 'PORTUGUÊS · CRASE', 'Às 13h ou as 13h?', 'Às 13h', '✍️',
  'Crase de novo, porque é a que mais cai.',
  'O sinal indicativo de crase está correto em:', ['Começou à chover durante a prova.', 'Os portões fecham às 13h.', 'Entregou o documento à ele.', 'Fez a prova à lápis.', 'Ficou cara à cara com o fiscal.'], 'B',
  'Em qual frase a crase está certa?',
  'Letra B: fecham às 13h', 'Letra B!',
  ('Onde nunca tem crase', 'nunca', ['Antes de verbo: a chover', 'Antes de pronome pessoal: a ele', 'Antes de masculino: a lápis', 'Palavras repetidas: cara a cara'],
   'Nunca tem crase antes de verbo, de pronome pessoal e de palavra masculina. Nem entre palavras repetidas. Mas hora marcada tem: às treze horas.', ['nunca', 'pessoal', 'masculina', 'nem']),
  None,
  '#portugues #crase', 'Português do Escrevente TJSP: crase antes de hora.', asize=44)
q('c-331-senao', '2026-11-08 19:30', 'PORTUGUÊS · SENÃO OU SE NÃO', 'Senão ou se não?', 'se não?', '✍️',
  'Senão junto ou se não separado?',
  'Está correto o emprego de "senão" ou "se não" em:', ['Estude, se não vai reprovar.', 'Não fazia nada senão estudar.', 'Senão chover, irei à prova.', 'Não estudei, se não teria passado.', 'Senão houver vagas, haverá cadastro.'], 'B',
  'Em qual frase o senão ou se não está certo?',
  'Letra B: nada senão estudar', 'Letra B!',
  ('O teste', 'teste', ['Senão = caso contrário / a não ser', 'Se não = caso não'],
   'Senão, junto, quer dizer caso contrário ou a não ser. Se não, separado, quer dizer caso não: se não chover.', ['senão', 'se']),
  ('"Estude, senão vai reprovar": junto', 'junto', 'Estude, senão vai reprovar: é caso contrário, então é junto.'),
  '#portugues', 'Português do Escrevente TJSP: senão ou se não?', asize=44)

print('\n'.join(V))
