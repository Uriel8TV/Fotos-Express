# procesador.py
from PIL import Image


def optimizar_modo_imagen(img):
    """
    Asegura que la imagen esté en modo RGB.
    Quita transparencias (RGBA) o paletas indexadas (P) para evitar errores en el PDF.
    """
    if img.mode in ('RGBA', 'P'):
        return img.convert('RGB')
    return img


def recorte_automatico_centrado(img, ancho_objetivo, alto_objetivo):
    """
    Función de respaldo: Recorta una imagen en una proporción fija
    completamente centrada (ideal si el usuario no quiere usar el arrastre manual).
    """
    img = optimizar_modo_imagen(img)
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

    return img.crop(recuadro)
