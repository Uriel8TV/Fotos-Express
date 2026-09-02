import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk
from config import MEDIDAS_FOTOS
import generador_pdf


class AppFotosExpress:
    def __init__(self, root):
        self.root = root
        self.root.title("Papelería - Fotos Express")
        self.root.geometry("820x520")
        self.root.resizable(False, False)

        self.img_alta_resolucion = None  # Guarda la foto original a máxima calidad
        self.img_base = None  # Imagen en tamaño de pantalla sin deformar
        self.img_modificada = None  # Imagen con el zoom actual aplicado
        self.img_preview = None  # Objeto PhotoImage para Tkinter
        self.var_bn = tk.IntVar(value=0)

        # Coordenadas de arrastre y escala
        self.img_x = 0
        self.img_y = 0
        self.start_x = 0
        self.start_y = 0
        self.escala_zoom = 1.0

        self.crear_componentes()

    def crear_componentes(self):
        # Panel Izquierdo: Controles
        panel_izq = tk.Frame(self.root, width=350, padx=20)
        panel_izq.pack(side=tk.LEFT, fill=tk.Y)

        lbl_titulo = tk.Label(panel_izq, text="Generador de Fotos", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=20)

        self.btn_cargar = tk.Button(panel_izq, text="1. Seleccionar Foto", command=self.seleccionar_foto,
                                    font=("Arial", 11), bg="#2196F3", fg="white", width=22)
        self.btn_cargar.pack(pady=10)

        self.lbl_archivo = tk.Label(panel_izq, text="Ningún archivo seleccionado", fg="gray",
                                    font=("Arial", 9, "italic"))
        self.lbl_archivo.pack(pady=5)

        frame_zoom = tk.LabelFrame(panel_izq, text=" Ajustar Tamaño (Zoom) ", padx=5, pady=5)
        frame_zoom.pack(pady=10, fill=tk.X)

        self.btn_zoom_in = tk.Button(frame_zoom, text="➕ Acercar", command=self.acercar_foto,
                                     font=("Arial", 10, "bold"), bg="#FF9800", fg="white", width=9, state=tk.DISABLED)
        self.btn_zoom_in.pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_zoom_out = tk.Button(frame_zoom, text="➖ Alejar", command=self.alejar_foto, font=("Arial", 10, "bold"),
                                      bg="#FF9800", fg="white", width=9, state=tk.DISABLED)
        self.btn_zoom_out.pack(side=tk.RIGHT, padx=10, pady=5)

        self.chk_bn = tk.Checkbutton(panel_izq, text="Imprimir en Blanco y Negro", variable=self.var_bn,
                                     command=self.actualizar_vista_canvas, font=("Arial", 10))
        self.chk_bn.pack(pady=10)

        self.btn_generar = tk.Button(panel_izq, text="2. Generar PDF Guía", command=self.procesar_recorte_final,
                                     font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", width=22, state=tk.DISABLED)
        self.btn_generar.pack(pady=15)

        lbl_instrucciones = tk.Label(panel_izq,
                                     text="💡 Instrucciones:\n1. Usa + / - para cambiar el tamaño.\n2. Arrastra la foto con el mouse\npara encuadrar rostro y cabello.",
                                     font=("Arial", 9), fg="darkblue", justify=tk.LEFT)
        lbl_instrucciones.pack(pady=5)

        # Panel Derecho: Lienzo de Ajuste Visual
        self.panel_der = tk.LabelFrame(self.root, text=" Vista previa de Ajuste (Proporción Infantil) ")
        self.panel_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)

        self.canvas = tk.Canvas(self.panel_der, width=250, height=300, bg="#E0E0E0", highlightthickness=2,
                                highlightbackground="green")
        self.canvas.pack(pady=35)

        self.canvas.bind("<ButtonPress-1>", self.iniciar_arrastre)
        self.canvas.bind("<B1-Motion>", self.arrastrar_foto)

    def seleccionar_foto(self):
        tipos_archivos = [("Imágenes", "*.jpg *.jpeg *.png *.webp")]
        ruta = filedialog.askopenfilename(title="Selecciona la foto de origen", filetypes=tipos_archivos)

        if ruta:
            self.lbl_archivo.config(text=f"Cargada: {os.path.basename(ruta)}", fg="green")

            # Guardamos la foto original intacta sin reducir píxeles
            self.img_alta_resolucion = Image.open(ruta)

            # Crear la copia miniatura exclusiva para mostrar en pantalla
            img_cargada = self.img_alta_resolucion.copy()
            img_cargada.thumbnail((500, 500))
            self.img_base = img_cargada

            self.escala_zoom = 1.0
            self.img_x = 0
            self.img_y = 0

            self.img_modificada = self.img_base.copy()
            self.actualizar_vista_canvas()

            self.btn_generar.config(state=tk.NORMAL)
            self.btn_zoom_in.config(state=tk.NORMAL)
            self.btn_zoom_out.config(state=tk.NORMAL)

    def actualizar_vista_canvas(self):
        if not self.img_modificada:
            return

        img_temp = self.img_modificada.copy()
        if self.var_bn.get() == 1:
            img_temp = img_temp.convert("L")

        self.img_preview = ImageTk.PhotoImage(img_temp)
        self.canvas.delete("all")
        self.canvas.create_image(self.img_x, self.img_y, image=self.img_preview, anchor=tk.NW)
        self.canvas.create_rectangle(2, 2, 250, 300, outline="green", width=3)

    def acercar_foto(self):
        if not self.img_base: return
        self.escala_zoom += 0.1
        self.aplicar_escala_imagen()

    def alejar_foto(self):
        if not self.img_base: return
        if self.escala_zoom > 0.2:
            self.escala_zoom -= 0.1
            self.aplicar_escala_imagen()

    def aplicar_escala_imagen(self):
        ancho_nuevo = int(self.img_base.width * self.escala_zoom)
        alto_nuevo = int(self.img_base.height * self.escala_zoom)

        self.img_modificada = self.img_base.resize((ancho_nuevo, alto_nuevo), Image.Resampling.LANCZOS)
        self.actualizar_vista_canvas()

    def iniciar_arrastre(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def arrastrar_foto(self, event):
        if not self.img_modificada:
            return
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        self.img_x += dx
        self.img_y += dy

        self.start_x = event.x
        self.start_y = event.y
        self.actualizar_vista_canvas()

    def procesar_recorte_final(self):
        try:
            if not self.img_modificada: return
            aplicar_bn = True if self.var_bn.get() == 1 else False

            # Calcular el factor matemático entre la foto de alta calidad y la de pantalla
            factor_escala_original = self.img_alta_resolucion.width / self.img_base.width
            factor_total = factor_escala_original / self.escala_zoom

            # Mapear las coordenadas del recuadro verde (250x300) a los píxeles reales de alta calidad
            orig_x1 = int(max(0, -self.img_x) * factor_total)
            orig_y1 = int(max(0, -self.img_y) * factor_total)
            orig_x2 = int(orig_x1 + (250 * factor_total))
            orig_y2 = int(orig_y1 + (300 * factor_total))

            # Hacer el recorte directamente sobre el archivo original de máxima resolución
            img_base_recortada = self.img_alta_resolucion.crop((orig_x1, orig_y1, orig_x2, orig_y2))

            imagenes_listas = {}
            for tipo, (ancho_puntos, alto_puntos) in MEDIDAS_FOTOS.items():
                # Factor exacto para alcanzar una densidad nativa de impresión de 300 DPI puros en ReportLab (300/72)
                DPI_FACTOR = 4.1667

                # Píxeles idóneos proporcionales e independientes para cada tamaño
                px_w = int(ancho_puntos * DPI_FACTOR)
                px_h = int(alto_puntos * DPI_FACTOR)

                # Calcular proporciones exactas para evitar distorsiones o estiramientos
                proporcion_destino = px_w / px_h
                proporcion_recorte = img_base_recortada.width / img_base_recortada.height

                if proporcion_recorte > proporcion_destino:
                    # El recorte es más ancho de lo necesario, se ajustan los laterales
                    ancho_nuevo = int(img_base_recortada.height * proporcion_destino)
                    offset = (img_base_recortada.width - ancho_nuevo) // 2
                    caja_ajustada = (offset, 0, offset + ancho_nuevo, img_base_recortada.height)
                else:
                    # El recorte es más alto de lo necesario, se ajusta el margen superior/inferior
                    alto_nuevo = int(img_base_recortada.width / proporcion_destino)
                    offset = (img_base_recortada.height - alto_nuevo) // 2
                    caja_ajustada = (0, offset, img_base_recortada.width, offset + alto_nuevo)

                # Extraer el sub-recorte perfectamente encuadrado
                img_proporcional = img_base_recortada.crop(caja_ajustada)

                # Redimensionamiento fotográfico de alta calidad con filtro LANCZOS
                img_escalada = img_proporcional.resize((px_w, px_h), Image.Resampling.LANCZOS)

                if aplicar_bn:
                    img_escalada = img_escalada.convert("L")
                # --- CONTINUACIÓN EXACTA DESDE TU CORTE ---
                imagenes_listas[tipo] = img_escalada

            # Enviar las imágenes en súper resolución al constructor del PDF
            ruta_final_pdf = generador_pdf.crear_pdf_combo(imagenes_listas)

            messagebox.showinfo("¡Éxito!",
                                f"El PDF con guías de corte se guardó en tu Escritorio.\n\nCarpeta: 'Archivos Fotos'")

            # Limpiar interfaz para el siguiente flujo de trabajo
            self.btn_generar.config(state=tk.DISABLED)
            self.btn_zoom_in.config(state=tk.DISABLED)
            self.btn_zoom_out.config(state=tk.DISABLED)
            self.lbl_archivo.config(text="Ningún archivo seleccionado", fg="gray")
            self.canvas.delete("all")
            self.img_alta_resolucion = None
            self.img_base = None
            self.img_modificada = None

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar la imagen de forma correcta:\n{str(e)}")
