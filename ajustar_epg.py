import gzip
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import urllib.request

# Download do EPG original
url = 'https://epgshare01.online/epgshare01/epg_ripper_PT1.xml.gz'
urllib.request.urlretrieve(url, 'epg.xml.gz')

# Descomprimir
with gzip.open('epg.xml.gz', 'rb') as f_in:
    xml_data = f_in.read()

# Parse XML
root = ET.fromstring(xml_data)

def ajustar_data(data_str):
    dt = datetime.strptime(data_str, "%Y%m%d%H%M%S %z")
    dt += timedelta(minutes=1)
    return dt.strftime("%Y%m%d%H%M%S %z")

# Ajustar horários
for prog in root.findall('programme'):
    prog.set('start', ajustar_data(prog.get('start')))
    prog.set('stop', ajustar_data(prog.get('stop')))

# Guardar XML corrigido
ET.ElementTree(root).write("epg_corrigido.xml", encoding="utf-8", xml_declaration=True)
