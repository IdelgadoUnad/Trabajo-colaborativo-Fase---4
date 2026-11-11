import tkinter as tk
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
import re
import logging


# ==========================================================
# PROYECTO: SOFTWARE FJ
# SISTEMA INTEGRAL DE GESTION DE CLIENTES Y SERVICIOS
#
# ARCHIVO: Sistema_de_Gestión-COMPILADO.py
#
# INTEGRANTES:
# FELIPE - ESTUDIANTE 1: ARQUITECTURA Y GESTION DE CLIENTES
# MAICOL - ESTUDIANTE 2: GESTION DE SERVICIOS
# IVAN DELGADO - ESTUDIANTE 5: INTERFAZ GRAFICA E INTEGRACION
#
# NOTA:
# El modulo de RESERVAS (Estudiante 3) y el modulo de
# EXCEPCIONES Y LOGS (Estudiante 4) se integraran cuando
# sus desarrollos sean entregados. La estructura visual y
# los puntos de integracion ya se encuentran preparados.
# ==========================================================


# ==========================================================
# CONFIGURACION DEL SISTEMA DE LOGS
# Entregada junto con el modulo de Servicios (Maicol).
# Se conserva tal cual para su uso transversal en el sistema.
# ==========================================================
logging.basicConfig(
    filename='registro_eventos.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger("ModuloServicios")


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
    Clase que representa un cliente. Hereda de Entidad e implementa encapsulación,
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
# ESTUDIANTE 2 - MAICOL
# MODULO DE GESTION DE SERVICIOS
# ==========================================================

# 1. EXCEPCIONES PERSONALIZADAS

class ServicioError(Exception):
    """Clase base para todas las excepciones relacionadas con Servicios."""
    pass


class ValidacionParametroError(ServicioError):
    """Lanzada cuando un parámetro del servicio no cumple las reglas de negocio."""
    pass


class CalculoCostoError(ServicioError):
    """Lanzada cuando hay una inconsistencia matemática en el cálculo."""
    pass


# 2. CLASE ABSTRACTA BASE

class Servicio(ABC):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float):
        # Encapsulación de atributos
        self._id_servicio = id_servicio
        self._nombre = nombre
        self._tarifa_base = tarifa_base

        # Validar al momento de instanciar
        self.validar_parametros()

    # Getters Propiedades para respetar la encapsulación
    @property
    def id_servicio(self):
        return self._id_servicio

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    # Métodos Abstractos que obligan a las clases hijas a implementarlos
    @abstractmethod
    def describir_servicio(self) -> str:
        pass

    @abstractmethod
    def validar_parametros(self):
        pass

    @abstractmethod
    def calcular_costo(self, cantidad: int, aplicar_impuesto: bool = False, porcentaje_descuento: float = 0.0) -> float:
        """
        Método 'sobrecargado' mediante parámetros opcionales.
        Permite calcular el costo de múltiples formas.
        """
        pass


# 3. CLASES DERIVADAS Herencia y Polimorfismo

class ReservaSala(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad: int, incluye_proyector: bool):
        self._capacidad = capacidad
        self._incluye_proyector = incluye_proyector
        super().__init__(id_servicio, nombre, tarifa_base)

    def validar_parametros(self):
        try:
            if not isinstance(self._capacidad, int) or self._capacidad <= 0:
                raise ValidacionParametroError("La capacidad de la sala debe ser un entero mayor a 0.")
            if self._tarifa_base < 0:
                raise ValidacionParametroError("La tarifa base no puede ser negativa.")
        except ValidacionParametroError as e:
            logger.error(f"Error de validación al crear ReservaSala '{self._nombre}': {e}")
            raise  # Relanzamos para que el sistema lo maneje arriba

    def describir_servicio(self) -> str:
        extra = "con proyector" if self._incluye_proyector else "sin equipos extra"
        return f"[SALA] {self.nombre} - Capacidad: {self._capacidad} personas ({extra})."

    def calcular_costo(self, horas: int, aplicar_impuesto: bool = False, porcentaje_descuento: float = 0.0) -> float:
        costo_final = 0.0
        try:
            # Validación estricta del parámetro
            if horas <= 0:
                raise CalculoCostoError("Las horas de reserva deben ser al menos 1.")

            costo_final = self.tarifa_base * horas

            # Polimorfismo: Lógica única de este servicio
            if self._incluye_proyector:
                costo_final += (15000 * horas)  # Recargo por equipos

            if porcentaje_descuento > 0:
                costo_final -= costo_final * (porcentaje_descuento / 100)

            if aplicar_impuesto:
                costo_final *= 1.19  # IVA del 19%

        except CalculoCostoError as e:
            logger.error(f"Inconsistencia calculando costo en ReservaSala: {e}")
            raise
        except Exception as e:
            logger.critical(f"Fallo no previsto: {e}")
            # Encadenamiento de excepciones
            raise CalculoCostoError("Fallo interno al procesar cálculo de Sala.") from e
        else:
            # Si TODO sale bien en el try, entra al else
            logger.info(f"Cálculo exitoso para {self.nombre}: ${costo_final}")
            return round(costo_final, 2)
        finally:
            # Se ejecuta siempre (haya error o no), ideal para auditar
            logger.debug(f"Operación calcular_costo finalizada para {self.id_servicio}.")


class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, requiere_deposito: bool):
        self._requiere_deposito = requiere_deposito
        super().__init__(id_servicio, nombre, tarifa_base)

    def validar_parametros(self):
        if not self._nombre.strip():
            logger.error("Nombre de equipo vacío.")
            raise ValidacionParametroError("El nombre del equipo no puede estar vacío.")

    def describir_servicio(self) -> str:
        deposito = "Requiere depósito de garantía" if self._requiere_deposito else "No requiere depósito"
        return f"[EQUIPO] {self.nombre} - {deposito}."

    def calcular_costo(self, dias: int, aplicar_impuesto: bool = False, porcentaje_descuento: float = 0.0) -> float:
        costo_final = 0.0
        try:
            if dias <= 0:
                raise CalculoCostoError("Los días de alquiler deben ser mayores a 0.")

            costo_final = self.tarifa_base * dias

            # Lógica única: Si requiere depósito, suma un valor fijo que se devuelve luego
            if self._requiere_deposito:
                costo_final += 50000

            if porcentaje_descuento > 0:
                costo_final -= costo_final * (porcentaje_descuento / 100)

            if aplicar_impuesto:
                costo_final *= 1.19

            return round(costo_final, 2)

        except Exception as e:
            logger.error(f"Error en AlquilerEquipo: {e}")
            raise


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, nivel_experto: str):
        self._nivel_experto = nivel_experto.lower()
        super().__init__(id_servicio, nombre, tarifa_base)

    def validar_parametros(self):
        niveles_validos = ['junior', 'senior', 'master']
        if self._nivel_experto not in niveles_validos:
            msg = f"Nivel '{self._nivel_experto}' inválido. Debe ser: {niveles_validos}"
            logger.error(msg)
            raise ValidacionParametroError(msg)

    def describir_servicio(self) -> str:
        return f"[ASESORIA] {self.nombre} - Nivel del consultor: {self._nivel_experto.upper()}"

    def calcular_costo(self, horas_asesoria: int, aplicar_impuesto: bool = False, porcentaje_descuento: float = 0.0) -> float:
        try:
            if horas_asesoria < 2:
                raise CalculoCostoError("La asesoría requiere un mínimo de 2 horas.")

            costo_final = self.tarifa_base * horas_asesoria

            # Polimorfismo: Multiplicador según el nivel de experiencia
            multiplicadores = {'junior': 1.0, 'senior': 1.5, 'master': 2.0}
            costo_final *= multiplicadores[self._nivel_experto]

            if porcentaje_descuento > 0:
                costo_final -= costo_final * (porcentaje_descuento / 100)

            if aplicar_impuesto:
                costo_final *= 1.19

            return round(costo_final, 2)

        except CalculoCostoError as e:
            logger.error(e)
            raise


# ==========================================================
# ESTUDIANTE 5 - IVAN DELGADO
# INTERFAZ GRAFICA E INTEGRACION
# ==========================================================

class InterfazSoftwareFJ(tk.Tk):

    def __init__(self):

        # Inicializar la ventana principal
        super().__init__()

        # --------------------------------------------------
        # COLECCIONES DE OBJETOS DEL SISTEMA
        # --------------------------------------------------
        # Clientes registrados (Felipe - Estudiante 1)
        self.clientes = {}

        # Servicios disponibles (Maicol - Estudiante 2)
        # Se precargan servicios de ejemplo para poder consultarlos
        # y calcular sus costos desde la interfaz.
        self.servicios = {
            "SALA-001": ReservaSala(
                "SALA-001", "Sala de Conferencias A", 50000, 20, True
            ),
            "SALA-002": ReservaSala(
                "SALA-002", "Sala de Reuniones B", 30000, 10, False
            ),
            "EQUIPO-001": AlquilerEquipo(
                "EQUIPO-001", "Proyector Portatil", 25000, True
            ),
            "EQUIPO-002": AlquilerEquipo(
                "EQUIPO-002", "Laptop de Alto Rendimiento", 40000, True
            ),
            "ASESORIA-001": AsesoriaEspecializada(
                "ASESORIA-001", "Consultoria en Sistemas", 80000, "senior"
            ),
            "ASESORIA-002": AsesoriaEspecializada(
                "ASESORIA-002", "Auditoria de Seguridad", 100000, "master"
            ),
        }

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
        self.crear_boton_menu("Servicios", self.mostrar_servicios)
        self.crear_boton_menu("Reservas", self.mostrar_reservas)

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
            text="Administracion de clientes y servicios",
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
            formulario, "Nombre completo:", 0, 0
        )

        self.entrada_documento = self.crear_campo(
            formulario, "Documento:", 0, 1
        )

        self.entrada_correo = self.crear_campo(
            formulario, "Correo electronico:", 1, 0
        )

        self.entrada_telefono = self.crear_campo(
            formulario, "Telefono:", 1, 1
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
                nombre, documento, correo, telefono
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
                nombre, documento_nuevo, correo, telefono
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
    # ESTUDIANTE 5 - INTERFAZ E INTEGRACION CON MAICOL
    # MODULO DE GESTION DE SERVICIOS
    # ======================================================

    def mostrar_servicios(self):

        self.limpiar_area()

        self.crear_titulo(
            "Gestion de servicios",
            "Consulta de los servicios ofrecidos y calculo de sus costos."
        )

        # --------------------------------------------------
        # INTEGRACION CON MAICOL - ESTUDIANTE 2
        #
        # Se utilizan las clases ReservaSala, AlquilerEquipo
        # y AsesoriaEspecializada desarrolladas por Maicol.
        # La interfaz respeta la encapsulacion y el polimorfismo
        # de su implementacion.
        #
        # El metodo describir_servicio() y calcular_costo()
        # se invocan de forma polimorfica desde aqui.
        # --------------------------------------------------

        # ---- Seccion 1: servicios disponibles ----
        tk.Label(
            self.area_principal,
            text="Servicios disponibles",
            font=("Arial", 12, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto
        ).pack(anchor="w", padx=35, pady=(0, 8))

        contenedor_servicios = tk.Frame(
            self.area_principal,
            bg=self.color_fondo
        )

        contenedor_servicios.pack(fill="x", padx=35, pady=(0, 15))

        for i, (codigo, servicio) in enumerate(self.servicios.items()):
            fila = i // 3
            columna = i % 3
            self.crear_tarjeta_servicio(
                contenedor_servicios, servicio, fila, columna
            )

        for c in range(3):
            contenedor_servicios.grid_columnconfigure(c, weight=1)

        # ---- Seccion 2: calculadora de costos ----
        calculadora = tk.LabelFrame(
            self.area_principal,
            text="Calculadora de costos",
            font=("Arial", 11, "bold"),
            bg=self.color_fondo,
            fg=self.color_texto,
            padx=15,
            pady=12
        )

        calculadora.pack(fill="x", padx=35, pady=(0, 15))

        # Selector de servicio
        tk.Label(
            calculadora,
            text="Servicio:",
            font=("Arial", 9),
            bg=self.color_fondo,
            fg=self.color_texto
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.combo_servicio = ttk.Combobox(
            calculadora,
            state="readonly",
            width=45
        )

        self.combo_servicio["values"] = [
            f"{codigo} - {servicio.nombre}"
            for codigo, servicio in self.servicios.items()
        ]

        self.combo_servicio.grid(
            row=0, column=1, columnspan=4,
            sticky="ew", padx=5, pady=5
        )

        self.combo_servicio.bind(
            "<<ComboboxSelected>>",
            self.actualizar_unidad_cantidad
        )

        # Cantidad (horas o dias)
        self.label_cantidad = tk.Label(
            calculadora,
            text="Cantidad:",
            font=("Arial", 9),
            bg=self.color_fondo,
            fg=self.color_texto
        )

        self.label_cantidad.grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )

        self.entrada_cantidad = tk.Entry(
            calculadora,
            font=("Arial", 10),
            relief="solid",
            bd=1,
            width=15
        )

        self.entrada_cantidad.grid(
            row=1, column=1, sticky="w", padx=5, pady=5
        )

        # Descuento
        tk.Label(
            calculadora,
            text="Descuento %:",
            font=("Arial", 9),
            bg=self.color_fondo,
            fg=self.color_texto
        ).grid(row=1, column=2, sticky="w", padx=5, pady=5)

        self.entrada_descuento = tk.Entry(
            calculadora,
            font=("Arial", 10),
            relief="solid",
            bd=1,
            width=15
        )

        self.entrada_descuento.grid(
            row=1, column=3, sticky="w", padx=5, pady=5
        )

        # IVA
        self.var_impuesto = tk.BooleanVar()

        tk.Checkbutton(
            calculadora,
            text="Aplicar IVA (19%)",
            variable=self.var_impuesto,
            font=("Arial", 9),
            bg=self.color_fondo,
            fg=self.color_texto,
            activebackground=self.color_fondo,
            selectcolor=self.color_blanco
        ).grid(row=1, column=4, sticky="w", padx=5, pady=5)

        # Boton calcular
        self.crear_boton_accion(
            calculadora,
            "Calcular costo",
            self.calcular_costo_servicio
        ).grid(row=2, column=0, columnspan=2, sticky="w",
               padx=5, pady=(12, 5))

        # Resultado
        self.label_resultado = tk.Label(
            calculadora,
            text="",
            font=("Arial", 13, "bold"),
            bg=self.color_fondo,
            fg="#1C5F91"
        )

        self.label_resultado.grid(
            row=2, column=2, columnspan=3, sticky="w",
            padx=5, pady=(12, 5)
        )

        calculadora.grid_columnconfigure(1, weight=1)

        self.barra_estado.config(
            text=f"Servicios disponibles: {len(self.servicios)}"
        )

    def crear_tarjeta_servicio(self, contenedor, servicio, fila, columna):
        # Tarjeta visual para cada servicio disponible
        tarjeta = tk.Frame(
            contenedor,
            bg=self.color_blanco,
            highlightbackground=self.color_borde,
            highlightthickness=1
        )

        tarjeta.grid(
            row=fila, column=columna,
            padx=8, pady=8, sticky="nsew"
        )

        tk.Label(
            tarjeta,
            text=servicio.nombre,
            font=("Arial", 12, "bold"),
            bg=self.color_blanco,
            fg=self.color_texto
        ).pack(anchor="w", padx=15, pady=(15, 5))

        # Se invoca describir_servicio() de forma polimorfica
        tk.Label(
            tarjeta,
            text=servicio.describir_servicio(),
            font=("Arial", 9),
            bg=self.color_blanco,
            fg="#687787",
            wraplength=240,
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 8))

        tk.Label(
            tarjeta,
            text=f"Tarifa base: ${servicio.tarifa_base:,.0f}",
            font=("Arial", 10, "bold"),
            bg=self.color_blanco,
            fg=self.color_secundario
        ).pack(anchor="w", padx=15, pady=(0, 15))

    def _obtener_servicio_seleccionado(self):
        # Obtener la instancia del servicio elegido en el combo
        seleccion = self.combo_servicio.get()

        if not seleccion:
            return None

        codigo = seleccion.split(" - ")[0]

        return self.servicios.get(codigo)

    def actualizar_unidad_cantidad(self, evento=None):
        # Ajustar la etiqueta de cantidad segun el tipo de servicio
        servicio = self._obtener_servicio_seleccionado()

        if isinstance(servicio, ReservaSala):
            self.label_cantidad.config(text="Horas de reserva:")
        elif isinstance(servicio, AlquilerEquipo):
            self.label_cantidad.config(text="Dias de alquiler:")
        elif isinstance(servicio, AsesoriaEspecializada):
            self.label_cantidad.config(text="Horas de asesoria (min 2):")
        else:
            self.label_cantidad.config(text="Cantidad:")

    def calcular_costo_servicio(self):
        # Obtener el servicio seleccionado
        servicio = self._obtener_servicio_seleccionado()

        if servicio is None:
            messagebox.showwarning(
                "Seleccion requerida",
                "Seleccione un servicio para calcular su costo."
            )
            return

        # Validar la cantidad
        try:
            cantidad = int(self.entrada_cantidad.get())
        except ValueError:
            messagebox.showerror(
                "Error de entrada",
                "La cantidad debe ser un numero entero."
            )
            return

        # Validar descuento
        texto_descuento = self.entrada_descuento.get().strip()

        try:
            descuento = float(texto_descuento) if texto_descuento else 0.0
        except ValueError:
            messagebox.showerror(
                "Error de entrada",
                "El descuento debe ser un numero."
            )
            return

        if descuento < 0 or descuento > 100:
            messagebox.showwarning(
                "Descuento invalido",
                "El descuento debe estar entre 0 y 100."
            )
            return

        # Ejecutar el calculo respetando las excepciones de Maicol
        try:
            costo = servicio.calcular_costo(
                cantidad,
                aplicar_impuesto=self.var_impuesto.get(),
                porcentaje_descuento=descuento
            )

            self.label_resultado.config(
                text=f"Costo total: ${costo:,.2f}",
                fg="#1C5F91"
            )

            self.barra_estado.config(
                text=f"Costo calculado para {servicio.nombre}: ${costo:,.2f}"
            )

        except ServicioError as error:
            # Errores controlados por el modulo de Maicol
            self.label_resultado.config(
                text=f"Error: {error}",
                fg="#B00020"
            )
            messagebox.showerror(
                "Error de calculo",
                str(error)
            )

        except Exception as error:
            # Cualquier otro error no previsto
            self.label_resultado.config(
                text="Error inesperado",
                fg="#B00020"
            )
            self.manejar_error(error)

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
        #
        # Aqui se conectara la clase Reserva cuando sea
        # entregada. Los botones ya se encuentran preparados.
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

        formulario.pack(fill="x", padx=35, pady=5)

        # Campos visuales para la reserva
        self.entrada_cliente_reserva = self.crear_campo(
            formulario, "Documento del cliente:", 0, 0
        )

        self.entrada_servicio_reserva = self.crear_campo(
            formulario, "Tipo de servicio:", 0, 1
        )

        self.entrada_duracion_reserva = self.crear_campo(
            formulario, "Duracion:", 1, 0
        )

        # Botones de operaciones de reservas
        botones = tk.Frame(
            self.area_principal,
            bg=self.color_fondo
        )

        botones.pack(fill="x", padx=35, pady=12)

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
            ).pack(side="left", padx=4)

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

    # ======================================================
    # ESTUDIANTE 4 (SIN ASIGNAR)
    # MANEJO DE EXCEPCIONES Y REGISTRO DE EVENTOS
    # ======================================================

    def manejar_error(self, error):
        # PUNTO DE INTEGRACION - ESTUDIANTE 4
        # Se conectara con su sistema de logs cuando entregue.
        logger.error(f"Error en la interfaz: {error}")
        messagebox.showerror(
            "Error del sistema",
            str(error)
        )

    # ======================================================
    # ESTUDIANTE 5 - PUNTO PROVISIONAL DE INTEGRACION
    # ======================================================

    def integracion_pendiente(self, nombre_operacion):
        # Metodo provisional mientras llegan los modulos faltantes
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