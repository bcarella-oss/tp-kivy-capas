"""CAPA HARDWARE
Registros de control del sistema y simulación de periféricos físicos.
"""

from dataclasses import dataclass
from typing import Dict
import time


@dataclass
class RegisterHardware:
    """Simula los registros de hardware del microcontrolador."""
    
    # Registros de control GPIO
    GPIO_PORT_A: int = 0x00000000
    GPIO_PORT_B: int = 0x00000000
    GPIO_PORT_C: int = 0x00000000
    
    # Registros de comunicación
    UART_STATUS: int = 0x00000000
    UART_DATA: int = 0x00000000
    
    # Registros ADC (conversor analógico-digital)
    ADC_CHANNEL_0: int = 0
    ADC_CHANNEL_1: int = 0
    ADC_CHANNEL_2: int = 0
    
    # Registros de tiempo/Clock
    CLOCK_CONTROL: int = 0x00000001
    TIMER_COUNT: int = 0
    

class HardwareLayer:
    """Simula el acceso directo a registros de hardware."""
    
    def __init__(self):
        self.registers = RegisterHardware()
        self._log_operations = []
    
    def write_register(self, register_name: str, value: int) -> None:
        """Escribe un valor en un registro de hardware."""
        if hasattr(self.registers, register_name):
            setattr(self.registers, register_name, value)
            self._log_operations.append(
                f"[HW] WRITE: {register_name} = 0x{value:08X} @ {time.time()}"
            )
        else:
            raise ValueError(f"Registro no existe: {register_name}")
    
    def read_register(self, register_name: str) -> int:
        """Lee el valor de un registro de hardware."""
        if hasattr(self.registers, register_name):
            value = getattr(self.registers, register_name)
            self._log_operations.append(
                f"[HW] READ: {register_name} = 0x{value:08X} @ {time.time()}"
            )
            return value
        else:
            raise ValueError(f"Registro no existe: {register_name}")
    
    def set_bit(self, register_name: str, bit_position: int, value: bool) -> None:
        """Modifica un bit específico de un registro."""
        current = self.read_register(register_name)
        if value:
            current |= (1 << bit_position)
        else:
            current &= ~(1 << bit_position)
        self.write_register(register_name, current)
    
    def get_bit(self, register_name: str, bit_position: int) -> bool:
        """Lee un bit específico de un registro."""
        value = self.read_register(register_name)
        return bool(value & (1 << bit_position))
    
    def get_operation_log(self) -> list:
        """Retorna el historial de operaciones."""
        return self._log_operations.copy()
    
    def clear_log(self) -> None:
        """Limpia el historial de operaciones."""
        self._log_operations.clear()


# Instancia global de hardware (singleton)
hardware = HardwareLayer()
