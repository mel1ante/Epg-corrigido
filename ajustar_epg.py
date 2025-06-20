import requests
import gzip
from lxml import etree
from datetime import datetime, timedelta

# Fazer download do EPG original
url = "https://epgshare01.online/epgshare01/epg_ripper_PT1.xml.gz"
r = requests.get(url)
with open("epg_ripper_PT1.xml.gz", "wb") as f:
    f.write(r.content)

# Descomprimir o XML
with gzip.open("epg_ripper_PT1.xml.gz", "rb") as f:
    tree = etree.parse(f)

root = tree.getroot()

# Função para somar 1 minuto e 1 segundo
def ajustar_tempo(valor):
    dt = datetime.strptime(valor, "%Y%m%d%H%M%S %z")
    dt += timedelta(minutes=1, seconds=1)
    return dt.strftime("%Y%m%d%H%M%S %z")

# Corrigir tempos dos <programme>
for prog in root.findall("programme"):
    prog.attrib["start"] = ajustar_tempo(prog.attrib["start"])
    prog.attrib["stop"] = ajustar_tempo(prog.attrib["stop"])

# Guardar mantendo a formatação e codificação
tree.write("epg_corrigido.xml", encoding="utf-8", xml_declaration=True, pretty_print=True)
