"""Canal B (espanhol): orações originais. Gera specs/fe/b-es-*.json.
Textos escritos do zero (sem copiar orações de terceiros); citações bíblicas curtas (1 versículo), com referência.
Formato com evidência (pesquisa 17/11/2026, research/q_nichos_2026-11-17.json): "Oración de la noche" 2–5 min
(LUZ PARA EL ALMA, criado 31/07/2026: 40,3 mil inscritos, 160–250 mil views por vídeo) + Shorts "Antes de dormir, dile esto a Dios"."""
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fe")
os.makedirs(OUT, exist_ok=True)
VOICE = "es-MX-JorgeNeural"
TAGS = ["oración", "oración de la noche", "oración para dormir", "dios", "jesús", "fe", "oración poderosa", "salmos", "paz", "oracion catolica", "oracion cristiana"]
DESC_TAIL = ("\n\nSi esta oración tocó tu corazón, escribe \"Amén\" en los comentarios y compártela con alguien que la necesite hoy.\n"
             "Suscríbete para recibir una oración nueva cada noche.\n\n{music}\nVoz generada con inteligencia artificial; oración escrita para este canal.\n\n"
             "#oracion #oraciondelanoche #dios #fe #jesus")


def L(text, ref=None, pause=None):
    d = {"text": text}
    if ref: d["ref"] = ref
    if pause is not None: d["pause"] = pause
    return d


def save(id_, at, fmt, scene, seed, kicker, title, subtitle, lines, yt_title, yt_desc, thumb, music="Meditation Impromptu 01", tags=(), outro="Amén.", outro2="Suscríbete y comparte esta oración"):
    spec = dict(id=id_, channel="B", lang="es", voice=VOICE, rate="-10%", pitch="-2Hz", format=fmt, scene=scene, seed=seed,
                kicker=kicker, title=title, subtitle=subtitle, lines=lines, outro=outro, outro2=outro2, pause=0.9 if fmt == "long" else 0.45,
                intro=3.8 if fmt == "long" else 1.6, music=dict(track=music, vol=0.17, alt=["Meditation Impromptu 02", "Dreamer"]),
                thumb=thumb, yt=dict(title=yt_title, description=yt_desc + DESC_TAIL, tags=list(TAGS) + list(tags), lang="es", categoryId="22"),
                publish=dict(at=at))
    json.dump(spec, open(f"{OUT}/{id_}.json", "w"), ensure_ascii=False, indent=1)
    words = sum(len(l["text"].split()) for l in lines)
    print(id_, fmt, words, "palabras")


# ---------------- LARGOS ----------------
save("b-es-001", "2026-11-18T01:00:00Z", "long", "night", 11, "Oración de la noche", "Oración para dormir en paz", "Entrega tus preocupaciones a Dios", [
    L("Señor, antes de cerrar los ojos esta noche, vengo a Ti tal como estoy."),
    L("Con el cuerpo cansado, con la mente llena de pensamientos, y con el corazón que a veces no sabe qué hacer con tanto peso."),
    L("Gracias por este día, Padre. Por lo que salió bien, y también por lo que no salió como yo quería."),
    L("Porque aun en lo que no entiendo, Tú seguiste conmigo."),
    L("Hoy pongo en tus manos cada preocupación que traigo guardada.", pause=1.2),
    L("Las cuentas que no sé cómo voy a pagar. Las conversaciones que me dolieron. Las personas que amo y que no puedo cuidar como quisiera."),
    L("Todo eso te lo entrego ahora, Señor. No quiero llevarlo conmigo a la cama."),
    L("Tú dijiste: vengan a mí todos los que están cansados y cargados, y yo les daré descanso.", ref="Mateo 11:28"),
    L("Aquí estoy, Jesús. Cansado. Cargado. Y confiando en tu promesa."),
    L("Calma mi mente esta noche. Que los pensamientos que dan vueltas se queden quietos.", pause=1.2),
    L("Si me despierto en la madrugada, que lo primero que recuerde sea que Tú estás despierto por mí."),
    L("Cuida mi casa, Señor. Pon tus ángeles en cada puerta y en cada ventana."),
    L("Cuida a mi familia, a los que duermen cerca y a los que están lejos."),
    L("Cuida a los enfermos, a los que tienen miedo, y a los que esta noche no tienen dónde dormir."),
    L("Perdóname por las palabras duras de hoy, por la impaciencia, por las veces que dudé de tu amor.", pause=1.2),
    L("Y ayúdame a perdonar también, para que ningún rencor me robe el sueño."),
    L("En paz me acuesto y en paz me duermo, porque solo Tú, Señor, me haces vivir confiado.", ref="Salmo 4:8"),
    L("Mañana será un nuevo día, y tus misericordias serán nuevas otra vez."),
    L("No sé todo lo que viene, pero sé quién va delante de mí."),
    L("Por eso descanso. Por eso suelto. Por eso cierro los ojos en paz.", pause=1.4),
    L("Te lo pido en el nombre de Jesús."),
], "Oración de la Noche para Dormir en Paz | Entrega tus Preocupaciones a Dios 🙏",
    "Una oración de la noche para soltar las preocupaciones del día y dormir en la paz de Dios. Escúchala antes de dormir, en silencio, y entrega a Dios lo que te quita el sueño.",
    dict(top="ORACIÓN DE LA NOCHE", big="Suelta tus preocupaciones y duerme en paz", sub="Escúchala antes de dormir"),
    tags=["oración para dormir tranquilo", "oración de la noche para dormir en paz"])

save("b-es-002", "2026-11-19T01:00:00Z", "long", "candle", 23, "Oración de la noche", "Oración por mi familia y mi hogar", "Que la paz de Dios cubra tu casa", [
    L("Padre bueno, esta noche no vengo a pedir solo por mí. Vengo a pedir por mi familia."),
    L("Tú conoces cada nombre, cada historia y cada herida que hay dentro de esta casa."),
    L("Conoces las preocupaciones que callamos y las lágrimas que nadie ve."),
    L("Te pido, Señor, que cubras mi hogar con tu presencia.", pause=1.2),
    L("Que donde hubo gritos, haya calma. Donde hubo silencio frío, haya conversación. Donde hubo distancia, haya abrazo."),
    L("Bendice a mis padres, con su salud y con sus años. Dales fuerzas y dales paz."),
    L("Bendice a mis hijos, o a los niños que amo como si fueran míos. Guárdalos de todo mal, del peligro de la calle y del peligro que entra por una pantalla."),
    L("Bendice a mi esposo, a mi esposa, a quien camina a mi lado. Renueva el amor que el cansancio fue apagando."),
    L("Y si hay alguien en mi familia que se alejó de Ti, o que se alejó de nosotros, tráelo de vuelta, Señor, a tu tiempo y a tu manera.", pause=1.2),
    L("Tú dijiste: yo y mi casa serviremos al Señor.", ref="Josué 24:15"),
    L("Hoy lo declaro sobre mi casa. Aunque seamos imperfectos, queremos ser tuyos."),
    L("Que no falte el pan en nuestra mesa, ni el trabajo en nuestras manos, ni la fe en nuestro corazón."),
    L("Aleja de esta casa la envidia, la división, la enfermedad y el miedo."),
    L("Y cuando lleguen los días difíciles, porque llegarán, que nos encuentren unidos y de rodillas.", pause=1.2),
    L("Esta noche, mientras todos duermen, quédate en cada cuarto."),
    L("Pon tu mano sobre cada cabeza, Señor, y que cada uno descanse sabiendo que es amado."),
    L("Gracias por mi familia, con sus defectos y con su amor. Es el regalo más grande que me diste."),
    L("En el nombre de Jesús.", pause=1.4),
], "Oración de la Noche por Mi Familia y Mi Hogar | Que la Paz de Dios Cubra Tu Casa 🙏",
    "Una oración de la noche para pedir protección, unión y paz para tu familia y tu hogar. Escríbele en los comentarios el nombre de quien quieres poner en esta oración.",
    dict(top="ORACIÓN POR TU FAMILIA", big="Que la paz de Dios cubra tu casa esta noche", sub="Escúchala antes de dormir"),
    music="Meditation Impromptu 02", tags=["oración por la familia", "oración por mi hogar", "oración de protección"])

save("b-es-003", "2026-11-20T01:00:00Z", "long", "sky", 37, "Oración", "Oración para la ansiedad", "Dios tiene el control", [
    L("Señor, hoy mi mente no se detiene. El corazón va rápido y el pecho se siente apretado."),
    L("Tengo miedo de cosas que todavía no pasaron, y me canso pensando en todo lo que podría salir mal."),
    L("Por eso me detengo ahora, aunque sea un momento, para respirar delante de Ti.", pause=1.6),
    L("Respiro, y recuerdo que Tú eres Dios, y yo no."),
    L("No tengo que controlar todo. No tengo que resolver mañana esta noche."),
    L("Tu palabra me dice: por nada estén afanosos, sino presenten sus peticiones a Dios en oración, con acción de gracias.", ref="Filipenses 4:6"),
    L("Entonces te presento lo que me inquieta, Padre.", pause=1.2),
    L("El trabajo, la salud, el dinero, las relaciones, el futuro. Lo pongo todo sobre la mesa, delante de Ti."),
    L("Y te doy gracias, aunque todavía no vea la respuesta, porque sé que me escuchas."),
    L("Cambia mi ansiedad por tu paz, esa paz que no se explica, que sobrepasa todo entendimiento."),
    L("Cuando vuelvan los pensamientos que me asustan, recuérdame esta oración.", pause=1.2),
    L("Recuérdame que ya me sostuviste en días peores, y que no me soltaste."),
    L("Dame un descanso verdadero. Para el cuerpo, para la mente y para el alma."),
    L("Y si hoy alguien a mi lado también está luchando en silencio, dale a esa persona la misma paz."),
    L("Gracias, Señor, porque tienes el control, aun cuando yo siento que lo perdí todo.", pause=1.4),
    L("En tus manos estoy seguro. En el nombre de Jesús."),
], "Oración para la Ansiedad | Dios Tiene el Control 🙏 Escucha Esto Cuando Sientas Miedo",
    "Una oración corta para los momentos de ansiedad, preocupación y miedo al futuro. Respira, escucha y entrega a Dios lo que no puedes controlar.",
    dict(top="ORACIÓN PARA LA ANSIEDAD", big="Respira. Dios tiene el control", sub="Escúchala cuando sientas miedo"),
    music="Dreamer", tags=["oración para la ansiedad", "oración para la paz", "dios tiene el control"])

save("b-es-004", "2026-11-21T01:00:00Z", "long", "night", 51, "Oración de la noche", "Oración de protección para esta noche", "Inspirada en el Salmo 91", [
    L("Señor, esta noche busco refugio en Ti."),
    L("Como dice tu palabra: el que habita al abrigo del Altísimo morará bajo la sombra del Omnipotente.", ref="Salmo 91:1"),
    L("Quiero habitar ahí, Padre. No solo visitarte cuando tengo miedo, sino vivir cerca de Ti."),
    L("Tú eres mi esperanza y mi castillo. En Ti confío.", pause=1.2),
    L("Protege mi vida esta noche. Protege mi cuerpo mientras duermo y mi mente mientras sueño."),
    L("Protege mi casa de todo peligro, de todo accidente y de toda mano que quiera hacer daño."),
    L("Cubre con tu sombra a los que amo, estén donde estén."),
    L("Al que va por la carretera, al que trabaja de noche, al que está en un hospital, al que está solo."),
    L("Tu palabra promete que no temerás el terror nocturno, ni la flecha que vuele de día.", ref="Salmo 91:5"),
    L("Entonces, en tu nombre, suelto el miedo.", pause=1.4),
    L("Suelto el miedo a la enfermedad, el miedo a perder lo que tengo, el miedo a quedarme solo."),
    L("Manda a tus ángeles a cuidarme en todos mis caminos, como lo prometiste."),
    L("Y si esta noche algo intenta robarme la paz, que encuentre la puerta cerrada, porque esta casa te pertenece."),
    L("Gracias por las veces que me libraste sin que yo lo supiera.", pause=1.2),
    L("Gracias por los peligros que nunca llegaron, porque Tú estabas delante."),
    L("Hoy duermo bajo tus alas. Y mañana, cuando despierte, seguiré bajo ellas."),
    L("En el nombre de Jesús."),
], "Oración de Protección para Esta Noche | Inspirada en el Salmo 91 🙏",
    "Una oración de protección para tu vida, tu casa y tu familia, inspirada en el Salmo 91. Escúchala antes de dormir y descansa bajo las alas de Dios.",
    dict(top="SALMO 91", big="Duerme bajo la protección de Dios", sub="Oración de protección para esta noche"),
    music="Meditation Impromptu 03", tags=["salmo 91", "oración de protección", "salmo 91 para dormir"])

# ---------------- SHORTS ----------------
save("b-es-s01", "2026-11-17T23:00:00Z", "short", "night", 61, "Antes de dormir", "Antes de dormir, dile esto a Dios", None, [
    L("Señor, hoy no fue un día fácil."),
    L("Pero aquí estoy, dándote gracias igual."),
    L("Todo lo que no pude resolver, te lo entrego."),
    L("Cuida mi casa, cuida a los que amo, y cuida mi corazón."),
    L("En paz me acuesto y en paz me duermo, porque solo Tú me haces vivir confiado.", ref="Salmo 4:8"),
    L("Si crees en esto, escribe Amén."),
], "Antes de dormir, dile esto a Dios 🙏 #oracion #dios #fe",
    "Una oración corta para decirle a Dios antes de dormir.",
    dict(top="ANTES DE DORMIR", big="Dile esto a Dios", sub="Oración corta"), outro="Amén 🙏", outro2="Suscríbete para más oraciones")

save("b-es-s02", "2026-11-18T13:00:00Z", "short", "sky", 73, "Mensaje para ti", "Si estás viendo esto, no es casualidad", None, [
    L("Si este video llegó a ti hoy, no es casualidad."),
    L("Dios sabe lo que estás cargando, aunque no se lo hayas contado a nadie."),
    L("Él no te olvidó. Él no llega tarde."),
    L("Lo que hoy parece cerrado, Él lo puede abrir."),
    L("No temas, porque yo estoy contigo.", ref="Isaías 41:10"),
    L("Si lo recibes, escribe: lo recibo, Señor."),
], "Si estás viendo esto, no es casualidad 🙏 Dios quiere decirte algo #dios #fe",
    "Un mensaje corto para tu día.",
    dict(top="MENSAJE PARA TI", big="Esto no es casualidad", sub="Dios quiere decirte algo"), music="Dreamer", outro="Amén 🙏", outro2="Suscríbete para más oraciones")

save("b-es-s03", "2026-11-18T23:00:00Z", "short", "candle", 83, "Oración por tu familia", "Una oración por tu familia esta noche", None, [
    L("Señor, esta noche te pido por mi familia."),
    L("Por los que duermen cerca y por los que están lejos."),
    L("Que no falte la paz en esta casa, ni el pan en la mesa."),
    L("Sana lo que está roto entre nosotros."),
    L("Yo y mi casa serviremos al Señor.", ref="Josué 24:15"),
    L("Escribe el nombre de tu familia y di Amén."),
], "Una oración por tu familia esta noche 🙏 #oracion #familia #dios",
    "Una oración corta por tu familia.",
    dict(top="POR TU FAMILIA", big="Ora por tu casa esta noche", sub="Oración corta"), music="Meditation Impromptu 02", outro="Amén 🙏", outro2="Suscríbete para más oraciones")

save("b-es-s04", "2026-11-19T13:00:00Z", "short", "dawn", 97, "Oración de la mañana", "Antes de empezar el día", None, [
    L("Buenos días, Señor."),
    L("Antes de mirar el celular, antes de las prisas, te busco a Ti."),
    L("Guía mis pasos hoy. Cuida mis palabras. Abre las puertas correctas."),
    L("Y cierra las que me harían daño."),
    L("Este es el día que hizo el Señor; nos gozaremos y alegraremos en él.", ref="Salmo 118:24"),
    L("Escribe Amén y empieza tu día con Dios."),
], "Oración corta para empezar el día 🙏 Antes de mirar el celular #oracion #dios",
    "Una oración corta para empezar la mañana con Dios.",
    dict(top="ORACIÓN DE LA MAÑANA", big="Empieza tu día con Dios", sub="Oración corta"), music="Dreamer", outro="Amén 🙏", outro2="Suscríbete para más oraciones")
