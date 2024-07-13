# PoC FastApi Auth JWT - Oauth2 - Sqlite

### **Fecha:**

07/10/2024

### **Versión del Documento:**

Versión

[1.0.0]

### **1. Introducción**

**1.1 Objetivo de la Prueba de Concepto**

El objetivo de esta Prueba de Concepto (PoC) es demostrar la capacidad de FastAPI para implementar un microservicio de autenticación de usuarios utilizando JSON Web Token (JWT) y OAuth2. Este microservicio garantizará la autenticación segura de usuarios y podrá ser integrado con otros servicios. Además, esta PoC emplea una arquitectura hexagonal, asegurando una separación clara de responsabilidades y facilitando la escalabilidad y mantenibilidad del código. Esta PoC servirá como una guía para escalar el servicio en múltiples tipos de proyectos, independientemente de su categoría, proporcionando una base sólida para futuras implementaciones.

**1.2 Alcance**

Esta PoC abarca las siguientes funcionalidades:

-  **Endpoints relacionados con la gestion de autenticación:**

	- **Endpoint de Autenticación con username y password**: Permite a los usuarios autenticarse utilizando su username y contraseña, generando un JWT válido.
	
	- **Endpoint de creación de refresh token**: Permite la generación de un token de actualización (refresh token) para extender la duración de la sesión del usuario.
	
	- **Endpoint para refrescar el JWT**: Proporciona un endpoint para refrescar un JWT expirado utilizando un refresh token válido.

-  **Endpoints relacionados con la gestión de usuarios:**
  
	- **Endpoint de creación de usuario**: Permite la creación de nuevos usuarios en el sistema, almacenando la información de usuario en la base de datos.
	
	- **Endpoint para obtener información del usuario en cuestión**: Permite obtener información del usuario autenticado.
	
	-  **Endpoint dummy  protegido **: Proporciona un endpoint de pureba para validar que es necesario que usuario este autenticado.

-  **Otros Endpoints:**

	- **Endpoint de health status**: Ofrece un endpoint para verificar el estado de salud del servicio, indicando si está en ejecución correctamente.

- **Almacenamiento en base de datos SQLite**: Utiliza SQLite como motor de base de datos para almacenar usuarios y tokens de forma segura y eficiente.

-  **Hash de Contraseñas**: Se utiliza la biblioteca `passlib` para el hashing seguro de contraseñas. Los métodos utilizados son. (Aunque la contraeña plana sea igual, la contraseña hasheada seria diferente)

Esta PoC se enfoca en la implementación de un sistema de autenticación robusto y seguro, utilizando JSON Web Tokens (JWT) para la gestión de sesiones de usuario.

---

### **2. Requerimientos**

**2.1 Requerimientos Funcionales**

1. Implementar un endpoint de autenticación con username y password.
2. Desarrollar un endpoint de creación de refresh token.
3. Implementar un endpoint para refrescar el JWT.
4. Crear un endpoint de creación de usuario.
5. Desarrollar un endpoint para obtener información del usuario autenticado.
6. Implementar un endpoint de prueba protegido para validación de autenticación.
7. Implementar un endpoint de health status.

**2.2 Requerimientos No Funcionales**

1. Utilizar `passlib` y bcrypt para el hashing seguro de contraseñas.
2. Utilizar SQLite como motor de base de datos para almacenar usuarios y tokens.
3. Mantener una documentación clara y completa del API con OpenAPI (Swagger).

Este conjunto de requerimientos funcionales y no funcionales asegura que la Prueba de Concepto (PoC) cubra las funcionalidades esenciales de autenticación y gestión de usuarios de manera segura y eficiente, utilizando tecnologías modernas y buenas prácticas de desarrollo.

---

### **3. Metodología**

**3.1 Enfoque**

El enfoque adoptado para esta PoC fue iterativo e incremental, permitiendo ajustes rápidos basados en el feedback recibido durante una semana de desarrollo.

**3.2 Herramientas y Tecnologías**

-  **Python 3.12**: Lenguaje de programación de alto nivel ampliamente utilizado en el desarrollo de aplicaciones web y de escritorio.
- **FastAPI 0.111.0**: Framework web de alto rendimiento para construir APIs en Python, conocido por su rapidez y facilidad de uso.
- **SQLAlchemy 2.0.31**: Biblioteca de mapeo objeto-relacional (ORM) para Python que facilita la interacción con bases de datos relacionales.
- **Pydantic 2.8.2**: Librería para la validación de datos y serialización basada en type hints de Python, utilizada para definir y validar los esquemas de datos de la API.
- **Passlib 1.7.4**: Framework para el hashing seguro de contraseñas en Python, utilizado para almacenar contraseñas de manera segura en la base de datos.
- **PyJWT 2.8.0**: Implementación de JSON Web Tokens (JWT) en Python, utilizado para la autenticación y la gestión de sesiones de usuario en la API.
- **uvicorn 0.30.1**: Servidor ASGI de alta velocidad que permite ejecutar aplicaciones web de manera eficiente en Python.
- **SQLite**: Motor de base de datos relacional ligero utilizado localmente para almacenar datos de manera eficiente y escalable durante el desarrollo y pruebas.
- **Poetry 1.8.3**: Herramienta para la gestión de dependencias y entornos virtuales en Python, que facilita la creación y distribución de proyectos Python.
- **PyCharm 2024.1.4 (Community Edition)**: Entorno de desarrollo integrado (IDE) de JetBrains diseñado para facilitar la escritura de código Python, con características avanzadas de autocompletado, depuración y gestión de proyectos.

Estas herramientas y tecnologías son esenciales para el desarrollo y la implementación de la Prueba de Concepto (PoC), proporcionando las capacidades necesarias para construir una API robusta, segura y escalable utilizando Python como lenguaje principal y PyCharm como el entorno de desarrollo integrado.

---

### **4. Desarrollo**

**4.1 Diseño Arquitectónico**

El diseño arquitectónico de esta PoC sigue el patrón de Arquitectura Hexagonal (o Puertos y Adaptadores), que se caracteriza por su separación clara entre las capas de negocio, adaptadores de infraestructura y interfaces externas. A continuación, se presenta un esquema general de la arquitectura:

![[Pasted image 20240712201402.png]]

**4.2 Descripción de Componentes**

- **Componente 1:** Descripción del componente 1
- **Componente 2:** Descripción del componente 2
- **Componente 3:** Descripción del componente 3

**4.3 Integración**

- **Componente 1: Application Layer**
    
    - Este componente contiene los casos de uso (`use_cases`) que implementan la lógica de negocio de la aplicación.
    - Ejemplos: Autenticación de usuarios, gestión de usuarios, generación de tokens JWT.
    
- **Componente 2: Domain Layer**
    
    - Aquí residen las entidades de dominio que encapsulan la lógica y los datos de la aplicación.
    - Ejemplos: Entidades como `User` que representan los datos de usuario y sus métodos asociados.
    
- **Componente 3: Infrastructure Layer**
    
    - Incluye adaptadores que conectan la aplicación con recursos externos como bases de datos, servicios web, etc.
    - Ejemplos: Repositorios que implementan interfaces definidas en el dominio, configuración del servidor FastAPI, y modelos de base de datos SQLAlchemy.

**4.3 Integración**

La integración de los componentes y sistemas se realiza de la siguiente manera, considerando la estructura del proyecto:

- **Integración de Componentes:**
    
    - Los casos de uso (`use_cases`) en la capa de aplicación interactúan con los repositorios definidos en el dominio para acceder y manipular datos de usuario.
    - Los adaptadores de infraestructura, como `SQLAlchemyUserRepository`, implementan los repositorios definidos en el dominio para la persistencia de datos utilizando SQLite.
    
- **Estructura del Proyecto:**
    
    - El proyecto está organizado con una estructura hexagonal, donde los directorios en `src` representan diferentes capas y componentes.
    - Los archivos de configuración, como `pyproject.toml` y `.env.*`, proporcionan configuraciones para diferentes entornos (desarrollo, producción, testing).
    - Scripts como `seed_users.py` en la carpeta `scripts` se utilizan para inicializar o manipular datos en la base de datos.

Esta estructura facilita la separación de preocupaciones y la escalabilidad del código, permitiendo cambios y mejoras en componentes específicos sin afectar otras partes del sistema.

---

### **5. Pruebas**

Puedo complementar la sección de Pruebas de la siguiente manera:

### **5. Pruebas**

**5.1 Estrategia de Pruebas**

La estrategia de pruebas para esta PoC se centra principalmente en pruebas end-to-end (E2E) realizadas manualmente, dadas las limitaciones de tiempo y recursos. Esta estrategia se enfoca en validar el flujo completo de las funcionalidades desde el inicio hasta el final, asegurando que todas las partes integradas funcionen correctamente como un sistema completo.

**5.2 Criterios de Aceptación**

Para considerar exitosa esta PoC, se establecen los siguientes criterios de aceptación:

- **Criterio de Aceptación 1:** El sistema permite a los usuarios autenticarse utilizando un username y contraseña válidos, generando un JWT correctamente.
  
- **Criterio de Aceptación 2:** El sistema permite la creación de nuevos usuarios, almacenando la información correctamente en la base de datos SQLite y generando tokens de autenticación adecuados.

- **Criterio de Aceptación 3:** El sistema es capaz de manejar adecuadamente la actualización de tokens JWT utilizando refresh tokens, extendiendo la sesión de los usuarios de manera segura.

Dado el enfoque de pruebas E2E manual, se asegurará que cada uno de estos criterios sea verificado y validado durante el proceso de prueba. Esta metodología proporciona una visión integral del funcionamiento del sistema en condiciones simuladas de uso real.

#### **Nota sobre Pruebas de Código**

No se han realizado pruebas unitarias o de integración automatizadas debido a las limitaciones de tiempo. Sin embargo, se ha priorizado la validación del sistema a través de pruebas E2E manuales para garantizar la funcionalidad básica y la integridad del flujo de trabajo principal.

Esta estrategia permite obtener retroalimentación rápida y directa sobre la funcionalidad del sistema, enfocándose en validar las características clave que demuestran el éxito de la PoC en términos de sus objetivos principales.

---

### **6. Resultados Esperados**

Se espera que esta PoC demuestre:

- La capacidad del servicio de autenticación para gestionar eficazmente el proceso de autenticación de usuarios utilizando JWT y OAuth2, asegurando la seguridad y la integridad de las credenciales.
    
- Cumplimiento con el alcance definido, incluyendo la implementación de endpoints específicos como autenticación con username y password, creación de usuarios, generación y uso de tokens JWT, y gestión de sesiones extendidas mediante refresh tokens.
    
- Evaluación de la funcionalidad y la interoperabilidad del servicio de autenticación en un entorno de desarrollo, asegurando que los endpoints definidos funcionen según lo esperado y proporcionen respuestas correctas y seguras.
    

Estos resultados se alinean con el objetivo principal de esta PoC, que es demostrar la viabilidad y funcionalidad del servicio de autenticación desarrollado con FastAPI y otras tecnologías seleccionadas, proporcionando una base sólida para su integración en proyectos futuros.

---


### **7. Riesgos y Mitigaciones**

**7.1 Riesgos**

- **Riesgo 1:** Posible vulnerabilidad de seguridad debido a la falta de actualización de bibliotecas y dependencias del proyecto.
  
- **Riesgo 2:** Problemas de interoperabilidad con otros servicios o sistemas debido a diferencias en la implementación de estándares de autenticación.

**7.2 Estrategias de Mitigación**

- **Riesgo 1:** Implementar un proceso regular de actualización y revisión de bibliotecas y dependencias del proyecto para mitigar posibles vulnerabilidades de seguridad. Utilizar herramientas de escaneo de vulnerabilidades y seguir las mejores prácticas de seguridad en el desarrollo.

- **Riesgo 2:** Realizar pruebas exhaustivas de integración con otros servicios durante el desarrollo para identificar y resolver problemas de interoperabilidad. Documentar claramente los estándares y protocolos de autenticación utilizados para facilitar la integración con otros sistemas.

Estas estrategias ayudarán a minimizar los riesgos identificados y garantizarán la robustez y la seguridad del servicio de autenticación desarrollado en esta PoC.

---
### **8. Conclusión y Próximos Pasos**

**8.1 Conclusión**

En conclusión, esta Prueba de Concepto (PoC) ha demostrado de manera satisfactoria la capacidad de FastAPI para implementar un microservicio de autenticación de usuarios utilizando JSON Web Token (JWT) y OAuth2. El servicio desarrollado cumple con los objetivos establecidos, proporcionando endpoints seguros y eficientes para la autenticación de usuarios. La arquitectura hexagonal adoptada ha facilitado la separación de responsabilidades y la integración con otros componentes del sistema de manera flexible.

**8.2 Próximos Pasos**

Los próximos pasos incluyen:

- **Implementación en Entorno de Producción:** Transferir la solución desarrollada a un entorno de producción para su despliegue real.
    
- **Adopción de una Base de Datos más Robusta:** Considerar migrar de SQLite a una base de datos más robusta como MariaDB o PostgreSQL. Gracias a SQLAlchemy, esta migración puede realizarse de manera relativamente sencilla y minimizando el impacto en el código existente.
    
- **Utilización de Alembic para Migraciones de Base de Datos:** Implementar Alembic para gestionar las migraciones de esquema de base de datos de manera controlada y automatizada.
    
- **Dockerización del Servicio:** Dockerizar la aplicación para facilitar su despliegue y gestión en diferentes entornos y configuraciones.
    
- **Implementación de un Sistema de Logs:** Establecer un sistema de logs para registrar las actividades de autenticación, incluyendo quién se ha autenticado y desde qué direcciones IP, proporcionando así un registro detallado de la actividad del servicio.
    

Estos pasos adicionales no solo mejorarán la robustez y la seguridad del servicio de autenticación, sino que también sentarán las bases para su escalabilidad y mantenimiento continuo en un entorno de producción.

---

### **9. Anexos**

Documentación automática con swagger
![[Pasted image 20240712202351.png]]

Arbol de la estructura de carpetas y archivos de la PoC 

Project
|   .env.development
|   .env.example
|   .env.production
|   .env.testing
|   entrypoint.py
|   poetry.lock
|   pyproject.toml
|   README.md
|   test.db
|   
+---scripts
|   |   seed_users.py
|   |   __init__.py
|   |   
+---src
|   |   __init__.py
|   |   
|   +---application
|   |   |   __init__.py
|   |   |   
|   |   +---use_cases
|   |   |   |   auth_uc.py
|   |   |   |   __init__.py
|   |   |   |   
|   |   |           
|   |           
|   +---domain
|   |   |   __init__.py
|   |   |   
|   |   +---entities
|   |   |   |   user_entities.py
|   |   |   |   __init__.py
|   |   |   |   
|   |   |           
|   |   +---ports
|   |   |   |   ISettingRepository.py
|   |   |   |   IUserRepository.py
|   |   |   |   __init__.py
|   |   |   |   
|   |   |           
|   |           
|   +---infrastructure
|   |   |   __init__.py
|   |   |   
|   |   +---adapters
|   |   |   |   __init__.py
|   |   |   |   
|   |   |   +---db
|   |   |   |   |   database.py
|   |   |   |   |   __init__.py
|   |   |   |   |   
|   |   |   |   +---models
|   |   |   |   |   |   user.py
|   |   |   |   |   |   __init__.py
|   |   |   |   |   |   
|   |   |   |   |           
|   |   |   |   +---repositories
|   |   |   |   |   |   sql_alchemy_user_repository.py
|   |   |   |   |   |   __init__.py
|   |   |   |   |   |   
|   |   |   |   |           
|   |   |   |           
|   |   |   +---fastapi
|   |   |   |   |   api.py
|   |   |   |   |   dependecies.py
|   |   |   |   |   deprecate_auth.py
|   |   |   |   |   oauth2.py
|   |   |   |   |   swagger_info.py
|   |   |   |   |   __init__.py
|   |   |   |   |   
|   |   |   |   +---routes
|   |   |   |   |   |   auth_routes.py
|   |   |   |   |   |   user_routes.py
|   |   |   |   |   |   
|   |   |   |   |           
|   |   |   |   +---schemas
|   |   |   |   |   |   user_schemas.py
|   |   |   |   |   |   __init__.py
|   |   |   |   |   |   
|   |   |   |   |           
|   |   |   |           
|   |   |           
|   |   +---config
|   |   |   |   settings.py
|   |   |   |   setting_repository.py
|   |   |   |   __init__.py
|   |   |   |   
|   |   |           
|   |           
|           
+---tests