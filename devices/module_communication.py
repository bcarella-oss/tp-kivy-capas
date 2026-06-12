"""MÓDULO COMUNICACIÓN SERIAL
Dispositivo para comunicación por puerto serial.
Usa el driver UART para su funcionamiento.
"""

from drivers.driver_uart import uart_driver, BaudRate, Parity
from typing import Optional


class CommunicationModule:
    """Módulo de Comunicación Serial - Usa UART driver."""
    
    def __init__(self):
        self.port_name = "COM1"
        self.is_initialized = False
        self.message_history = []
    
    def initialize(self, baud_rate: BaudRate = BaudRate.BAUD_9600, 
                  parity: Parity = Parity.NONE) -> bool:
        """Inicializa la comunicación serial."""
        success = uart_driver.initialize(baud_rate, parity)
        if success:
            self.is_initialized = True
            print(f"[MÓDULO COMUNICACIÓN] Inicializado: {baud_rate.value} bps")
        return success
    
    def deinitialize(self) -> bool:
        """Des-inicializa la comunicación serial."""
        success = uart_driver.deinitialize()
        if success:
            self.is_initialized = False
            print("[MÓDULO COMUNICACIÓN] Des-inicializado")
        return success
    
    def send_message(self, message: str) -> bool:
        """Envía un mensaje por el puerto serial."""
        if not self.is_initialized:
            print("[MÓDULO COMUNICACIÓN] ERROR: Comunicación no inicializada")
            return False
        
        success = uart_driver.transmit(message)
        if success:
            self.message_history.append({"type": "TX", "data": message})
        return success
    
    def receive_message(self, length: int = 1) -> Optional[str]:
        """Recibe un mensaje desde el puerto serial."""
        if not self.is_initialized:
            return None
        
        message = uart_driver.receive(length)
        if message:
            self.message_history.append({"type": "RX", "data": message})
        return message if message else None
    
    def change_baud_rate(self, baud_rate: BaudRate) -> bool:
        """Cambia la velocidad de comunicación."""
        return uart_driver.set_baud_rate(baud_rate)
    
    def get_message_history(self) -> list:
        """Obtiene el historial de mensajes."""
        return self.message_history.copy()
    
    def clear_message_history(self) -> None:
        """Limpia el historial de mensajes."""
        self.message_history.clear()
    
    def get_status(self) -> dict:
        """Obtiene el estado de la comunicación."""
        config = uart_driver.get_configuration()
        return {
            "module": "Comunicación Serial",
            "initialized": self.is_initialized,
            "port": self.port_name,
            "configuration": config,
            "message_history_size": len(self.message_history)
        }


# Instancia global del módulo Comunicación
communication_module = CommunicationModule()
