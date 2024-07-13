# PoC FastApi Auth JWT - Oauth2 - Sqlite



## Overview 🌐
El objetivo de esta Prueba de Concepto (PoC) es demostrar la capacidad de FastAPI para implementar un microservicio de autenticación de usuarios utilizando JSON Web Token (JWT) y OAuth2. Este microservicio garantizará la autenticación segura de usuarios y podrá ser integrado con otros servicios. Además, esta PoC emplea una arquitectura hexagonal, asegurando una separación clara de responsabilidades y facilitando la escalabilidad y mantenibilidad del código. Esta PoC servirá como una guía para escalar el servicio en múltiples tipos de proyectos, independientemente de su categoría, proporcionando una base sólida para futuras implementaciones.

## Requirements 🛠️
- Python 3.12
- FastAPI 0.111.0
- SQLAlchemy 2.0.31
- Pydantic 2.8.2
- Passlib 1.7.4
- PyJWT 2.8.0
- uvicorn 0.30.1
- SQLite
- Poetry 1.8.3
- PyCharm 2024.1.4 (Community Edition)

## Getting Started 🚀
### 1. Clone el Repositorio:
Clone este repositorio a su máquina local utilizando Git.

### 2. Instale Poetry:
Instale Poetry siguiendo las instrucciones en https://python-poetry.org/docs/#installation.

### 3. Instale Dependencias:
Desde una terminal PowerShell (PS), navegue hasta la ubicación del directorio `.../auth-fatapi/` y use Poetry para instalar las dependencias:
```bash
poetry install
```

### 4. Configuración de Variables de Entorno
Desde la misma PS sete el ambiente deseado (development, production, test) asegurese de tener configurado los archivos de configuración .env
```bash
$env:ENVIRONMENT = 'development'
```

Ubicado en el directorio `.../auth-fatapi/`
```bash
$env:PYTHONPATH = Get-Location
```

Puede verificar las variabes de entorno con:
```bash
echo $env:PYTHONPATH
echo $env:ENVIRONMENT
```
Nota: Este paso se debe ejecutar cada vez que abre una nueva terminal y dependerá de la consola que se utilice (Bash, PowerShell, CMD (Command Prompt):)

### 5. Inicie la Aplicación con Uvicorn:
Desde una terminal, navegue hasta la ubicación del directorio `.../auth-fatapi/` y ejecute Uvicorn para iniciar la aplicación:

```bash
uvicorn src.infrastructure.web.fastapi.api:app --reload
```
Este comando carga la aplicación FastAPI y la reinicia automáticamente cada vez que detecta un cambio en el código fuente.

### 6. Ejecutar el Script de Inserción de Usuarios

Para insertar usuarios de prueba utilizando el script `seed_users.py`, ejecute el siguiente comando con Poetry:

```bash
poetry run python scripts/seed_users.py
```

Este comando utiliza Poetry para ejecutar el script seed_users.py, que inserta usuarios de prueba en la base de datos configurada.

## Usage 💡
Acceder a Swagger para Probar la Autenticación

Después de configurar las variables de entorno y iniciar la aplicación, acceda a Swagger (normalmente disponible en http://localhost:8000/docs) para probar la autenticación utilizando el usuario de prueba:

```
Usuario: johndoe
```
```
Contraseña: secret
```


## Features 🌟
Registro de Usuarios: Permite registrar nuevos usuarios con contraseña segura.
Inicio de Sesión: Autentica a los usuarios y genera tokens JWT válidos.
Validación de Tokens: Verifica la autenticidad y validez de los tokens JWT.
Protección de Rutas: Ejemplo de cómo proteger rutas y endpoints usando JWT para autorización.
Screenshots 📸
Incluya capturas de pantalla de ejemplos de uso de la API para guiar visualmente.

## Deployment 🚀
Para implementar esta PoC de Auth con JWT:

Configure la configuración del entorno de producción en config.py.
Despliegue la aplicación usando Docker u otro método de implementación preferido.
## Contributing 🤝
¡Se aceptan contribuciones! Por favor, siga las pautas de contribución detalladas en CONTRIBUTING.md.

## License 📄
Este proyecto está bajo la Licencia MIT. Consulte el archivo LICENSE para obtener más detalles.

----

## Flujo de Autenticación con Tokens de Acceso y Refresh
1. Autenticación (Obtención del Token de Acceso)
   - El usuario envía sus credenciales (nombre de usuario y contraseña) al endpoint /token.
   - La API verifica las credenciales y genera un token de acceso si son válidas.
   - Este token de acceso tiene una duración limitada (por ejemplo, 15 minutos).

      ```http
      POST /token
      Content-Type: application/x-www-form-urlencoded
      username=user&password=password
      ```
  
2. Creación del Refresh Token
   - Después de obtener el token de acceso, el cliente puede solicitar un refresh token que le permitirá obtener un nuevo token de acceso sin necesidad de ingresar las credenciales nuevamente.
   - El refresh token tiene una duración más larga que el token de acceso (por ejemplo, 30 días).
     ```http
      POST /token/refresh
      Authorization: Bearer <refresh_token>
      ```
3. Renovación del Token de Acceso (Refresh Token)

   - Cuando el token de acceso expira, el cliente puede utilizar el refresh token para solicitar un nuevo token de acceso sin necesidad de autenticarse nuevamente.
   - La API valida el refresh token y emite un nuevo token de acceso.
     ```http
      POST /token/refresh
      Content-Type: application/x-www-form-urlencoded
      refresh_token=<refresh_token>
      ```

4. Manejo de Expiración de Tokens

   - Si tanto el token de acceso como el refresh token han expirado, el usuario debe autenticarse nuevamente (repetir el paso 1).

## Explicación del Flujo
### Autenticación: 
El cliente envía las credenciales al endpoint /token para obtener un token de acceso.
### Refresh Token: 
Después de obtener el token de acceso, el cliente puede solicitar un refresh token en el endpoint /token/refresh.
### Renovación del Token de Acceso: 
Cuando el token de acceso expira, el cliente usa el refresh token en /token/refresh para obtener un nuevo token de acceso.
### Manejo de Expiración: 
Si ambos tokens expiran, el usuario debe autenticarse nuevamente en /token.

Este flujo asegura que los usuarios puedan mantenerse autenticados de manera segura y continua en tu API, minimizando la necesidad de ingresar credenciales repetidamente y manteniendo un alto nivel de seguridad. Asegúrate de adaptar este flujo según las necesidades específicas y requisitos de tu aplicación.