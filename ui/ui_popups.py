"""POPUPS REUTILIZABLES PARA LA INTERFAZ KIVY"""

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock


class ConfirmationPopup(Popup):
    """Popup de confirmación con botones Sí/No."""
    
    def __init__(self, title: str = "Confirmación", message: str = "", 
                 on_confirm=None, on_cancel=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (0.7, 0.4)
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        label = Label(text=message, size_hint_y=0.6)
        layout.add_widget(label)
        
        button_layout = BoxLayout(size_hint_y=0.4, spacing=10)
        
        btn_yes = Button(text='Sí')
        btn_yes.bind(on_press=self._on_confirm)
        button_layout.add_widget(btn_yes)
        
        btn_no = Button(text='No')
        btn_no.bind(on_press=self._on_cancel)
        button_layout.add_widget(btn_no)
        
        layout.add_widget(button_layout)
        self.add_widget(layout)
    
    def _on_confirm(self, instance):
        if self.on_confirm:
            self.on_confirm()
        self.dismiss()
    
    def _on_cancel(self, instance):
        if self.on_cancel:
            self.on_cancel()
        self.dismiss()


class InputPopup(Popup):
    """Popup para ingreso de texto."""
    
    def __init__(self, title: str = "Ingreso", label_text: str = "", 
                 input_type: str = 'text', on_submit=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (0.8, 0.5)
        self.on_submit = on_submit
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        label = Label(text=label_text, size_hint_y=0.3)
        layout.add_widget(label)
        
        self.text_input = TextInput(multiline=False, size_hint_y=0.4)
        self.text_input.input_filter = input_type
        layout.add_widget(self.text_input)
        
        button_layout = BoxLayout(size_hint_y=0.3, spacing=10)
        
        btn_accept = Button(text='Aceptar')
        btn_accept.bind(on_press=self._on_submit)
        button_layout.add_widget(btn_accept)
        
        btn_cancel = Button(text='Cancelar')
        btn_cancel.bind(on_press=self.dismiss)
        button_layout.add_widget(btn_cancel)
        
        layout.add_widget(button_layout)
        self.add_widget(layout)
    
    def _on_submit(self, instance):
        if self.on_submit:
            self.on_submit(self.text_input.text)
        self.dismiss()


class SelectionPopup(Popup):
    """Popup para selección de opciones."""
    
    def __init__(self, title: str = "Seleccione", options: list = None, 
                 on_select=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (0.7, 0.5)
        self.on_select = on_select
        self.options = options or []
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.spinner = Spinner(text=self.options[0] if self.options else "Seleccione",
                              values=self.options,
                              size_hint_y=0.6)
        layout.add_widget(self.spinner)
        
        button_layout = BoxLayout(size_hint_y=0.4, spacing=10)
        
        btn_accept = Button(text='Aceptar')
        btn_accept.bind(on_press=self._on_select)
        button_layout.add_widget(btn_accept)
        
        btn_cancel = Button(text='Cancelar')
        btn_cancel.bind(on_press=self.dismiss)
        button_layout.add_widget(btn_cancel)
        
        layout.add_widget(button_layout)
        self.add_widget(layout)
    
    def _on_select(self, instance):
        if self.on_select:
            self.on_select(self.spinner.text)
        self.dismiss()


class ProgressPopup(Popup):
    """Popup con barra de progreso."""
    
    def __init__(self, title: str = "Procesando", duration: float = 5.0, 
                 on_complete=None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (0.8, 0.4)
        self.on_complete = on_complete
        self.duration = duration
        self.auto_dismiss = False
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.label = Label(text=f"Procesando... 0%", size_hint_y=0.4)
        layout.add_widget(self.label)
        
        self.progress_bar = ProgressBar(max=100, value=0, size_hint_y=0.3)
        layout.add_widget(self.progress_bar)
        
        self.add_widget(layout)
        
        # Inicia el progreso
        self.start_time = Clock.get_time()
        self.event = Clock.schedule_interval(self._update_progress, 0.05)
    
    def _update_progress(self, dt):
        elapsed = Clock.get_time() - self.start_time
        progress = min(100, (elapsed / self.duration) * 100)
        self.progress_bar.value = progress
        self.label.text = f"Procesando... {int(progress)}%"
        
        if progress >= 100:
            Clock.unschedule(self.event)
            if self.on_complete:
                self.on_complete()
            self.dismiss()
