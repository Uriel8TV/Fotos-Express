# generador_pdf.py
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from config import CARTA_ANCHO, CARTA_ALTO, MEDIDAS_FOTOS, MARGEN_IZQUIERDO, MARGEN_SUPERIOR, MM_A_PUNTOS


def dibujar_marco_punteado(c, x, y, ancho, alto):
    """Dibuja una línea guía gris y punteada para corte con guillotina"""
    c.saveState()
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.setLineWidth(0.5)
    c.setDash(2, 2)
    c.rect(x, y, ancho, alto, stroke=1, fill=0)
    c.restoreState()


def crear_pdf_combo(imagenes_procesadas):
    # --- MODIFICACIÓN DE RUTA ABSOLUTA INTELIGENTE ---
    # 1. Definimos las rutas más comunes de tu sistema de forma fija
    rutas_posibles = [
        r"D:\Users\Uriel\Escritorio",
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop"),
        os.path.join(os.path.expanduser("~"), "OneDrive", "Escritorio"),
        os.path.join(os.path.expanduser("~"), "Escritorio")
    ]

    # 2. Buscamos cuál de esas carpetas sí existe físicamente en tu PC
    ruta_escritorio = None
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            ruta_escritorio = ruta
            break

    # 3. Si no encuentra ninguna (caso raro), la crea en la raíz del proyecto
    if not ruta_escritorio:
        ruta_escritorio = os.getcwd()

    carpeta_destino = os.path.join(ruta_escritorio, "Archivos Fotos")

    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    # El resto del código se queda exactamente igual abajo...
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_salida = os.path.join(carpeta_destino, f"Combo_Fotos_{timestamp}.pdf")

    c = canvas.Canvas(ruta_salida, pagesize=(CARTA_ANCHO, CARTA_ALTO))

    rutas_temporales = {}
    for tipo, img in imagenes_procesadas.items():
        ruta_tmp = f"temp_{tipo}.jpg"
        img.save(ruta_tmp, "JPEG", quality=95)
        rutas_temporales[tipo] = ruta_tmp

    # --- 1. FOTOS INFANTILES (6 piezas arriba) ---
    w_inf, h_inf = MEDIDAS_FOTOS["infantil"]
    separacion_x = 5.0 * MM_A_PUNTOS
    x_inicio = MARGEN_IZQUIERDO
    y_infantil = CARTA_ALTO - MARGEN_SUPERIOR - h_inf

    for i in range(6):
        x_pos = x_inicio + i * (w_inf + separacion_x)
        c.drawImage(rutas_temporales["infantil"], x_pos, y_infantil, width=w_inf, height=h_inf)
        dibujar_marco_punteado(c, x_pos, y_infantil, w_inf, h_inf)

    # --- 2. FOTOS CREDENCIAL (2 piezas en medio) ---
    w_cred, h_cred = MEDIDAS_FOTOS["credencial"]
    y_credencial = y_infantil - h_cred - (10.0 * MM_A_PUNTOS)

    for i in range(2):
        x_pos = x_inicio + i * (w_cred + separacion_x)
        c.drawImage(rutas_temporales["credencial"], x_pos, y_credencial, width=w_cred, height=h_cred)
        dibujar_marco_punteado(c, x_pos, y_credencial, w_cred, h_cred)

    # --- 3. FOTO POSTAL (1 pieza grande abajo) ---
    w_post, h_post = MEDIDAS_FOTOS["postal"]
    y_postal = y_credencial - h_post - (10.0 * MM_A_PUNTOS)

    c.drawImage(rutas_temporales["postal"], x_inicio, y_postal, width=w_post, height=h_post)
    dibujar_marco_punteado(c, x_inicio, y_postal, w_post, h_post)

    c.showPage()
    c.save()

    for ruta in rutas_temporales.values():
        if os.path.exists(ruta):
            os.remove(ruta)

    return ruta_salida
