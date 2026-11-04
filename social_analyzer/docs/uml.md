# UML de PRAC3

El diagrama refleja la arquitectura implementada en `src/analizador_redes`. Las relaciones de composición muestran que la fachada `Analizador` coordina servicios especializados, pero no implementa sus algoritmos.

```mermaid
classDiagram
    direction LR

    class Importador {
        <<abstract>>
        +importar(ruta, nombre) Conversacion*
        +validar_ruta(ruta) Path
    }

    class ImportadorCSV {
        +COLUMNAS set
        +importar(ruta, nombre) Conversacion
        -_crear_mensaje(fila, numero_linea) Mensaje
    }

    class Usuario {
        +nombre str
    }

    class Mensaje {
        +autor Usuario
        +contenido str
        +fecha datetime
    }

    class Conversacion {
        +id int?
        +nombre str
        +mensajes list~Mensaje~
        +participantes tuple~Usuario~
        +agregar(mensaje)
    }

    class AnalizadorParticipacion {
        +analizar(conversacion) list~Participacion~
    }

    class AnalizadorTemas {
        +analizar(conversacion, limite) list
    }

    class AnalizadorTemporal {
        +por_fecha(conversacion) dict
        +por_hora(conversacion) dict
    }

    class Analizador {
        -_participacion AnalizadorParticipacion
        -_temas AnalizadorTemas
        -_temporal AnalizadorTemporal
        +participacion(conversacion) list
        +temas(conversacion, limite) list
        +actividad_por_fecha(conversacion) dict
        +actividad_por_hora(conversacion) dict
        +resumen(conversacion, limite) dict
    }

    class RepositorioSQLite {
        +ruta Path
        +inicializar()
        +guardar(conversacion) int
        +obtener(id) Conversacion
        +listar() list
        +eliminar(id)
        -_conexion() Iterator~Connection~
    }

    class CLI {
        +ejecutar(args, importador) int
        +main(argv) int
    }

    Importador <|-- ImportadorCSV : herencia y sobrescritura
    ImportadorCSV ..> Conversacion : crea
    Conversacion "1" *-- "0..*" Mensaje
    Mensaje "0..*" --> "1" Usuario
    Analizador *-- AnalizadorParticipacion
    Analizador *-- AnalizadorTemas
    Analizador *-- AnalizadorTemporal
    RepositorioSQLite ..> Conversacion : persiste
    CLI ..> Importador : usa polimórficamente
    CLI ..> Analizador
    CLI ..> RepositorioSQLite
```

## Decisiones representadas

- **Abstracción:** `Importador` define el contrato común y no puede instanciarse.
- **Herencia y sobrescritura:** `ImportadorCSV` hereda de `Importador` e implementa `importar`.
- **Polimorfismo:** `cli.ejecutar` recibe opcionalmente cualquier `Importador`; la implementación CSV es solo el valor por defecto.
- **Responsabilidad única:** los algoritmos de participación, temas y tiempo viven en analizadores separados.
- **Compatibilidad:** `Analizador` sigue ofreciendo los métodos públicos de PRAC2 y actúa únicamente como fachada de composición.
- **Gestión de recursos:** `RepositorioSQLite._conexion` delimita transacción y cierre con un gestor de contexto.
