"""MÓDULO SENSOR DE TEMPERATURA
Dispositivo para lectura de temperatura.
Usa el driver ADC para su funcionamiento.
"""

from drivers.driver_adc import adc_driver


class TemperatureSensorModule:
    """Módulo Sensor de Temperatura - Usa ADC driver."""
    
    def __init__(self, channel: int = 0, sensor_type: str = "LM35"):
        self.channel = channel
        self.sensor_type = sensor_type
        self.is_initialized = False
        self.min_temp = -40
        self.max_temp = 150
    
    def initialize(self) -> bool:
        """Inicializa el módulo del sensor de temperatura."""
        adc_driver.initialize()
        adc_driver.enable_channel(self.channel)
        self.is_initialized = True
        print(f"[MÓDULO SENSOR TEMP] Inicializado: {self.sensor_type} en canal {self.channel}")
        return True
    
    def deinitialize(self) -> bool:
        """Des-inicializa el módulo del sensor."""
        adc_driver.disable_channel(self.channel)
        adc_driver.deinitialize()
        self.is_initialized = False
        print("[MÓDULO SENSOR TEMP] Des-inicializado")
        return True
    
    def read_temperature(self) -> float:
        """Lee la temperatura del sensor."""
        if not self.is_initialized:
            print("[MÓDULO SENSOR TEMP] ERROR: Sensor no inicializado")
            return 0.0
        
        # Lee el valor ADC
        adc_value = adc_driver.read_channel(self.channel)
        
        # Convierte ADC a temperatura (0-255 -> -40 a 150°C)
        temp_range = self.max_temp - self.min_temp
        temperature = self.min_temp + (adc_value / 255.0) * temp_range
        
        print(f"[MÓDULO SENSOR TEMP] Temperatura leída: {temperature:.2f}°C")
        return temperature
    
    def set_calibration(self, offset: int) -> bool:
        """Calibra el sensor aplicando un offset."""
        return adc_driver.set_calibration(self.channel, offset)
    
    def get_status(self) -> dict:
        """Obtiene el estado del sensor de temperatura."""
        return {
            "module": "Sensor de Temperatura",
            "initialized": self.is_initialized,
            "sensor_type": self.sensor_type,
            "channel": self.channel,
            "current_reading": self.read_temperature() if self.is_initialized else None,
            "range": f"{self.min_temp}°C a {self.max_temp}°C"
        }


# Instancia global del módulo Sensor
sensor_module = TemperatureSensorModule()
