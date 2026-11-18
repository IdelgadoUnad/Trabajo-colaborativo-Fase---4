import logging
# Importamos la clase Servicio y sus errores desde el archivo que ya hiciste
from servicios import Servicio, ServicioError 

logger = logging.getLogger("ModuloReservas")

# 1. EXCEPCIONES PERSONALIZADAS DE RESERVA
class ReservaError(Exception):
    """Clase base para errores generales de reservas."""
    pass

class EstadoReservaError(ReservaError):
    """Lanzada cuando se intenta una operación no permitida para el estado actual."""
    pass

class DatosReservaError(ReservaError):
    """Lanzada cuando los datos de la reserva son inválidos o están incompletos."""
    pass

# 2. CLASE RESERVA
class Reserva:
    def __init__(self, id_reserva: str, cliente, servicio: Servicio, duracion: int):
        # Encapsulación estricta
        self._id_reserva = id_reserva
        self._cliente = cliente  # Se asume que el sistema le pasará un objeto Cliente
        self._servicio = servicio # Objeto Servicio (Sala, Equipo o Asesoría)
        self._duracion = duracion
        self._estado = "Pendiente" # Estados: Pendiente, Confirmada, Cancelada, Procesada
        
        self._validar_datos_iniciales()

    def _validar_datos_iniciales(self):
        """Valida que los objetos y datos necesarios existan antes de crear la reserva."""
        try:
            if not self._cliente or not self._servicio:
                raise DatosReservaError("La reserva debe tener un cliente y un servicio válidos asignados.")
            if not isinstance(self._duracion, int) or self._duracion <= 0:
                raise DatosReservaError("La duración del servicio debe ser un número entero mayor a cero.")
        except DatosReservaError as e:
            logger.error(f"Fallo al crear reserva {self._id_reserva}: {e}")
            raise # Relanzar para que el programa principal lo capture

    # Propiedades (Getters)
    @property
    def estado(self):
        return self._estado
    
    @property
    def id_reserva(self):
        return self._id_reserva

    def confirmar(self):
        """Cambia el estado a Confirmada validando que no esté cancelada."""
        try:
            if self._estado == "Cancelada":
                raise EstadoReservaError("No se puede confirmar una reserva que ya fue cancelada.")
            if self._estado == "Confirmada":
                raise EstadoReservaError("La reserva ya se encuentra confirmada.")
            
            self._estado = "Confirmada"
            logger.info(f"Reserva {self._id_reserva} confirmada exitosamente.")
            
        except EstadoReservaError as e:
            logger.warning(f"Intento inválido de confirmación en reserva {self._id_reserva}: {e}")
            raise

    def cancelar(self):
        """Permite cancelar la reserva siempre y cuando no se haya cobrado/procesado."""
        try:
            if self._estado == "Procesada":
                raise EstadoReservaError("No se puede cancelar una reserva que ya fue procesada y facturada.")
            
            self._estado = "Cancelada"
            logger.info(f"Reserva {self._id_reserva} cancelada a petición.")
            
        except EstadoReservaError as e:
            logger.warning(f"Intento inválido de cancelación en reserva {self._id_reserva}: {e}")
            raise

    def procesar_reserva(self, aplicar_impuesto: bool = True, porcentaje_descuento: float = 0.0) -> float:
        """
        Procesa el cobro interactuando con el Servicio.
        Implementa el manejo riguroso de excepciones (try/except/else/finally) 
        exigido en la rúbrica del proyecto.
        """
        costo_total = 0.0
        try:
            # 1. Validar estado
            if self._estado != "Confirmada":
                raise EstadoReservaError(f"Solo se pueden procesar reservas Confirmadas. Estado actual: {self._estado}")
            
            # 2. Polimorfismo: Delegamos el cálculo al método sobrecargado de tu clase Servicio
            costo_total = self._servicio.calcular_costo(
                self._duracion, 
                aplicar_impuesto=aplicar_impuesto, 
                porcentaje_descuento=porcentaje_descuento
            )
            
        except EstadoReservaError as e:
            logger.error(f"Error de estado al procesar reserva {self._id_reserva}: {e}")
            raise
            
        except ServicioError as e:
            logger.error(f"El servicio rechazó el cálculo de costo para la reserva {self._id_reserva}: {e}")
            # Encadenamiento de excepciones: Convertimos un error de Servicio en uno de Reserva
            raise ReservaError("No se pudo procesar la reserva por una inconsistencia en el servicio.") from e
            
        except Exception as e:
            logger.critical(f"Error crítico e inesperado procesando reserva {self._id_reserva}: {e}")
            raise ReservaError("Fallo interno grave durante el procesamiento.") from e
            
        else:
            # Se ejecuta SOLO si el bloque 'try' funcionó sin errores
            self._estado = "Procesada"
            logger.info(f"Reserva {self._id_reserva} procesada con éxito. Costo total: ${costo_total}")
            return costo_total
            
        finally:
            # Se ejecuta SIEMPRE, ideal para cerrar archivos o dejar rastros de auditoría
            logger.debug(f"Finaliza el intento de procesamiento para la reserva {self._id_reserva}.")
