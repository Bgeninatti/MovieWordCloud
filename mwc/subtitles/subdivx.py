import requests
from bs4 import BeautifulSoup

# Este es el parametro a buscar
busqueda = 'El secreto de sus ojos'


resp_buscar = requests.get('https://www.subdivx.com/index.php?buscar={}&accion=5&masdesc=&subtitulos=1&realiza_b=1'.format(busqueda))
cookies = resp_buscar.cookies
soup = BeautifulSoup(resp_buscar.text, 'html.parser')

titulos = soup.find_all(id='menu_detalle_buscador')
detalles = soup.find_all(id='buscador_detalle')

assert len(titulos) == len(detalles) # test
i = 0 # para test

resultados = []

for i in range(len(titulos)):
    titulo = titulos[i].text
    link_intermedio = titulos[i].find('a').get('href')
    detalle = detalles[i].find(id='buscador_detalle_sub').text
    pais = detalles[i].find(src=lambda v: v and v.startswith("/pais/")).get('src')
    resultados.append((titulo, link_intermedio, detalle, pais, ))

# se podría listar «resultados» para elegir cual.
# asumimos el primero

elegido = resultados[0]
titulo, link_intermedio, detalle, pais = elegido

# se necesita navegar a una pagina intermedia 
# para obtener el link de descarga..
resp_intermedia = requests.get(link_intermedio, cookies=cookies)
cookies = resp_intermedia.cookies
soup = BeautifulSoup(resp_intermedia.text, 'html.parser')

# Obtengo el link del srt (que viene en un RAR)
link_srt = soup.find('a', href=lambda v: v and v.startswith("bajar.php")).get('href')


import rarfile, io

# Descargo el RAR, en la variable «z»

srt_filename = ''
with requests.get('https://www.subdivx.com/' + link_srt, 
                cookies=cookies, stream=True,
                allow_redirects=True,
                headers={'Referer': link_intermedio}) as r:
    r.raise_for_status()
    z = rarfile.RarFile(io.BytesIO(r.content))
    for filename in z.namelist():
        # busco un archivo srt dentro del rar 
        if '.srt' in filename:
            srt_filename = filename


# extraigo el archivo srt, si quiero
z.extract(srt_filename)


# proceso el srt...
import srt

# esta funcion es util porque los archivos estan subidos con
# con cualquier encoding
def decode_srt(filename, encoding='utf-8', retry=True):
    with open(filename, 'r', encoding=encoding) as srt_file:
        text = "".join(srt_file.readlines())
        try: 
            subs = list(srt.parse(text))
        except srt.SRTParseError:
            if retry:
                if encoding != 'latin-1':
                    subs = decode_srt(filename, 'latin-1')
                else:
                    subs = decode_srt(filename, 'ISO-8859-15', False)
    return subs

# anda.
subs = decode_srt(srt_filename)
todos_los_dialogos = "".join([sub.content for sub in subs])

