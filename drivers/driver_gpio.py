"""DRIVER GPIO
Acceso a entradas y salidas digitales.
"""

from hardware_layer import hardware
from enum import Enum


class PinMode(Enum):
    """Modos de configuración de pines GPIO."""
    OUTPUT = 0
    INPUT = 1
    PWM = 2


class GPIODriver:
    """Driver para control de GPIO (Salidas/Entradas digitales)."""
    
    def __init__(self):
        self.pin_modes = {}
        self.pin_values = {}
    
    def initialize(self) -> None:
        """Inicializa el driver GPIO."""
        hardware.write_register("GPIO_PORT_A", 0x00000000)
        hardware.write_register("GPIO_PORT_B", 0x00000000)
        hardware.write_register("GPIO_PORT_C", 0x00000000)
        print("[DRIVER GPIO] Inicializado")
    
    def deinitialize(self) -> None:
        """Des-inicializa el driver GPIO."""
        hardware.write_register("GPIO_PORT_A", 0x00000000)
        hardware.write_register("GPIO_PORT_B", 0x00000000)
        hardware.write_register("GPIO_PORT_C", 0x00000000)
        print("[DRIVER GPIO] Des-inicializado")
    
    def configure_pin(self, port: str, pin: int, mode: PinMode) -> bool:
        """Configura un pin en modo específico."""
        pin_id = f"{port}_{pin}"
        self.pin_modes[pin_id] = mode
        print(f"[DRIVER GPIO] Pin {pin_id} configurado como {mode.name}")
        return True
    
    def write_pin(self, port: str, pin: int, value: bool) -> bool:
        """Escribe un valor lógico en un pin de salida."""
        pin_id = f"{port}_{pin}"
        if pin_id not in self.pin_modes or self.pin_modes[pin_id] != PinMode.OUTPUT:
            print(f"[DRIVER GPIO] ERROR: Pin {pin_id} no está configurado como OUTPUT")
            return False
        
        self.pin_values[pin_id] = value
        hardware.set_bit(f"GPIO_PORT_{port}", pin, value)
        return True
    
    def read_pin(self, port: str, pin: int) -> bool:
        """Lee el valor lógico de un pin."""
        pin_id = f"{port}_{pin}"
        if pin_id not in self.pin_modes:
            print(f"[DRIVER GPIO] ERROR: Pin {pin_id} no está configurado")
            return False
        
        value = hardware.get_bit(f"GPIO_PORT_{port}", pin)
        self.pin_values[pin_id] = value
        return value
    
    def get_pin_status(self, port: str, pin: int) -> dict:
        """Obtiene el estado y configuración de un pin."""
        pin_id = f"{port}_{pin}"
        return {
            "pin": pin_id,
            "mode": self.pin_modes.get(pin_id, "NOT CONFIGURED").name if pin_id in self.pin_modes else "NOT CONFIGURED",
            "value": self.pin_values.get(pin_id, None)
        }


# Instancia global del driver GPIO
gpio_driver = GPIODriver()
