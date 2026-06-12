"""DRIVER ADC
Acceso a conversor analógico-digital.
"""

from hardware_layer import hardware
import random


class ADCDriver:
    """Driver para conversión analógico-digital."""
    
    def __init__(self):
        self.resolution = 8  # bits
        self.max_value = (2 ** self.resolution) - 1
        self.channels_enabled = {}
        self.calibration_offset = {}
    
    def initialize(self) -> None:
        """Inicializa el driver ADC."""
        self.channels_enabled = {0: False, 1: False, 2: False}
        self.calibration_offset = {0: 0, 1: 0, 2: 0}
        print("[DRIVER ADC] Inicializado")
    
    def deinitialize(self) -> None:
        """Des-inicializa el driver ADC."""
        self.channels_enabled = {0: False, 1: False, 2: False}
        print("[DRIVER ADC] Des-inicializado")
    
    def enable_channel(self, channel: int) -> bool:
        """Habilita un canal ADC."""
        if channel not in self.channels_enabled:
            print(f"[DRIVER ADC] ERROR: Canal {channel} no existe")
            return False
        
        self.channels_enabled[channel] = True
        print(f"[DRIVER ADC] Canal {channel} habilitado")
        return True
    
    def disable_channel(self, channel: int) -> bool:
        """Deshabilita un canal ADC."""
        if channel not in self.channels_enabled:
            return False
        
        self.channels_enabled[channel] = False
        print(f"[DRIVER ADC] Canal {channel} deshabilitado")
        return True
    
    def read_channel(self, channel: int) -> int:
        """Lee el valor del canal ADC."""
        if not self.channels_enabled.get(channel, False):
            print(f"[DRIVER ADC] ERROR: Canal {channel} no está habilitado")
            return 0
        
        # Simula lectura de sensor con ruido
        raw_value = random.randint(0, self.max_value)
        calibrated = max(0, min(self.max_value, raw_value + self.calibration_offset[channel]))
        
        register_name = f"ADC_CHANNEL_{channel}"
        hardware.write_register(register_name, calibrated)
        
        return calibrated
    
    def set_calibration(self, channel: int, offset: int) -> bool:
        """Establece el offset de calibración para un canal."""
        if channel not in self.channels_enabled:
            return False
        
        self.calibration_offset[channel] = offset
        print(f"[DRIVER ADC] Canal {channel} calibrado con offset: {offset}")
        return True
    
    def get_channel_status(self, channel: int) -> dict:
        """Obtiene el estado de un canal ADC."""
        return {
            "channel": channel,
            "enabled": self.channels_enabled.get(channel, False),
            "value": hardware.read_register(f"ADC_CHANNEL_{channel}"),
            "calibration_offset": self.calibration_offset.get(channel, 0)
        }


# Instancia global del driver ADC
adc_driver = ADCDriver()
