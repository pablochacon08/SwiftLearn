# ============================================================
# SwiftLearn - Interfaz gráfica (Tkinter)
# Proyecto de Lenguajes de Programación - ESPOL
#
# Uso:
#   python3 interfaz.py
# ============================================================

import contextlib
import io
import os
import re
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox, ttk

# Se trabaja desde la carpeta del proyecto, para que logs/ y algoritmos/
# se encuentren aunque la interfaz se abra desde otra carpeta
CARPETA_PROYECTO = os.path.dirname(os.path.abspath(__file__))
os.chdir(CARPETA_PROYECTO)

# Al importar, PLY construye el lexer y el parser e imprime sus avisos
# (warnings) en la consola. Se silencian solo aquí, en la interfaz;
# por consola (lexer.py / parser.py) se siguen viendo igual que antes.
with contextlib.redirect_stderr(io.StringIO()):
    import lexer as analizador_lexico
    import parser as analizador_sintactico


# Integrantes: nombre visible -> (NombreApellido para el log léxico,
#                                 usuarioGit para los logs sintáctico y semántico)
USUARIOS = {
    'Pablo Chacón': ('PabloChacon', 'pablochacon08'),
    'Danna Ayala': ('DannaAyala', 'ayaladanna04'),
    'Jack Vera': ('JackVera', 'cevicheman'),
}

# Categoría de cada error según el texto del mensaje (se usa la primera
# que coincida). Si ninguna coincide, la tarjeta no muestra categoría.
CATEGORIAS = (
    ('se usa antes de declararse', 'Identificadores'),
    ('constante', 'Identificadores'),
    ('es de tipo', 'Asignación de tipo'),
    ('dentro de un ciclo', 'Estructuras de Control'),
)

AVISO_SINTACTICO = ('Hay errores sintácticos; corrígelos primero, porque '
                    'pueden causar errores semánticos adicionales.')

# Paleta de colores: fondo claro, rojo suave para errores y verde suave
# para "sin errores"
COLOR = {
    'fondo': '#F4F5F7',
    'panel': '#FFFFFF',
    'borde': '#D0D5DD',
    'texto': '#1D2939',
    'suave': '#667085',
    'logo': '#2563EB',           # azul del logo SL
    'acento': '#F05138',         # naranja de Swift (botón activo)
    'acento_claro': '#FDE7E2',
    'error_fondo': '#FDECEC',
    'error_borde': '#F4B4B4',
    'error_texto': '#B42318',
    'linea_error': '#FAD4D4',    # resaltado de línea en el editor
    'ok_fondo': '#E8F6EC',
    'ok_borde': '#A6DDB6',
    'ok_texto': '#067647',
    'aviso_fondo': '#FFF5E0',
    'aviso_borde': '#F5CF85',
    'aviso_texto': '#9A5B00',
}


def separar_mensaje(mensaje):
    """Separa un mensaje de error en (línea, explicación, sugerencia).

    - línea: número de la línea, o None si el error es al final del archivo.
    - explicación: lo que va después de 'línea N:' (o 'columna C:' o
      'final del archivo:') hasta el primer punto final.
    - sugerencia: el resto del mensaje, o None si no se puede separar.
    """
    encontrada = re.search(r'línea (\d+)', mensaje)
    linea = int(encontrada.group(1)) if encontrada else None

    cuerpo = re.search(r'(?:columna \d+|línea \d+|final del archivo): (.*)',
                       mensaje, re.DOTALL)
    if not cuerpo:
        return linea, mensaje, None
    texto = cuerpo.group(1)

    fin = texto.find('. ')          # primer punto final seguido de espacio
    if fin == -1:
        return linea, texto[:1].upper() + texto[1:], None
    explicacion = texto[:fin + 1]
    sugerencia = texto[fin + 2:].strip()
    return linea, explicacion[:1].upper() + explicacion[1:], sugerencia or None


def categoria_de(mensaje):
    """Devuelve la categoría del error según su texto, o None."""
    for frase, categoria in CATEGORIAS:
        if frase in mensaje:
            return categoria
    return None


def plural_errores(cantidad):
    return f"{cantidad} error" if cantidad == 1 else f"{cantidad} errores"


class SwiftLearnApp:
    """Ventana principal de SwiftLearn."""

    def __init__(self, raiz):
        self.raiz = raiz
        raiz.title('SwiftLearn - Analizador educativo para Swift')
        raiz.geometry('1200x800')
        raiz.minsize(900, 600)
        raiz.configure(bg=COLOR['fondo'])

        self.ruta_archivo = None        # archivo abierto (para el log)
        self.etiquetas_ajustables = []  # textos de las tarjetas que se ajustan al ancho

        self._crear_fuentes()
        self._crear_estilos()

        # La ventana se divide en 4 filas: encabezado, acciones,
        # contenido (la única que crece) y barra de estado
        raiz.columnconfigure(0, weight=1)
        raiz.rowconfigure(2, weight=1)

        self._crear_encabezado()
        self._crear_barra_acciones()
        self._crear_contenido()
        self._crear_barra_estado()

    # ---------------------------------------------------------------
    # Fuentes y estilos
    # ---------------------------------------------------------------
    def _crear_fuentes(self):
        familias = set(tkfont.families())
        mono = next((f for f in ('DejaVu Sans Mono', 'Ubuntu Mono', 'Consolas',
                                 'Menlo', 'Courier New') if f in familias),
                    'TkFixedFont')
        self.f_mono = tkfont.Font(family=mono, size=11)
        self.f_normal = tkfont.nametofont('TkDefaultFont')
        self.f_normal.configure(size=10)
        base = self.f_normal.actual('family')
        self.f_negrita = tkfont.Font(family=base, size=10, weight='bold')
        self.f_pequena = tkfont.Font(family=base, size=9)
        self.f_titulo = tkfont.Font(family=base, size=18, weight='bold')
        self.f_subtitulo = tkfont.Font(family=base, size=10)
        self.f_logo = tkfont.Font(family=base, size=16, weight='bold')
        self.f_seccion = tkfont.Font(family=base, size=11, weight='bold')

    def _crear_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use('clam')    # tema que permite cambiar colores y bordes

        estilo.configure('.', background=COLOR['fondo'],
                         foreground=COLOR['texto'], font=self.f_normal)
        estilo.configure('TFrame', background=COLOR['fondo'])
        estilo.configure('TLabel', background=COLOR['fondo'])
        estilo.configure('Seccion.TLabel', background=COLOR['panel'],
                         font=self.f_seccion)

        # Botones con borde
        estilo.configure('TButton', background=COLOR['panel'],
                         bordercolor=COLOR['borde'], lightcolor=COLOR['panel'],
                         darkcolor=COLOR['panel'], padding=(14, 6),
                         relief='solid', borderwidth=1)
        estilo.map('TButton',
                   background=[('active', '#EEF0F3')],
                   bordercolor=[('active', COLOR['suave'])])

        # Botón de la última fase ejecutada (resaltado)
        estilo.configure('Activo.TButton', background=COLOR['acento_claro'],
                         bordercolor=COLOR['acento'],
                         lightcolor=COLOR['acento_claro'],
                         darkcolor=COLOR['acento_claro'],
                         foreground=COLOR['acento'], font=self.f_negrita)
        estilo.map('Activo.TButton',
                   background=[('active', '#FBD5CC')],
                   bordercolor=[('active', COLOR['acento'])])

        # Tabla de tokens con fuente monoespaciada
        estilo.configure('Treeview', background=COLOR['panel'],
                         fieldbackground=COLOR['panel'], font=self.f_mono,
                         rowheight=self.f_mono.metrics('linespace') + 6,
                         bordercolor=COLOR['borde'])
        estilo.configure('Treeview.Heading', font=self.f_negrita,
                         background='#EEF0F3', bordercolor=COLOR['borde'])
        estilo.map('Treeview', background=[('selected', '#DCE6F5')],
                   foreground=[('selected', COLOR['texto'])])

        estilo.configure('TCombobox', padding=4)
        estilo.configure('TPanedwindow', background=COLOR['fondo'])

    # ---------------------------------------------------------------
    # Encabezado: logo, título, subtítulo y selector de usuario
    # ---------------------------------------------------------------
    def _crear_encabezado(self):
        encabezado = ttk.Frame(self.raiz, padding=(16, 12, 16, 6))
        encabezado.grid(row=0, column=0, sticky='ew')
        encabezado.columnconfigure(1, weight=1)

        logo = tk.Label(encabezado, text='SL', font=self.f_logo, fg='white',
                        bg=COLOR['logo'], width=3, height=1, padx=4, pady=6)
        logo.grid(row=0, column=0, rowspan=2, padx=(0, 12))

        ttk.Label(encabezado, text='SwiftLearn', font=self.f_titulo).grid(
            row=0, column=1, sticky='sw')
        ttk.Label(encabezado, text='Analizador educativo para Swift',
                  font=self.f_subtitulo, foreground=COLOR['suave']).grid(
            row=1, column=1, sticky='nw')

        selector = ttk.Frame(encabezado)
        selector.grid(row=0, column=2, rowspan=2, sticky='e')
        ttk.Label(selector, text='Usuario:', font=self.f_negrita).pack(
            side='left', padx=(0, 6))
        self.usuario = tk.StringVar(value='Pablo Chacón')
        ttk.Combobox(selector, textvariable=self.usuario, state='readonly',
                     values=list(USUARIOS), width=16).pack(side='left')

    # ---------------------------------------------------------------
    # Barra de acciones
    # ---------------------------------------------------------------
    def _crear_barra_acciones(self):
        barra = ttk.Frame(self.raiz, padding=(16, 4, 16, 8))
        barra.grid(row=1, column=0, sticky='ew')

        ttk.Button(barra, text='Abrir', command=self.abrir).pack(
            side='left', padx=(0, 16))

        # Los botones de fase se guardan para poder resaltar el último usado
        self.botones_fase = {}
        for fase, texto in (('léxico', 'Análisis léxico'),
                            ('sintáctico', 'Análisis sintáctico'),
                            ('semántico', 'Análisis semántico')):
            boton = ttk.Button(barra, text=texto,
                               command=lambda f=fase: self.analizar(f))
            boton.pack(side='left', padx=(0, 8))
            self.botones_fase[fase] = boton

        ttk.Button(barra, text='Limpiar', command=self.limpiar).pack(
            side='right')

    # ---------------------------------------------------------------
    # Contenido: editor y tokens arriba, errores abajo a todo el ancho
    # ---------------------------------------------------------------
    def _crear_contenido(self):
        contenido = ttk.PanedWindow(self.raiz, orient='vertical')
        contenido.grid(row=2, column=0, sticky='nsew', padx=16)

        arriba = ttk.PanedWindow(contenido, orient='horizontal')
        arriba.add(self._crear_editor(arriba), weight=3)
        arriba.add(self._crear_panel_tokens(arriba), weight=2)

        contenido.add(arriba, weight=3)
        contenido.add(self._crear_panel_errores(contenido), weight=2)

    def _marco_panel(self, padre, titulo):
        """Marco blanco con borde y título, usado por los tres paneles."""
        marco = tk.Frame(padre, bg=COLOR['panel'],
                         highlightbackground=COLOR['borde'],
                         highlightcolor=COLOR['borde'],
                         highlightthickness=1)
        marco.columnconfigure(0, weight=1)
        ttk.Label(marco, text=titulo, style='Seccion.TLabel').grid(
            row=0, column=0, sticky='w', padx=10, pady=(8, 6))
        return marco

    def _crear_editor(self, padre):
        marco = self._marco_panel(padre, 'Código Swift')
        marco.rowconfigure(1, weight=1)

        area = tk.Frame(marco, bg=COLOR['panel'])
        area.grid(row=1, column=0, sticky='nsew')
        area.columnconfigure(1, weight=1)
        area.rowconfigure(0, weight=1)

        # Números de línea: un Canvas al costado que se redibuja
        # cada vez que cambia el texto o se mueve el scroll
        self.numeros = tk.Canvas(area, width=44, bg='#F2F4F7',
                                 highlightthickness=0)
        self.numeros.grid(row=0, column=0, sticky='ns')

        self.editor = tk.Text(area, font=self.f_mono, wrap='none', undo=True,
                              bg=COLOR['panel'], fg=COLOR['texto'],
                              insertbackground=COLOR['texto'],
                              selectbackground='#C7D7F0', relief='flat',
                              padx=8, pady=4, tabs=self.f_mono.measure('    '),
                              borderwidth=0, highlightthickness=0)
        self.editor.grid(row=0, column=1, sticky='nsew')

        scroll_y = ttk.Scrollbar(area, orient='vertical',
                                 command=self._scroll_editor)
        scroll_y.grid(row=0, column=2, sticky='ns')
        scroll_x = ttk.Scrollbar(area, orient='horizontal',
                                 command=self.editor.xview)
        scroll_x.grid(row=1, column=1, sticky='ew')

        def al_mover(*args):
            scroll_y.set(*args)
            self.redibujar_numeros()
        self.editor.configure(yscrollcommand=al_mover,
                              xscrollcommand=scroll_x.set)

        # Resaltado de las líneas con error (rojo claro)
        self.editor.tag_configure('error', background=COLOR['linea_error'])
        # La selección se ve por encima del resaltado de error
        self.editor.tag_raise('sel')

        self.editor.bind('<<Modified>>', self._al_modificar)
        self.editor.bind('<Configure>', lambda e: self.redibujar_numeros())
        return marco

    def _scroll_editor(self, *args):
        self.editor.yview(*args)
        self.redibujar_numeros()

    def _al_modificar(self, _evento=None):
        self.redibujar_numeros()
        self.editor.edit_modified(False)   # para recibir el próximo cambio

    def redibujar_numeros(self):
        """Dibuja el número de cada línea visible del editor."""
        self.numeros.delete('all')
        ancho = self.numeros.winfo_width()
        indice = self.editor.index('@0,0')
        while True:
            info = self.editor.dlineinfo(indice)
            if info is None:
                break
            numero = indice.split('.')[0]
            self.numeros.create_text(ancho - 8, info[1], anchor='ne',
                                     text=numero, font=self.f_mono,
                                     fill=COLOR['suave'])
            siguiente = self.editor.index(f'{indice}+1line')
            if siguiente == indice:
                break
            indice = siguiente

    def _crear_panel_tokens(self, padre):
        marco = self._marco_panel(padre, 'Tokens')
        marco.rowconfigure(1, weight=1)

        tabla_marco = tk.Frame(marco, bg=COLOR['panel'])
        tabla_marco.grid(row=1, column=0, sticky='nsew', padx=8, pady=(0, 8))
        tabla_marco.columnconfigure(0, weight=1)
        tabla_marco.rowconfigure(0, weight=1)

        self.tabla_tokens = ttk.Treeview(
            tabla_marco, columns=('linea', 'tipo', 'valor'), show='headings')
        for columna, titulo, ancho, estira in (('linea', 'Línea', 70, False),
                                               ('tipo', 'Tipo', 140, False),
                                               ('valor', 'Valor', 160, True)):
            self.tabla_tokens.heading(columna, text=titulo, anchor='w')
            self.tabla_tokens.column(columna, width=ancho, minwidth=50,
                                     stretch=estira, anchor='w')
        self.tabla_tokens.grid(row=0, column=0, sticky='nsew')

        scroll = ttk.Scrollbar(tabla_marco, orient='vertical',
                               command=self.tabla_tokens.yview)
        scroll.grid(row=0, column=1, sticky='ns')
        self.tabla_tokens.configure(yscrollcommand=scroll.set)
        return marco

    def _crear_panel_errores(self, padre):
        marco = self._marco_panel(padre, 'Errores encontrados')
        marco.rowconfigure(2, weight=1)

        # Contadores: Léxico N · Sintáctico N · Semántico N
        fila = tk.Frame(marco, bg=COLOR['panel'])
        fila.grid(row=1, column=0, sticky='w', padx=10, pady=(0, 8))
        self.contadores = {}
        for i, fase in enumerate(('léxico', 'sintáctico', 'semántico')):
            if i:
                tk.Label(fila, text='·', bg=COLOR['panel'],
                         fg=COLOR['suave']).pack(side='left', padx=4)
            etiqueta = tk.Label(fila, font=self.f_negrita, padx=8, pady=2,
                                bd=0, highlightthickness=1)
            etiqueta.pack(side='left')
            self.contadores[fase] = etiqueta
            self.poner_contador(fase, None)

        # Área de tarjetas con scroll: un Canvas que contiene un Frame
        contenedor = tk.Frame(marco, bg=COLOR['panel'])
        contenedor.grid(row=2, column=0, sticky='nsew', padx=8, pady=(0, 8))
        contenedor.columnconfigure(0, weight=1)
        contenedor.rowconfigure(0, weight=1)

        self.lienzo_tarjetas = tk.Canvas(contenedor, bg=COLOR['panel'],
                                         highlightthickness=0)
        self.lienzo_tarjetas.grid(row=0, column=0, sticky='nsew')
        scroll = ttk.Scrollbar(contenedor, orient='vertical',
                               command=self.lienzo_tarjetas.yview)
        scroll.grid(row=0, column=1, sticky='ns')
        self.lienzo_tarjetas.configure(yscrollcommand=scroll.set)

        self.tarjetas = tk.Frame(self.lienzo_tarjetas, bg=COLOR['panel'])
        self.ventana_tarjetas = self.lienzo_tarjetas.create_window(
            (0, 0), window=self.tarjetas, anchor='nw')
        # El scroll se ajusta al alto de todas las tarjetas
        self.tarjetas.bind('<Configure>', lambda e: self.lienzo_tarjetas.
                           configure(scrollregion=self.lienzo_tarjetas.bbox('all')))
        # Las tarjetas toman el ancho del panel y su texto se ajusta
        self.lienzo_tarjetas.bind('<Configure>', self._ajustar_ancho_tarjetas)

        # Rueda del mouse: se escucha en toda la ventana, pero solo mueve
        # las tarjetas si el cursor está sobre ellas
        for evento in ('<MouseWheel>', '<Button-4>', '<Button-5>'):
            self.raiz.bind_all(evento, self._rueda, add='+')
        return marco

    def _ajustar_ancho_tarjetas(self, evento=None):
        ancho = self.lienzo_tarjetas.winfo_width()
        self.lienzo_tarjetas.itemconfigure(self.ventana_tarjetas, width=ancho)
        for etiqueta in self.etiquetas_ajustables:
            etiqueta.configure(wraplength=max(ancho - 40, 200))

    def _rueda(self, evento):
        if not str(evento.widget).startswith(str(self.lienzo_tarjetas)):
            return
        if evento.num == 4 or getattr(evento, 'delta', 0) > 0:
            self.lienzo_tarjetas.yview_scroll(-1, 'units')
        else:
            self.lienzo_tarjetas.yview_scroll(1, 'units')

    def poner_contador(self, fase, cantidad):
        """Muestra el contador de una fase: verde si es 0, rojo si hay errores.
        Con cantidad None (todavía no se analiza) se ve gris con un guion."""
        if cantidad is None:
            fondo, borde, texto, valor = ('#F2F4F7', COLOR['borde'],
                                          COLOR['suave'], '–')
        elif cantidad == 0:
            fondo, borde, texto, valor = (COLOR['ok_fondo'], COLOR['ok_borde'],
                                          COLOR['ok_texto'], '0')
        else:
            fondo, borde, texto, valor = (COLOR['error_fondo'],
                                          COLOR['error_borde'],
                                          COLOR['error_texto'], str(cantidad))
        self.contadores[fase].configure(
            text=f'{fase.capitalize()} {valor}', bg=fondo, fg=texto,
            highlightbackground=borde, highlightcolor=borde)

    # ---------------------------------------------------------------
    # Barra de estado
    # ---------------------------------------------------------------
    def _crear_barra_estado(self):
        barra = tk.Frame(self.raiz, bg='#E9ECF0',
                         highlightbackground=COLOR['borde'],
                         highlightthickness=1)
        barra.grid(row=3, column=0, sticky='ew', pady=(8, 0))
        self.estado = tk.Label(barra, text='Listo', bg='#E9ECF0',
                               fg=COLOR['texto'], anchor='w', padx=16, pady=4)
        self.estado.pack(side='left')
        self.estado_log = tk.Label(barra, text='', bg='#E9ECF0',
                                   fg=COLOR['suave'], anchor='e', padx=16,
                                   pady=4)
        self.estado_log.pack(side='right')

    # ---------------------------------------------------------------
    # Tarjetas de error
    # ---------------------------------------------------------------
    def _vaciar_tarjetas(self):
        for hijo in self.tarjetas.winfo_children():
            hijo.destroy()
        self.etiquetas_ajustables.clear()
        self.lienzo_tarjetas.yview_moveto(0)

    def _tarjeta(self, colores, titulo, icono, explicacion=None,
                 sugerencia=None, categoria=None, linea=None, clic=False):
        """Crea una tarjeta. colores = (fondo, borde, color del título).
        Si clic es True, al hacer clic el editor salta a la línea del error."""
        fondo, borde, color_titulo = colores
        tarjeta = tk.Frame(self.tarjetas, bg=fondo, padx=12, pady=8,
                           highlightbackground=borde, highlightthickness=1)
        tarjeta.pack(fill='x', padx=4, pady=4)

        cabecera = tk.Frame(tarjeta, bg=fondo)
        cabecera.pack(fill='x')
        # Ícono + texto del tipo: el color no es el único indicador
        tk.Label(cabecera, text=f'{icono}  {titulo}', bg=fondo,
                 fg=color_titulo, font=self.f_negrita).pack(side='left')
        if categoria:
            tk.Label(cabecera, text=categoria, bg=COLOR['panel'],
                     fg=COLOR['suave'], font=self.f_pequena, padx=6, pady=1,
                     highlightthickness=1,
                     highlightbackground=borde).pack(side='right')

        ancho = max(self.lienzo_tarjetas.winfo_width() - 40, 200)
        if explicacion:
            texto = tk.Label(tarjeta, text=explicacion, bg=fondo,
                             fg=COLOR['texto'], justify='left', anchor='w',
                             wraplength=ancho)
            texto.pack(fill='x', pady=(4, 0))
            self.etiquetas_ajustables.append(texto)
        if sugerencia:
            texto = tk.Label(tarjeta, text=f'Cómo corregirlo: {sugerencia}',
                             bg=fondo, fg=COLOR['suave'], justify='left',
                             anchor='w', wraplength=ancho)
            texto.pack(fill='x', pady=(2, 0))
            self.etiquetas_ajustables.append(texto)

        if clic:
            # El clic funciona en cualquier parte de la tarjeta
            widgets = [tarjeta, cabecera] + list(cabecera.winfo_children()) \
                + list(tarjeta.winfo_children())
            for widget in widgets:
                widget.configure(cursor='hand2')
                widget.bind('<Button-1>', lambda e, l=linea: self.ir_a_linea(l))

    def mostrar_errores(self, fase, errores):
        """Una tarjeta por error, o una tarjeta verde si no hay errores."""
        if not errores:
            self._tarjeta((COLOR['ok_fondo'], COLOR['ok_borde'],
                           COLOR['ok_texto']),
                          f'Sin errores {fase}s', '✓')
            return
        for mensaje in errores:
            linea, explicacion, sugerencia = separar_mensaje(mensaje)
            lugar = f'Línea {linea}' if linea else 'Final del archivo'
            self._tarjeta((COLOR['error_fondo'], COLOR['error_borde'],
                           COLOR['error_texto']),
                          f'Error {fase} · {lugar}', '⚠',
                          explicacion, sugerencia, categoria_de(mensaje),
                          linea, clic=True)

    # ---------------------------------------------------------------
    # Editor: ir a una línea y resaltar líneas con error
    # ---------------------------------------------------------------
    def _ultima_linea_con_texto(self):
        codigo = self.editor.get('1.0', 'end-1c').rstrip()
        return codigo.count('\n') + 1

    def ir_a_linea(self, linea):
        """Lleva el editor a la línea indicada y la selecciona."""
        if linea is None:                       # error al final del archivo
            linea = self._ultima_linea_con_texto()
        self.editor.tag_remove('sel', '1.0', 'end')
        self.editor.tag_add('sel', f'{linea}.0', f'{linea}.end')
        self.editor.mark_set('insert', f'{linea}.0')
        self.editor.see(f'{linea}.0')
        self.editor.focus_set()

    def resaltar_lineas(self, errores):
        self.editor.tag_remove('error', '1.0', 'end')
        for mensaje in errores:
            linea = separar_mensaje(mensaje)[0]
            if linea is None:
                linea = self._ultima_linea_con_texto()
            self.editor.tag_add('error', f'{linea}.0', f'{linea + 1}.0')

    # ---------------------------------------------------------------
    # Acciones de los botones
    # ---------------------------------------------------------------
    def abrir(self):
        ruta = filedialog.askopenfilename(
            title='Abrir código Swift',
            initialdir=os.path.join(CARPETA_PROYECTO, 'algoritmos'),
            filetypes=[('Código Swift', '*.swift'), ('Todos los archivos', '*')])
        if not ruta:
            return                              # el usuario canceló
        try:
            with open(ruta, encoding='utf-8') as archivo:
                codigo = archivo.read()
        except (OSError, UnicodeDecodeError) as error:
            messagebox.showerror('No se pudo abrir',
                                 f'No se pudo leer el archivo:\n{error}')
            return

        self._limpiar_resultados()
        self.editor.delete('1.0', 'end')
        self.editor.insert('1.0', codigo)
        self.editor.edit_reset()                # el deshacer empieza aquí
        self.editor.mark_set('insert', '1.0')
        self.editor.see('1.0')
        # Ruta relativa para el log, igual que por consola: algoritmos/x.swift
        self.ruta_archivo = os.path.relpath(ruta, CARPETA_PROYECTO)
        self.estado.configure(text=f'Archivo cargado: {self.ruta_archivo}')

    def analizar(self, fase):
        """Ejecuta una sola fase sobre el texto del editor."""
        codigo = self.editor.get('1.0', 'end-1c')
        if not codigo.strip():
            messagebox.showwarning(
                'Editor vacío',
                'Escribe o abre un código Swift antes de analizarlo.')
            return

        autor, usuario_git = USUARIOS[self.usuario.get()]
        ruta = self.ruta_archivo or '(editor)'

        # Cualquier aviso que PLY imprima mientras analiza no llega a la interfaz
        with contextlib.redirect_stderr(io.StringIO()), \
                contextlib.redirect_stdout(io.StringIO()):
            if fase == 'léxico':
                resultado = analizador_lexico.analizar_codigo(codigo, autor, ruta)
            elif fase == 'sintáctico':
                resultado = analizador_sintactico.analizar_sintactico(
                    codigo, usuario_git, ruta)
            else:
                resultado = analizador_sintactico.analizar_semantico(
                    codigo, usuario_git, ruta)
        errores = resultado['errores']

        # Tabla de tokens (solo el análisis léxico la llena)
        if fase == 'léxico':
            self.tabla_tokens.delete(*self.tabla_tokens.get_children())
            for linea, tipo, valor in resultado['tokens']:
                self.tabla_tokens.insert('', 'end', values=(linea, tipo, valor))

        # Tarjetas: primero el aviso (si corresponde) y luego los errores
        self._vaciar_tarjetas()
        if fase == 'semántico' and resultado['errores_sintacticos']:
            self._tarjeta((COLOR['aviso_fondo'], COLOR['aviso_borde'],
                           COLOR['aviso_texto']),
                          'Aviso', '⚠', AVISO_SINTACTICO)
        self.mostrar_errores(fase, errores)

        self.poner_contador(fase, len(errores))
        self.resaltar_lineas(errores)
        for nombre, boton in self.botones_fase.items():
            boton.configure(style='Activo.TButton' if nombre == fase
                            else 'TButton')
        self.estado.configure(
            text=f'Análisis {fase} completado con {plural_errores(len(errores))}')
        self.estado_log.configure(text=f"Log: {resultado['log']}")

    def _limpiar_resultados(self):
        """Borra tokens, tarjetas, contadores, resaltados y barra de estado."""
        self.tabla_tokens.delete(*self.tabla_tokens.get_children())
        self._vaciar_tarjetas()
        for fase in self.contadores:
            self.poner_contador(fase, None)
        self.editor.tag_remove('error', '1.0', 'end')
        for boton in self.botones_fase.values():
            boton.configure(style='TButton')
        self.estado.configure(text='Listo')
        self.estado_log.configure(text='')

    def limpiar(self):
        self.editor.delete('1.0', 'end')
        self.editor.edit_reset()
        self.ruta_archivo = None
        self._limpiar_resultados()


if __name__ == '__main__':
    raiz = tk.Tk()
    SwiftLearnApp(raiz)
    raiz.mainloop()
