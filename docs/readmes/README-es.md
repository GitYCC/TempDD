# Template-Driven Development Framework for AI-Augmented Coding

![banner](../../misc/banner.png)

## Descripción General

TempDD es un marco de desarrollo basado en plantillas que permite la colaboración estructurada humano-IA a través de flujos de trabajo personalizables e interacciones de plantillas guiadas por agentes.

A medida que aumenta la complejidad de los proyectos, los Agentes de IA enfrentan desafíos operando independientemente, haciendo que la colaboración humano-en-el-bucle sea cada vez más crítica. Los desarrolladores necesitan herramientas efectivas para comunicarse con estos Agentes de IA de caja negra. Los enfoques basados en plantillas proporcionan comunicación estructurada, reducen la carga cognitiva y permiten colaboración consistente con IA a través de flujos de trabajo guiados. Este repositorio proporciona un marco que permite a los usuarios personalizar flujos de trabajo según sus proyectos de desarrollo, simplificando el proceso en una serie de tareas de llenado de plantillas. El marco incorpora mecanismos de agentes para reducir la complejidad de las plantillas, permitiendo que los Agentes de IA ayuden efectivamente a los usuarios a completar la documentación. Visualizamos que este marco será aplicable en varios escenarios de desarrollo e incluso contextos de no desarrollo, mientras fomenta la colaboración de código abierto para integrar conocimiento global.

## Características

- 📚 **Dominio progresivo de IA a través de documentos en capas** - Transforma de usuario de IA a maestro de IA con documentación sofisticada de múltiples capas que amplifica tu control sobre el comportamiento de la IA
- 📋 **Flujo de trabajo basado en plantillas personalizable** - Enfoque estructurado para el desarrollo de proyectos con plantillas personalizables
- 💬 **Interacción de plantillas guiada por agentes personalizable** - Agentes personalizables se adaptan a cada plantilla, proporcionando orientación interactiva para ayudar a los usuarios a llenar plantillas colaborativamente
- 🤖 **Integración de herramientas de IA cruzadas** - Integración perfecta con Claude Code, Gemini CLI, Cursor y GitHub Copilot
- 🌐 **Soporte multiidioma** - Los usuarios pueden llenar plantillas usando su idioma preferido

## Inicio Rápido

### 1. Instalación

Instala `tempdd` usando uv:

```bash
uv tool install --force --from git+https://github.com/GitYCC/TempDD.git tempdd && exec $SHELL
```

### 2. Inicializar Proyecto

Crea un nuevo directorio de proyecto e inicializa TempDD:

```bash
mkdir demo
cd demo
tempdd init  # Puedes elegir el flujo de trabajo incorporado y la herramienta de IA preferida durante la inicialización
```

### 3. Ejemplo: Flujo de Trabajo Predeterminado con Claude Code

El siguiente ejemplo demuestra el uso del flujo de trabajo predeterminado con Claude Code. Para opciones de personalización detalladas y flujos de trabajo disponibles, consulta `tempdd help`.

Una vez que entres a Claude Code, ejecuta los siguientes comandos en secuencia:

```bash
# Obtener ayuda y entender los comandos disponibles
/tempdd-go help

# Generar documento de requisitos del producto
/tempdd-go prd build

# Después de terminar el PRD, crear diseño de arquitectura
/tempdd-go arch build

# Después de terminar el documento de diseño de arquitectura, realizar investigación
/tempdd-go research build

# Después de terminar el reporte de investigación, construir plano de implementación
/tempdd-go blueprint build

# Después de terminar el plano, generar lista de tareas
/tempdd-go tasks build

# Después de terminar la lista de tareas, ejecutar tareas para generar los códigos
/tempdd-go tasks run
```

Desde este ejemplo, puedes ver que el desarrollo progresa de la idea a la implementación a través de documentación de múltiples capas. Cada documento es llenado por IA preguntando a los usuarios por entrada cuando es necesario, lo que reduce la complejidad de llenado de formularios para los usuarios mientras mejora el consenso entre IA y humanos. Vale la pena señalar, el paso de investigación involucra a la IA buscando proactivamente información en línea para mejorar su comprensión de la implementación. Creo que existen mejores flujos de trabajo, y no deberíamos esperar que un flujo de trabajo satisfaga cada proyecto. Por lo tanto, este marco está diseñado para ser fácilmente personalizable. Consulta la sección ["Personaliza tu flujo de trabajo"](#personaliza-tu-flujo-de-trabajo) para aprender más.

## Personaliza tu flujo de trabajo

TempDD te permite crear flujos de trabajo personalizados adaptados a tus necesidades específicas de desarrollo.

Sigue los siguientes pasos para personalizar tu flujo de trabajo:
1. **Lee la guía**: Consulta [./customized/](../../customized/) para instrucciones completas de creación de flujos de trabajo
2. **Crea tu flujo de trabajo** siguiendo la estructura y ejemplos proporcionados
3. **Inicializa proyecto** con tu flujo de trabajo personalizado:

```bash
tempdd init --workflow /path/to/your/custom/workflow_dir/
```

## Contribuyendo Flujos de Trabajo Incorporados

¡Alentamos a los contribuyentes a ayudar a expandir la colección de flujos de trabajo incorporados de TempDD! Al contribuir nuevos flujos de trabajo, puedes ayudar a otros desarrolladores a beneficiarse de patrones de desarrollo probados y flujos de trabajo de dominios especializados.

### Cómo Contribuir un Nuevo Flujo de Trabajo Incorporado

1. **Haz fork de este repositorio** - Crea tu propio fork para trabajar
2. **Agrega tus archivos de flujo de trabajo**:
   - Agrega nuevos archivos de configuración a `./tempdd/core/configs/`
   - Agrega plantillas correspondientes a `./tempdd/core/templates/`
3. **Envía un Pull Request** - Comparte tu flujo de trabajo con la comunidad

¡Tus contribuciones ayudarán a hacer TempDD más valioso para desarrolladores en diferentes dominios y casos de uso. Ya sea un flujo de trabajo para desarrollo móvil, ciencia de datos, DevOps, o cualquier otra especialización, damos la bienvenida a tu experiencia!

## Integración de Herramientas de IA Cruzadas

TempDD se integra perfectamente con múltiples herramientas de desarrollo de IA:

| Herramienta de IA | Estado |
|---------|--------|
| **Claude Code** | ✅ Soporte Completo |
| **Gemini CLI** | ✅ Soporte Completo |
| **Cursor** | ✅ Soporte Completo |
| **GitHub Copilot** | ✅ Soporte Completo |

## Agradecimientos

Gracias a los siguientes repositorios por la inspiración:
- [github/spec-kit](https://github.com/github/spec-kit)
- [coleam00/context-engineering-intro](https://github.com/coleam00/context-engineering-intro)