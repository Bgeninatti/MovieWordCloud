import requests
from bs4 import BeautifulSoup


busqueda = 'Argentina'


resp_buscar = requests.get('https://www.subdivx.com/index.php?buscar={}&accion=5&masdesc=&subtitulos=1&realiza_b=1'.format(busqueda))
cookies = resp_buscar.cookies
soup = BeautifulSoup(resp.text, 'html.parser')

titulos = soup.find_all(id='menu_detalle_buscador')
detalles = soup.find_all(id='buscador_detalle')

assert len(titulos) == len(detalles)

i = 0

resultados = []

for i in range(len(titulos)):
    titulo = titulos[i].text
    link_intermedio = titulos[i].find('a').get('href')
    detalle = detalles[i].find(id='buscador_detalle_sub').text
    pais = detalles[i].find(src=lambda v: v and v.startswith("/pais/")).get('src')
    resultados.append((titulo, link_intermedio, detalle, pais, ))


elegido = resultados[0]

titulo, link_intermedio, detalle, pais = elegido

resp_intermedia = requests.get(link_intermedio, cookies=cookies)
cookies = resp_intermedia.cookies
soup = BeautifulSoup(resp_intermedia.text, 'html.parser')

link_srt = soup.find('a', href=lambda v: v and v.startswith("bajar.php")).get('href')


import rarfile


srt_filename = ''
with requests.get('https://www.subdivx.com/' + link_srt, 
                cookies=cookies, stream=True,
                allow_redirects=True,
                headers={'Referer': link_intermedio}) as r:
    r.raise_for_status()
    z = rarfile.RarFile(io.BytesIO(r.content))
    for filename in z.namelist():
        if '.srt' in filename:
            z.extract(filename)
            srt_filename = filename


import srt


with open(srt_filename, 'r', encoding='latin-1') as srt_file:
    text = "".join(srt_file.readlines())
    subs = list(srt.parse(text))

todos_los_dialogos = "".join([sub.content for sub in subs])

