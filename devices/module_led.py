"""MÓDULO LED RGB
Dispositivo compuesto por 3 LEDs (Rojo, Verde, Azul).
Usa el driver GPIO para su funcionamiento.
"""

from drivers.driver_gpio import gpio_driver, PinMode
from enum import Enum


class LEDColor(Enum):
    """Colores disponibles para el LED RGB."""
    RED = (1, 0, 0)
    GREEN = (0, 1, 0)
    BLUE = (0, 0, 1)
    YELLOW = (1, 1, 0)
    CYAN = (0, 1, 1)
    MAGENTA = (1, 0, 1)
    WHITE = (1, 1, 1)
    BLACK = (0, 0, 0)


class LEDRGBModule:
    """Módulo de LED RGB - Usa GPIO driver."""
    
    def __init__(self, port: str = "A", pin_r: int = 0, pin_g: int = 1, pin_b: int = 2):
        self.port = port
        self.pin_r = pin_r
        self.pin_g = pin_g
        self.pin_b = pin_b
        self.current_color = LEDColor.BLACK
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Inicializa el módulo LED RGB."""
        gpio_driver.initialize()
        gpio_driver.configure_pin(self.port, self.pin_r, PinMode.OUTPUT)
        gpio_driver.configure_pin(self.port, self.pin_g, PinMode.OUTPUT)
        gpio_driver.configure_pin(self.port, self.pin_b, PinMode.OUTPUT)
        self.is_initialized = True
        self.set_color(LEDColor.BLACK)
        print(f"[MÓDULO LED RGB] Inicializado en puerto {self.port}")
        return True
    
    def deinitialize(self) -> bool:
        """Des-inicializa el módulo LED RGB."""
        self.set_color(LEDColor.BLACK)
        gpio_driver.deinitialize()
        self.is_initialized = False
        print("[MÓDULO LED RGB] Des-inicializado")
        return True
    
    def set_color(self, color: LEDColor) -> bool:
        """Establece el color del LED RGB."""
        if not self.is_initialized:
            print("[MÓDULO LED RGB] ERROR: Módulo no inicializado")
            return False
        
        r, g, b = color.value
        gpio_driver.write_pin(self.port, self.pin_r, bool(r))
        gpio_driver.write_pin(self.port, self.pin_g, bool(g))
        gpio_driver.write_pin(self.port, self.pin_b, bool(b))
        
        self.current_color = color
        print(f"[MÓDULO LED RGB] Color establecido: {color.name}")
        return True
    
    def toggle(self) -> bool:
        """Alterna el estado del LED."""
        if self.current_color == LEDColor.BLACK:
            return self.set_color(LEDColor.WHITE)
        else:
            return self.set_color(LEDColor.BLACK)
    
    def get_status(self) -> dict:
        """Obtiene el estado del LED RGB."""
        return {
            "module": "LED RGB",
            "initialized": self.is_initialized,
            "current_color": self.current_color.name,
            "port": self.port,
            "pins": {"R": self.pin_r, "G": self.pin_g, "B": self.pin_b}
        }


# Instancia global del módulo LED
led_module = LEDRGBModule()
