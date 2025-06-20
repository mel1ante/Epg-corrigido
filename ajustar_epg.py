import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import gzip

# Fazer download do ficheiro original
url = "https://epgshare01.online/epgshare01/epg_ripper_PT1.xml.gz"
r = requests.get(url)
with open("epg_ripper_PT1.xml.gz", "wb") as f:
    f.write(r.content)

# Descomprimir o ficheiro original
with gzip.open("epg_ripper_PT1.xml.gz", "rb") as f:
    tree = ET.parse(f)

root = tree.getroot()

# Função para somar 1 minuto ao formato de tempo EPG
def ajustar_tempo(data_str):
    dt = datetime.strptime(data_str, "%Y%m%d%H%M%S %z")
    dt += timedelta(minutes=1)
    return dt.strftime("%Y%m%d%H%M%S %z")

# Ajustar horários dos elementos <programme>
for prog in root.findall("programme"):
    prog.attrib["start"] = ajustar_tempo(prog.attrib["start"])
    prog.attrib["stop"] = ajustar_tempo(prog.attrib["stop"])

# Guardar o novo ficheiro corrigido
tree.write("epg_corrigido.xml", encoding="utf-8", xml_declaration=True)
