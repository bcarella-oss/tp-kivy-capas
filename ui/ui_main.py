"""INTERFAZ PRINCIPAL CON KIVY"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.uix.popup import Popup

from app_logic import system_controller
from ui.ui_popups import (
    ConfirmationPopup, InputPopup, SelectionPopup, ProgressPopup
)
from devices.module_led import LEDColor
from drivers.driver_uart import BaudRate


class MainScreen(Screen):
    """Pantalla principal - Panel de control del sistema."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout.canvas.before.clear()
        layout.canvas.before.add(Color(0.15, 0.15, 0.18, 1))
        layout.canvas.before.add(Rectangle(size=layout.size, pos=layout.pos))
        
        # Título
        title = Label(text="[b]Panel de Control del Sistema[/b]",
                     markup=True,
                     font_size='24sp',
                     size_hint_y=0.1)
        layout.add_widget(title)
        
        # Área de botones (scroll)
        scroll = ScrollView(size_hint=(1, 0.8))
        button_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, padding=10)
        button_grid.bind(minimum_height=button_grid.setter('height'))
        
        buttons_config = [
            ("Inicializar LED", self.init_led),
            ("Cambiar Color LED", self.change_led_color),
            ("Apagar LED", self.turn_off_led),
            ("Inicializar Display", self.init_display),
            ("Mostrar Número", self.show_number),
            ("Limpiar Display", self.clear_display),
            ("Inicializar Sensor", self.init_sensor),
            ("Leer Temperatura", self.read_temperature),
            ("Calibrar Sensor", self.calibrate_sensor),
            ("Inicializar Comunicación", self.init_communication),
            ("Enviar Mensaje", self.send_message),
            ("Ver Estado", self.view_status),
        ]
        
        for label_text, callback in buttons_config:
            btn = Button(text=label_text, size_hint_y=None, height='50dp')
            btn.bind(on_press=callback)
            button_grid.add_widget(btn)
        
        scroll.add_widget(button_grid)
        layout.add_widget(scroll)
        
        # Botón de apagado
        btn_shutdown = Button(text="Apagar Sistema",
                             size_hint_y=0.1,
                             background_color=(0.8, 0.2, 0.2, 1))
        btn_shutdown.bind(on_press=self.shutdown_system)
        layout.add_widget(btn_shutdown)
        
        self.add_widget(layout)
    
    # ===== CALLBACKS DE LED =====
    def init_led(self, instance):
        result = system_controller.init_led()
        self.show_message("LED Inicializado" if result else "Error al inicializar LED")
    
    def change_led_color(self, instance):
        colors = [color.name for color in LEDColor]
        popup = SelectionPopup(
            title="Seleccione color",
            options=colors,
            on_select=self._on_color_selected
        )
        popup.open()
    
    def _on_color_selected(self, color):
        result = system_controller.set_led_color(color)
        self.show_message(f"Color {color} establecido" if result else "Error")
    
    def turn_off_led(self, instance):
        result = system_controller.set_led_color("BLACK")
        self.show_message("LED apagado" if result else "Error")
    
    # ===== CALLBACKS DE DISPLAY =====
    def init_display(self, instance):
        result = system_controller.init_display()
        self.show_message("Display inicializado" if result else "Error")
    
    def show_number(self, instance):
        popup = InputPopup(
            title="Ingrese número",
            label_text="Digite un número del 0 al 9:",
            input_type='int',
            on_submit=self._on_number_entered
        )
        popup.open()
    
    def _on_number_entered(self, number):
        try:
            num = int(number)
            result = system_controller.display_number(num)
            self.show_message(f"Mostrando {num}" if result else "Número inválido")
        except ValueError:
            self.show_message("Ingrese un número válido")
    
    def clear_display(self, instance):
        result = system_controller.clear_display()
        self.show_message("Display limpiado" if result else "Error")
    
    # ===== CALLBACKS DE SENSOR =====
    def init_sensor(self, instance):
        result = system_controller.init_sensor()
        self.show_message("Sensor inicializado" if result else "Error")
    
    def read_temperature(self, instance):
        temp = system_controller.read_temperature()
        self.show_message(f"Temperatura: {temp:.2f}°C")
    
    def calibrate_sensor(self, instance):
        popup = InputPopup(
            title="Calibrar Sensor",
            label_text="Ingrese offset de calibración:",
            input_type='int',
            on_submit=self._on_calibration_offset
        )
        popup.open()
    
    def _on_calibration_offset(self, offset):
        try:
            off = int(offset)
            result = system_controller.calibrate_sensor(off)
            self.show_message("Sensor calibrado" if result else "Error")
        except ValueError:
            self.show_message("Ingrese un valor válido")
    
    # ===== CALLBACKS DE COMUNICACIÓN =====
    def init_communication(self, instance):
        baud_options = ['9600', '19200', '38400', '115200']
        popup = SelectionPopup(
            title="Seleccione velocidad",
            options=baud_options,
            on_select=self._on_baud_selected
        )
        popup.open()
    
    def _on_baud_selected(self, baud):
        result = system_controller.init_communication(baud_rate=baud)
        self.show_message(f"Comunicación a {baud} bps" if result else "Error")
    
    def send_message(self, instance):
        popup = InputPopup(
            title="Enviar Mensaje",
            label_text="Digite el mensaje:",
            on_submit=self._on_message_sent
        )
        popup.open()
    
    def _on_message_sent(self, message):
        result = system_controller.send_message(message)
        self.show_message(f"Enviado: {message}" if result else "Error")
    
    # ===== OTROS =====
    def view_status(self, instance):
        status = system_controller.get_system_status()
        message = self._format_status(status)
        popup_content = Label(text=message, markup=True)
        p = Popup(title="Estado del Sistema", content=popup_content, size_hint=(0.9, 0.9))
        p.open()
    
    def _format_status(self, status) -> str:
        text = "[b]ESTADO DEL SISTEMA[/b]\n\n"
        for key, value in status.items():
            if value is not None:
                text += f"[b]{key}:[/b] {str(value)}\n"
        return text
    
    def shutdown_system(self, instance):
        popup = ConfirmationPopup(
            title="Apagar Sistema",
            message="¿Desea apagar el sistema completamente?",
            on_confirm=self._confirm_shutdown
        )
        popup.open()
    
    def _confirm_shutdown(self):
        system_controller.shutdown_all()
        self.show_message("Sistema apagado")
    
    def show_message(self, message):
        """Muestra un mensaje temporal."""
        label = Label(text=message)
        popup = Popup(title="Información", content=label, size_hint=(0.7, 0.3))
        popup.open()
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)


class SystemApp(App):
    """Aplicación principal."""
    
    def build(self):
        self.title = "Sistema de Control - Arquitectura en Capas"
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm


if __name__ == '__main__':
    SystemApp().run()
