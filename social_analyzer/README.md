# Analizador de Redes Sociales

Proyecto desarrollado en Python para la asignatura de Técnicas de Programación Avanzada.

La aplicación permitirá importar y analizar conversaciones procedentes de redes sociales o plataformas de mensajería, con el objetivo de obtener estadísticas de participación, detectar temas frecuentes, estudiar la actividad temporal y generar informes visuales.

## Miembros del grupo

- Javier Del Pozo
- Nombre y apellidos del integrante 2
- Nombre y apellidos del integrante 3
- Nombre y apellidos del integrante 4

## Funcionalidades principales

La aplicación contará con las siguientes funcionalidades:

1. Importación de conversaciones.
2. Gestión de usuarios, mensajes y conversaciones.
3. Cálculo de estadísticas de participación.
4. Detección de palabras y temas frecuentes.
5. Análisis temporal de la actividad.
6. Generación de informes y gráficos.

## Alcance de la PRAC1

En esta primera práctica se desarrollará la estructura inicial del proyecto y el modelo de dominio.

La primera versión incluirá:

- Creación de usuarios.
- Creación de conversaciones.
- Registro de participantes.
- Creación y almacenamiento de mensajes.
- Cálculo del número total de mensajes.
- Cálculo del número de participantes.
- Programa principal de prueba.
- Pruebas unitarias básicas.

Las funcionalidades avanzadas, como la detección de temas y la generación de gráficos, se implementarán en posteriores iteraciones.

## Modelo de dominio preliminar

El modelo de dominio está formado inicialmente por las siguientes clases:

### Usuario

Representa a una persona que participa en una conversación.

#### Atributos

- `id_usuario`: identificador único del usuario.
- `nombre`: nombre del usuario.

#### Responsabilidades

- Almacenar la información del participante.
- Identificar al autor de cada mensaje.
- Permitir el cálculo de estadísticas de participación.

### Mensaje

Representa un mensaje individual enviado por un usuario.

#### Atributos

- `id_mensaje`: identificador único del mensaje.
- `contenido`: texto del mensaje.
- `fecha`: fecha y hora de envío.
- `usuario`: usuario que ha enviado el mensaje.

#### Responsabilidades

- Almacenar el contenido del mensaje.
- Relacionar el mensaje con su autor.
- Almacenar la fecha y hora de envío.
- Obtener la longitud del mensaje.
- Extraer las palabras contenidas en el mensaje.

### Conversacion

Representa una conversación formada por participantes y mensajes.

#### Atributos

- `id_conversacion`: identificador único de la conversación.
- `titulo`: nombre descriptivo de la conversación.
- `mensajes`: colección de mensajes.
- `participantes`: colección de usuarios.

#### Responsabilidades

- Agregar participantes.
- Agregar mensajes.
- Evitar participantes duplicados.
- Obtener el número total de mensajes.
- Obtener la lista de participantes.

### Analizador

Contiene la lógica necesaria para analizar una conversación.

#### Responsabilidades

- Calcular estadísticas generales.
- Calcular la participación de cada usuario.
- Detectar palabras y temas frecuentes.
- Analizar la actividad temporal.
- Generar un resumen de resultados.

### Informe

Se encargará de presentar y exportar los resultados obtenidos.

#### Responsabilidades

- Generar gráficos.
- Mostrar resultados.
- Exportar estadísticas a CSV.
- Generar un informe final.

La clase `Informe` se implementará en una iteración posterior.

## Relaciones entre las clases

Las relaciones principales del modelo son:

- Un `Usuario` puede enviar varios `Mensaje`.
- Cada `Mensaje` pertenece a un único `Usuario`.
- Una `Conversacion` contiene varios `Mensaje`.
- Una `Conversacion` puede tener varios `Usuario`.
- Un `Analizador` analiza una `Conversacion`.
- Un `Informe` utiliza los resultados generados por el `Analizador`.

## Diagrama de clases preliminar

```mermaid
classDiagram
    class Usuario {
        -str id_usuario
        -str nombre
        +total_mensajes()
        +palabras_utilizadas()
    }

    class Mensaje {
        -str id_mensaje
        -str contenido
        -datetime fecha
        -Usuario usuario
        +obtener_longitud()
        +obtener_palabras()
    }

    class Conversacion {
        -str id_conversacion
        -str titulo
        -list mensajes
        -list participantes
        +agregar_mensaje(mensaje)
        +agregar_participante(usuario)
        +total_mensajes()
        +obtener_participantes()
    }

    class Analizador {
        -Conversacion conversacion
        +calcular_estadisticas()
        +calcular_participacion()
        +detectar_temas()
        +analizar_actividad_temporal()
    }

    class Informe {
        -Analizador analizador
        +generar_graficos()
        +exportar_csv()
        +exportar_pdf()
    }

    Usuario "1" --> "0..*" Mensaje : envía
    Conversacion "1" *-- "0..*" Mensaje : contiene
    Conversacion "1" o-- "0..*" Usuario : participantes
    Analizador --> Conversacion : analiza
    Informe --> Analizador : utiliza