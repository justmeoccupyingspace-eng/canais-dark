"""Semana 48 (23–29/11) do Gabarito do Dia (TikTok/Reels, PT-BR): 14 vídeos, 12:00 e 19:00 BRT (paleta clara).
PLANO.md (07/11), caminho 3 do TikTok: conteúdo que a busca interna pede (inscrição, planilha 2027, prazo) + questões VUNESP de Português e Direito.
Fatos do edital: Edital de Abertura nº 02/2026 (DJE 19/10/2026) — R$ 6.782,54, inscrições 28/10 a 10/12/2026 no site da VUNESP, taxa R$ 81,
prova 14/03/2027 à tarde (5 h), 70 questões em 3 blocos, redação 0–40 (mín. 24), cadastro de reserva, 50 circunscrições da 2ª à 10ª RAJ, sem troca.
Isca "PLANILHA": planilha de estudos de 18 semanas (09/11 → 14/03/2027) enviada pelo WhatsApp (gera lista). Uso: python3 specs/week48.py -> specs/v3/c-3xx-*.json
Conteúdo de Direito do edital 2026 (Folha/QConcursos, 21/10/2026): Penal, Processual Penal, Processual Civil, Constitucional, Administrativo, Legislação Interna do TJSP.
Bases: CF art. 5º LXVIII–LXXII; CP arts. 316, 317, 333; Súmula 473 STF; CPC arts. 219 e 224; CPP art. 17; Acordo Ortográfico de 1990 (Base XVI, hífen)."""
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


# ---------------- 23/11 ----------------
q('c-360-encontro', '2026-11-23 12:00', 'PORTUGUÊS · EXPRESSÕES', '"Ao encontro de" ou "de encontro a"?', 'de encontro a', '✍️',
  'Ao encontro de ou de encontro a? Uma é concordar, a outra é bater de frente.',
  'O sentido da expressão destacada está correto em:', ['A decisão veio de encontro ao que pedimos, e comemoramos.', 'O carro foi ao encontro do muro e quebrou.', 'A proposta vai ao encontro do que defendemos, por isso a apoiamos.', 'A sentença veio ao encontro da lei e foi anulada.', 'Fomos de encontro aos amigos na saída.'], 'C',
  'Em qual frase o sentido está certo?',
  'Letra C: vai ao encontro do que defendemos', 'Letra C!',
  ('A diferença', 'diferença', ['Ao encontro de: a favor, em direção', 'De encontro a: contra, choque', 'Ir ao encontro de alguém: ir até ele', 'Bater de encontro ao muro'],
   'Ao encontro de é estar a favor, ou ir em direção a algo: a proposta vai ao encontro do que defendemos. De encontro a é oposição, choque: o carro foi de encontro ao muro.', ['favor', 'choque', 'direção', 'muro']),
  ('"Veio de encontro" e comemorou? Não combina', 'comemorou', 'Pegadinha: se veio de encontro ao pedido, foi contra. Não tem o que comemorar.'),
  '#portugues #semantica', 'Português do Escrevente TJSP: ao encontro de x de encontro a.', qsize=50, asize=38)
q('c-361-corrupcao', '2026-11-23 19:00', 'DIREITO PENAL · CRIMES CONTRA A ADM.', 'Servidor que aceita propina comete qual crime?', 'aceita propina', '⚖️',
  'O servidor não pediu nada, só aceitou a promessa de dinheiro. Já é crime?',
  'O funcionário público que aceita promessa de vantagem indevida, em razão da função, comete:', ['Concussão', 'Corrupção passiva', 'Corrupção ativa', 'Prevaricação', 'Nenhum crime, pois não recebeu'], 'B',
  'Qual é o crime?',
  'Letra B: corrupção passiva', 'Letra B!',
  ('Não confunda', 'confunda', ['Concussão (316): servidor EXIGE', 'Corrupção passiva (317): solicita, recebe ou aceita', 'Corrupção ativa (333): particular oferece', 'Basta aceitar a promessa'],
   'Concussão, artigo trezentos e dezesseis: o servidor exige. Corrupção passiva, trezentos e dezessete: solicita, recebe ou aceita promessa de vantagem indevida. Corrupção ativa, trezentos e trinta e três: é o particular que oferece ou promete.', ['exige', 'aceita', 'particular', 'promessa']),
  ('Não precisa receber o dinheiro', 'receber', 'Pegadinha: aceitar a promessa já consuma a corrupção passiva, mesmo que o dinheiro nunca chegue.'),
  '#direitopenal #crimescontraaadministracao', 'Direito Penal para o Escrevente TJSP: corrupção passiva x concussão x corrupção ativa.', qsize=50, asize=44)

# ---------------- 24/11 ----------------
q('c-362-cujo', '2026-11-24 12:00', 'PORTUGUÊS · PRONOME RELATIVO', '"Cujo o" existe?', 'Cujo o', '✍️',
  'O processo cujo o prazo venceu. Tem um erro aí. Achou?',
  'O pronome "cujo" está empregado de acordo com a norma-padrão em:', ['O réu cujo o advogado faltou foi ouvido.', 'A lei cuja a vigência começou ontem.', 'O servidor cujo nome saiu no diário tomou posse.', 'O processo que o prazo venceu foi arquivado.', 'A vara cujos o juiz é novo.'], 'C',
  'Em qual frase está certo?',
  'Letra C: cujo nome', 'Letra C!',
  ('Regras do cujo', 'cujo', ['Nunca vem com artigo depois', 'Concorda com o que vem depois', 'Indica posse: o nome DO servidor', 'Não troque por "que o"'],
   'Cujo nunca leva artigo depois: cujo nome, e não cujo o nome. Ele concorda com a palavra que vem depois: cuja vigência, cujos autos. E indica posse: o nome do servidor. Trocar por que o, como em o processo que o prazo venceu, está errado.', ['artigo', 'concorda', 'posse', 'que o']),
  ('"Cuja a" também está errado', 'Cuja a', 'Pegadinha: no feminino é igual. Cuja vigência, nunca cuja a vigência.'),
  '#portugues #pronomes', 'Português do Escrevente TJSP: pronome relativo cujo.', qsize=54, asize=42)
q('c-363-habeasdata', '2026-11-24 19:00', 'DIREITO CONSTITUCIONAL · REMÉDIOS', 'Dados errados no cadastro do governo: qual remédio?', 'qual remédio?', '⚖️',
  'Seus dados estão errados num cadastro do governo. Qual ação você usa?',
  'Para assegurar o conhecimento ou a retificação de dados pessoais em banco de dados de entidade governamental, cabe:', ['Habeas corpus', 'Mandado de segurança', 'Habeas data', 'Mandado de injunção', 'Ação popular'], 'C',
  'Qual é o remédio?',
  'Letra C: habeas data', 'Letra C!',
  ('Cada remédio, um problema', 'remédio', ['Habeas corpus: liberdade de locomoção', 'Habeas data: seus dados pessoais', 'Mandado de injunção: falta de norma', 'Mandado de segurança: o que sobra'],
   'Habeas corpus protege a liberdade de ir e vir. Habeas data, conhecer ou corrigir seus dados em cadastro público. Mandado de injunção, quando falta a norma que regulamenta um direito. E mandado de segurança protege direito líquido e certo que não cabe nos outros dois habeas.', ['ir e vir', 'dados', 'falta', 'líquido']),
  ('Dados de OUTRA pessoa: não é habeas data', 'OUTRA pessoa', 'Pegadinha: o habeas data é para informações sobre o próprio impetrante. Dados de terceiros, não.'),
  '#direitoconstitucional #remedios', 'Direito Constitucional para o Escrevente TJSP: habeas data e os remédios constitucionais.', qsize=50, asize=46)

# ---------------- 25/11 ----------------
q('c-364-preferir', '2026-11-25 12:00', 'PORTUGUÊS · REGÊNCIA VERBAL', '"Prefiro mais isso do que aquilo" está certo?', 'Prefiro mais', '✍️',
  'Prefiro mais estudar do que trabalhar. Dois erros numa frase só.',
  'A regência do verbo "preferir" está de acordo com a norma-padrão em:', ['Prefiro mais o fórum do que o cartório.', 'Prefiro o fórum do que o cartório.', 'Prefiro mil vezes o fórum ao cartório.', 'Prefiro o fórum ao cartório.', 'Prefiro antes o fórum que o cartório.'], 'D',
  'Em qual frase está certo?',
  'Letra D: prefiro o fórum ao cartório', 'Letra D!',
  ('Como usar preferir', 'preferir', ['Preferir uma coisa A outra', 'Sem "mais", sem "antes"', 'Sem "do que"', 'Prefiro estudar a trabalhar'],
   'Preferir é preferir uma coisa a outra: prefiro o fórum ao cartório. Não leva mais nem antes, porque preferir já é querer mais. E não leva do que. Com verbo também: prefiro estudar a trabalhar.', ['outra', 'antes', 'do que', 'estudar']),
  ('"Mil vezes" também é intensificador proibido', 'Mil vezes', 'Pegadinha: prefiro mil vezes também está fora da norma-padrão. Preferir não aceita intensificador.'),
  '#portugues #regencia', 'Português do Escrevente TJSP: regência do verbo preferir.', qsize=52, asize=44)
q('c-365-anulacao', '2026-11-25 19:00', 'DIREITO ADMINISTRATIVO · ATOS', 'Anular ou revogar um ato?', 'revogar', '⚖️',
  'A Administração descobre que um ato é ilegal. Ela anula ou revoga?',
  'Segundo a Súmula 473 do STF, a Administração pode:', ['Revogar seus atos ilegais, com efeitos retroativos.', 'Anular seus atos ilegais e revogar os inconvenientes, respeitados os direitos adquiridos.', 'Anular atos só com autorização do Judiciário.', 'Revogar atos de outro Poder por conveniência.', 'Apenas revogar, nunca anular, seus próprios atos.'], 'B',
  'Qual alternativa está certa?',
  'Letra B: anula o ilegal, revoga o inconveniente', 'Letra B!',
  ('Anulação x revogação', 'revogação', ['Anulação: ato ILEGAL', 'Revogação: conveniência e oportunidade', 'Judiciário pode anular, não revogar', 'Revogação respeita direito adquirido'],
   'Anulação é para ato ilegal, e pode ser feita pela própria Administração ou pelo Judiciário. Revogação é por conveniência e oportunidade, só pela própria Administração, respeitando os direitos adquiridos.', ['ilegal', 'conveniência', 'Judiciário', 'adquiridos']),
  ('Judiciário não revoga ato de outro Poder', 'não revoga', 'Pegadinha: o juiz pode anular um ato administrativo ilegal, mas não pode revogar por achar inconveniente.'),
  '#direitoadministrativo #atosadministrativos', 'Direito Administrativo para o Escrevente TJSP: anulação x revogação (Súmula 473 do STF).', qsize=50, asize=36)

# ---------------- 26/11 ----------------
info('c-366-faltam14', '2026-11-26 12:00', 'Inscrição do TJSP: faltam 14 dias',
     'Escrevente TJSP: as inscrições fecham em 10/12, no site da VUNESP. Taxa de R$ 81. A circunscrição escolhida não troca depois.',
     '#inscricao #edital #tjsp', [
         {'type': 'hook', 'kicker': 'Edital 2026', 'text': 'Faltam 14 dias para fechar a inscrição', 'hl': '14 dias', 'icon': '⏳', 'narration': 'Faltam catorze dias para fechar a inscrição do escrevente do TJ de São Paulo.', 'min_duration': 2.4},
         {'type': 'big', 'text': 'Último dia', 'hl': 'Último dia', 'big': '10/12', 'label': 'inscrição no site da VUNESP · taxa R$ 81', 'narration': 'O último dia é dez de dezembro, no site da VUNESP. A taxa é de oitenta e um reais.', 'min_duration': 2.8},
         {'type': 'steps', 'text': 'Antes de pagar o boleto', 'hl': 'boleto', 'rows': [{'t': 'Escolha a circunscrição', 'icon': '📍', 'cue': 'circunscrição'}, {'t': 'Ela não troca depois', 'icon': '🔒', 'cue': 'troca'}, {'t': 'Pague a taxa no prazo', 'icon': '💳', 'cue': 'prazo'}, {'t': 'Guarde o comprovante', 'icon': '🧾', 'cue': 'comprovante'}], 'result': False,
          'narration': 'Antes de pagar, escolhe bem a circunscrição, porque ela não troca depois. Paga a taxa dentro do prazo e guarda o comprovante.', 'min_duration': 3.8},
         {'type': 'text', 'kicker': 'Prova', 'text': '14/03/2027, à tarde', 'hl': '14/03/2027', 'icon': '📅', 'pose': 'pointUp', 'narration': 'E a prova é dia quatorze de março, à tarde.', 'min_duration': 2.2},
     ])
q('c-367-hifen', '2026-11-26 19:00', 'PORTUGUÊS · HÍFEN', 'Micro-ondas tem hífen? E autoescola?', 'hífen?', '✍️',
  'Micro-ondas tem hífen. Autoescola não tem. Antissocial dobra o s. Qual é a regra?',
  'A grafia está de acordo com o Acordo Ortográfico em:', ['auto-escola', 'anti-social', 'micro-ondas', 'contra-regra', 'micro ondas'], 'C',
  'Qual palavra está escrita certo?',
  'Letra C: micro-ondas', 'Letra C!',
  ('A regra do prefixo', 'prefixo', ['Vogal igual: hífen (micro-ondas)', 'Vogal diferente: junto (autoescola)', 'Antes de R ou S: dobra (antissocial)', 'Anti-inflamatório: vogal igual'],
   'Prefixo terminado em vogal: se a palavra começa com a mesma vogal, leva hífen, micro-ondas, anti-inflamatório. Se a vogal é diferente, vai junto, autoescola. E antes de r ou s, junta e dobra a letra: antissocial, contrarregra.', ['mesma vogal', 'diferente', 'dobra', 'contrarregra']),
  ('Contrarregra: junto e com rr', 'Contrarregra', 'Pegadinha: contra-regra perdeu o hífen. Agora é contrarregra, junto e com dois erres.'),
  '#portugues #ortografia', 'Português do Escrevente TJSP: hífen depois do Acordo Ortográfico.', qsize=54, asize=52)

# ---------------- 27/11 ----------------
q('c-368-prazos', '2026-11-27 12:00', 'DIREITO PROCESSUAL CIVIL · PRAZOS', 'Prazo de 15 dias conta sábado e domingo?', 'sábado e domingo?', '⚖️',
  'Prazo de quinze dias no processo civil. Sábado e domingo entram na conta?',
  'Segundo o CPC, na contagem de prazo processual em dias:', ['Computam-se os dias corridos.', 'Computam-se somente os dias úteis.', 'Inclui-se o dia do começo.', 'Exclui-se o dia do vencimento.', 'Os feriados contam normalmente.'], 'B',
  'Qual alternativa está certa?',
  'Letra B: só dias úteis', 'Letra B!',
  ('Como contar no CPC', 'contar', ['Só dias úteis (art. 219)', 'Exclui o dia do começo (art. 224)', 'Inclui o dia do vencimento', 'Vale para prazo processual'],
   'No CPC, o prazo em dias conta só os dias úteis, artigo duzentos e dezenove. E pelo artigo duzentos e vinte e quatro, exclui o dia do começo e inclui o dia do vencimento. Isso vale para prazo processual.', ['úteis', 'começo', 'vencimento', 'processual']),
  ('Processo penal conta dias corridos', 'penal', 'Pegadinha: a regra dos dias úteis é do CPC. No processo penal, o prazo corre em dias corridos.'),
  '#direitoprocessualcivil #cpc #prazos', 'Direito Processual Civil para o Escrevente TJSP: contagem de prazos (arts. 219 e 224 do CPC).', qsize=54, asize=46)
q('c-369-maismas', '2026-11-27 19:00', 'PORTUGUÊS · MAS OU MAIS', 'Mas ou mais?', 'mais?', '✍️',
  'Estudei, mais não passei. Errou. Mas por quê?',
  'O emprego de "mas" ou "mais" está correto em:', ['Estudei muito, mais não passei.', 'Ele é mas dedicado que o colega.', 'Quero mas tempo para revisar.', 'Revisei o edital, mas esqueci a taxa.', 'Faltam mas dez dias.'], 'D',
  'Em qual frase está certo?',
  'Letra D: revisei, mas esqueci', 'Letra D!',
  ('O truque', 'truque', ['Mas = porém (oposição)', 'Mais = quantidade (oposto de menos)', 'Troque por porém: se couber, é mas', 'Troque por menos: se couber, é mais'],
   'Mas é oposição, igual a porém: revisei, mas esqueci. Mais é quantidade, o contrário de menos: mais tempo, mais dedicado. O truque é trocar: se cabe porém, é mas. Se cabe menos, é mais.', ['porém', 'menos', 'trocar', 'cabe']),
  ('"Mais" com som de "mas" engana na fala', 'fala', 'Pegadinha: na fala os dois soam parecidos. Na escrita, troca por porém antes de decidir.'),
  '#portugues', 'Português do Escrevente TJSP: mas ou mais.', asize=44)

# ---------------- 28/11 ----------------
q('c-370-apartir', '2026-11-28 12:00', 'PORTUGUÊS · CRASE', '"À partir de amanhã" tem crase?', 'À partir', '✍️',
  'À partir de amanhã, com crase. Tá certo? Nunca.',
  'O uso do acento indicativo de crase está correto em:', ['À partir de amanhã, o prazo corre.', 'Começou à estudar ontem.', 'O prazo corre a partir de amanhã.', 'Ele foi à pé até o fórum.', 'Entregou o processo à ele.'], 'C',
  'Em qual frase está certo?',
  'Letra C: a partir de amanhã, sem crase', 'Letra C!',
  ('Onde nunca tem crase', 'nunca', ['Antes de verbo: a partir, a estudar', 'Antes de palavra masculina: a pé', 'Antes de pronome pessoal: a ele', 'Partir é verbo: a partir'],
   'Crase nunca vem antes de verbo: a partir, a estudar. Nem antes de palavra masculina: a pé. Nem antes de pronome pessoal: a ele. Partir é verbo, então a partir de amanhã fica sem crase.', ['verbo', 'masculina', 'pessoal', 'Partir']),
  ('À medida que tem crase; a partir, não', 'À medida', 'Pegadinha: à medida que leva crase, porque medida é palavra feminina. A partir não, porque partir é verbo.'),
  '#portugues #crase', 'Português do Escrevente TJSP: crase antes de verbo (a partir de).', qsize=54, asize=44)
q('c-371-inquerito', '2026-11-28 19:00', 'DIREITO PROCESSUAL PENAL · INQUÉRITO', 'O delegado pode arquivar o inquérito?', 'arquivar', '⚖️',
  'Não achou prova nenhuma. O delegado pode mandar arquivar o inquérito?',
  'Segundo o art. 17 do Código de Processo Penal, a autoridade policial:', ['Pode arquivar o inquérito se não houver provas.', 'Pode arquivar com autorização da vítima.', 'Não poderá mandar arquivar autos de inquérito.', 'Pode arquivar se o crime for de menor potencial.', 'Arquiva após trinta dias sem diligências.'], 'C',
  'Qual alternativa está certa?',
  'Letra C: não pode arquivar', 'Letra C!',
  ('O delegado nunca arquiva', 'nunca', ['Art. 17 do CPP: não pode arquivar', 'Nem por falta de provas', 'Nem com pedido da vítima', 'Arquivamento passa pelo Ministério Público'],
   'O artigo dezessete do CPP é direto: a autoridade policial não poderá mandar arquivar autos de inquérito. Nem por falta de provas, nem a pedido da vítima. O arquivamento passa pelo Ministério Público.', ['dezessete', 'provas', 'vítima', 'Ministério']),
  ('Falta de prova não muda nada', 'Falta de prova', 'Pegadinha: a alternativa mais tentadora é a da falta de provas. Mesmo assim, o delegado não arquiva.'),
  '#direitoprocessualpenal #inquerito', 'Direito Processual Penal para o Escrevente TJSP: arquivamento do inquérito (art. 17 do CPP).', qsize=54, asize=42)

# ---------------- 29/11 ----------------
q('c-372-anexo', '2026-11-29 12:00', 'PORTUGUÊS · CONCORDÂNCIA NOMINAL', '"Segue anexo as cópias" está certo?', 'anexo', '✍️',
  'Segue anexo as cópias. Todo mundo escreve assim no e-mail. Tá errado.',
  'A concordância está de acordo com a norma-padrão em:', ['Segue anexo as cópias do processo.', 'Seguem anexo as certidões.', 'Seguem anexas as certidões.', 'Segue anexa os documentos.', 'Seguem em anexas as cópias.'], 'C',
  'Em qual frase está certo?',
  'Letra C: seguem anexas as certidões', 'Letra C!',
  ('Anexo concorda', 'concorda', ['Anexo é adjetivo: concorda', 'Anexas as certidões, anexos os laudos', 'O verbo também: seguem', 'Em anexo: não varia'],
   'Anexo é adjetivo, então concorda com o que vem junto: anexas as certidões, anexos os laudos. O verbo também vai ao plural: seguem. E em anexo, com a preposição, não varia: seguem em anexo as cópias.', ['adjetivo', 'laudos', 'seguem', 'preposição']),
  ('"Em anexo" não vai ao plural', 'Em anexo', 'Pegadinha: em anexas está errado. Com em na frente, fica sempre em anexo.'),
  '#portugues #concordancia', 'Português do Escrevente TJSP: concordância de anexo.', qsize=54, asize=44)
info('c-373-apostila', '2026-11-29 19:00', '182 questões comentadas: amostra grátis',
     'Apostila do Escrevente TJSP com 182 questões comentadas, no estilo das questões desta semana. Amostra grátis no WhatsApp da bio: manda APOSTILA.',
     '#apostila #questoes #tjsp', [
         {'type': 'hook', 'kicker': 'Escrevente TJSP', 'text': '182 questões comentadas', 'hl': '182', 'icon': '📚', 'narration': 'Gostou das questões da semana? Tem cento e oitenta e duas, todas comentadas.', 'min_duration': 2.6},
         {'type': 'steps', 'text': 'Nesta semana caiu', 'hl': 'semana', 'rows': [{'t': 'Cujo, preferir, anexo', 'icon': '✍️', 'cue': 'Cujo'}, {'t': 'Hífen, crase, mas ou mais', 'icon': '✍️', 'cue': 'Hífen'}, {'t': 'Corrupção passiva, habeas data', 'icon': '⚖️', 'cue': 'Corrupção'}, {'t': 'Prazos do CPC, inquérito', 'icon': '⚖️', 'cue': 'Prazos'}], 'result': False,
          'narration': 'Nesta semana caiu: cujo, preferir e anexo. Hífen, crase e mas ou mais. Corrupção passiva e habeas data. Prazos do CPC e arquivamento do inquérito.', 'min_duration': 4.2},
         {'type': 'text', 'kicker': 'Como pegar', 'text': 'Manda APOSTILA no WhatsApp da bio', 'hl': 'APOSTILA', 'icon': '📲', 'pose': 'pointUp', 'narration': 'Manda apostila no WhatsApp da bio, que eu te mando uma amostra grátis.', 'min_duration': 3.0},
     ], sell='Amostra grátis no WhatsApp da bio.')

print(len(V), 'vídeos:', ', '.join(V))
