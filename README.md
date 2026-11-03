PLAN DE TRABAJO COLABORATIVO – FASE 4

Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ

1. Organización del proyecto

Compañeros, para el desarrollo de esta actividad ya contamos con un repositorio creado en GitHub, donde centralizaremos los archivos y avances del proyecto.

Repositorio oficial:

https://github.com/IdelgadoUnad/Trabajo-colaborativo-Fase---4

Todos los integrantes deberán tener acceso como colaboradores para poder consultar, publicar y actualizar sus respectivos archivos.

2. Metodología de trabajo

Para facilitar el desarrollo y permitir que cada integrante avance de manera independiente, trabajaremos con archivos separados por cada componente del sistema.

Sin embargo, tendremos un archivo principal que será nuestra referencia para la integración de todo el proyecto:

Archivo maestro: Sistema_de_Gestión-COMPILADO.py

Consultar archivo maestro en GitHub

Este archivo será utilizado para integrar y consolidar los desarrollos individuales hasta obtener un programa completo y funcional.

¿Cómo trabajaremos?

Cada integrante desarrollará su parte en el archivo correspondiente.

Cada avance deberá probarse antes de publicarse.

Una vez realizado un avance o modificación, el integrante deberá actualizar su archivo en GitHub.

Posteriormente, deberá informar en el grupo de WhatsApp qué archivo actualizó y qué cambios realizó.

Los demás integrantes podrán consultar los avances publicados para mantenerse al tanto del desarrollo.

El líder revisará los aportes y realizará la integración correspondiente en el archivo maestro.

Después de cada integración se realizarán pruebas para verificar que el programa siga funcionando correctamente.

Importante: No debemos modificar directamente el archivo maestro sin coordinación previa. La integración se realizará de manera organizada para evitar conflictos y pérdida de información.

3. Distribución de responsabilidades

ESTUDIANTE 1 – Arquitectura y gestión de clientes

Responsabilidades:

Crear la clase abstracta general Entidad.

Desarrollar la clase Cliente.

Implementar atributos y métodos con encapsulación.

Establecer validaciones para los datos de los clientes.

Garantizar el manejo adecuado de la información personal.

Archivo de trabajo: entidades_clientes.py

ESTUDIANTE 2 – Gestión de servicios

Responsabilidades:

Crear la clase abstracta Servicio.

Desarrollar las clases derivadas:

ReservaSala.

AlquilerEquipo.

AsesoriaEspecializada.

Implementar herencia y polimorfismo.

Sobrescribir métodos para describir servicios, validar parámetros y calcular costos.

Incorporar los mecanismos de cálculo de costos solicitados.

Archivo de trabajo: servicios.py

ESTUDIANTE 3 – Gestión de reservas

Responsabilidades:

Desarrollar la clase Reserva.

Establecer la relación entre clientes y servicios.

Implementar duración, costos y estados de las reservas.

Crear los métodos de confirmación, cancelación y procesamiento.

Incorporar el manejo de excepciones en las operaciones correspondientes.

Archivo de trabajo: reservas.py

ESTUDIANTE 4 – Excepciones y registro de eventos

Responsabilidades:

Crear las excepciones personalizadas.

Implementar los mecanismos de manejo de errores.

Demostrar el uso de try/except, try/except/else y try/except/finally.

Implementar el encadenamiento de excepciones.

Registrar los errores y eventos en archivos de log.

Garantizar que la aplicación pueda continuar funcionando ante errores controlados.

Archivo de trabajo: excepciones_logs.py

ESTUDIANTE 5 – Interfaz gráfica e integración

Responsabilidades:

Desarrollar la interfaz gráfica utilizando Tkinter.

Crear la ventana principal y los controles necesarios.

Permitir la interacción con clientes, servicios y reservas.

Conectar las opciones de la interfaz con las funcionalidades del sistema.

Apoyar las pruebas de funcionamiento e integración.

Archivo de trabajo: interfaz.py

4. Reglas de desarrollo e integración

Para evitar inconvenientes durante la integración, debemos tener en cuenta las siguientes reglas:

Respetar los nombres acordados: las clases, métodos, atributos y parámetros deben conservar los nombres establecidos entre todos los integrantes.

Mantener una estructura común: debemos utilizar los mismos criterios para definir las clases, sus relaciones y el funcionamiento de los métodos.

Publicar los avances: cada modificación debe subirse al repositorio para que todos podamos consultar el estado actual del proyecto.

Informar los cambios: después de actualizar un archivo, se debe comunicar en WhatsApp qué se modificó y qué funcionalidades se incorporaron.

Probar antes de publicar: cada integrante debe verificar que su código funcione correctamente.

Coordinar la integración: los cambios se incorporarán al archivo maestro después de su revisión.

Evitar trabajar sobre versiones desactualizadas: antes de continuar, debemos consultar la última versión publicada en GitHub.

5. Pruebas y cumplimiento de la guía

Durante el desarrollo realizaremos pruebas progresivas para verificar el funcionamiento de cada componente y posteriormente del sistema completo.

Debemos garantizar el cumplimiento de los requisitos de la actividad, incluyendo:

Programación orientada a objetos.

Abstracción, encapsulación, herencia y polimorfismo.

Métodos sobrescritos y sobrecarga simulada mediante parámetros opcionales u otros mecanismos equivalentes en Python.

Excepciones personalizadas y manejo de errores.

Registro de eventos y errores mediante archivos.

Mínimo 10 operaciones completas, combinando casos válidos e inválidos.

Interfaz gráfica funcional.

Código organizado y debidamente comentado.

6. Compromiso del equipo

La idea es que todos participemos activamente en el desarrollo, cumplamos con nuestras responsabilidades y mantengamos comunicación sobre los avances.

Como líder del grupo, estaré pendiente de coordinar las actividades, revisar los aportes y mantener actualizado el archivo maestro.

Si algún integrante presenta dificultades o no puede completar su parte, deberá comunicarlo oportunamente para reorganizar las actividades y evitar retrasos en la entrega.

El objetivo es construir entre todos un único sistema funcional, integrando progresivamente el trabajo de cada integrante.

¡Trabajemos de manera organizada, con comunicación y compromiso para sacar adelante este proyecto!
