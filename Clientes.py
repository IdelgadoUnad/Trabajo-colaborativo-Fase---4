"""
Módulo: entidades_clientes.py
Rol: Estudiante 1 - Arquitectura y gestión de clientes
Descripción:
- Clase abstracta 'Entidad'
- Clase 'Cliente' con encapsulación y validaciones
- Pruebas unitarias integradas (unittest)
"""

from abc import ABC, abstractmethod
import re
import unittest


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


# ==========================================
# 3. PRUEBAS UNITARIAS (UNITTEST)
# ==========================================
class TestCliente(unittest.TestCase):

    def test_creacion_exitosa(self):
        """Prueba que un cliente se pueda crear con datos válidos."""
        cliente = Cliente("Juan Pérez", "12345678", "juan@example.com", "+573101234567")
        self.assertEqual(cliente.nombre, "Juan Pérez")
        self.assertEqual(cliente.documento, "12345678")
        self.assertEqual(cliente.correo, "juan@example.com")
        self.assertEqual(cliente.telefono, "+573101234567")

    def test_nombre_invalido(self):
        """Prueba que un nombre vacío o con caracteres inválidos lance ValueError."""
        with self.assertRaises(ValueError):
            Cliente("", "12345678", "juan@example.com", "3101234567")
        with self.assertRaises(ValueError):
            Cliente("   ", "12345678", "juan@example.com", "3101234567")
        with self.assertRaises(ValueError):
            Cliente("Juan123", "12345678", "juan@example.com", "3101234567")

    def test_documento_invalido(self):
        """Prueba que documentos fuera de rango numérico (7-10 dígitos) lancen ValueError."""
        with self.assertRaises(ValueError):
            Cliente("Juan", "123456", "juan@example.com", "3101234567")  # 6 dígitos
        with self.assertRaises(ValueError):
            Cliente("Juan", "12345678901", "juan@example.com", "3101234567")  # 11 dígitos
        with self.assertRaises(ValueError):
            Cliente("Juan", "abc7654321", "juan@example.com", "3101234567")  # Con letras

    def test_correo_invalido(self):
        """Prueba que correos con formatos inválidos lancen ValueError."""
        with self.assertRaises(ValueError):
            Cliente("Juan", "12345678", "juan.com", "3101234567")
        with self.assertRaises(ValueError):
            Cliente("Juan", "12345678", "juan@com", "3101234567")
        with self.assertRaises(ValueError):
            Cliente("Juan", "12345678", "@example.com", "3101234567")

    def test_telefono_invalido(self):
        """Prueba que teléfonos con formatos inválidos lancen ValueError."""
        with self.assertRaises(ValueError):
            Cliente("Juan", "12345678", "juan@example.com", "123456")  # Corto
        with self.assertRaises(ValueError):
            Cliente("Juan", "12345678", "juan@example.com", "1234567890123456")  # Largo
        with self.assertRaises(ValueError):
            Cliente("Juan", "12345678", "juan@example.com", "+57-310-123")  # Guiones no permitidos


if __name__ == '__main__':
    # Ejecuta el suite de pruebas al correr este archivo directamente
    unittest.main()
