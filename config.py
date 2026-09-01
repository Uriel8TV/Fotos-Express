# config.py

# Dimensiones de la hoja Carta en mm y puntos de PDF (1 mm = 2.83465 puntos)
CARTA_ANCHO_MM = 215.9
CARTA_ALTO_MM = 279.4
MM_A_PUNTOS = 2.83465

CARTA_ANCHO = CARTA_ANCHO_MM * MM_A_PUNTOS
CARTA_ALTO = CARTA_ALTO_MM * MM_A_PUNTOS

# Medidas exactas de las fotos en mm (Ancho, Alto)
MEDIDAS_FOTOS = {
    "infantil": (25.0 * MM_A_PUNTOS, 30.0 * MM_A_PUNTOS),
    "credencial": (35.0 * MM_A_PUNTOS, 50.0 * MM_A_PUNTOS),
    "postal": (100.0 * MM_A_PUNTOS, 150.0 * MM_A_PUNTOS)
}

MARGEN_IZQUIERDO = 15.0 * MM_A_PUNTOS
MARGEN_SUPERIOR = 15.0 * MM_A_PUNTOS
