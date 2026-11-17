"""Roteiros "E se...?" do canal B (PT-BR, Shorts verticais de até ~2:55).
Modelo copiado do que está crescendo agora (Hiperfocando: 12 mil inscritos em 2 semanas, mediana 142 mil views):
pergunta-gancho brasileira, mapa com território na bandeira do dono, emoji reagindo, fatos reais de apoio, reviravolta no fim,
pergunta para comentar + "manda pro amigo". Números: Banco Mundial (research/wb_mundo_2026-11-17.json) e fontes históricas.
Uso: python specs/ese_pt.py  → specs/ese/b-pt-NNN.json"""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ese")
os.makedirs(OUT, exist_ok=True)
SA = {"c": [-60, -24], "s": 1.0}
TAGS = ["curiosidades", "brasil", "mapas", "geografia", "história", "simulação", "e se", "hiperfoco", "américa do sul"]
TAIL = ("\n\nCenário imaginário: só um \"e se\" no mapa. Os fatos de apoio são reais.\n"
        "Inscreva-se pra ver o próximo \"e se\".\n\n#curiosidades #brasil #mapas #geografia #historia")


def save(n, title, hook, beats, desc, thumb, at, tags=(), music="Hidden Agenda", uf=False):
    spec = dict(id=f"b-pt-{n:03d}", channel="B", lang="pt", format="short", hook=hook, hook_end=2.8, badge="SÓ IMAGINAÇÃO", uf=uf,
                voice="Fenrir", music=dict(track=music, vol=0.12, alt=["Investigations", "Curiosity"]), beats=beats,
                thumb=thumb, yt=dict(title=title, description=desc + TAIL, tags=TAGS + list(tags), lang="pt-BR", categoryId="27"),
                publish=dict(at=at))
    def fix(o):  # dict(from_=...) -> "from"
        if isinstance(o, dict): return {("from" if k == "from_" else k): fix(v) for k, v in o.items()}
        if isinstance(o, list): return [fix(v) for v in o]
        return o
    spec = fix(spec)
    words = sum(len(b["say"].split()) for b in beats)
    json.dump(spec, open(f"{OUT}/{spec['id']}.json", "w"), ensure_ascii=False, indent=1)
    print(spec["id"], words, "palavras", f"~{words / 2.75:.0f}s")


# ---------------------------------------------------------------- 1. Acre (Tratado de Petrópolis, 17/11/1903)
ACRE = [-70.4, -9.2]
save(1, "E se o Acre ainda fosse da Bolívia? #curiosidades #brasil",
     "E SE O ACRE|AINDA FOSSE DA|BOLÍVIA?",
     [
         dict(say="E se o Acre ainda fosse da Bolívia? Parece meme, mas por muito pouco esse pedaço do mapa não é brasileiro até hoje.",
              cam={"c": [-62, -12], "s": 1.9}, own={"BRA": "BRA", "BOL": "BOL"},
              balls=[dict(iso="BRA", face="shock", d=0.4), dict(iso="BOL", face="smirk", d=1.2)]),
         dict(say="Esse é o Acre. Mais de cento e sessenta mil quilômetros quadrados, quase do tamanho do Uruguai inteiro.",
              cam={"c": ACRE, "s": 4.6}, hl=["BR-AC"], balls=[], cards=[dict(text="Acre:", big="164 mil km²", iso="BRA", d=1.0)]),
         dict(say="Só que, pelos tratados do século dezenove, essa terra era da Bolívia.",
              own={"BR-AC": "BOL"}, od=0.3, cards=[], balls=[dict(iso="BR-AC", face="smirk", skin="emoji", d=0.6)]),
         dict(say="Aí veio a febre da borracha. Milhares de nordestinos, principalmente cearenses, atravessaram a Amazônia pra trabalhar nos seringais.",
              cam={"c": [-56, -7], "s": 1.35}, balls=[], arrows=[dict(from_="BR-CE", to="BR-AC", d=0.8)]),
         dict(say="Resultado: a terra era boliviana, mas quem morava lá era brasileiro.",
              cam={"c": ACRE, "s": 4.0}, arrows=[], balls=[dict(iso="BR-AC", face="neutral", dx=-70, d=0.2), dict(iso="BR-AC", face="shock", skin="red", dx=90, r=0.8, d=1.0)]),
         dict(say="Em mil novecentos e um, a Bolívia fez uma jogada ousada: arrendou a região pra um consórcio estrangeiro com sede em Nova York, o Bolivian Syndicate.",
              cards=[dict(text="1901:", big="Acre alugado", iso="BOL", d=0.5), dict(text="Bolivian", big="Syndicate", iso="USA", d=3.5)],
              balls=[dict(iso="BR-AC", face="angry", skin="red", d=0.3)]),
         dict(say="Os seringueiros não aceitaram. Um gaúcho chamado Plácido de Castro montou um exército de seringueiros e começou a Revolução Acreana.",
              cards=[], cam={"c": [-60, -18], "s": 1.3}, arrows=[dict(from_="BR-RS", to="BR-AC", d=1.2, color="#ff5a3c")],
              balls=[dict(iso="BR-RS", face="angry", skin="red", r=0.8, d=0.8)]),
         dict(say="No começo de mil novecentos e três, os rebeldes já controlavam quase todo o Acre. A Bolívia ameaçou mandar tropas.",
              cam={"c": [-66, -12], "s": 2.6}, arrows=[dict(from_="BOL", to="BR-AC", d=1.6, color="#ff5a3c")],
              balls=[dict(iso="BR-AC", face="cool", d=0.2), dict(iso="BOL", face="angry", skin="red", d=1.4)]),
         dict(say="Aí entrou o Barão do Rio Branco. Em vez de guerra, ele fez uma proposta: comprar o Acre.",
              arrows=[], balls=[dict(iso="BRA", ll=[-60, -10], face="cool", d=0.3), dict(iso="BOL", face="shock", d=1.6)],
              cards=[dict(text="Barão do", big="Rio Branco", iso="BRA", d=0.4)]),
         dict(say="No dia dezessete de novembro de mil novecentos e três, os dois países assinaram o Tratado de Petrópolis.",
              cards=[dict(text="17/11/1903:", big="Tratado de Petrópolis", d=0.4)], own={"BR-AC": "BRA"}, od=2.0,
              cam={"c": ACRE, "s": 3.6}, balls=[dict(iso="BR-AC", face="happy", d=2.4)]),
         dict(say="O Brasil pagou dois milhões de libras esterlinas, cedeu algumas terras na fronteira e prometeu construir uma ferrovia, a Madeira-Mamoré.",
              cards=[dict(text="Preço:", big="2 milhões de libras", iso="BRA", d=0.4), dict(text="+ ferrovia", big="Madeira-Mamoré", d=4.8)]),
         dict(say="E o tal consórcio de Nova York? Levou mais cento e dez mil libras só pra desistir do negócio.",
              cards=[dict(text="Indenização:", big="110 mil libras", iso="USA", d=0.6)], balls=[dict(iso="BR-AC", face="cool", d=0.2)]),
         dict(say="Agora imagina o contrário. O Brasil não paga, e o Acre continua boliviano.",
              cards=[], cam={"c": [-63, -13], "s": 2.0}, own={"BR-AC": "BOL"}, od=1.0,
              balls=[dict(iso="BOL", face="happy", d=1.2), dict(iso="BRA", ll=[-55, -9], face="sad", d=1.8)]),
         dict(say="A Bolívia ficaria quase quinze por cento maior. E o Brasil teria um estado a menos. A piada de que o Acre não existe ia virar verdade.",
              cards=[dict(text="Bolívia:", big="+15% de território", iso="BOL", d=0.4), dict(text="Brasil:", big="25 estados", iso="BRA", d=3.4)]),
         dict(say="Mais de oitocentas mil pessoas que hoje são acreanas iam ter documento boliviano, pagar as contas em bolivianos e torcer pra seleção da Bolívia.",
              cards=[], cam={"c": ACRE, "s": 4.0}, balls=[dict(iso="BR-AC", face="shock", d=0.3)]),
         dict(say="E o Chico Mendes, o seringueiro de Xapuri que virou símbolo da Amazônia no mundo inteiro? Ia nascer na Bolívia.",
              cards=[dict(text="Chico Mendes:", big="boliviano?", iso="BOL", d=0.6)]),
         dict(say="Mas o detalhe mais irônico tá na capital. Rio Branco, a capital do Acre, tem justamente o nome do barão que comprou o Acre.",
              own={"BR-AC": "BRA"}, od=0.2, cards=[dict(text="Capital:", big="Rio Branco", iso="BRA", d=1.6)], balls=[dict(iso="BR-AC", face="cool", d=0.6)]),
         dict(say="Agora me fala: o Brasil fez um bom negócio ou devia ter deixado o Acre com a Bolívia? Comenta aí. E manda pro amigo que jura que o Acre não existe.",
              cards=[], cam={"c": [-62, -12], "s": 1.9}, balls=[dict(iso="BRA", face="happy", d=0.3), dict(iso="BOL", face="smirk", d=1.0)]),
     ],
     "Em 17 de novembro de 1903, o Brasil comprou o Acre da Bolívia: 2 milhões de libras esterlinas, umas terras na fronteira e a promessa de uma ferrovia. "
     "Antes disso teve febre da borracha, um consórcio de Nova York alugando a região e uma revolução liderada por um gaúcho.\n"
     "O Brasil fez um bom negócio? Comenta aí. E manda pro amigo que jura que o Acre não existe.",
     dict(title="E SE O ACRE|FOSSE DA|BOLÍVIA?", c=[-63, -14], s=1.9, own={"BOL": "BOL", "BR-AC": "BOL", "BRA": "BRA"},
          balls=[dict(iso="BR-AC", face="smirk", r=110), dict(iso="BRA", ll=[-52, -11], face="rage", skin="red", r=150)],
          arrows=[dict(from_="BOL", to="BR-AC")]),
     "2026-11-17T19:30:00Z", tags=["acre", "bolívia", "tratado de petrópolis", "o acre existe", "plácido de castro", "barão do rio branco"], uf=True)

# ---------------------------------------------------------------- 2. Uruguai / Cisplatina / Maracanaço
URY = {"c": [-56, -31.5], "s": 3.0}
save(2, "E se o Uruguai fosse do Brasil? #curiosidades #brasil",
     "E SE O URUGUAI|FOSSE DO|BRASIL?",
     [
         dict(say="E se o Uruguai fosse um estado brasileiro? Parece loucura, mas durante alguns anos ele foi.",
              cam=URY, own={"BRA": "BRA", "URY": "URY", "ARG": "ARG"},
              balls=[dict(iso="URY", face="shock", d=0.5), dict(iso="BRA", ll=[-53, -29], face="smirk", d=1.4)]),
         dict(say="Antes de virar país, aquela terra era disputada por todo mundo: espanhóis, portugueses e os vizinhos de Buenos Aires.",
              balls=[dict(iso="URY", face="sad", d=0.2), dict(iso="ARG", ll=[-60, -34], face="angry", skin="red", r=0.8, d=1.8)],
              arrows=[dict(from_=[-60, -34], to="URY", d=2.0, color="#7fd3ff"), dict(from_=[-53, -29], to="URY", d=2.6)]),
         dict(say="Em mil oitocentos e dezessete, tropas luso-brasileiras ocuparam Montevidéu. E em mil oitocentos e vinte e um, a região foi anexada com um nome novo: Província Cisplatina.",
              arrows=[], own={"URY": "BRA"}, od=4.0, cards=[dict(text="1821:", big="Província Cisplatina", iso="BRA", d=4.2)],
              balls=[dict(iso="URY", face="cool", skin="flag", d=4.4)]),
         dict(say="Quando o Brasil ficou independente, em mil oitocentos e vinte e dois, a Cisplatina veio junto. Era o extremo sul do Império.",
              cards=[], cam={"c": [-55, -22], "s": 1.25}, balls=[dict(iso="BRA", face="cool", d=0.4)]),
         dict(say="Só que os uruguaios não queriam ser brasileiros, e Buenos Aires também queria a região. Em mil oitocentos e vinte e cinco começou a Guerra da Cisplatina.",
              cam=URY, balls=[dict(iso="URY", face="angry", skin="red", d=0.3), dict(iso="ARG", ll=[-60, -34], face="angry", skin="red", r=0.8, d=1.4)],
              arrows=[dict(from_=[-60, -34], to="URY", d=1.6, color="#ff5a3c")], cards=[dict(text="1825:", big="Guerra da Cisplatina", d=5.0)]),
         dict(say="Foram três anos de guerra, sem vencedor claro. Até que a Inglaterra, de olho no comércio do Rio da Prata, entrou no meio pra negociar a paz.",
              arrows=[], cards=[dict(text="Mediador:", big="Inglaterra", iso="GBR", d=4.0)]),
         dict(say="Em mil oitocentos e vinte e oito, os dois lados abriram mão da região. E nasceu um país novo, bem no meio dos dois: o Uruguai.",
              own={"URY": "URY"}, od=2.8, cards=[], balls=[dict(iso="URY", face="happy", d=3.0)]),
         dict(say="Agora imagina que o Brasil tivesse ganhado. O Uruguai seria mais um estado brasileiro, colado no Rio Grande do Sul.",
              own={"URY": "BRA"}, od=1.2, cam={"c": [-56, -26], "s": 1.6}, balls=[dict(iso="BRA", ll=[-52, -14], face="happy", d=1.4)]),
         dict(say="Seriam três milhões e quatrocentas mil pessoas a mais. E um território maior que o Ceará inteiro.",
              cards=[dict(text="+3,4 milhões", big="de pessoas", iso="URY", d=0.4), dict(text="+176 mil km²", big="> Ceará", iso="BRA", d=3.0)]),
         dict(say="E um estado rico: hoje o PIB por pessoa do Uruguai é mais que o dobro do brasileiro.",
              cards=[dict(text="PIB por pessoa:", big="Uruguai 25 mil dólares", iso="URY", d=0.3), dict(text="Brasil:", big="10,7 mil dólares", iso="BRA", d=2.6)]),
         dict(say="Mas a parte que mais ia mudar é o futebol.",
              cards=[], cam={"c": [-43.2, -22.9], "s": 5.0}, balls=[dict(ll=[-43.23, -22.91], iso="BRA", face="shock", d=0.3)]),
         dict(say="Mil novecentos e cinquenta. Jogo decisivo da Copa, no Maracanã, perto de duzentas mil pessoas. O Uruguai vira o jogo e ganha de dois a um. O Maracanaço.",
              cards=[dict(text="16/07/1950:", big="Brasil 1 x 2 Uruguai", iso="URY", d=0.4)],
              balls=[dict(ll=[-43.23, -22.91], iso="BRA", face="sad", d=0.2), dict(ll=[-45.5, -24.5], iso="URY", face="cool", skin="flag", r=0.8, d=5.5)]),
         dict(say="Se o Uruguai fosse brasileiro, o Maracanaço simplesmente não existiria.",
              cards=[], balls=[dict(ll=[-43.23, -22.91], iso="BRA", face="shock", d=0.2)]),
         dict(say="E tem mais. Em cinquenta o Brasil jogava de branco. Foi depois dessa derrota que nasceu a camisa amarela. Sem Maracanaço, talvez nem existisse a amarelinha.",
              cards=[dict(text="Antes de 1950:", big="camisa branca", d=0.6), dict(text="Depois:", big="amarelinha", iso="BRA", d=4.6)]),
         dict(say="E as estrelas na camisa? Cinco Copas do Brasil, mais duas do Uruguai. Seriam sete.",
              cards=[dict(text="Brasil 5 + Uruguai 2 =", big="7 estrelas", iso="BRA", d=2.4)], cam={"c": [-55, -24], "s": 1.3},
              balls=[dict(iso="BRA", face="love", d=1.0)]),
         dict(say="Me fala: você trocava o Maracanaço por um Uruguai brasileiro? Comenta aí. E manda pro seu amigo uruguaio, se tiver coragem.",
              cards=[], cam=URY, balls=[dict(iso="URY", face="smirk", d=0.3), dict(iso="BRA", ll=[-53, -29], face="happy", d=1.0)]),
     ],
     "O Uruguai já foi brasileiro: de 1821 a 1828 ele era a Província Cisplatina. Uma guerra, a Inglaterra no meio, e nasceu um país novo. "
     "Se o Brasil tivesse ficado com ele, sumia o Maracanaço… e talvez a amarelinha.\n"
     "Você trocava o Maracanaço por um Uruguai brasileiro? Comenta aí. E manda pro seu amigo uruguaio, se tiver coragem.",
     dict(title="E SE O URUGUAI|FOSSE DO|BRASIL?", c=[-55, -27], s=1.9, own={"BRA": "BRA", "URY": "BRA"},
          balls=[dict(iso="URY", face="shock", r=110), dict(iso="BRA", ll=[-50, -14], face="smirk", r=150)],
          arrows=[dict(from_=[-52, -22], to="URY")]),
     "2026-11-17T14:00:00Z", tags=["uruguai", "cisplatina", "maracanaço", "copa de 1950", "amarelinha", "seleção brasileira"])

# ---------------------------------------------------------------- 3. América do Sul num país só
ALL = ["BRA", "ARG", "COL", "PER", "VEN", "CHL", "ECU", "BOL", "PRY", "URY", "GUY", "SUR"]
save(3, "E se a América do Sul fosse um país só? #curiosidades #brasil",
     "E SE A AMÉRICA|DO SUL FOSSE|UM PAÍS SÓ?",
     [
         dict(say="E se a América do Sul inteira virasse um país só? Doze países, uma bandeira. E os números assustam.",
              cam=SA, own={k: k for k in ALL},
              balls=[dict(iso="BRA", face="shock", d=0.5), dict(iso="ARG", face="smirk", r=0.8, d=1.2), dict(iso="COL", face="neutral", r=0.7, d=1.8)]),
         dict(say="Hoje são doze países independentes. Do Brasil, gigante, até o Suriname, com pouco mais de seiscentas mil pessoas.",
              balls=[dict(iso="BRA", face="cool", d=0.3), dict(iso="SUR", face="shock", r=0.55, d=3.0)], hl=["SUR"]),
         dict(say="E aquele pedacinho ali em cima não conta. A Guiana Francesa é parte da França. Ou seja: a França faz fronteira com o Brasil.",
              cam={"c": [-54, 3], "s": 4.2}, hl=["FRA"], balls=[dict(ll=[-53.2, 4.0], iso="FRA", skin="flag", face="smirk", r=0.7, d=0.6)]),
         dict(say="Agora junta tudo.",
              cam=SA, hl=[], balls=[], own={k: "SUL" for k in ALL}, od=0.4,
              arrows=[dict(from_="ARG", to=[-56, -14], d=0.2), dict(from_="COL", to=[-58, -10], d=0.3), dict(from_="PER", to=[-60, -12], d=0.4), dict(from_="CHL", to=[-58, -16], d=0.5)]),
         dict(say="O novo país teria quase quatrocentos e quarenta milhões de habitantes. O terceiro mais populoso do mundo, atrás só da Índia e da China, e na frente dos Estados Unidos.",
              arrows=[], balls=[dict(iso="BRA", ll=[-58, -14], face="shock", r=1.2, d=0.4)],
              cards=[dict(text="População:", big="437 milhões", d=0.6), dict(text="Estados Unidos:", big="342 milhões", iso="USA", d=7.0)]),
         dict(say="E em tamanho? Dezessete milhões e setecentos mil quilômetros quadrados. Mais que a Rússia. Seria o maior país do planeta.",
              cards=[dict(text="Área:", big="17,7 milhões de km²", d=0.6), dict(text="Rússia:", big="17,1 milhões", iso="RUS", d=4.6)],
              balls=[dict(iso="BRA", ll=[-58, -14], face="cool", r=1.2, d=7.2)]),
         dict(say="A economia somada passaria de quatro trilhões e meio de dólares. O dobro do Brasil sozinho.",
              cards=[dict(text="PIB:", big="US$ 4,57 trilhões", d=0.4), dict(text="Brasil sozinho:", big="US$ 2,28 tri", iso="BRA", d=3.4)], balls=[]),
         dict(say="Aí começa a briga. Os países de língua espanhola somam uns duzentos e vinte e três milhões de pessoas. O Brasil sozinho, duzentos e treze. Quase empate.",
              own={k: k for k in ALL}, od=0.3, cards=[dict(text="Espanhol:", big="223 milhões", iso="ARG", d=1.0), dict(text="Português:", big="213 milhões", iso="BRA", d=6.4)],
              balls=[dict(iso="ARG", face="angry", skin="red", r=0.8, d=1.2), dict(iso="BRA", face="angry", skin="red", d=6.6)]),
         dict(say="E a capital? Brasília, Buenos Aires ou Bogotá?",
              cards=[], balls=[dict(ll=[-47.9, -15.8], iso="BRA", face="smirk", r=0.6, d=0.3), dict(ll=[-58.4, -34.6], iso="ARG", face="smirk", r=0.6, d=1.0), dict(ll=[-74.1, 4.7], iso="COL", face="smirk", r=0.6, d=1.8)]),
         dict(say="No futebol seria covardia. Brasil tem cinco Copas, Argentina três, Uruguai duas. A seleção já entraria em campo com dez estrelas.",
              balls=[], own={k: "SUL" for k in ALL}, od=0.2,
              cards=[dict(text="Brasil 5 + Argentina 3 + Uruguai 2 =", big="10 estrelas", d=1.0)]),
         dict(say="E o mais curioso: um pedaço disso já existiu. Simón Bolívar juntou Colômbia, Venezuela, Equador e Panamá na Grã-Colômbia. Durou pouco mais de dez anos.",
              cards=[], cam={"c": [-72, 3], "s": 2.2}, own={"BRA": "BRA", "ARG": "ARG", "PER": "PER", "CHL": "CHL", "BOL": "BOL", "PRY": "PRY", "URY": "URY", "GUY": "GUY", "SUR": "SUR",
                                                               "COL": "COL", "VEN": "COL", "ECU": "COL", "PAN": "COL"}, od=0.5,
              balls=[dict(iso="COL", face="happy", d=1.0)]),
         dict(say="E aí: qual seria o nome desse país, e qual seria a capital? Comenta aí. E manda pro amigo argentino que ia odiar dividir a seleção.",
              cam=SA, own={k: "SUL" for k in ALL + ["PAN"]}, od=0.2, balls=[dict(iso="BRA", ll=[-58, -14], face="love", r=1.2, d=0.6)]),
     ],
     "Doze países, uma bandeira só. A América do Sul unida teria 437 milhões de pessoas (3º do mundo), 17,7 milhões de km² (maior que a Rússia) "
     "e uma seleção com 10 estrelas. Dados: Banco Mundial.\n"
     "Qual seria o nome desse país, e a capital? Comenta aí. E manda pro amigo argentino que ia odiar dividir a seleção.",
     dict(title="E SE A AMÉRICA|DO SUL FOSSE|UM PAÍS SÓ?", c=[-60, -24], s=1.0, y=0.66, own={k: "SUL" for k in ALL},
          balls=[dict(iso="BRA", ll=[-58, -14], face="shock", r=150)]),
     "2026-11-18T15:00:00Z", tags=["américa do sul", "união sul-americana", "grã-colômbia", "simón bolívar", "seleção", "maior país do mundo"])

# ---------------------------------------------------------------- 4. Tordesilhas valendo hoje
TL = -48.6  # meridiano aproximado (a linha passa entre Belém-PA e Laguna-SC)
BRZ = {"c": [-50, -15], "s": 1.55}
save(4, "E se o Tratado de Tordesilhas valesse até hoje? #curiosidades #brasil",
     "E SE|TORDESILHAS|VALESSE HOJE?",
     [
         dict(say="E se aquela linha do livro de história valesse até hoje? O Brasil ia encolher. E muito.",
              cam=SA, own={"BRA": "BRA"}, balls=[dict(iso="BRA", face="shock", d=0.5)]),
         dict(say="Mil quatrocentos e noventa e quatro. Portugal e Espanha dividem um mundo que ainda nem tinha sido todo descoberto, com uma linha: trezentas e setenta léguas a oeste de Cabo Verde.",
              cam={"c": [-38, 2], "s": 0.5}, own={"PRT": "PRT", "ESP": "ESP"}, balls=[dict(iso="PRT", ll=[-9, 40], face="cool", r=0.5, d=1.0), dict(iso="ESP", ll=[-3, 41], face="smirk", r=0.5, d=1.6)],
              cards=[dict(text="7 de junho de 1494:", big="Tordesilhas", d=0.6)], pins=[dict(ll=[-24, 16], label="Cabo Verde", d=6.0)], line=dict(lon=TL, d=7.5)),
         dict(say="Tudo a leste da linha era de Portugal. Tudo a oeste, da Espanha.",
              cards=[], pins=[], balls=[], cam={"c": [-52, -14], "s": 1.15}, split=dict(lon=TL, west="ESP", east="PRT", d=0.3)),
         dict(say="No mapa de hoje, a linha passa mais ou menos de Belém, no Pará, até Laguna, em Santa Catarina.",
              cam=BRZ, pins=[dict(ll=[-48.5, -1.45], label="Belém", d=1.6), dict(ll=[-48.78, -28.48], label="Laguna", d=4.2)]),
         dict(say="Se ela valesse até hoje, o Brasil ficaria com só um terço do tamanho atual. Uma faixa no litoral.",
              pins=[], cards=[dict(text="Brasil hoje:", big="8,5 milhões de km²", iso="BRA", d=1.2), dict(text="Com Tordesilhas:", big="~1/3 disso", iso="PRT", d=3.0)],
              balls=[dict(ll=[-40, -10], iso="PRT", face="sad", d=3.4)]),
         dict(say="Do lado português ficariam o Nordeste inteiro, o Rio, quase todo Minas, a cidade de São Paulo e até Brasília.",
              cards=[], balls=[], pins=[dict(ll=[-38.5, -12.97], label="Salvador"), dict(ll=[-43.2, -22.9], label="Rio"), dict(ll=[-46.63, -23.55], label="São Paulo"), dict(ll=[-47.9, -15.8], label="Brasília")]),
         dict(say="Mas do lado espanhol? Manaus, Cuiabá, Campo Grande, Goiânia, Curitiba e Porto Alegre.",
              pins=[dict(ll=[-60.0, -3.1], label="Manaus", left=True), dict(ll=[-56.1, -15.6], label="Cuiabá", left=True), dict(ll=[-54.6, -20.45], label="Campo Grande", left=True),
                    dict(ll=[-49.25, -16.68], label="Goiânia", left=True), dict(ll=[-49.27, -25.43], label="Curitiba", left=True), dict(ll=[-51.2, -30.03], label="Porto Alegre", left=True)]),
         dict(say="A Amazônia quase inteira ia falar espanhol. E o gaúcho ia tomar chimarrão do outro lado da fronteira.",
              pins=[], balls=[dict(ll=[-62, -5], iso="ESP", face="happy", d=0.4), dict(ll=[-52.5, -29.5], iso="ESP", face="cool", r=0.8, d=3.0)]),
         dict(say="Então por que o Brasil é tão grande? Porque ninguém respeitou a linha.",
              balls=[dict(ll=[-40, -10], iso="PRT", face="smirk", d=1.4)]),
         dict(say="De mil quinhentos e oitenta a mil seiscentos e quarenta, Portugal e Espanha tiveram o mesmo rei. Foi a União Ibérica, e a linha virou detalhe.",
              balls=[], cards=[dict(text="1580–1640:", big="União Ibérica", d=0.6)]),
         dict(say="Os bandeirantes saíram de São Paulo mata adentro, atrás de ouro, de pedras preciosas e de gente pra escravizar. E foram empurrando a fronteira pro oeste.",
              cards=[], line=None, arrows=[dict(from_=[-46.6, -23.5], to=[-56, -15], d=1.0), dict(from_=[-46.6, -23.5], to=[-60, -3], d=2.2), dict(from_=[-46.6, -23.5], to=[-53, -29], d=3.4)]),
         dict(say="Em mil setecentos e cinquenta, o Tratado de Madri oficializou: a terra fica com quem ocupa. E o Brasil ficou com quase tudo que tinha avançado.",
              arrows=[], split=None, own={"BRA": "BRA"}, cards=[dict(text="1750:", big="Tratado de Madri", iso="PRT", d=0.6)], balls=[dict(iso="BRA", face="cool", d=2.0)]),
         dict(say="Me fala: se a linha valesse hoje, sua cidade ia ser brasileira ou espanhola? Comenta aí. E manda pro amigo gaúcho que ia ter que aprender espanhol.",
              cards=[], split=dict(lon=TL, west="ESP", east="PRT", d=0.2), line=dict(lon=TL), balls=[dict(ll=[-40, -10], iso="PRT", face="happy", d=0.6), dict(ll=[-60, -10], iso="ESP", face="smirk", d=1.2)]),
     ],
     "Em 1494, Portugal e Espanha dividiram o mundo com uma linha. No mapa de hoje ela passa de Belém (PA) a Laguna (SC): Manaus, Curitiba e Porto Alegre ficariam do lado espanhol. "
     "O Brasil só é desse tamanho porque ninguém respeitou a linha.\n"
     "Sua cidade ia ser brasileira ou espanhola? Comenta aí. E manda pro amigo gaúcho que ia ter que aprender espanhol.",
     dict(title="E SE|TORDESILHAS|VALESSE HOJE?", c=[-52, -16], s=1.25, y=0.64, split=dict(lon=TL, west="ESP", east="PRT"),
          balls=[dict(ll=[-40, -10], iso="PRT", face="cool", r=120), dict(ll=[-61, -8], iso="ESP", face="rage", skin="red", r=150)]),
     "2026-11-18T21:00:00Z", tags=["tordesilhas", "tratado de tordesilhas", "bandeirantes", "tratado de madri", "história do brasil", "portugal", "espanha"])

# ---------------------------------------------------------------- 5. Nordeste país
NE = ["BR-MA", "BR-PI", "BR-CE", "BR-RN", "BR-PB", "BR-PE", "BR-AL", "BR-SE", "BR-BA"]
NEC = {"c": [-41.5, -9.5], "s": 2.1}
save(5, "E se o Nordeste fosse um país? #curiosidades #brasil",
     "E SE O|NORDESTE FOSSE|UM PAÍS?",
     [
         dict(say="E se o Nordeste virasse um país? E não é só imaginação: isso quase aconteceu. Duas vezes.",
              cam={"c": [-48, -13], "s": 1.35}, own={"BRA": "BRA", **{k: "NOR" for k in NE}}, od=1.0,
              balls=[dict(ll=[-40.5, -8], iso="BRA", face="cool", d=1.4), dict(ll=[-53, -12], iso="BRA", face="shock", d=2.4)]),
         dict(say="Nove estados, do Maranhão à Bahia.",
              cam=NEC, balls=[], hl=NE),
         dict(say="O novo país teria mais de cinquenta e quatro milhões de habitantes. Mais que a Argentina, mais que a Espanha, mais que a Colômbia.",
              hl=[], cards=[dict(text="Nordeste:", big="54,7 milhões", d=0.6), dict(text="Argentina:", big="45,9 mi", iso="ARG", d=4.2), dict(text="Espanha:", big="49,4 mi", iso="ESP", d=5.6), dict(text="Colômbia:", big="53,4 mi", iso="COL", d=6.8)]),
         dict(say="Seria o segundo país mais populoso da América do Sul, atrás só do que sobrou do Brasil.",
              cards=[], cam={"c": [-55, -20], "s": 1.0}, own={k: k for k in ["ARG", "COL", "PER", "VEN", "CHL"]},
              balls=[dict(ll=[-40.5, -8], iso="BRA", face="cool", d=0.6), dict(iso="COL", face="shock", r=0.7, d=2.0), dict(iso="ARG", face="sad", r=0.7, d=2.6)]),
         dict(say="E grande: mais de um milhão e meio de quilômetros quadrados. Maior que o Peru, maior que a Colômbia.",
              balls=[], cards=[dict(text="Área:", big="1,55 milhão de km²", d=0.6), dict(text="Peru:", big="1,29 milhão", iso="PER", d=3.6)], hl=["PER", "COL"]),
         dict(say="E a capital? Aí começa a briga. Salvador, Recife ou Fortaleza? Pelo último Censo, a maior cidade nem é mais Salvador. É Fortaleza.",
              cards=[], hl=[], cam=NEC, pins=[dict(ll=[-38.5, -12.97], label="Salvador", d=1.4), dict(ll=[-34.88, -8.05], label="Recife", left=True, d=2.1), dict(ll=[-38.53, -3.72], label="Fortaleza", d=2.8)],
              balls=[dict(ll=[-38.53, -4.6], iso="BRA", face="cool", r=0.6, d=7.4)]),
         dict(say="Mas essa ideia não é nova. Em mil oitocentos e dezessete, Pernambuco se declarou uma república independente. A Revolução Pernambucana durou uns setenta e cinco dias.",
              pins=[], balls=[], own={k: "BRA" for k in NE}, od=0.2, hl=["BR-PE"], cam={"c": [-37.5, -8.3], "s": 4.0},
              cards=[dict(text="1817:", big="Revolução Pernambucana", d=2.6)]),
         dict(say="Sete anos depois veio a Confederação do Equador: Pernambuco, Paraíba, Rio Grande do Norte e Ceará tentando formar um país separado do Império.",
              cards=[dict(text="1824:", big="Confederação do Equador", d=1.4)], hl=[], cam={"c": [-38.5, -6.5], "s": 3.0},
              own={"BR-PE": "NOR", "BR-PB": "NOR", "BR-RN": "NOR", "BR-CE": "NOR"}, od=3.6),
         dict(say="Dom Pedro primeiro mandou tropas e esmagou o movimento em poucos meses. Um dos líderes, Frei Caneca, foi condenado à forca. Mas nenhum carrasco aceitou enforcar ele. Acabou fuzilado.",
              cards=[], arrows=[dict(from_=[-43.2, -22.9], to=[-35.5, -7.5], d=0.8, color="#ff5a3c")], own={k: "BRA" for k in ["BR-PE", "BR-PB", "BR-RN", "BR-CE"]}, od=3.0,
              balls=[dict(ll=[-37.5, -6.6], iso="BRA", face="sad", d=5.5)]),
         dict(say="E é por isso que a bandeira de Pernambuco tem um arco-íris e um sol. Ela vem da revolução de mil oitocentos e dezessete.",
              arrows=[], balls=[], hl=["BR-PE"], cards=[dict(text="Bandeira de Pernambuco:", big="nasceu em 1817", d=1.0)]),
         dict(say="Agora imagina se tivesse dado certo. O São João de Campina Grande e de Caruaru ia ser festa internacional. E na Copa, Rivaldo, Vavá, Daniel Alves e Hulk iam jogar por outra seleção.",
              hl=[], cards=[], cam=NEC, own={k: "NOR" for k in NE}, od=0.4,
              pins=[dict(ll=[-35.88, -7.23], label="Campina Grande", d=1.8), dict(ll=[-35.97, -8.28], label="Caruaru", left=True, d=2.6)],
              balls=[dict(ll=[-41, -10.5], iso="BRA", face="love", d=6.5)]),
         dict(say="Me fala: qual seria a capital da República do Nordeste? Comenta aí. E manda pro seu amigo nordestino que ia querer o passaporte novo.",
              pins=[], cam={"c": [-48, -13], "s": 1.35}, balls=[dict(ll=[-40.5, -8], iso="BRA", face="happy", d=0.4), dict(ll=[-53, -12], iso="BRA", face="sad", d=1.2)]),
     ],
     "Nove estados, 54,7 milhões de pessoas (Censo 2022): mais que Argentina, Espanha e Colômbia. E a ideia já foi tentada de verdade: Revolução Pernambucana (1817) e Confederação do Equador (1824).\n"
     "Qual seria a capital? Comenta aí. E manda pro seu amigo nordestino.",
     dict(title="E SE O|NORDESTE FOSSE|UM PAÍS?", c=[-47, -12], s=1.6, y=0.64, own={"BRA": "BRA", **{k: "NOR" for k in NE}},
          balls=[dict(ll=[-40.5, -8], iso="BRA", face="cool", r=130), dict(ll=[-53, -10], iso="BRA", face="shock", skin="red", r=140)]),
     "2026-11-19T15:00:00Z", tags=["nordeste", "república do nordeste", "confederação do equador", "revolução pernambucana", "frei caneca", "pernambuco", "fortaleza"], uf=True)
