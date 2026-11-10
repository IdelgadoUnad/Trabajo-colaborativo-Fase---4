import logging
from abc import ABC, abstractmethod

# Configuración del archivo de logs 
logging.basicConfig(
    filename='registro_eventos.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger("ModuloServicios")

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

# 2. CLASE ABSTRACTA Base

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
