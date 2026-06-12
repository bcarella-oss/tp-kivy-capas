"""MÓDULO DISPLAY 7 SEGMENTOS
Dispositivo para mostrar dígitos numéricos.
Usa el driver GPIO para su funcionamiento.
"""

from drivers.driver_gpio import gpio_driver, PinMode


class Display7SegmentModule:
    """Módulo Display 7 Segmentos - Usa GPIO driver."""
    
    # Tablas de segmentos para dígitos 0-9
    DIGIT_PATTERNS = {
        0: 0b0111111,  # abcdef (sin g)
        1: 0b0000110,  # bc
        2: 0b1011011,  # abdeg
        3: 0b1001111,  # abcdg
        4: 0b1100110,  # bcfg
        5: 0b1101101,  # acdfg
        6: 0b1111101,  # acdefg
        7: 0b0000111,  # abc
        8: 0b1111111,  # abcdefg
        9: 0b1101111,  # abcdfg
    }
    
    def __init__(self, port: str = "B", start_pin: int = 0):
        self.port = port
        self.start_pin = start_pin
        self.current_digit = 0
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Inicializa el módulo Display 7 Segmentos."""
        gpio_driver.initialize()
        for i in range(7):
            gpio_driver.configure_pin(self.port, self.start_pin + i, PinMode.OUTPUT)
        self.is_initialized = True
        self.display_digit(0)
        print(f"[MÓDULO DISPLAY 7SEG] Inicializado en puerto {self.port}")
        return True
    
    def deinitialize(self) -> bool:
        """Des-inicializa el módulo Display 7 Segmentos."""
        self.display_digit(0)
        gpio_driver.deinitialize()
        self.is_initialized = False
        print("[MÓDULO DISPLAY 7SEG] Des-inicializado")
        return True
    
    def display_digit(self, digit: int) -> bool:
        """Muestra un dígito en el display."""
        if not self.is_initialized:
            print("[MÓDULO DISPLAY 7SEG] ERROR: Módulo no inicializado")
            return False
        
        if digit not in self.DIGIT_PATTERNS:
            print(f"[MÓDULO DISPLAY 7SEG] ERROR: Dígito no válido: {digit}")
            return False
        
        pattern = self.DIGIT_PATTERNS[digit]
        
        # Escribe cada bit en su respectivo segmento
        for segment in range(7):
            bit_value = bool((pattern >> segment) & 1)
            gpio_driver.write_pin(self.port, self.start_pin + segment, bit_value)
        
        self.current_digit = digit
        print(f"[MÓDULO DISPLAY 7SEG] Mostrando dígito: {digit}")
        return True
    
    def clear(self) -> bool:
        """Limpia el display (apaga todos los segmentos)."""
        return self.display_digit(0)
    
    def get_status(self) -> dict:
        """Obtiene el estado del display."""
        return {
            "module": "Display 7 Segmentos",
            "initialized": self.is_initialized,
            "current_digit": self.current_digit,
            "port": self.port,
            "start_pin": self.start_pin
        }


# Instancia global del módulo Display
display_module = Display7SegmentModule()
