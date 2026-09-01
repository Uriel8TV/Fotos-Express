# procesador.py
from PIL import Image


def recortar_y_redimensionar(ruta_imagen, ancho_objetivo, alto_objetivo, blanco_y_negro=False):
    """
    Recorta la imagen en una proporción fija centrada en el rostro,
    la prepara para las dimensiones del PDF y aplica filtro B/N si se solicita.
    """
    img = Image.open(ruta_imagen)

    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    ancho_orig, alto_orig = img.size
    proporcion_objetivo = ancho_objetivo / alto_objetivo
    proporcion_orig = ancho_orig / alto_orig

    if proporcion_orig > proporcion_objetivo:
        nuevo_ancho = int(alto_orig * proporcion_objetivo)
        offset = (ancho_orig - nuevo_ancho) // 2
        recuadro = (offset, 0, offset + nuevo_ancho, alto_orig)
    else:
        nuevo_alto = int(ancho_orig / proporcion_objetivo)
        offset = (alto_orig - nuevo_alto) // 2
        recuadro = (0, offset, ancho_orig, offset + nuevo_alto)

    img_recortada = img.crop(recuadro)

    if blanco_y_negro:
        img_recortada = img_recortada.convert("L")

    return img_recortada
