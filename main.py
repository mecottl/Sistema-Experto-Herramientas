import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import shutil
from PIL import Image, ImageTk 

# ==========================================
# 1. CONFIGURACIÓN Y MAPEOS
# ==========================================

NOMBRE_ARCHIVO_HECHOS = "base_hechos.json"
CARPETA_IMG = "imagenes"

# Traducción de los Botones (A, B, C) a Valores Internos
# IMPORTANTE: Esto asegura que el código (ej: AAAA) coincida con la lógica
MAPAS = {
    0: {"A": "carpinteria", "B": "electricidad", "C": "mecanica", "D": "pintura_albanileria"},
    1: {"A": "manual_portatil", "B": "portatil_motorizada", "C": "estacionaria"},
    2: {"A": "precision", "B": "fuerza", "C": "medicion"},
    3: {"A": "madera", "B": "metal", "C": "multiuso"}
}

# Texto que ve el usuario en los botones
BASE_CONOCIMIENTOS = {
    0: {
        "pregunta": "¿Cuál es el uso de la herramienta?",
        "opciones": {"A": "A) Carpintería", "B": "B) Electricidad", "C": "C) Mecánica", "D": "D) Pintura / Albañilería"}
    },
    1: {
        "pregunta": "¿Cuál es la movilidad de la herramienta?",
        "opciones": {"A": "A)Manual portátil", "B": "B) Portátil motorizada", "C": "C) Estacionaria"}
    },
    2: {
        "pregunta": "¿Qué tipo de acción ejecuta la herramienta?",
        "opciones": {"A": "A) Precisión", "B": "B) Fuerza", "C": "C) Medición"}
    },
    3: {
        "pregunta": "¿Con qué material se usa la herramienta?",
        "opciones": {"A": "A) Madera", "B": "B) Metal", "C": "C) Multiuso"}
    }
}

class SistemaExpertoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto: Herramientas")
        self.root.geometry("950x750")
        
        if not os.path.exists(CARPETA_IMG):
            os.makedirs(CARPETA_IMG)

        self.base_hechos = self.cargar_base_hechos()
        self.respuestas_usuario = [] 
        
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"))

        self.crear_interfaz_principal()

    def motor_inferencia(self, uso_input, mov_input, acc_input, mat_input):
        print(f"BUSCANDO: {uso_input} / {mov_input} / {acc_input} / {mat_input}")
        
        for hecho in self.base_hechos:
            if (hecho["uso"] == uso_input and
                hecho["movilidad"] == mov_input and
                hecho["accion"] == acc_input and
                hecho["material"] == mat_input):
                return hecho
        return None

    # GESTIÓN DE ARCHIVOS
    def cargar_base_hechos(self):
        if os.path.exists(NOMBRE_ARCHIVO_HECHOS):
            try:
                with open(NOMBRE_ARCHIVO_HECHOS, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    if isinstance(datos, list): return datos 
            except: pass
        self.guardar_base_hechos(BASE_HECHOS_INICIAL)
        return BASE_HECHOS_INICIAL

    def guardar_base_hechos(self, data=None):
        if data is None: data = self.base_hechos
        with open(NOMBRE_ARCHIVO_HECHOS, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # INTERFAZ GRÁFICA
    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def crear_interfaz_principal(self):
        self.limpiar_ventana()
        # Ajusté un poco el padding general para dar espacio a la imagen
        frame = ttk.Frame(self.root, padding="30")
        frame.pack(expand=True, fill="both")

        # --- NUEVO: SECCIÓN DE IMAGEN BANNER ---
        ruta_banner = os.path.join(CARPETA_IMG, "Herramientas.png")
        
        # Verificamos si la imagen existe antes de intentar cargarla
        if os.path.exists(ruta_banner):
            try:
                pil_img = Image.open(ruta_banner)
                
                # --- Redimensionado Proporcional ---
                # Definimos un ancho objetivo (ej. 450px) y calculamos la altura para no deformarla
                target_width = 200
                width_percent = (target_width / float(pil_img.size[0]))
                target_height = int((float(pil_img.size[1]) * float(width_percent)))
                # Redimensionar usando LANCZOS para buena calidad
                pil_img = pil_img.resize((target_width, target_height), Image.Resampling.LANCZOS)

                # Convertir a formato Tkinter
                tk_img = ImageTk.PhotoImage(pil_img)
                
                # ¡IMPORTANTE! Guardar una referencia para evitar que el recolector de basura la borre
                frame.banner_ref = tk_img

                # Crear etiqueta para la imagen y mostrarla
                img_label = ttk.Label(frame, image=tk_img)
                # pady=(0, 20) da 0 espacio arriba y 20 abajo (separación del título)
                img_label.pack(pady=(0, 20))
                
            except Exception as e:
                print(f"Error al cargar la imagen de portada: {e}")
                # Opcional: mostrar un texto si falla
                # ttk.Label(frame, text="[Imagen de Portada no disponible]", foreground="gray").pack(pady=(0,20))
        # ---------------------------------------

        ttk.Label(frame, text="SISTEMA EXPERTO DE RECOMENDACIÓN DE HERRAMIENTAS", style="Header.TLabel").pack(pady=10)
        ttk.Label(frame, text="Sistema que recomienda las herramientas ideal según el tipo de trabajo y material a utilizar.").pack(pady=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=40)

        ttk.Button(btn_frame, text="Iniciar Consulta", command=self.iniciar_consulta, width=25).grid(row=0, column=0, padx=20, ipady=10)
        ttk.Button(btn_frame, text="Modo Experto ", command=self.abrir_modo_experto, width=25).grid(row=0, column=1, padx=20, ipady=10)
    def iniciar_consulta(self):
        self.respuestas_usuario = []
        self.mostrar_pregunta(0)

    def mostrar_pregunta(self, indice_pregunta):
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, padding="30")
        frame.pack(expand=True, fill="both")
        info_pregunta = BASE_CONOCIMIENTOS[indice_pregunta]
        ttk.Label(frame, text=f"Paso {indice_pregunta + 1} de 4", foreground="#7f8c8d").pack(anchor="w")
        ttk.Label(frame, text=info_pregunta["pregunta"], style="Header.TLabel").pack(pady=20)
        for codigo, texto in info_pregunta["opciones"].items():
            btn = ttk.Button(frame, text=f"{texto}", command=lambda c=codigo: self.procesar_respuesta(c, indice_pregunta))
            btn.pack(fill="x", pady=8, padx=100, ipady=5)
        ttk.Button(frame, text="Cancelar Operación", command=self.crear_interfaz_principal).pack(pady=30)

    def procesar_respuesta(self, codigo_respuesta, indice_actual):
        self.respuestas_usuario.append(codigo_respuesta)
        if indice_actual < 3:
            self.mostrar_pregunta(indice_actual + 1)
        else:
            self.mostrar_resultado()

    def mostrar_resultado(self):
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill="both")

        # 1. Obtener valores lógicos de las respuestas
        val_uso = MAPAS[0][self.respuestas_usuario[0]]
        val_mov = MAPAS[1][self.respuestas_usuario[1]]
        val_acc = MAPAS[2][self.respuestas_usuario[2]]
        val_mat = MAPAS[3][self.respuestas_usuario[3]]

        # 2. Ejecutar Motor de Inferencia
        resultado = self.motor_inferencia(val_uso, val_mov, val_acc, val_mat)

        if resultado:
            # --- CASO DE ÉXITO ---
            ttk.Label(frame, text="Herramienta Recomendada:", foreground="green").pack()
            nombre_mostrar = resultado.get("nombre", resultado["id"])
            ttk.Label(frame, text=nombre_mostrar, style="Header.TLabel").pack(pady=10)
            
            # Mostrar Imagen
            self.mostrar_imagen(frame, nombre_mostrar)

            # ==================================================
            # LÓGICA DE EXPLICACIÓN OCULTA (TOGGLE)
            # ==================================================
            
            # Frame contenedor (invisible) para organizar el texto
            frame_expl = ttk.Frame(frame)
            frame_expl.pack(pady=10, fill="x")

            # El Label con la explicación (NO se empaca todavía, está en memoria)
            lbl_texto = ttk.Label(frame_expl, text=resultado["explicacion"], 
                                  wraplength=700, justify="center", 
                                  background="#f0f0f0", padding=10, relief="solid", borderwidth=1)

            # Función interna para mostrar/ocultar
            def toggle_explicacion():
                if lbl_texto.winfo_ismapped(): # ¿Está visible?
                    lbl_texto.pack_forget()    # Ocultar
                    btn_toggle.config(text="Ver Explicación Técnica ▼")
                else:                          # ¿Está oculto?
                    lbl_texto.pack(pady=5)     # Mostrar
                    btn_toggle.config(text="Ocultar Explicación ▲")

            # Botón interruptor
            btn_toggle = ttk.Button(frame, text="Ver Explicación Técnica ▼", command=toggle_explicacion)
            btn_toggle.pack(pady=5)
            # ==================================================

            # Botones de Acción
            btn_area = ttk.Frame(frame)
            btn_area.pack(pady=20)
            ttk.Button(btn_area, text="Editar en Modo Experto", command=lambda: self.abrir_modo_experto(datos_editar=resultado)).pack(side="left", padx=10)
            ttk.Button(btn_area, text="Inicio", command=self.crear_interfaz_principal).pack(side="left", padx=10)
        
        else:
            ttk.Label(frame, text="Herramienta No Encontrada", style="Header.TLabel", foreground="#c0392b").pack(pady=20)
            
            texto_ctx = f"Camino escogido: {val_uso} > {val_mov} > {val_acc} > {val_mat}"
            ttk.Label(frame, text=texto_ctx, font=("Consolas", 9)).pack(pady=5)
            
            btn_area = ttk.Frame(frame)
            btn_area.pack(pady=20)
            
            # Pre-llenar datos para enseñar al sistema
            datos_nuevos = {"uso": val_uso, "movilidad": val_mov, "accion": val_acc, "material": val_mat}
            
            ttk.Button(btn_area, text="Agregar al sistema", 
                       command=lambda: self.abrir_modo_experto(datos_editar=datos_nuevos, es_nuevo=True)).pack(side="left", padx=10)
            ttk.Button(btn_area, text="Inicio", command=self.crear_interfaz_principal).pack(side="left", padx=10)
    def mostrar_imagen(self, parent, nombre_herramienta):
        # Esta función busca la imagen con variaciones de extensión
        canvas = tk.Canvas(parent, width=300, height=200, bg="#ecf0f1", highlightthickness=0)
        canvas.pack(pady=10)

        # Buscar archivo exacto o con variaciones
        nombres_posibles = [
            nombre_herramienta, # Nombre exacto del JSON
            nombre_herramienta + ".png",
            nombre_herramienta + ".jpg",
            nombre_herramienta + ".jpeg",
            nombre_herramienta.replace(".png", ".jpg")
        ]
        
        ruta_final = None
        for n in nombres_posibles:
            path = os.path.join(CARPETA_IMG, n)
            if os.path.exists(path):
                ruta_final = path
                break
        
        if ruta_final:
            try:
                pil_img = Image.open(ruta_final)
                pil_img.thumbnail((300, 200), Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(pil_img)
                parent.tk_img_ref = tk_img
                canvas.create_image(150, 100, image=tk_img)
            except:
                canvas.create_text(150, 100, text="Error imagen")
        else:
            canvas.create_text(150, 100, text=f"Imagen no encontrada:\n{nombre_herramienta}", fill="gray")

 # ==========================================
    # 4. MODO EXPERTO (EDICIÓN Y APRENDIZAJE)
    # ==========================================
    def abrir_modo_experto(self, datos_editar=None, es_nuevo=False):
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill="both")

        # Título dinámico
        titulo = "Adquisición de Conocimiento" if es_nuevo else ("Editor de Hechos" if datos_editar else "Gestor de Base de Hechos")
        ttk.Label(frame, text=titulo, style="Header.TLabel").pack(pady=10)

        # Marco para las Reglas (Comboboxes)
        form_frame = ttk.LabelFrame(frame, text="Definición de Reglas y Atributos", padding="15")
        form_frame.pack(pady=10, fill="x")

        vars_seleccion = []
        
        # Recuperar valores actuales si estamos editando
        valores_actuales = [None]*4
        if datos_editar:
            valores_actuales[0] = datos_editar.get("uso")
            valores_actuales[1] = datos_editar.get("movilidad")
            valores_actuales[2] = datos_editar.get("accion")
            valores_actuales[3] = datos_editar.get("material")

        # Generar formulario dinámico (4 preguntas)
        for i in range(4):
            row_f = ttk.Frame(form_frame)
            row_f.pack(fill="x", pady=5)
            ttk.Label(row_f, text=BASE_CONOCIMIENTOS[i]["pregunta"], width=45).pack(side="left")
            
            # Crear lista de opciones legibles para el humano (UI)
            values_ui = []
            for codigo, texto_ui in BASE_CONOCIMIENTOS[i]["opciones"].items():
                values_ui.append(texto_ui)
            
            cbox = ttk.Combobox(row_f, values=values_ui, state="readonly", width=30)
            cbox.pack(side="left")
            cbox.mapa_interno = MAPAS[i] # Guardamos el mapa para traducción inversa
            
            # Pre-seleccionar valor si estamos editando
            if valores_actuales[i]:
                # Buscar qué Texto UI corresponde al valor interno de la base de datos
                val_buscado = valores_actuales[i]
                for cod, val in MAPAS[i].items():
                    if val == val_buscado:
                        cbox.set(BASE_CONOCIMIENTOS[i]["opciones"][cod])
                        break
            
            vars_seleccion.append(cbox)

        # Sección de Datos Descriptivos (ID, Nombre, Explicación)
        detail_frame = ttk.LabelFrame(frame, text="Datos Descriptivos", padding="15")
        detail_frame.pack(pady=10, fill="x")

        ttk.Label(detail_frame, text="ID Único (sin espacios):").grid(row=0, column=0, sticky="w")
        entry_id = ttk.Entry(detail_frame, width=40)
        entry_id.grid(row=0, column=1, pady=5, sticky="w")

        ttk.Label(detail_frame, text="Nombre Comercial:").grid(row=1, column=0, sticky="w")
        entry_nombre = ttk.Entry(detail_frame, width=40)
        entry_nombre.grid(row=1, column=1, pady=5, sticky="w")
        
        ttk.Label(detail_frame, text="Explicación / Ruta:").grid(row=2, column=0, sticky="nw")
        entry_explicacion = tk.Text(detail_frame, height=5, width=50)
        entry_explicacion.grid(row=2, column=1, pady=5, sticky="w")

        # Pre-llenado de campos de texto
        if datos_editar:
            entry_id.insert(0, datos_editar.get("id", ""))
            entry_nombre.insert(0, datos_editar.get("nombre", ""))
            entry_explicacion.insert("1.0", datos_editar.get("explicacion", ""))
            # Si editamos un existente, bloqueamos el ID para no duplicar
            if not es_nuevo and "id" in datos_editar:
                entry_id.config(state="disabled")

        # Gestión de Imagen
        ttk.Label(detail_frame, text="Imagen del Producto:").grid(row=3, column=0, sticky="w")
        self.ruta_img_temp = None # Variable temporal para guardar ruta
        
        texto_imagen_actual = datos_editar.get("imagen", "No asignada") if datos_editar else "No asignada"
        lbl_img_status = ttk.Label(detail_frame, text=texto_imagen_actual, foreground="gray")
        lbl_img_status.grid(row=3, column=1, sticky="w")

        def seleccionar_img():
            ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
            if ruta:
                self.ruta_img_temp = ruta
                lbl_img_status.config(text=f"Seleccionado: {os.path.basename(ruta)}", foreground="blue")

        ttk.Button(detail_frame, text="Cargar Imagen...", command=seleccionar_img).grid(row=4, column=1, sticky="w", pady=5)

        # LÓGICA DE GUARDADO
        def guardar_cambios():
            # 1. Recuperar lógica de los Comboboxes y traducir a valores internos
            vals_seleccionados = []
            for idx, cb in enumerate(vars_seleccion):
                txt = cb.get()
                if not txt:
                    messagebox.showerror("Error", "Faltan selecciones en las reglas (Comboboxes).")
                    return
                
                # Traducción Inversa: Texto UI -> Código -> Valor Interno
                val_interno = None
                for cod, texto_opcion in BASE_CONOCIMIENTOS[idx]["opciones"].items():
                    if texto_opcion == txt:
                        val_interno = MAPAS[idx][cod]
                        break
                vals_seleccionados.append(val_interno)

            # 2. Recuperar textos
            id_obj = entry_id.get().strip()
            nombre = entry_nombre.get().strip()
            explicacion = entry_explicacion.get("1.0", tk.END).strip()

            if not id_obj or not nombre:
                messagebox.showerror("Error", "El ID y el Nombre son obligatorios.")
                return

            # 3. Procesar Imagen (Copiar archivo si se seleccionó uno nuevo)
            nombre_imagen = datos_editar.get("imagen", "") if datos_editar else ""
            if self.ruta_img_temp:
                try:
                    ext = os.path.splitext(self.ruta_img_temp)[1] # Obtener extensión (.jpg)
                    # Usamos el NOMBRE exacto de la herramienta para facilitar la búsqueda
                    nombre_imagen = f"{nombre}{ext}" 
                    shutil.copy(self.ruta_img_temp, os.path.join(CARPETA_IMG, nombre_imagen))
                except Exception as e:
                    messagebox.showwarning("Advertencia", f"Datos guardados, pero error al copiar imagen: {e}")

            # 4. Construir el Objeto Nuevo
            nuevo_hecho = {
                "id": id_obj,
                "nombre": nombre,
                "uso": vals_seleccionados[0],
                "movilidad": vals_seleccionados[1],
                "accion": vals_seleccionados[2],
                "material": vals_seleccionados[3],
                "explicacion": explicacion,
                "imagen": nombre_imagen
            }

            # 5. Actualizar la Lista (Base de Hechos)
            encontrado = False
            for idx, item in enumerate(self.base_hechos):
                if item["id"] == id_obj:
                    self.base_hechos[idx] = nuevo_hecho
                    encontrado = True
                    break
            
            if not encontrado:
                self.base_hechos.append(nuevo_hecho)

            # 6. Guardar en disco y salir
            self.guardar_base_hechos()
            messagebox.showinfo("Sistema Experto", "Base de Conocimiento Actualizada Exitosamente.")
            self.crear_interfaz_principal()

        # Botones de Acción inferior
        btn_area = ttk.Frame(frame)
        btn_area.pack(pady=20)
        ttk.Button(btn_area, text="Guardar Cambios", command=guardar_cambios).pack(side="left", padx=10)
        ttk.Button(btn_area, text="Cancelar", command=self.crear_interfaz_principal).pack(side="left", padx=10)
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaExpertoApp(root)
    root.mainloop()