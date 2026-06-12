# Sistema de Control Industrial - Arquitectura en Capas

## Descripción

Proyecto educativo que implementa un **sistema de control industrial** usando Kivy (framework Python para interfaces gráficas) siguiendo una **arquitectura en capas**.

## Arquitectura del Proyecto

### 1. **CAPA HARDWARE** (`hardware_layer.py`)
- Simula registros del microcontrolador
- Proporciona acceso de bajo nivel a registros
- Operaciones bit a bit
- **No se llama directamente desde la aplicación**

### 2. **CAPA DRIVERS** (`drivers/`)
Proporciona funciones de acceso a periféricos específicos:

- **`driver_gpio.py`**: Control de entradas/salidas digitales
  - Configuración de pines (INPUT/OUTPUT/PWM)
  - Lectura y escritura de pines
  - Consulta de estado

- **`driver_adc.py`**: Conversor analógico-digital
  - Habilitación de canales
  - Lectura de valores
  - Calibración

- **`driver_uart.py`**: Comunicación serial
  - Inicialización con parámetros (baud rate, paridad)
  - Transmisión y recepción
  - Configuración de parámetros

### 3. **CAPA DISPOSITIVOS/MÓDULOS** (`devices/`)
Abstracción de dispositivos físicos. Usa drivers para su funcionamiento:

- **`module_led.py`**: LED RGB
  - Inicialización
  - Cambio de color
  - Toggle
  - Estado

- **`module_display.py`**: Display 7 segmentos
  - Mostrar dígitos
  - Tablas de patrones
  - Limpieza

- **`module_sensor.py`**: Sensor de temperatura
  - Lectura de temperatura
  - Calibración
  - Rango de valores

- **`module_communication.py`**: Comunicación serial
  - Inicialización
  - Envío/recepción de mensajes
  - Historial de comunicación

### 4. **CAPA LÓGICA DE APLICACIÓN** (`app_logic.py`)
- `SystemController`: Orquesta el uso de los módulos
- No conoce detalles internos de los dispositivos
- Proporciona una interfaz simple y coherente

### 5. **CAPA INTERFAZ/APLICACIÓN** (`ui/`)
- `ui_main.py`: Pantalla principal con Kivy
- `ui_popups.py`: Componentes reutilizables (popups)
- Maneja interacción con el usuario

## Flujo de la Aplicación

```
Usuario (Interfaz Kivy)
    ↓
Pantalla Principal (ui_main.py)
    ↓
Controlador del Sistema (app_logic.py)
    ↓
Módulos/Dispositivos (devices/)
    ↓
Drivers (drivers/)
    ↓
Capa Hardware (hardware_layer.py)
    ↓
Registros del Sistema
```

## Ejemplo de Uso

### Cambiar color del LED

1. **Usuario interactúa** con la interfaz Kivy
2. **MainScreen** llama a `system_controller.set_led_color("RED")`
3. **SystemController** delega a `led_module.set_color(LEDColor.RED)`
4. **LEDModule** llama a `gpio_driver.write_pin()` para cada pin (R, G, B)
5. **GPIODriver** actualiza los registros en `hardware_layer`

### Leer temperatura

1. **Usuario** solicita lectura de temperatura
2. **MainScreen** llama a `system_controller.read_temperature()`
3. **SystemController** delega a `sensor_module.read_temperature()`
4. **SensorModule** llama a `adc_driver.read_channel()`
5. **ADCDriver** lee el registro en `hardware_layer` y convierte el valor
6. **SensorModule** convierte ADC a temperatura
7. El valor se retorna al usuario

## Ventajas de esta Arquitectura

✅ **Claridad**: Cada capa tiene responsabilidades específicas

✅ **Mantenibilidad**: Cambios en hardware se aíslan en drivers

✅ **Reutilización**: Los drivers pueden usarse en múltiples dispositivos

✅ **Escalabilidad**: Fácil agregar nuevos dispositivos

✅ **Testing**: Cada capa puede testearse independientemente

✅ **Comprensibilidad**: No es necesario conocer detalles de bajo nivel

## Cómo Ejecutar

### Requisitos
```bash
pip install kivy
```

### Ejecución
```bash
python main.py
```

## Estructura de Carpetas

```
proyecto/
├── main.py                 # Punto de entrada
├── hardware_layer.py       # Capa de hardware
├── app_logic.py           # Lógica de aplicación
│
├── drivers/
│   ├── __init__.py
│   ├── driver_gpio.py
│   ├── driver_adc.py
│   └── driver_uart.py
│
├── devices/
│   ├── __init__.py
│   ├── module_led.py
│   ├── module_display.py
│   ├── module_sensor.py
│   └── module_communication.py
│
└── ui/
    ├── __init__.py
    ├── ui_main.py
    └── ui_popups.py
```

## Conceptos Clave

### Registros de Hardware
- Variables que representan el estado del hardware
- Se escriben y leen a través de `HardwareLayer`
- En sistemas reales, son direcciones de memoria mapeadas

### Drivers
- Traducen operaciones de alto nivel a operaciones de hardware
- Conocen los detalles de cómo funciona un periférico específico
- Proporcionan funciones para: init, deinit, read, write, configure

### Módulos/Dispositivos
- Agrupan funcionalidades relacionadas
- Usan drivers para acceder al hardware
- Proporcionan una interfaz simple y coherente

### Lógica de Aplicación
- Orquesta el uso de módulos
- No accede directamente a drivers o hardware
- Proporciona servicios al nivel de aplicación

### Interfaz/UI
- Interactúa solo con la lógica de aplicación
- No conoce detalles de periféricos
- Puede ser reemplazada sin afectar el resto del sistema

## Ampliaciones Posibles

- Agregar nuevos dispositivos (motores, relés, pantallas LCD)
- Implementar persistencia (guardar configuración)
- Agregar logging y debugging
- Crear tests unitarios para cada capa
- Implementar mecanismos de error y excepciones
- Agregar timer y eventos asincronos
