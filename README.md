# Bookstore Inventory API 📚

Esta es una API REST robusta desarrollada con **Django** y **Django Rest Framework** para la gestión de inventario de una cadena de librerías. El sistema permite administrar libros y realizar cálculos de precios de venta en tiempo real integrando tasas de cambio externas.

## 🚀 Características
- **CRUD Completo**: Gestión total de libros (Crear, Leer, Actualizar, Eliminar).
- **Validación de Negocio**: Control de ISBN (10/13 dígitos), stocks no negativos y precios mayores a cero.
- **Integración Externa**: Conexión con *ExchangeRate-API* para obtener tasas USD -> EUR en tiempo real.
- **Bulk Create**: Endpoint especializado para carga masiva de datos.
- **Búsqueda y Filtros**: Filtrado por categorías y detección de bajo stock.

## 🛠️ Tecnologías Utilizadas
- **Backend**: Python 3.12+, Django 5.x
- **API**: Django Rest Framework (DRF)
- **Base de Datos**: SQLite (Configurada para portabilidad inmediata)
- **Librerías Extra**: `requests` (para consumo de API externa)

## 📦 Instalación y Ejecución

Sigue estos pasos para levantar el proyecto localmente:

1. **Clonar el repositorio:**
   ```bash
   git clone <url-de-tu-repositorio>
   cd bookstore-inventory-api
   ```
Crear y activar entorno virtual:
    ```bash
    python -m venv venv
    ```
# En Windows:
    ```bash
    .\venv\Scripts\activate
    

Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```

Ejecutar migraciones:
    ```bash
    python manage.py migrate
    ```

Iniciar el servidor:
    ```bash
    python manage.py runserver
    ```

La API estará disponible en:

http://127.0.0.1:8000/api/


## Endpoints Principales

| Método | Endpoint                            | Descripción                         |
|--------|-------------------------------------|-------------------------------------|
| POST   | /api/books/                         | Crea un nuevo libro                 |
| GET    | /api/books/                         | Lista todos los libros              |
| GET    | /api/books/{id}/                    | Detalle de un libro                 |
| PUT    | /api/books/{id}/                    | Actualización total                 |
| DELETE | /api/books/{id}/                    | Eliminar un libro                   |
| POST   | /api/books/{id}/calculate-price/    | Calcula precio sugerido             |
| POST   | /api/books/bulk-create/             | Carga masiva de libros              |


## Lógica de Negocio: Cálculo de Precio

El endpoint `/calculate-price/` realiza las siguientes acciones:

- Obtiene el `cost_usd` del libro.
- Consulta la tasa de cambio actual (USD a EUR) vía API externa.
- Aplica un margen de ganancia del 40 por ciento.
- Actualiza automáticamente el campo `selling_price_local` en la base de datos.
- Si la API externa falla, el sistema utiliza una tasa de respaldo (0.85) para asegurar la continuidad operativa.


## Notas de Entrega

- Se ha implementado un manejo de errores detallado (400, 404, 500).
- Las validaciones de ISBN previenen duplicados y formatos incorrectos incluso en actualizaciones (PUT).
- Se adjunta la colección de Postman en la raíz del proyecto para facilitar las pruebas.
- Desarrollado como parte de la prueba técnica para Nextep Innovation.
