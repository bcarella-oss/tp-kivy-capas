"""LÓGICA DE APLICACIÓN
Capa que coordina el uso de los dispositivos/módulos sin conocer los detalles
internos de cómo funcionan.
"""

from devices.module_led import led_module, LEDColor
from devices.module_display import display_module
from devices.module_sensor import sensor_module
from devices.module_communication import communication_module
from drivers.driver_uart import BaudRate, Parity
from typing import Dict, Any


class SystemController:
    """Controlador del sistema - Orquesta todos los dispositivos."""
    
    def __init__(self):
        self.system_state = {
            "led_initialized": False,
            "display_initialized": False,
            "sensor_initialized": False,
            "communication_initialized": False
        }
    
    # ===== CONTROL DE LED RGB =====
    def init_led(self) -> bool:
        """Inicializa el LED RGB."""
        success = led_module.initialize()
        self.system_state["led_initialized"] = success
        return success
    
    def set_led_color(self, color_name: str) -> bool:
        """Establece el color del LED RGB."""
        if not self.system_state["led_initialized"]:
            print("[APP] ERROR: LED no inicializado")
            return False
        
        try:
            color = LEDColor[color_name.upper()]
            return led_module.set_color(color)
        except KeyError:
            print(f"[APP] ERROR: Color '{color_name}' no existe")
            return False
    
    def toggle_led(self) -> bool:
        """Alterna el LED."""
        if not self.system_state["led_initialized"]:
            return False
        return led_module.toggle()
    
    def deinit_led(self) -> bool:
        """Des-inicializa el LED RGB."""
        success = led_module.deinitialize()
        self.system_state["led_initialized"] = False
        return success
    
    # ===== CONTROL DE DISPLAY =====
    def init_display(self) -> bool:
        """Inicializa el display 7 segmentos."""
        success = display_module.initialize()
        self.system_state["display_initialized"] = success
        return success
    
    def display_number(self, number: int) -> bool:
        """Muestra un número en el display."""
        if not self.system_state["display_initialized"]:
            print("[APP] ERROR: Display no inicializado")
            return False
        
        if 0 <= number <= 9:
            return display_module.display_digit(number)
        else:
            print(f"[APP] ERROR: Número fuera de rango: {number}")
            return False
    
    def clear_display(self) -> bool:
        """Limpia el display."""
        if not self.system_state["display_initialized"]:
            return False
        return display_module.clear()
    
    def deinit_display(self) -> bool:
        """Des-inicializa el display."""
        success = display_module.deinitialize()
        self.system_state["display_initialized"] = False
        return success
    
    # ===== CONTROL DE SENSOR =====
    def init_sensor(self) -> bool:
        """Inicializa el sensor de temperatura."""
        success = sensor_module.initialize()
        self.system_state["sensor_initialized"] = success
        return success
    
    def read_temperature(self) -> float:
        """Lee la temperatura del sensor."""
        if not self.system_state["sensor_initialized"]:
            print("[APP] ERROR: Sensor no inicializado")
            return 0.0
        return sensor_module.read_temperature()
    
    def calibrate_sensor(self, offset: int) -> bool:
        """Calibra el sensor."""
        if not self.system_state["sensor_initialized"]:
            return False
        return sensor_module.set_calibration(offset)
    
    def deinit_sensor(self) -> bool:
        """Des-inicializa el sensor."""
        success = sensor_module.deinitialize()
        self.system_state["sensor_initialized"] = False
        return success
    
    # ===== CONTROL DE COMUNICACIÓN =====
    def init_communication(self, baud_rate: str = "9600", parity: str = "NONE") -> bool:
        """Inicializa la comunicación serial."""
        try:
            br = BaudRate[f"BAUD_{baud_rate}"]
            p = Parity[parity]
            success = communication_module.initialize(br, p)
            self.system_state["communication_initialized"] = success
            return success
        except KeyError as e:
            print(f"[APP] ERROR: Configuración inválida: {e}")
            return False
    
    def send_message(self, message: str) -> bool:
        """Envía un mensaje por comunicación serial."""
        if not self.system_state["communication_initialized"]:
            print("[APP] ERROR: Comunicación no inicializada")
            return False
        return communication_module.send_message(message)
    
    def deinit_communication(self) -> bool:
        """Des-inicializa la comunicación."""
        success = communication_module.deinitialize()
        self.system_state["communication_initialized"] = False
        return success
    
    # ===== ESTADO DEL SISTEMA =====
    def get_system_status(self) -> Dict[str, Any]:
        """Obtiene el estado completo del sistema."""
        return {
            "system_state": self.system_state,
            "led": led_module.get_status() if self.system_state["led_initialized"] else None,
            "display": display_module.get_status() if self.system_state["display_initialized"] else None,
            "sensor": sensor_module.get_status() if self.system_state["sensor_initialized"] else None,
            "communication": communication_module.get_status() if self.system_state["communication_initialized"] else None,
        }
    
    def shutdown_all(self) -> bool:
        """Apaga todos los dispositivos."""
        results = []
        if self.system_state["led_initialized"]:
            results.append(self.deinit_led())
        if self.system_state["display_initialized"]:
            results.append(self.deinit_display())
        if self.system_state["sensor_initialized"]:
            results.append(self.deinit_sensor())
        if self.system_state["communication_initialized"]:
            results.append(self.deinit_communication())
        
        print("[APP] Sistema apagado completamente")
        return all(results) if results else True


# Instancia global del controlador
system_controller = SystemController()
