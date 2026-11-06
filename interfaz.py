
import tkinter as tk
from tkinter import ttk, messagebox


# ==========================================================
# PROYECTO: SOFTWARE FJ (Asignar nombre)
# SISTEMA INTEGRAL DE GESTION DE CLIENTES, SERVICIOS Y RESERVAS
#
# ARCHIVO: interfaz.py
# RESPONSABLE: IVAN DARIO DELGADO - ESTUDIANTE 5
#
# DESCRIPCION:
# Desarrollo de la interfaz grafica utilizando Tkinter.
# Este archivo contiene la estructura visual y los puntos
# de integracion para conectar las funcionalidades del sistema.
#
# Los componentes se desarrollaran inicialmente por separado
# y posteriormente se integraran en el archivo maestro:
# Sistema_de_Gestión-COMPILADO.py
# Tal y como se estipulo en el plan de trabajo del proyecto grupal.
# ==========================================================


class InterfazSoftwareFJ(tk.Tk):

    def __init__(self):

        # Inicializar la ventana principal
        super().__init__()

        # Configuracion general de la ventana
        self.title("Software FJ - Sistema Integral de Gestion")
        self.geometry("1150x720")
        self.minsize(950, 600)
        self.configure(bg="#F2F4F7")

        # Asigno colores para la interfaz y dar una apariencia formal.
        self.color_principal = "#20344D"
        self.color_secundario = "#2878B5"
        self.color_fondo = "#F2F4F7"
        self.color_blanco = "#FFFFFF"
        self.color_texto = "#263445"
        self.color_borde = "#DCE2E8"

        # Construccion de la estructura principal
        self.crear_contenedor_principal()
        self.crear_menu_lateral()
        self.crear_area_principal()
        self.crear_barra_estado()

        # Mostrar pantalla inicial
        self.mostrar_inicio()

    # ======================================================
    # IVAN DELGADO - ESTUDIANTE 5 - INTERFAZ GRAFICA E INTEGRACION
    # ESTRUCTURA GENERAL DE LA APLICACION
    # ======================================================

    def crear_contenedor_principal(self):

        # Contenedor general de la aplicacion
        self.contenedor = tk.Frame(
            self,
            bg=self.color_fondo
        )

        self.contenedor.pack(
            fill="both",
            expand=True
        )

    def crear_menu_lateral(self):

        # Configuro un panel lateral para la navegacion de los modulos
        self.menu_lateral = tk.Frame(
            self.contenedor,
            bg=self.color_principal,
            width=230
        )

        self.menu_lateral.pack(
            side="left",
            fill="y"
        )

        self.menu_lateral.pack_propagate(False)

        # Nombre del sistema (Importante ver si se va a cambiar)
        tk.Label(
            self.menu_lateral,
            text="SOFTWARE FJ",
            font=("Arial", 20, "bold"),
            bg=self.color_principal,
            fg=self.color_blanco
        ).pack(pady=(35, 5))

        tk.Label(
            self.menu_lateral,
            text="Sistema Integral de Gestion",
            font=("Arial", 9),
            bg=self.color_principal,
            fg="#C8D5E3"
        ).pack(pady=(0, 35))

        # Opciones principales de navegacion
        self.crear_boton_menu("Inicio", self.mostrar_inicio)
        self.crear_boton_menu("Clientes", self.mostrar_clientes)
        self.crear_boton_menu("Servicios", self.mostrar_servicios)
        self.crear_boton_menu("Reservas", self.mostrar_reservas)

        # Separador visual
        tk.Frame(
            self.menu_lateral,
            bg="#52677F",
            height=1
        ).pack(fill="x", padx=20, pady=25)

        # Informacion inferior del sistema (version academica)
        tk.Label(
            self.menu_lateral,
            text="SOFTWARE FJ\nVersion academica",
            font=("Arial", 9),
            bg=self.color_principal,
            fg="#C8D5E3",
            justify="center"
        ).pack(side="bottom", pady=25)

    def crear_boton_menu(self, texto, comando):

        # Boton reutilizable para la navegacion
        tk.Button(
            self.menu_lateral,
            text="   " + texto,
            command=comando,
            font=("Arial", 11),
            bg=self.color_principal,
            fg=self.color_blanco,
            activebackground=self.color_secundario,
            activeforeground=self.color_blanco,
            relief="flat",
            anchor="w",
            padx=20,
            pady=13,
            cursor="hand2"
        ).pack(fill="x", padx=10, pady=3)

    def crear_area_principal(self):

        # Area donde se visualizaran los diferentes modulos
        self.area_principal = tk.Frame(
            self.contenedor,
            bg=self.color_fondo
        )

        self.area_principal.pack(
            side="left",
            fill="both",
            expand=True
        )

    def crear_barra_estado(self):

        # Barra inferior de informacion para mostrar mensajes del sistema
        self.barra_estado = tk.Label(
            self,
            text="Sistema listo | Software FJ",
            font=("Arial", 9),
            bg="#E1E6EC",
            fg="#526170",
            anchor="w",
            padx=15,
            pady=8
        )

        self.barra_estado.pack(
            side="bottom",
            fill="x"
        )

    # ======================================================
    # IVAN DELGADO - ESTUDIANTE 5 - FUNCIONES AUXILIARES DE LA INTERFAZ
    # ======================================================

    def limpiar_area(self):

        # Eliminar los elementos de la pantalla anterior
        for elemento in self.area_principal.winfo_children():
            elemento.destroy()

    def crear_titulo(self, titulo, descripcion):

        # Titulo principal de cada modulo
        tk.Label(
            self.area_principal,
            text=titulo,
            font=("Arial", 22, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", padx=35, pady=(30, 5))

        # Descripcion del modulo
        tk.Label(
            self.area_principal,
            text=descripcion,
            font=("Arial", 10),
            bg=self.color_fondo,
            fg="#687787"
        ).pack(anchor="w", padx=35, pady=(0, 25))

    def crear_boton_accion(self, contenedor, texto, comando):

        # Crear botones reutilizables para las operaciones
        return tk.Button(
            contenedor,
            text=texto,
            command=comando,
            font=("Arial", 10, "bold"),
            bg=self.color_secundario,
            fg=self.color_blanco,
            activebackground="#1C5F91",
            activeforeground=self.color_blanco,
            relief="flat",
            padx=15,
            pady=9,
            cursor="hand2"
        )

    def crear_tabla(self, contenedor, columnas, encabezados):

        # Crear una tabla reutilizable para mostrar informacion
        tabla = ttk.Treeview(
            contenedor,
            columns=columnas,
            show="headings",
            height=9
        )

        # Configurar encabezados y columnas
        for columna, encabezado in zip(columnas, encabezados):

            tabla.heading(
                columna,
                text=encabezado
            )

            tabla.column(
                columna,
                anchor="center",
                width=130
            )

        # Barra de desplazamiento vertical para agregar comodidad y hacerlo mas intuitivo
        scroll = ttk.Scrollbar(
            contenedor,
            orient="vertical",
            command=tabla.yview
        )

        tabla.configure(
            yscrollcommand=scroll.set
        )

        tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll.pack(
            side="right",
            fill="y"
        )

        return tabla

    # ======================================================
    # IVAN DELGADO - ESTUDIANTE 5 - PANTALLA PRINCIPAL
    # ======================================================

    def mostrar_inicio(self):

        self.limpiar_area()

        self.crear_titulo(
            "Panel principal",
            "Bienvenido al Sistema Integral de Gestion de Software FJ."
        )

        tk.Label(
            self.area_principal,
            text="Administracion de clientes, servicios y reservas",
            font=("Arial", 13),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", padx=35, pady=(0, 25))

        # Contenedor de tarjetas principales
        contenedor = tk.Frame(
            self.area_principal,
            bg=self.color_fondo
        )

        contenedor.pack(
            fill="x",
            padx=25
        )

        # Tarjeta de clientes
        self.crear_tarjeta(
            contenedor,
            "Clientes",
            "Registro y administracion de clientes.",
            "Ingresar",
            self.mostrar_clientes,
            0
        )

        # Tarjeta de servicios
        self.crear_tarjeta(
            contenedor,
            "Servicios",
            "Consulta de salas, equipos y asesorias.",
            "Consultar",
            self.mostrar_servicios,
            1
        )

        # Tarjeta de reservas
        self.crear_tarjeta(
            contenedor,
            "Reservas",
            "Gestion y seguimiento de reservas.",
            "Ingresar",
            self.mostrar_reservas,
            2
        )

        for columna in range(3):
            contenedor.grid_columnconfigure(
                columna,
                weight=1
            )

        # Mensaje informativo
        tk.Label(
            self.area_principal,
            text="Seleccione una opcion del menu para comenzar.",
            font=("Arial", 10, "italic"),
            bg=self.color_fondo,
            fg="#687787"
        ).pack(anchor="w", padx=35, pady=35)

    def crear_tarjeta(self, contenedor, titulo, descripcion,
                      texto_boton, comando, columna):

        # Crear una tarjeta visual para cada modulo
        tarjeta = tk.Frame(
            contenedor,
            bg=self.color_blanco,
            highlightbackground=self.color_borde,
            highlightthickness=1
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        tk.Label(
            tarjeta,
            text=titulo,
            font=("Arial", 15, "bold"),
            bg=self.color_blanco,
            fg=self.color_texto
        ).pack(anchor="w", padx=18, pady=(18, 8))

        tk.Label(
            tarjeta,
            text=descripcion,
            font=("Arial", 9),
            bg=self.color_blanco,
            fg="#687787",
            wraplength=210,
            justify="left"
        ).pack(anchor="w", padx=18, pady=(0, 18))

        self.crear_boton_accion(
            tarjeta,
            texto_boton,
            comando
        ).pack(anchor="w", padx=18, pady=(0, 18))

    # ======================================================
    # ESTUDIANTE 1 - FELIPE
    # MODULO DE GESTION DE CLIENTES
    # ======================================================

    def mostrar_clientes(self):

        self.limpiar_area()

        self.crear_titulo(
            "Gestion de clientes",
            "Registro, consulta y administracion de clientes."
        )

        # --------------------------------------------------
        # PUNTO DE INTEGRACION - FELIPE
        # Clase: Cliente
        #
        # Aqui se conectaran las funcionalidades desarrolladas
        # por Felipe en su archivo entidades_clientes.py.
        #
        # Operaciones que debe permitir la interfaz:
        # 1. Registrar un cliente.
        # 2. Consultar clientes registrados.
        # 3. Modificar informacion de un cliente.
        # 4. Eliminar o desactivar un cliente, segun el diseño.
        # 5. Validar los datos personales ingresados.
        #
        # IMPORTANTE:
        # Los nombres definitivos de los metodos se estableceran
        # de acuerdo con el codigo publicado por Felipe.
        # --------------------------------------------------

        # Formulario visual de clientes
        formulario = tk.LabelFrame(
            self.area_principal,
            text="Informacion del cliente",
            font=("Arial", 11, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto,
            padx=15,
            pady=12
        )

        formulario.pack(
            fill="x",
            padx=35,
            pady=5
        )

        # Campos de informacion
        self.entrada_nombre = self.crear_campo(
            formulario,
            "Nombre completo:",
            0,
            0
        )

        self.entrada_documento = self.crear_campo(
            formulario,
            "Documento:",
            0,
            1
        )

        self.entrada_correo = self.crear_campo(
            formulario,
            "Correo electronico:",
            1,
            0
        )

        self.entrada_telefono = self.crear_campo(
            formulario,
            "Telefono:",
            1,
            1
        )

        # Botones de operaciones de clientes
        botones = tk.Frame(
            self.area_principal,
            bg=self.color_fondo
        )

        botones.pack(
            fill="x",
            padx=35,
            pady=12
        )

        self.crear_boton_accion(
            botones,
            "Registrar cliente",
            lambda: self.integracion_pendiente(
                "Felipe - Registrar cliente"
            )
        ).pack(side="left", padx=4)

        self.crear_boton_accion(
            botones,
            "Consultar clientes",
            lambda: self.integracion_pendiente(
                "Felipe - Consultar clientes"
            )
        ).pack(side="left", padx=4)

        self.crear_boton_accion(
            botones,
            "Modificar cliente",
            lambda: self.integracion_pendiente(
                "Felipe - Modificar cliente"
            )
        ).pack(side="left", padx=4)

        # Tabla para mostrar los clientes registrados
        tk.Label(
            self.area_principal,
            text="Clientes registrados",
            font=("Arial", 12, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", padx=35, pady=(10, 8))

        contenedor_tabla = tk.Frame(
            self.area_principal,
            bg=self.color_fondo
        )

        contenedor_tabla.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 15)
        )

        self.tabla_clientes = self.crear_tabla(
            contenedor_tabla,
            ("documento", "nombre", "correo", "telefono"),
            ("Documento", "Nombre", "Correo", "Telefono")
        )

        # PENDIENTE FELIPE:
        # Conectar la consulta de clientes con la tabla.
        # Los registros se mostraran cuando se integre Cliente.

    def crear_campo(self, contenedor, etiqueta, fila, columna):

        # Crear un campo de texto reutilizable
        bloque = tk.Frame(
            contenedor,
            bg=self.color_fondo
        )

        bloque.grid(
            row=fila,
            column=columna,
            padx=10,
            pady=7,
            sticky="ew"
        )

        tk.Label(
            bloque,
            text=etiqueta,
            font=("Arial", 9),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w")

        entrada = tk.Entry(
            bloque,
            font=("Arial", 10),
            relief="solid",
            bd=1
        )

        entrada.pack(
            fill="x",
            pady=(4, 0)
        )

        contenedor.grid_columnconfigure(
            columna,
            weight=1
        )

        return entrada

    # ======================================================
    # ESTUDIANTE 2 - MAICOL
    # MODULO DE GESTION DE SERVICIOS
    # ======================================================

    def mostrar_servicios(self):

        self.limpiar_area()

        self.crear_titulo(
            "Gestion de servicios",
            "Consulta de los servicios ofrecidos por Software FJ."
        )

        # --------------------------------------------------
        # PUNTO DE INTEGRACION - MAICOL
        # Clase abstracta: Servicio
        # Clases derivadas:
        # - ReservaSala
        # - AlquilerEquipo
        # - AsesoriaEspecializada
        #
        # Aqui se conectaran las funcionalidades desarrolladas
        # por Maicol en su archivo servicios.py.
        #
        # Operaciones que debe permitir la interfaz:
        # 1. Consultar los servicios disponibles.
        # 2. Mostrar la descripcion de cada servicio.
        # 3. Consultar los costos correspondientes.
        # 4. Validar los parametros de cada servicio.
        # 5. Aplicar los calculos de costos correspondientes.
        #
        # IMPORTANTE:
        # Se respetara el polimorfismo implementado por Maicol.
        # Los nombres de los metodos se ajustaran a su entrega.
        # --------------------------------------------------

        contenedor = tk.Frame(
            self.area_principal,
            bg=self.color_fondo
        )

        contenedor.pack(
            fill="both",
            expand=True,
            padx=35
        )

        # Servicios disponibles
        servicios = [
            (
                "Reserva de salas",
                "Administracion de espacios y salas disponibles.",
                "Consultar salas"
            ),
            (
                "Alquiler de equipos",
                "Gestion de alquiler de equipos tecnologicos.",
                "Consultar equipos"
            ),
            (
                "Asesorias especializadas",
                "Gestion de servicios de asesoria especializada.",
                "Consultar asesorias"
            )
        ]

        for nombre, descripcion, boton_texto in servicios:

            tarjeta = tk.LabelFrame(
                contenedor,
                text=nombre,
                font=("Arial", 11, "bold"),
                bg=self.color_fondo,
                fg=self.color_texto,
                padx=15,
                pady=12
            )

            tarjeta.pack(
                fill="x",
                pady=8
            )

            tk.Label(
                tarjeta,
                text=descripcion,
                font=("Arial", 10),
                bg=self.color_fondo,
                fg="#687787"
            ).pack(anchor="w", pady=(0, 10))

            self.crear_boton_accion(
                tarjeta,
                boton_texto,
                lambda servicio=nombre: self.integracion_pendiente(
                    f"Maicol - {servicio}"
                )
            ).pack(anchor="w")

        # PENDIENTE MAICOL:
        # Conectar cada servicio con su clase correspondiente.
        # Mostrar descripcion, parametros y costos reales.

    # ======================================================
    # ESTUDIANTE 3 (SIN ASIGNAR)
    # MODULO DE GESTION DE RESERVAS
    # ======================================================

    def mostrar_reservas(self):

        self.limpiar_area()

        self.crear_titulo(
            "Gestion de reservas",
            "Administracion y seguimiento de las reservas."
        )

        # --------------------------------------------------
        # PUNTO DE INTEGRACION - ESTUDIANTE 3 (SIN ASIGNAR)
        # Clase: Reserva
        #
        # Aqui se conectaran las funcionalidades desarrolladas
        # por el Estudiante 3 en su modulo de reservas.
        #
        # Operaciones que debe permitir la interfaz:
        # 1. Crear una reserva.
        # 2. Consultar las reservas existentes.
        # 3. Confirmar una reserva.
        # 4. Cancelar una reserva.
        # 5. Procesar una reserva.
        # 6. Consultar duracion, costo y estado.
        #
        # La reserva debera relacionar un cliente con un servicio.
        #
        # IMPORTANTE:
        # Los nombres definitivos de los metodos se estableceran
        # cuando se integre el codigo del Estudiante 3.
        # --------------------------------------------------

        # Formulario de reserva
        formulario = tk.LabelFrame(
            self.area_principal,
            text="Datos de la reserva",
            font=("Arial", 11, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto,
            padx=15,
            pady=12
        )

        formulario.pack(
            fill="x",
            padx=35,
            pady=5
        )

        # Campos visuales para la reserva
        self.entrada_cliente_reserva = self.crear_campo(
            formulario,
            "Documento del cliente:",
            0,
            0
        )

        self.entrada_servicio_reserva = self.crear_campo(
            formulario,
            "Tipo de servicio:",
            0,
            1
        )

        self.entrada_duracion_reserva = self.crear_campo(
            formulario,
            "Duracion:",
            1,
            0
        )

        # Botones de operaciones de reservas
        botones = tk.Frame(
            self.area_principal,
            bg=self.color_fondo
        )

        botones.pack(
            fill="x",
            padx=35,
            pady=12
        )

        operaciones = [
            "Crear reserva",
            "Consultar reservas",
            "Confirmar reserva",
            "Cancelar reserva"
        ]

        for operacion in operaciones:

            self.crear_boton_accion(
                botones,
                operacion,
                lambda nombre=operacion: self.integracion_pendiente(
                    f"Estudiante 3 - {nombre}"
                )
            ).pack(
                side="left",
                padx=4
            )

        # Tabla de reservas
        tk.Label(
            self.area_principal,
            text="Reservas registradas",
            font=("Arial", 12, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", padx=35, pady=(10, 8))

        contenedor_tabla = tk.Frame(
            self.area_principal,
            bg=self.color_fondo
        )

        contenedor_tabla.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(0, 15)
        )

        self.tabla_reservas = self.crear_tabla(
            contenedor_tabla,
            ("numero", "cliente", "servicio", "duracion", "estado"),
            ("N. Reserva", "Cliente", "Servicio", "Duracion", "Estado")
        )

        # PENDIENTE ESTUDIANTE 3 (SIN ASIGNAR):
        # Conectar las operaciones con la clase Reserva.
        # Mostrar los registros y actualizar sus estados.

    # ======================================================
    # ESTUDIANTE 4 (SIN ASIGNAR)
    # MANEJO DE EXCEPCIONES Y REGISTRO DE EVENTOS
    # ======================================================

    # ------------------------------------------------------
    # PUNTO DE INTEGRACION - ESTUDIANTE 4 (SIN ASIGNAR)
    #
    # Aqui se conectaran las excepciones personalizadas
    # y los mecanismos de registro desarrollados por
    # el Estudiante 4 en su modulo excepciones_logs.py.
    #
    # Responsabilidades:
    # 1. Gestionar los errores producidos en las operaciones.
    # 2. Registrar errores en archivos de log.
    # 3. Registrar eventos importantes del sistema.
    # 4. Implementar el manejo de excepciones personalizadas.
    # 5. Evitar que un error controlado cierre la aplicacion.
    #
    # Tambien se debera coordinar el uso de try/except,
    # else, finally y encadenamiento de excepciones.
    #
    # IMPORTANTE:
    # El manejo definitivo de errores se integrara cuando
    # el Estudiante 4 publique su desarrollo.
    # ------------------------------------------------------

    def manejar_error(self, error):

        # PENDIENTE ESTUDIANTE 4 (SIN ASIGNAR):
        # Conectar este punto con el sistema de registro de logs.
        #
        # Aqui se enviaran los errores generados por las
        # operaciones de clientes, servicios y reservas.

        messagebox.showerror(
            "Error del sistema",
            str(error)
        )

    # ======================================================
    # ESTUDIANTE 5 (SIN ASIGNAR) - PUNTO PROVISIONAL DE INTEGRACION
    # ======================================================

    def integracion_pendiente(self, nombre_operacion):

        # Este metodo es provisional.
        # Permite probar la navegacion y los botones mientras
        # los demas integrantes desarrollan sus funcionalidades.
        #
        # Cuando se integren las clases:
        # - Se reemplazaran las llamadas provisionales.
        # - Se conectaran los metodos reales.
        # - Se utilizara el manejo de errores del Estudiante 4.

        messagebox.showinfo(
            "Integracion pendiente",
            f"La operacion '{nombre_operacion}' "
            "se habilitara cuando se integre su funcionalidad."
        )

    # ======================================================
    # EJECUCION PRINCIPAL DEL PROGRAMA
    # ======================================================


if __name__ == "__main__":

    # Crear la aplicacion
    aplicacion = InterfazSoftwareFJ()

    # Iniciar el ciclo principal de Tkinter
    aplicacion.mainloop()
