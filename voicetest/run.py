import asyncio, edge_tts, os, subprocess
TEXT = ("Um salário de três mil reais em janeiro de 2019. Quanto ele precisa ser hoje para comprar o mesmo? "
        "Na média dos preços medidos pelo IPCA, hoje ele precisa ser de quatro mil, quinhentos e doze reais. "
        "Os preços subiram cinquenta por cento no período, segundo o IBGE.")
async def main():
    vs = [v["ShortName"] for v in await edge_tts.list_voices() if v["Locale"] == "pt-BR"]
    print("vozes pt-BR:", vs)
    os.makedirs("out_v", exist_ok=True)
    for v in vs:
        await edge_tts.Communicate(TEXT, v, rate="+0%").save(f"out_v/{v}.mp3")
        print("ok", v)
asyncio.run(main())
