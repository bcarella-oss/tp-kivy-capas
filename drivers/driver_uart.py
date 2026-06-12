"""DRIVER UART
Acceso a comunicación serial.
"""

from hardware_layer import hardware
from enum import Enum
from collections import deque


class BaudRate(Enum):
    """Velocidades de transmisión soportadas."""
    BAUD_9600 = 9600
    BAUD_19200 = 19200
    BAUD_38400 = 38400
    BAUD_115200 = 115200


class Parity(Enum):
    """Opciones de paridad."""
    NONE = 0
    EVEN = 1
    ODD = 2


class UARTDriver:
    """Driver para comunicación UART/Serial."""
    
    def __init__(self):
        self.baud_rate = BaudRate.BAUD_9600
        self.parity = Parity.NONE
        self.data_bits = 8
        self.stop_bits = 1
        self.rx_buffer = deque(maxlen=256)
        self.tx_buffer = deque(maxlen=256)
        self.is_initialized = False
    
    def initialize(self, baud_rate: BaudRate = BaudRate.BAUD_9600, 
                  parity: Parity = Parity.NONE) -> bool:
        """Inicializa la comunicación UART."""
        self.baud_rate = baud_rate
        self.parity = parity
        self.is_initialized = True
        hardware.write_register("UART_STATUS", 0x00000001)
        print(f"[DRIVER UART] Inicializado: {baud_rate.value} bps, Paridad: {parity.name}")
        return True
    
    def deinitialize(self) -> bool:
        """Des-inicializa la comunicación UART."""
        self.is_initialized = False
        self.rx_buffer.clear()
        self.tx_buffer.clear()
        hardware.write_register("UART_STATUS", 0x00000000)
        print("[DRIVER UART] Des-inicializado")
        return True
    
    def transmit(self, data: str) -> bool:
        """Transmite datos por UART."""
        if not self.is_initialized:
            print("[DRIVER UART] ERROR: UART no está inicializado")
            return False
        
        for byte in data:
            self.tx_buffer.append(ord(byte))
        
        print(f"[DRIVER UART] Transmitiendo: {data}")
        return True
    
    def receive(self, length: int = 1) -> str:
        """Recibe datos desde UART (simulado)."""
        if not self.is_initialized:
            return ""
        
        data = ""
        for _ in range(min(length, len(self.rx_buffer))):
            data += chr(self.rx_buffer.popleft())
        
        return data
    
    def set_baud_rate(self, baud_rate: BaudRate) -> bool:
        """Cambia la velocidad de transmisión."""
        self.baud_rate = baud_rate
        print(f"[DRIVER UART] Velocidad cambiada a: {baud_rate.value} bps")
        return True
    
    def get_configuration(self) -> dict:
        """Obtiene la configuración actual del UART."""
        return {
            "baud_rate": self.baud_rate.value,
            "parity": self.parity.name,
            "data_bits": self.data_bits,
            "stop_bits": self.stop_bits,
            "initialized": self.is_initialized,
            "rx_buffer_size": len(self.rx_buffer),
            "tx_buffer_size": len(self.tx_buffer)
        }


# Instancia global del driver UART
uart_driver = UARTDriver()
