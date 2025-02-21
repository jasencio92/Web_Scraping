from flask import Flask
app = Flask(__name__)

# """
#    Función para cortar una imagen
# """
def cortar_imagen():  
   import base64
   import os
   filename = 'image.png'
   from PIL import Image

   img = Image.open(filename)
   area = (0, 0, 300, 300)
   cropped_img = img.crop(area)
   cropped_img.save("file.png")
   # cropped_img.show()

# """
#    Función para crear una imagen de un PDF
# """
@app.route("/cargar-pdf", methods=["POST"])
def crear_img():
   import pypdfium2 as pdfium
   #Aqui se captura el archivo PDF, para darle el tratamiento.
   pdf = pdfium.PdfDocument("sat_ale.pdf")
   n_pages = len(pdf)
   if n_pages:
      page = pdf.get_page(0)
      pil_image = page.render_topil(
         scale=1,
         rotation=0,
         crop=(0, 0, 0, 0),
         fill_colour=(255, 255, 255, 255),
         draw_annots =True,
         greyscale=False,
         optimise_mode=pdfium.OptimiseMode.NONE,
      )
      pil_image.save(f"image.png")

# """
#    Función para leer el código QR de una imagen
# """
def leer_data():
   import re
   import cv2
   import urllib3
   import requests
   from bs4 import BeautifulSoup

   image = cv2.imread('file.png')
   qcd = cv2.QRCodeDetector()
   decoded_info, points, straight_qrcode = qcd.detectAndDecode(image)
   print ("image", image)
   print ("qcd", qcd)
   print( "decoded_info", decoded_info )
   print( "points", points )
   print( "straight_qrcode", straight_qrcode )
   ###Certificados 
   requests.packages.urllib3.disable_warnings()
   requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
   try:
      requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
   except AttributeError:
      pass
   url = decoded_info
   print(url)
   # # Ejecutar GET-Request
   response = requests.get(url, verify=False)
   rfc = re.search( r'RFC: (.*?),', response.text )
   datos_sat = {
      "RFC": rfc.group(0).replace("RFC: ", '').replace(',',''),
      "CURP": "",
      "Nombre": "",
      "Apellido Paterno": "",
      "Apellido Materno": "",
      "Fecha Nacimiento": "",
      "Fecha de Inicio de operaciones": "",
      "Situación del contribuyente": "",
      "Fecha del último cambio de situación": "",
      "Entidad Federativa": "",
      "Municipio o delegación": "",
      "Localidad": "",
      "Tipo de vialidad": "",
      "Nombre de la vialidad": "",
      "Número exterior": "",
      "Número interior": "",
      "CP": "",
      "Correo electrónico": "",
      "AL": "",
      "Régimen": "",
      "Fecha de alta": ""
   }
   # x = re.search( r'<table(.*?)<\/table>', response.text )
   etiquetas_li = re.findall( r'<li>(.*?)<\/li>', response.text )
   for _idx, li in enumerate(etiquetas_li, 1):
      if _idx > 1:
         html = BeautifulSoup(li, 'html.parser')
         for _id, row in enumerate(html.select('table tr'),0):
            _td = row.findAll('td')
            if len( _td ) > 1:
               if _td[0].text.replace(':', '') in datos_sat:
                  datos_sat[_td[0].text.replace(':', '')] = _td[1].text

   # print( x.group() )
   # html = BeautifulSoup(x.group(0), 'html.parser')
   
   # for _id, row in enumerate(html.select('table tr'),0):
   #    _td = row.findAll('td')
   #    if len(_td) > 0 and _id > 0:
   #       datos_sat[_td[0].text.replace(':', '')] = _td[1].text

   print( datos_sat )

crear_img()
cortar_imagen()
leer_data()