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


def dibujar_marca_de_agua(c):
    """Dibuja el logotipo y branding de Foto-Express firmado por Core-TECH"""
    c.saveState()

    # Nombre de tu marca principal
    c.setFillColorRGB(0.15, 0.15, 0.15)
    c.setFont("Helvetica-Bold", 13)
    x_logo = CARTA_ANCHO - (85 * MM_A_PUNTOS)
    y_logo = 35 * MM_A_PUNTOS
    c.drawString(x_logo, y_logo, "Core-TECH Soluciones Digitales")

    # Línea divisoria elegante
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.setLineWidth(0.8)
    c.line(x_logo, y_logo - (5 * MM_A_PUNTOS), x_logo + (75 * MM_A_PUNTOS), y_logo - (5 * MM_A_PUNTOS))

    # Eslogan comercial del producto
    c.setFillColorRGB(0.45, 0.45, 0.45)
    c.setFont("Helvetica", 9)
    c.drawString(x_logo, y_logo - (14 * MM_A_PUNTOS), "Fotografías instantáneas de calidad")

    c.restoreState()


def crear_pdf_combo(imagenes_procesadas):
    # --- ENRUTADOR INTELIGENTE CON PRIORIDAD EN ONEDRIVE ---
    ruta_usuario = os.path.expanduser("~")

    rutas_posibles = [
        os.path.join(ruta_usuario, "OneDrive", "Escritorio"),
        os.path.join(ruta_usuario, "OneDrive", "Desktop"),
        os.path.join(ruta_usuario, "Desktop"),
        os.path.join(ruta_usuario, "Escritorio"),
        r"D:\Users\Uriel\Escritorio"
    ]

    ruta_escritorio = None
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            if os.access(ruta, os.W_OK):
                ruta_escritorio = ruta
                break

    if not ruta_escritorio:
        ruta_escritorio = os.getcwd()

    carpeta_destino = os.path.join(ruta_escritorio, "Archivos Fotos")

    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_salida = os.path.join(carpeta_destino, f"Combo_Fotos_{timestamp}.pdf")

    c = canvas.Canvas(ruta_salida, pagesize=(CARTA_ANCHO, CARTA_ALTO))

    # CAMBIO 1: Guardar las imágenes temporales en formato PNG (Sin pérdida de compresión)
    rutas_temporales = {}
    for tipo, img in imagenes_procesadas.items():
        ruta_tmp = f"temp_{tipo}.png"
        img.save(ruta_tmp, "PNG")  # PNG nativo mantiene los píxeles perfectos
        rutas_temporales[tipo] = ruta_tmp

    # --- 1. FOTOS INFANTILES (6 piezas arriba) ---
    w_inf, h_inf = MEDIDAS_FOTOS["infantil"]
    separacion_x = 5.0 * MM_A_PUNTOS
    x_inicio = MARGEN_IZQUIERDO
    y_infantil = CARTA_ALTO - MARGEN_SUPERIOR - h_inf

    for i in range(6):
        x_pos = x_inicio + i * (w_inf + separacion_x)
        # CAMBIO 2: Se agrega mask='auto' para forzar la máxima resolución de impresión
        c.drawImage(rutas_temporales["infantil"], x_pos, y_infantil, width=w_inf, height=h_inf, mask='auto')
        dibujar_marco_punteado(c, x_pos, y_infantil, w_inf, h_inf)

    # --- 2. FOTOS CREDENCIAL (2 piezas en medio) ---
    w_cred, h_cred = MEDIDAS_FOTOS["credencial"]
    y_credencial = y_infantil - h_cred - (10.0 * MM_A_PUNTOS)

    for i in range(2):
        x_pos = x_inicio + i * (w_cred + separacion_x)
        # CAMBIO 2: Se agrega mask='auto'
        c.drawImage(rutas_temporales["credencial"], x_pos, y_credencial, width=w_cred, height=h_cred, mask='auto')
        dibujar_marco_punteado(c, x_pos, y_credencial, w_cred, h_cred)

    # --- 3. FOTO POSTAL (1 pieza grande abajo) ---
    w_post, h_post = MEDIDAS_FOTOS["postal"]
    y_postal = y_credencial - h_post - (10.0 * MM_A_PUNTOS)

    # CAMBIO 2: Se agrega mask='auto'
    c.drawImage(rutas_temporales["postal"], x_inicio, y_postal, width=w_post, height=h_post, mask='auto')
    dibujar_marco_punteado(c, x_inicio, y_postal, w_post, h_post)

    # --- CAMBIO 3: Dibujar los elementos de branding de la App ---
    dibujar_marca_de_agua(c)

    c.showPage()
    c.save()

    for ruta in rutas_temporales.values():
        if os.path.exists(ruta):
            os.remove(ruta)

    return ruta_salida
