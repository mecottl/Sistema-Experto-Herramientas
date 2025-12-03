import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import shutil
from PIL import Image, ImageTk 

# ==========================================
# 1. CONFIGURACIÓN Y COLORES
# ==========================================

NOMBRE_ARCHIVO_HECHOS = "base_hechos.json"
CARPETA_IMG = "imagenes"

COLOR_FONDO = "#F4F6F7"       
COLOR_PRIMARIO = "#2C3E50"    
COLOR_SECUNDARIO = "#3498DB"  
COLOR_SECUNDARIO_HOVER = "#2980B9"
COLOR_EXITO = "#27AE60"       
COLOR_TEXTO = "#34495E"       
FUENTE_TITULO = ("Segoe UI", 24, "bold") 
FUENTE_NORMAL = ("Segoe UI", 11)
FUENTE_BOTON = ("Segoe UI", 11, "bold")

# Mapeos Lógicos
MAPAS = {
    0: {"A": "carpinteria", "B": "electricidad", "C": "mecanica", "D": "pintura_albanileria"},
    1: {"A": "manual_portatil", "B": "portatil_motorizada", "C": "estacionaria"},
    2: {"A": "precision", "B": "fuerza", "C": "medicion"},
    3: {"A": "madera", "B": "metal", "C": "multiuso"}
}

BASE_CONOCIMIENTOS = {
    0: {
        "pregunta": "¿Cuál es el uso principal de la herramienta?",
        "opciones": {"A": "Carpintería", "B": "Electricidad", "C": "Mecánica", "D": "Pintura / Albañilería"}
    },
    1: {
        "pregunta": "¿Cuál es la movilidad de la herramienta?",
        "opciones": {"A": "Manual portátil", "B": "Portátil motorizada", "C": "Estacionaria"}
    },
    2: {
        "pregunta": "¿Qué tipo de acción ejecuta la herramienta?",
        "opciones": {"A": "Precisión", "B": "Fuerza", "C": "Medición"}
    },
    3: {
        "pregunta": "¿Con qué material se usa la herramienta?",
        "opciones": {"A": "Madera", "B": "Metal", "C": "Multiuso"}
    }
}

# Base inicial (Nombres usados como ID directamente)
BASE_HECHOS_INICIAL = [
     {
        "id": "Martillo", "nombre": "Martillo",
        "uso": "carpinteria", "movilidad": "manual_portatil", "accion": "precision", "material": "madera",
        "explicacion": "Se recomienda para trabajos de carpintería manual que requieren precisión. Código: AAAA",
        "imagen": "Martillo.png"
    }
]

class SistemaExpertoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BOB: Sistema experto en herramientas")
        self.root.geometry("1000x800")
        self.root.configure(bg=COLOR_FONDO)
        
        if not os.path.exists(CARPETA_IMG): os.makedirs(CARPETA_IMG)

        self.base_hechos = self.cargar_base_hechos()
        self.respuestas_usuario = [] 

        style = ttk.Style()
        style.theme_use('clam') 

        style.configure("Main.TFrame", background=COLOR_FONDO)
        style.configure("Header.TLabel", background=COLOR_FONDO, foreground=COLOR_PRIMARIO, font=FUENTE_TITULO)
        style.configure("SubHeader.TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=("Segoe UI", 14))
        style.configure("Body.TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_NORMAL)
        
        style.configure("Primary.TButton", font=FUENTE_BOTON, background=COLOR_SECUNDARIO, foreground="white", borderwidth=0)
        style.map("Primary.TButton", background=[('active', COLOR_SECUNDARIO_HOVER)])

        style.configure("Secondary.TButton", font=FUENTE_NORMAL, background="#BDC3C7", foreground=COLOR_TEXTO, borderwidth=0)
        style.map("Secondary.TButton", background=[('active', '#95A5A6')])

        style.configure("Option.TButton", font=FUENTE_NORMAL, background="white", foreground=COLOR_PRIMARIO, anchor="center")
        style.map("Option.TButton", background=[('active', '#ECF0F1')])

        self.mostrar_bienvenida()

    def motor_inferencia(self, uso_input, mov_input, acc_input, mat_input):
        for hecho in self.base_hechos:
            if (hecho["uso"] == uso_input and
                hecho["movilidad"] == mov_input and
                hecho["accion"] == acc_input and
                hecho["material"] == mat_input):
                return hecho
        return None

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

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_bienvenida(self):
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, style="Main.TFrame")
        frame.pack(expand=True, fill="both", padx=50, pady=50)

        self.mostrar_imagen(frame, "Herramientas.png", size=(500, 300))

        ttk.Label(frame, text="Bienvenido a BOB, tu ayudante en construcción", style="Header.TLabel").pack(pady=(30, 10))
        ttk.Label(frame, text="Sistema inteligente para la selección de herramientas.", style="SubHeader.TLabel").pack(pady=5)

        btn_start = ttk.Button(frame, text="COMENZAR", style="Primary.TButton", command=self.crear_menu_principal, cursor="hand2")
        btn_start.pack(pady=40, ipadx=30, ipady=12)

    def crear_menu_principal(self):
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, style="Main.TFrame")
        frame.pack(expand=True, fill="both", padx=40, pady=40)

        header_frame = ttk.Frame(frame, style="Main.TFrame")
        header_frame.pack(pady=(0, 40), anchor="center")
        
        self.mostrar_imagen(header_frame, "Herramientas.png", size=(150, 150)) 
        
        lbl_title = ttk.Label(header_frame, text="Menú Principal", style="Header.TLabel")
        lbl_title.pack(pady=(10, 0))

        menu_frame = ttk.Frame(frame, style="Main.TFrame")
        menu_frame.pack(expand=True)

        ttk.Label(menu_frame, text="¿Buscas una herramienta específica?", style="Body.TLabel").pack(pady=(0, 10))
        btn_consulta = ttk.Button(menu_frame, text="🔍 INICIAR CONSULTA", style="Primary.TButton", command=self.iniciar_consulta)
        btn_consulta.pack(fill="x", ipadx=50, ipady=15, pady=(0, 40))

        ttk.Separator(menu_frame, orient='horizontal').pack(fill='x', pady=10)

        ttk.Label(menu_frame, text="Agregar nuevas herramientas", style="Body.TLabel", foreground="gray").pack(pady=(20, 10))
        btn_admin = ttk.Button(menu_frame, text="⚙️ Gestionar Sistema experto", style="Secondary.TButton", command=self.abrir_modo_experto)
        btn_admin.pack(fill="x", ipady=8)

        ttk.Button(frame, text="Volver al Inicio", command=self.mostrar_bienvenida).pack(side="bottom", pady=20)

    def iniciar_consulta(self):
        self.respuestas_usuario = []
        self.mostrar_pregunta(0)

    def mostrar_pregunta(self, indice):
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, style="Main.TFrame")
        frame.pack(expand=True, fill="both", padx=50, pady=40)

        info = BASE_CONOCIMIENTOS[indice]

        ttk.Label(frame, text=f"Paso {indice + 1} de 4", style="SubHeader.TLabel", foreground=COLOR_SECUNDARIO).pack(anchor="w")
        progress = ttk.Progressbar(frame, value=(indice+1)*25, length=900)
        progress.pack(pady=(5, 30), fill="x")

        ttk.Label(frame, text=info["pregunta"], style="Header.TLabel", wraplength=800).pack(pady=20)

        opts_frame = ttk.Frame(frame, style="Main.TFrame")
        opts_frame.pack(fill="both", expand=True)

        for codigo, texto in info["opciones"].items():
            btn = ttk.Button(opts_frame, text=f"{texto}", style="Option.TButton", 
                             command=lambda c=codigo: self.procesar_respuesta(c, indice))
            btn.pack(fill="x", pady=8, ipady=8, padx=100)

        ttk.Button(frame, text="Cancelar", command=self.crear_menu_principal).pack(pady=20)

    def procesar_respuesta(self, codigo, indice):
        self.respuestas_usuario.append(codigo)
        if indice < 3:
            self.mostrar_pregunta(indice + 1)
        else:
            self.mostrar_resultado()

    def mostrar_resultado(self):
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, style="Main.TFrame")
        frame.pack(expand=True, fill="both", padx=40, pady=20)

        val_uso = MAPAS[0][self.respuestas_usuario[0]]
        val_mov = MAPAS[1][self.respuestas_usuario[1]]
        val_acc = MAPAS[2][self.respuestas_usuario[2]]
        val_mat = MAPAS[3][self.respuestas_usuario[3]]

        resultado = self.motor_inferencia(val_uso, val_mov, val_acc, val_mat)

        if resultado:
            ttk.Label(frame, text="Herramienta Identificada", style="SubHeader.TLabel", foreground=COLOR_EXITO).pack(pady=(10, 5))
            
            nombre_show = resultado["nombre"] 
            ttk.Label(frame, text=nombre_show, style="Header.TLabel", foreground=COLOR_PRIMARIO).pack(pady=10)
            
            self.mostrar_imagen(frame, resultado.get("imagen", ""), size=(350, 250))

            expl_container = ttk.Frame(frame, style="Main.TFrame")
            expl_container.pack(pady=20, fill="x")

            lbl_texto = ttk.Label(expl_container, text=resultado["explicacion"], 
                                  style="Body.TLabel", wraplength=700, justify="center",
                                  background="white", padding=15, relief="solid", borderwidth=1)

            def toggle_explicacion():
                if lbl_texto.winfo_ismapped():
                    lbl_texto.pack_forget()
                    btn_toggle.config(text="Ver Explicación Técnica ▼")
                else:
                    lbl_texto.pack(pady=10)
                    btn_toggle.config(text="Ocultar Explicación ▲")

            btn_toggle = ttk.Button(expl_container, text="Ver Explicación Técnica ▼", 
                                    style="Primary.TButton", command=toggle_explicacion)
            btn_toggle.pack()

            btn_frame = ttk.Frame(frame, style="Main.TFrame")
            btn_frame.pack(pady=20)
            ttk.Button(btn_frame, text="Editar Herramienta", command=lambda: self.abrir_modo_experto(datos_editar=resultado)).pack(side="left", padx=10)
            ttk.Button(btn_frame, text="Volver al Menú", command=self.crear_menu_principal).pack(side="left", padx=10)

        else:
            ttk.Label(frame, text="Herramienta No Encontrada", font=("Segoe UI", 18, "bold"), foreground="#E74C3C", background=COLOR_FONDO).pack(pady=30)
            
            ctx = f"Criterios: {val_uso} > {val_mov} > {val_acc} > {val_mat}"
            ttk.Label(frame, text=ctx, font=("Consolas", 11), background="#ECF0F1", padding=10).pack(pady=10)
            
            ttk.Label(frame, text="¿Desea agregar esta herramienta al sistema?", style="Body.TLabel").pack(pady=20)
            
            datos_nuevos = {"uso": val_uso, "movilidad": val_mov, "accion": val_acc, "material": val_mat}
            ttk.Button(frame, text="Sí, Enseñar al Sistema", style="Primary.TButton", 
                       command=lambda: self.abrir_modo_experto(datos_editar=datos_nuevos, es_nuevo=True)).pack(pady=10)
            ttk.Button(frame, text="Cancelar", command=self.crear_menu_principal).pack()

    def abrir_modo_experto(self, datos_editar=None, es_nuevo=False):
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, style="Main.TFrame")
        frame.pack(expand=True, fill="both", padx=30, pady=20)

        titulo = "Agregar Nueva Herramienta" if es_nuevo else ("Editor de Herramientas" if datos_editar else "Gestión de Conocimiento")
        ttk.Label(frame, text=titulo, style="Header.TLabel").pack(pady=(0, 20))

        content = ttk.Frame(frame, style="Main.TFrame")
        content.pack(fill="both", expand=True)

        left_p = ttk.LabelFrame(content, text=" Reglas Lógicas ", padding=15)
        left_p.pack(side="left", fill="both", expand=True, padx=10)

        vars_sel = []
        vals_act = [None]*4
        if datos_editar:
            vals_act = [datos_editar.get(k) for k in ["uso", "movilidad", "accion", "material"]]

        for i in range(4):
            f = ttk.Frame(left_p)
            f.pack(fill="x", pady=10)
            ttk.Label(f, text=BASE_CONOCIMIENTOS[i]["pregunta"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
            
            vals_ui = list(BASE_CONOCIMIENTOS[i]["opciones"].values())
            cb = ttk.Combobox(f, values=vals_ui, state="readonly", font=FUENTE_NORMAL)
            cb.pack(fill="x", pady=2)
            cb.mapa = MAPAS[i]
            
            if vals_act[i]:
                for k, v in MAPAS[i].items():
                    if v == vals_act[i]:
                        cb.set(BASE_CONOCIMIENTOS[i]["opciones"][k])
                        break
            vars_sel.append(cb)

        right_p = ttk.LabelFrame(content, text=" Detalles ", padding=15)
        right_p.pack(side="right", fill="both", expand=True, padx=10)

        ttk.Label(right_p, text="Nombre de la herramienta").pack(anchor="w")
        e_nom = ttk.Entry(right_p, font=FUENTE_NORMAL)
        e_nom.pack(fill="x", pady=5)
        
        ttk.Label(right_p, text="Explicación Técnica:").pack(anchor="w")
        e_exp = tk.Text(right_p, height=5, font=FUENTE_NORMAL, relief="flat", borderwidth=1)
        e_exp.pack(fill="x", pady=5)

        self.tmp_img = None
        lbl_img = ttk.Label(right_p, text="Sin imagen seleccionada", foreground="gray")
        lbl_img.pack(anchor="w", pady=(10, 0))
        
        def sel_img():
            path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
            if path:
                self.tmp_img = path
                lbl_img.config(text=os.path.basename(path), foreground=COLOR_SECUNDARIO)
        
        ttk.Button(right_p, text="Seleccionar Imagen...", command=sel_img).pack(anchor="w", pady=5)

        if datos_editar:
            e_nom.insert(0, datos_editar.get("nombre", ""))
            e_exp.insert("1.0", datos_editar.get("explicacion", ""))

        def guardar():
            sel_vals = []
            for idx, cb in enumerate(vars_sel):
                txt = cb.get()
                if not txt: 
                    messagebox.showerror("Error", "Faltan selecciones lógicas")
                    return
                found = False
                for k, v in BASE_CONOCIMIENTOS[idx]["opciones"].items():
                    if v == txt:
                        sel_vals.append(MAPAS[idx][k])
                        found = True
                        break
                if not found: sel_vals.append(None)
             
            for item in self.base_hechos:
                if (item["uso"] == sel_vals[0] and
                    item["movilidad"] == sel_vals[1] and
                    item["accion"] == sel_vals[2] and
                    item["material"] == sel_vals[3]):
                    
                    if item["id"] != uid:
                        advertencia = f"¡Cuidado! Ya existe una herramienta en este camino:\n'{item['nombre']}'\n\nSi guardas, la nueva herramienta podría no aparecer en las búsquedas."
                        respuesta = messagebox.askyesno("Conflicto de Lógica", advertencia + "\n\n¿Deseas guardarla de todos modos?")
                        if not respuesta:
                            return
                            
            nom = e_nom.get().strip()
            exp = e_exp.get("1.0", tk.END).strip()
            
            if not nom:
                messagebox.showerror("Error", "Falta el Nombre")
                return

            uid = nom 

            img_name = datos_editar.get("imagen", "") if datos_editar else ""
            
            if self.tmp_img:
                try:
                    ext = os.path.splitext(self.tmp_img)[1]
                    img_name = f"{uid}{ext}" # Nombre exacto + extensión
                    shutil.copy(self.tmp_img, os.path.join(CARPETA_IMG, img_name))
                except Exception as e:
                    messagebox.showwarning("Error Imagen", str(e))
            elif not img_name:
                img_name = f"{uid}.png"

            obj = {
                "id": uid, 
                "nombre": nom, 
                "explicacion": exp, 
                "imagen": img_name,
                "uso": sel_vals[0], 
                "movilidad": sel_vals[1], 
                "accion": sel_vals[2], 
                "material": sel_vals[3]
            }

            updated = False
            for idx, item in enumerate(self.base_hechos):
                if item["id"] == uid:
                    self.base_hechos[idx] = obj
                    updated = True
                    break
            if not updated: self.base_hechos.append(obj)
            
            self.guardar_base_hechos()
            messagebox.showinfo("Éxito", "Datos Guardados Correctamente")
            self.crear_menu_principal()

        btn_bar = ttk.Frame(frame, style="Main.TFrame")
        btn_bar.pack(pady=20)
        ttk.Button(btn_bar, text="GUARDAR CAMBIOS", style="Primary.TButton", command=guardar).pack(side="left", padx=10)
        ttk.Button(btn_bar, text="Cancelar", command=self.crear_menu_principal).pack(side="left", padx=10)

    def mostrar_imagen(self, parent, name, size=(300, 200), bg_color=COLOR_FONDO):
        canvas = tk.Canvas(parent, width=size[0], height=size[1], bg=bg_color, highlightthickness=0)
        canvas.pack(pady=(0, 10)) 
        
        path = None
        if name:
            posibles = [name, name+".png", name+".jpg", name.replace(".png", ".jpg")]
            for p in posibles:
                fp = os.path.join(CARPETA_IMG, p)
                if os.path.exists(fp):
                    path = fp
                    break
        
        if path:
            try:
                img = Image.open(path)
                img.thumbnail(size, Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(img)
                parent.ref = tk_img 
                x = (size[0] - tk_img.width()) // 2
                y = (size[1] - tk_img.height()) // 2
                canvas.create_image(x, y, anchor="nw", image=tk_img)
            except:
                canvas.create_text(size[0]//2, size[1]//2, text="Error Imagen", fill="gray")
        else:
            if name == "Herramientas.png":
                 canvas.destroy() 
            else:
                 canvas.create_text(size[0]//2, size[1]//2, text="Sin Imagen", fill="gray")

if __name__ == "__main__":
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1) 
    except: pass
    app = SistemaExpertoApp(root)
    root.mainloop()