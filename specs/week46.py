"""Semana 46 (09–15/11) do Gabarito do Dia (TikTok/Reels, PT-BR): 14 vídeos, 12:00 e 19:00 BRT (paleta clara).
PLANO.md (07/11), caminho 3 do TikTok: conteúdo que a busca interna pede (inscrição, planilha 2027, prazo) + questões VUNESP de Português e Direito.
Fatos do edital: Edital de Abertura nº 02/2026 (DJE 19/10/2026) — R$ 6.782,54, inscrições 28/10 a 10/12/2026 no site da VUNESP, taxa R$ 81,
prova 14/03/2027 à tarde (5 h), 70 questões em 3 blocos, redação 0–40 (mín. 24), cadastro de reserva, 50 circunscrições da 2ª à 10ª RAJ, sem troca.
Isca "PLANILHA": planilha de estudos de 18 semanas (09/11 → 14/03/2027) enviada pelo WhatsApp (gera lista). Uso: python3 specs/week46.py -> specs/v3/c-3xx-*.json"""
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


# ---------------- 09/11 ----------------
info('c-332-inscricao', '2026-11-09 12:00', 'Inscrição do TJSP: passo a passo',
     'Inscrição do Escrevente TJSP 2026, passo a passo: site da VUNESP, taxa de R$ 81, prazo 10/12, e a escolha da circunscrição que não pode ser trocada depois.',
     '#inscricao #edital #tjsp', [
         {'type': 'hook', 'kicker': 'Edital 2026', 'text': 'Inscrição do TJSP: passo a passo', 'hl': 'passo a passo', 'icon': '📝', 'narration': 'Inscrição do escrevente do TJ de São Paulo, passo a passo, em trinta segundos.', 'min_duration': 2.4},
         {'type': 'steps', 'text': 'Como se inscrever', 'hl': 'inscrever', 'rows': [{'t': 'Site da VUNESP: área do candidato', 'icon': '💻', 'cue': 'VUNESP'}, {'t': 'Dados pessoais e escolaridade', 'icon': '🪪', 'cue': 'dados'}, {'t': 'Escolha da circunscrição', 'icon': '📍', 'cue': 'circunscrição'}, {'t': 'Boleto de R$ 81 e pagamento', 'icon': '💳', 'cue': 'boleto'}], 'result': False,
          'narration': 'Entre no site da VUNESP, na área do candidato. Preencha os dados pessoais e a escolaridade. Escolha a circunscrição. Gere o boleto de oitenta e um reais e pague.', 'min_duration': 4.0},
         {'type': 'text', 'kicker': 'Atenção', 'text': 'A circunscrição não pode ser trocada depois', 'hl': 'não pode ser trocada', 'icon': '⚠️', 'pose': 'shock', 'narration': 'Atenção: a circunscrição não pode ser trocada depois. Veja onde você consegue trabalhar de verdade.', 'min_duration': 3.0},
         {'type': 'big', 'text': 'Prazo', 'hl': 'Prazo', 'big': '10/12', 'label': 'inscrições até 10 de dezembro · prova 14/03/2027', 'narration': 'O prazo vai até dez de dezembro. A prova é em quatorze de março.', 'min_duration': 2.8},
     ])
q('c-333-regencia', '2026-11-09 19:00', 'PORTUGUÊS · REGÊNCIA', 'Assistir o filme ou ao filme?', 'ao filme?', '✍️',
  'Assistir o filme ou assistir ao filme? A VUNESP cobra isso direto.',
  'A regência verbal está de acordo com a norma-padrão em:', ['Assistimos o filme ontem à noite.', 'Prefiro estudar do que trabalhar.', 'O juiz assistiu ao julgamento inteiro.', 'Ela chegou no fórum atrasada.', 'Obedeça o regulamento do concurso.'], 'C',
  'Em qual frase a regência está certa?',
  'Letra C: assistiu ao julgamento', 'Letra C!',
  ('Regências que caem', 'caem', ['Assistir (ver): assistir AO filme', 'Preferir: preferir X A Y', 'Chegar: chegar AO fórum', 'Obedecer: obedecer AO regulamento'],
   'Assistir, no sentido de ver, pede a preposição a: assistir ao filme. Preferir é uma coisa a outra, nunca do que. Chegar ao fórum, com a. E obedecer ao regulamento, também com a.', ['Assistir', 'Preferir', 'Chegar', 'obedecer']),
  ('"Assistir o doente" existe: significa ajudar', 'ajudar', 'Pegadinha: assistir o doente, sem a, existe. Mas aí significa ajudar, prestar assistência.'),
  '#portugues #regencia', 'Português do Escrevente TJSP: regência verbal (assistir, preferir, chegar, obedecer).', asize=44)

# ---------------- 10/11 ----------------
q('c-334-crase', '2026-11-10 12:00', 'PORTUGUÊS · CRASE', 'Crase antes de "ela"?', 'Crase', '✍️',
  'Entreguei o documento à ela. Tem crase aí?',
  'O emprego do acento indicativo de crase está correto em:', ['Entreguei o documento à ela.', 'Fui à pé até o cartório.', 'Refiro-me às pessoas citadas no processo.', 'Ele chegou à casa antes das oito.', 'Viajaram à Bahia nas férias.'], 'C',
  'Em qual frase a crase está certa?',
  'Letra C: refiro-me às pessoas', 'Letra C!',
  ('Onde não tem crase', 'não tem', ['Antes de pronome pessoal: a ela', 'Antes de palavra masculina: a pé', 'Casa sem adjetivo: chegou a casa', 'Plural com artigo: às pessoas ✔'],
   'Não tem crase antes de pronome pessoal: a ela. Nem antes de palavra masculina: a pé. Casa, sem adjetivo, também não: chegou a casa. Já às pessoas tem, porque o verbo pede a e a palavra aceita o artigo.', ['pronome', 'masculina', 'Casa', 'pessoas']),
  ('"Viajaram à Bahia" está certo: Bahia aceita artigo', 'Bahia', 'E a letra E? Viajaram à Bahia está certo, porque se diz a Bahia. O erro era não ter o acento no enunciado original.'),
  '#portugues #crase', 'Português do Escrevente TJSP: crase antes de pronome, palavra masculina e nome de lugar.', asize=44)
info('c-335-planilha', '2026-11-10 19:00', 'Planilha de estudos até a prova: grátis',
     'Planilha de estudos para o Escrevente TJSP 2027: 18 semanas até a prova de 14/03, com Português, Direito e redação distribuídos. Comenta PLANILHA que eu mando no WhatsApp.',
     '#planilha #cronograma #estudos', [
         {'type': 'hook', 'kicker': 'TJSP 2027', 'text': 'Planilha de estudos até a prova: grátis', 'hl': 'grátis', 'icon': '📅', 'narration': 'Planilha de estudos até a prova do TJ de São Paulo, de graça.', 'min_duration': 2.4},
         {'type': 'big', 'text': 'Faltam', 'hl': 'Faltam', 'big': '18 semanas', 'label': 'de hoje até a prova de 14/03/2027', 'narration': 'Faltam dezoito semanas até a prova. Dá tempo, se tiver plano.', 'min_duration': 2.8},
         {'type': 'steps', 'text': 'O que tem na planilha', 'hl': 'planilha', 'rows': [{'t': 'Semana a semana, matéria por matéria', 'icon': '🗓️', 'cue': 'Semana'}, {'t': 'Português e Direito todo dia', 'icon': '✍️', 'cue': 'todo dia'}, {'t': 'Uma redação por semana', 'icon': '📝', 'cue': 'redação'}, {'t': 'Revisão nas últimas 3 semanas', 'icon': '🔁', 'cue': 'Revisão'}], 'result': False,
          'narration': 'Semana a semana, matéria por matéria. Português e direito todo dia. Uma redação por semana. E revisão nas últimas três semanas.', 'min_duration': 4.0},
         {'type': 'text', 'kicker': 'Como pegar', 'text': 'Comenta PLANILHA que eu mando no WhatsApp', 'hl': 'PLANILHA', 'icon': '📲', 'pose': 'pointUp', 'narration': 'Comenta planilha aqui embaixo, e eu te mando no WhatsApp da bio.', 'min_duration': 3.0},
     ], sell='Comenta PLANILHA e pega a sua no WhatsApp da bio.')

# ---------------- 11/11 ----------------
q('c-336-principios', '2026-11-11 12:00', 'DIREITO CONSTITUCIONAL · ADM. PÚBLICA', 'Qual NÃO é princípio do art. 37?', 'NÃO é', '⚖️',
  'Legalidade, impessoalidade, moralidade, publicidade, eficiência. Qual desses não está no artigo trinta e sete?',
  'NÃO é princípio expresso da Administração Pública no caput do art. 37 da Constituição:', ['Legalidade', 'Impessoalidade', 'Moralidade', 'Proporcionalidade', 'Eficiência'], 'D',
  'Qual não é princípio expresso do artigo trinta e sete?',
  'Letra D: proporcionalidade', 'Letra D!',
  ('LIMPE: os cinco expressos', 'LIMPE', ['L de Legalidade', 'I de Impessoalidade', 'M de Moralidade', 'P de Publicidade', 'E de Eficiência'],
   'Decora o LIMPE: legalidade, impessoalidade, moralidade, publicidade e eficiência. Esses cinco estão escritos no caput.', ['legalidade', 'impessoalidade', 'moralidade', 'publicidade', 'eficiência']),
  ('Proporcionalidade existe, mas é implícito', 'implícito', 'Pegadinha: proporcionalidade e razoabilidade existem, mas são princípios implícitos. A questão pediu o expresso.'),
  '#direitoconstitucional #administracaopublica', 'Direito para o Escrevente TJSP: princípios expressos do art. 37 (LIMPE).', asize=46)
q('c-337-pronomes', '2026-11-11 19:00', 'PORTUGUÊS · PRONOMES', 'Entre eu e você ou entre mim e você?', 'mim', '✍️',
  'Entre eu e você, ou entre mim e você? Essa derruba muita gente.',
  'O emprego do pronome está de acordo com a norma-padrão em:', ['Isso é para mim fazer hoje.', 'Entre eu e você, está tudo certo.', 'Nada aconteceu entre mim e ti.', 'Mande o recurso para eu, por favor.', 'Ela saiu antes de mim ir embora.'], 'C',
  'Em qual frase o pronome está certo?',
  'Letra C: entre mim e ti', 'Letra C!',
  ('Eu ou mim?', 'mim', ['Depois de preposição: mim, ti (entre mim e ti)', 'Mim nunca faz ação: "para mim fazer" ✘', 'Com verbo no infinitivo: para EU fazer', 'Antes de EU ir embora'],
   'Depois de preposição, vem mim ou ti: entre mim e ti. Mas mim nunca faz ação. Se tem verbo depois, é eu: para eu fazer, antes de eu ir embora.', ['preposição', 'ação', 'fazer', 'embora']),
  ('"Para mim, estudar é fácil" está certo', 'certo', 'Pegadinha: para mim, estudar é fácil, está certo. O mim não é sujeito de estudar, é só opinião.'),
  '#portugues #pronomes', 'Português do Escrevente TJSP: eu ou mim depois de preposição.', asize=44)

# ---------------- 12/11 ----------------
info('c-338-faltam28', '2026-11-12 12:00', 'Faltam 28 dias para a inscrição fechar',
     'Inscrições do Escrevente TJSP 2026 fecham em 10/12. Checklist antes de pagar o boleto: circunscrição certa, dados conferidos, taxa de R$ 81.',
     '#inscricao #prazo #edital', [
         {'type': 'hook', 'kicker': 'TJSP 2026', 'text': 'Faltam 28 dias para a inscrição fechar', 'hl': '28 dias', 'icon': '⏳', 'narration': 'Faltam vinte e oito dias para a inscrição do escrevente do TJ fechar.', 'min_duration': 2.4},
         {'type': 'big', 'text': 'Último dia', 'hl': 'Último', 'big': '10/12', 'label': 'inscrição no site da VUNESP · taxa R$ 81', 'narration': 'O último dia é dez de dezembro, no site da VUNESP.', 'min_duration': 2.6},
         {'type': 'steps', 'text': 'Confira antes de pagar', 'hl': 'antes de pagar', 'rows': [{'t': 'Circunscrição: não troca depois', 'icon': '📍', 'cue': 'Circunscrição'}, {'t': 'Nome, CPF e data de nascimento', 'icon': '🪪', 'cue': 'CPF'}, {'t': 'E-mail que você realmente abre', 'icon': '📧', 'cue': 'mail'}, {'t': 'Boleto pago e comprovante guardado', 'icon': '🧾', 'cue': 'comprovante'}], 'result': False,
          'narration': 'Confira antes de pagar: a circunscrição, que não troca depois. Nome, CPF e data de nascimento. Um e-mail que você realmente abre. E guarde o comprovante do boleto.', 'min_duration': 4.2},
         {'type': 'text', 'kicker': 'Dica', 'text': 'Não deixe para o último dia: o site cai', 'hl': 'último dia', 'icon': '⚠️', 'pose': 'shrug', 'narration': 'E não deixa pro último dia. Site de concurso cai, e o prazo não espera.', 'min_duration': 2.8},
     ])
q('c-339-concnominal', '2026-11-12 19:00', 'PORTUGUÊS · CONCORDÂNCIA NOMINAL', 'É proibido entrada ou proibida a entrada?', 'proibida', '✍️',
  'É proibido entrada ou é proibida a entrada? Tem regra.',
  'A concordância nominal está de acordo com a norma-padrão em:', ['É proibido a entrada de estranhos.', 'É proibida a entrada de estranhos.', 'Anexo seguem os documentos pedidos.', 'Seguem anexo as certidões.', 'São meio-dia e meio.'], 'B',
  'Em qual frase a concordância nominal está certa?',
  'Letra B: é proibida a entrada', 'Letra B!',
  ('A regra do artigo', 'artigo', ['Com artigo: é proibidA A entrada', 'Sem artigo: é proibido entrada', 'Anexo concorda: anexos seguem os documentos', 'Meio-dia e meiA (hora)'],
   'Com artigo, concorda: é proibida a entrada. Sem artigo, fica no masculino: é proibido entrada. Anexo concorda com o substantivo: anexos seguem os documentos. E é meio-dia e meia, porque é meia hora.', ['artigo', 'masculino', 'Anexo', 'meia']),
  ('"Em anexo" não varia', 'não varia', 'Pegadinha: em anexo, com a preposição, não varia. Em anexo seguem as certidões.'),
  '#portugues #concordancia', 'Português do Escrevente TJSP: concordância nominal (proibido, anexo, meio).', asize=42)

# ---------------- 13/11 ----------------
q('c-340-atributos', '2026-11-13 12:00', 'DIREITO ADMINISTRATIVO · ATO ADM.', 'Qual NÃO é atributo do ato administrativo?', 'NÃO é', '⚖️',
  'Presunção de legitimidade, imperatividade, autoexecutoriedade. E o que não é atributo?',
  'NÃO constitui atributo do ato administrativo:', ['Presunção de legitimidade', 'Imperatividade', 'Autoexecutoriedade', 'Tipicidade', 'Discricionariedade'], 'E',
  'Qual não é atributo do ato administrativo?',
  'Letra E: discricionariedade', 'Letra E!',
  ('Os atributos', 'atributos', ['Presunção de legitimidade: vale até prova em contrário', 'Imperatividade: obriga mesmo sem concordar', 'Autoexecutoriedade: executa sem o Judiciário', 'Tipicidade: cada ato tem figura em lei'],
   'Presunção de legitimidade: o ato vale até prova em contrário. Imperatividade: obriga, mesmo sem você concordar. Autoexecutoriedade: a administração executa sem pedir ao Judiciário. E tipicidade: cada ato corresponde a uma figura prevista em lei.', ['Presunção', 'Imperatividade', 'Autoexecutoriedade', 'tipicidade']),
  ('Discricionariedade é característica, não atributo', 'característica', 'Discricionariedade é a margem de escolha de alguns atos. É característica, não atributo.'),
  '#direitoadministrativo #atoadministrativo', 'Direito para o Escrevente TJSP: atributos do ato administrativo.', asize=46)
q('c-341-peculato', '2026-11-13 19:00', 'DIREITO PENAL · CRIMES CONTRA A ADM.', 'Ficar com bem público é qual crime?', 'qual crime?', '⚖️',
  'O servidor fica com um bem público que estava com ele por causa do cargo. Qual é o crime?',
  'O funcionário público que se apropria de bem público de que tem a posse em razão do cargo comete:', ['Concussão', 'Peculato', 'Corrupção passiva', 'Prevaricação', 'Excesso de exação'], 'B',
  'Qual é o crime?',
  'Letra B: peculato', 'Letra B!',
  ('Não confunda', 'confunda', ['Peculato: apropria-se do bem (posse pelo cargo)', 'Concussão: exige vantagem', 'Corrupção passiva: pede ou recebe vantagem', 'Prevaricação: deixa de agir por interesse próprio'],
   'Peculato: o servidor se apropria do bem que tem pelo cargo. Concussão: exige vantagem. Corrupção passiva: pede ou recebe vantagem. Prevaricação: deixa de praticar o ato por interesse pessoal.', ['Peculato', 'Concussão', 'Corrupção', 'Prevaricação']),
  ('Peculato-furto: sem a posse, mas com facilidade do cargo', 'Peculato-furto', 'Pegadinha: se ele não tinha a posse, mas usou a facilidade do cargo para subtrair, é peculato-furto. Continua peculato.'),
  '#direitopenal #peculato', 'Direito Penal para o Escrevente TJSP: peculato, concussão, corrupção passiva e prevaricação.', asize=46)

# ---------------- 14/11 ----------------
q('c-342-afim', '2026-11-14 12:00', 'PORTUGUÊS · A FIM OU AFIM', 'A fim de ou afim de?', 'afim', '✍️',
  'A fim de estudar, ou afim de estudar? Separado ou junto?',
  'O emprego de "a fim" ou "afim" está correto em:', ['Vim afim de resolver o problema.', 'Temos ideias a fim sobre o caso.', 'Ele veio a fim de ajudar na mudança.', 'São assuntos a fim entre si.', 'Afim de quê você perguntou isso?'], 'C',
  'Em qual frase está certo?',
  'Letra C: a fim de ajudar', 'Letra C!',
  ('Separado ou junto', 'junto', ['A fim de (separado): finalidade', 'Afim (junto): semelhante, parecido', 'Assuntos afins, ideias afins', 'Estou a fim de ir = com vontade'],
   'A fim de, separado, indica finalidade: a fim de ajudar. Afim, junto, é adjetivo: parecido. Assuntos afins, ideias afins. E estou a fim de ir, separado, é ter vontade.', ['finalidade', 'adjetivo', 'afins', 'vontade']),
  ('"Afim de" não existe na norma-padrão', 'não existe', 'Pegadinha simples: afim de, junto e com de, não existe na norma-padrão.'),
  '#portugues', 'Português do Escrevente TJSP: a fim de ou afim.', asize=44)
q('c-343-casa', '2026-11-14 19:00', 'DIREITO CONSTITUCIONAL · ART. 5º', 'Polícia pode entrar na sua casa à noite?', 'à noite?', '⚖️',
  'A polícia pode entrar na sua casa à noite sem você deixar?',
  'Segundo o art. 5º, XI, da Constituição, é possível entrar na casa sem consentimento do morador:', ['Em caso de flagrante delito, a qualquer hora.', 'Por determinação judicial, a qualquer hora.', 'Por ordem de autoridade policial, durante o dia.', 'Por ordem do delegado, durante a noite.', 'Em nenhuma hipótese.'], 'A',
  'Quando pode entrar sem consentimento?',
  'Letra A: flagrante, a qualquer hora', 'Letra A!',
  ('A casa é asilo inviolável, salvo', 'salvo', ['Flagrante delito: qualquer hora', 'Desastre ou prestar socorro: qualquer hora', 'Determinação judicial: só durante o DIA', 'Ordem policial sozinha: não basta'],
   'A casa é asilo inviolável, salvo: flagrante delito, a qualquer hora. Desastre ou socorro, a qualquer hora. Determinação judicial, só durante o dia. Ordem policial sozinha não basta.', ['flagrante', 'Desastre', 'judicial', 'policial']),
  ('Mandado judicial à noite: não pode', 'à noite', 'Pegadinha: até com mandado judicial, à noite não pode. O mandado só vale de dia.'),
  '#direitoconstitucional #art5', 'Direito Constitucional para o Escrevente TJSP: inviolabilidade do domicílio (art. 5º, XI).', asize=44)

# ---------------- 15/11 ----------------
q('c-344-sessao', '2026-11-15 12:00', 'PORTUGUÊS · HOMÔNIMOS', 'Sessão, seção ou cessão?', 'cessão?', '✍️',
  'Sessão, seção ou cessão? Três palavras, três sentidos. Cai em cartório e cai na prova.',
  'Preenche corretamente as lacunas: "A ___ do júri durou cinco horas; a ___ de direitos foi registrada; leia a ___ de esportes."', ['seção, sessão, cessão', 'sessão, cessão, seção', 'cessão, seção, sessão', 'sessão, seção, cessão', 'seção, cessão, sessão'], 'B',
  'Qual sequência preenche certo?',
  'Letra B: sessão, cessão, seção', 'Letra B!',
  ('Cada uma no seu lugar', 'seu lugar', ['Sessão: reunião, tempo (sessão do júri)', 'Cessão: ato de ceder (cessão de direitos)', 'Seção: parte, divisão (seção do jornal)'],
   'Sessão com dois esses é reunião: sessão do júri. Cessão com c é ceder: cessão de direitos. E seção com ç é divisão: seção do jornal.', ['Sessão', 'Cessão', 'seção']),
  None,
  '#portugues #ortografia', 'Português do Escrevente TJSP: sessão, seção ou cessão.', asize=44)
info('c-345-redacao', '2026-11-15 19:00', 'Redação do TJSP: 24 de 40 ou está fora',
     'Redação do Escrevente TJSP 2027: nota mínima 24 de 40, no mesmo dia da prova objetiva (14/03). O que a banca costuma cobrar e como treinar uma por semana.',
     '#redacao #edital #provatjsp', [
         {'type': 'hook', 'kicker': 'Edital 2026', 'text': 'Redação do TJSP: 24 de 40 ou está fora', 'hl': '24 de 40', 'icon': '📝', 'narration': 'Redação do escrevente do TJ: vinte e quatro de quarenta, ou você está fora.', 'min_duration': 2.4},
         {'type': 'big', 'text': 'Nota mínima', 'hl': 'mínima', 'big': '24/40', 'label': 'no mesmo dia da objetiva · 14/03/2027', 'narration': 'A nota mínima é vinte e quatro de quarenta, no mesmo dia da prova objetiva.', 'min_duration': 2.8},
         {'type': 'steps', 'text': 'Como treinar', 'hl': 'treinar', 'rows': [{'t': 'Uma redação por semana, cronometrada', 'icon': '⏱️', 'cue': 'semana'}, {'t': 'Tema atual + posição clara', 'icon': '🎯', 'cue': 'posição'}, {'t': 'Norma-padrão: crase, concordância, vírgula', 'icon': '✍️', 'cue': 'Norma'}, {'t': 'Releia e corte repetição', 'icon': '🔍', 'cue': 'Releia'}], 'result': False,
          'narration': 'Uma redação por semana, cronometrada. Tema atual e posição clara. Norma-padrão: crase, concordância e vírgula. E releia, cortando repetição.', 'min_duration': 4.0},
         {'type': 'text', 'kicker': 'Lembrete', 'text': 'Fuga ao tema zera a redação', 'hl': 'zera', 'icon': '⚠️', 'pose': 'shock', 'narration': 'E lembra: fugir do tema zera a redação. Leia a proposta duas vezes antes de escrever.', 'min_duration': 2.8},
     ])

print(len(V), 'vídeos:', ', '.join(V))
