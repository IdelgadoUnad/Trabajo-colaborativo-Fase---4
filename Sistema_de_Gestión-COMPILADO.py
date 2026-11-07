import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
import re


# ==========================================================
# PROYECTO: SOFTWARE FJ
# SISTEMA INTEGRAL DE GESTION DE CLIENTES
#
# ARCHIVO: Sistema_de_Gestión-COMPILADO.py
#
# INTEGRANTES:
# FELIPE - ESTUDIANTE 1: ARQUITECTURA Y GESTION DE CLIENTES
# IVAN DELGADO - ESTUDIANTE 5: INTERFAZ GRAFICA E INTEGRACION
#
# ==========================================================


# ==========================================================
# ESTUDIANTE 1 - FELIPE
# MODULO DE GESTION DE CLIENTES
# ==========================================================

# ==========================================
# 1. CLASE ABSTRACTA ENTIDAD
# ==========================================
class Entidad(ABC):
    """
    Clase base abstracta que define la estructura general para cualquier entidad dentro del sistema.
    """

    def __init__(self, id_entidad: str):
        self._id_entidad = id_entidad

    @property
    def id_entidad(self) -> str:
        """Getter para el identificador único de la entidad."""
        return self._id_entidad

    @abstractmethod
    def mostrar_informacion(self) -> str:
        """Método abstracto para mostrar información de la entidad."""
        pass


# ==========================================
# 2. CLASE CLIENTE (HERENCIA Y ENCAPSULACIÓN)
# ==========================================
class Cliente(Entidad):
    """
    Clase que representa un cliente. Heroda de Entidad e implementa encapsulación,
    validaciones estrictas y protección de datos.
    """

    def __init__(self, nombre: str, documento: str, correo: str, telefono: str):
        # Inicializamos la entidad abstracta usando el documento como id_entidad
        super().__init__(id_entidad=documento)

        # Atributos privados
        self.__nombre = ""
        self.__documento = ""
        self.__correo = ""
        self.__telefono = ""

        # Asignación mediante setters (para validar desde la instanciación)
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # --- GETTERS Y SETTERS CON VALIDACIÓN ---

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        valor_limpio = str(valor).strip()
        if not valor_limpio:
            raise ValueError("El nombre no puede estar vacío.")
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", valor_limpio):
            raise ValueError("El nombre solo debe contener letras y espacios.")
        self.__nombre = valor_limpio.title()

    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor: str):
        valor_limpio = str(valor).strip()
        if not valor_limpio.isdigit():
            raise ValueError("El documento debe ser numérico.")
        if not (7 <= len(valor_limpio) <= 10):
            raise ValueError("El documento debe tener entre 7 y 10 dígitos.")
        self.__documento = valor_limpio
        self._id_entidad = valor_limpio

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        valor_limpio = str(valor).strip().lower()
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron, valor_limpio):
            raise ValueError(f"El correo '{valor}' no tiene un formato válido.")
        self.__correo = valor_limpio

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        valor_limpio = str(valor).strip()
        # Permite opcionalmente prefijo '+' seguido de 10 a 14 dígitos numéricos
        if not re.match(r"^\+?\d{10,14}$", valor_limpio):
            raise ValueError("El teléfono no tiene un formato válido.")
        self.__telefono = valor_limpio

    # --- MÉTODOS DE LA CLASE ---

    def mostrar_informacion(self) -> str:
        return (
            f"--- DATOS DEL CLIENTE ---\n"
            f"Nombre: {self.__nombre}\n"
            f"Documento: {self.__documento}\n"
            f"Correo: {self.__correo}\n"
            f"Teléfono: {self.__telefono}\n"
            f"-------------------------"
        )

    def obtener_informacion_protegida(self) -> str:
        """Garantiza el manejo adecuado y seguro de la información sensible."""
        doc_oculto = "*" * (len(self.__documento) - 4) + self.__documento[-4:]
        partes_correo = self.__correo.split("@")
        correo_oculto = partes_correo[0][:2] + "****@" + partes_correo[1]
        tel_oculto = self.__telefono[:4] + "****" + self.__telefono[-3:]
        return f"Cliente: {self.__nombre} | Doc: {doc_oculto} | Correo: {correo_oculto} | Tel: {tel_oculto}"

    def __str__(self) -> str:
        return f"Cliente: {self.__nombre} (Doc: {self.__documento})"


# ==========================================================
# ESTUDIANTE 5 - IVAN DELGADO
# INTERFAZ GRAFICA E INTEGRACION
# ==========================================================

class InterfazSoftwareFJ(tk.Tk):

    def __init__(self):

        # Inicializar la ventana principal
        super().__init__()

        # Coleccion temporal para almacenar los objetos Cliente
        self.clientes = {}

        # Documento del cliente seleccionado para modificarlo
        self.documento_seleccionado = None

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
    # ESTUDIANTE 5 - ESTRUCTURA GENERAL DE LA APLICACION
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

        # Nombre del sistema
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

        # Separador visual
        tk.Frame(
            self.menu_lateral,
            bg="#52677F",
            height=1
        ).pack(fill="x", padx=20, pady=25)

        # Informacion inferior del sistema
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
    # ESTUDIANTE 5 - FUNCIONES AUXILIARES DE LA INTERFAZ
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

        # Barra de desplazamiento vertical
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
    # ESTUDIANTE 5 - PANTALLA PRINCIPAL
    # ======================================================

    def mostrar_inicio(self):

        self.limpiar_area()

        self.crear_titulo(
            "Panel principal",
            "Bienvenido al Sistema Integral de Gestion de Software FJ."
        )

        tk.Label(
            self.area_principal,
            text="Administracion de clientes",
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

        contenedor.grid_columnconfigure(
            0,
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

        # Crear una tarjeta visual para el modulo
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
    # ESTUDIANTE 5 - INTERFAZ E INTEGRACION CON FELIPE
    # MODULO DE GESTION DE CLIENTES
    # ======================================================

    def mostrar_clientes(self):

        self.limpiar_area()

        self.crear_titulo(
            "Gestion de clientes",
            "Registro, consulta y administracion de clientes."
        )

        # --------------------------------------------------
        # INTEGRACION CON FELIPE - ESTUDIANTE 1
        #
        # Se utiliza la clase Cliente desarrollada por Felipe.
        # La interfaz no modifica sus validaciones ni métodos.
        #
        # Las operaciones de registro, consulta y modificacion
        # se conectan con los atributos y métodos de Cliente.
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
            self.registrar_cliente
        ).pack(side="left", padx=4)

        self.crear_boton_accion(
            botones,
            "Consultar clientes",
            self.consultar_clientes
        ).pack(side="left", padx=4)

        self.crear_boton_accion(
            botones,
            "Modificar cliente",
            self.modificar_cliente
        ).pack(side="left", padx=4)

        self.crear_boton_accion(
            botones,
            "Limpiar campos",
            self.limpiar_campos
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

        # Al seleccionar una fila se cargan sus datos en el formulario
        self.tabla_clientes.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_cliente
        )

        # Mostrar los clientes almacenados
        self.consultar_clientes()

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
    # ESTUDIANTE 5 - CONEXION DE OPERACIONES CON CLIENTE
    # ======================================================

    def registrar_cliente(self):

        # Obtener los datos ingresados en el formulario
        nombre = self.entrada_nombre.get()
        documento = self.entrada_documento.get()
        correo = self.entrada_correo.get()
        telefono = self.entrada_telefono.get()

        try:

            # Verificar que el documento no este registrado
            if documento.strip() in self.clientes:
                raise ValueError("Ya existe un cliente con ese documento.")

            # Crear el objeto utilizando la clase de Felipe
            # Sus setters realizan las validaciones correspondientes
            nuevo_cliente = Cliente(
                nombre,
                documento,
                correo,
                telefono
            )

            # Almacenar el objeto en la coleccion
            self.clientes[nuevo_cliente.documento] = nuevo_cliente

            # Actualizar la tabla
            self.consultar_clientes()

            # Limpiar el formulario
            self.limpiar_campos()

            self.barra_estado.config(
                text="Cliente registrado correctamente."
            )

            messagebox.showinfo(
                "Registro exitoso",
                "El cliente fue registrado correctamente."
            )

        except ValueError as error:

            messagebox.showerror(
                "Error al registrar",
                str(error)
            )

    def consultar_clientes(self):

        # Limpiar los registros anteriores de la tabla
        for fila in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(fila)

        # Recorrer los objetos Cliente almacenados
        for documento, cliente in self.clientes.items():

            # Obtener la informacion mediante los atributos de Felipe
            self.tabla_clientes.insert(
                "",
                "end",
                values=(
                    cliente.documento,
                    cliente.nombre,
                    cliente.correo,
                    cliente.telefono
                )
            )

        self.barra_estado.config(
            text=f"Clientes registrados: {len(self.clientes)}"
        )

    def seleccionar_cliente(self, evento):

        # Obtener la fila seleccionada
        seleccion = self.tabla_clientes.selection()

        if not seleccion:
            return

        valores = self.tabla_clientes.item(
            seleccion[0],
            "values"
        )

        documento = valores[0]

        # Buscar el objeto Cliente correspondiente
        cliente = self.clientes.get(documento)

        if cliente is None:
            return

        # Guardar el documento original para la modificacion
        self.documento_seleccionado = documento

        # Cargar la informacion del cliente en el formulario
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_nombre.insert(0, cliente.nombre)

        self.entrada_documento.delete(0, tk.END)
        self.entrada_documento.insert(0, cliente.documento)

        self.entrada_correo.delete(0, tk.END)
        self.entrada_correo.insert(0, cliente.correo)

        self.entrada_telefono.delete(0, tk.END)
        self.entrada_telefono.insert(0, cliente.telefono)

        self.barra_estado.config(
            text=f"Cliente seleccionado: {cliente.nombre}"
        )

    def modificar_cliente(self):

        # Verificar que se haya seleccionado un cliente
        if self.documento_seleccionado is None:
            messagebox.showwarning(
                "Seleccion requerida",
                "Seleccione un cliente de la tabla para modificarlo."
            )
            return

        documento_anterior = self.documento_seleccionado

        # Obtener los nuevos datos del formulario
        nombre = self.entrada_nombre.get()
        documento_nuevo = self.entrada_documento.get()
        correo = self.entrada_correo.get()
        telefono = self.entrada_telefono.get()

        try:

            # Verificar que el nuevo documento no pertenezca a otro cliente
            if (
                documento_nuevo.strip() != documento_anterior
                and documento_nuevo.strip() in self.clientes
            ):
                raise ValueError(
                    "El nuevo documento ya pertenece a otro cliente."
                )

            # Crear una nueva instancia para validar todos los datos
            # Se conserva intacta la clase Cliente de Felipe
            cliente_actualizado = Cliente(
                nombre,
                documento_nuevo,
                correo,
                telefono
            )

            # Reemplazar el registro anterior por el actualizado
            del self.clientes[documento_anterior]

            self.clientes[cliente_actualizado.documento] = cliente_actualizado

            # Actualizar la tabla
            self.consultar_clientes()

            # Limpiar el formulario
            self.limpiar_campos()

            self.barra_estado.config(
                text="Informacion del cliente actualizada."
            )

            messagebox.showinfo(
                "Modificacion exitosa",
                "La informacion del cliente fue actualizada correctamente."
            )

        except ValueError as error:

            messagebox.showerror(
                "Error al modificar",
                str(error)
            )

    def limpiar_campos(self):

        # Limpiar los campos del formulario
        self.entrada_nombre.delete(0, tk.END)
        self.entrada_documento.delete(0, tk.END)
        self.entrada_correo.delete(0, tk.END)
        self.entrada_telefono.delete(0, tk.END)

        # Reiniciar el documento seleccionado
        self.documento_seleccionado = None

        # Quitar la seleccion de la tabla
        if hasattr(self, "tabla_clientes"):
            seleccion = self.tabla_clientes.selection()

            if seleccion:
                self.tabla_clientes.selection_remove(seleccion)

        self.barra_estado.config(
            text="Formulario listo."
        )


# ======================================================
# EJECUCION PRINCIPAL DEL PROGRAMA
# ======================================================

if __name__ == "__main__":

    # Crear la aplicacion
    aplicacion = InterfazSoftwareFJ()

    # Iniciar el ciclo principal de Tkinter
    aplicacion.mainloop()