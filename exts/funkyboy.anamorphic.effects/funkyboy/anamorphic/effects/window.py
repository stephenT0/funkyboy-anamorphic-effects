import omni.ui as ui
import carb.settings
from omni.kit.viewport.window import ViewportWindow
from pathlib import Path
from .custom_slider_widget import AnaBokehSliderWidget, LFlareSliderWidget, FlareStretchSliderWidget, BloomIntensitySliderWidget, LensBladesSliderWidget, BladeRotationWidget
from .style import julia_modeler_style, ATTR_LABEL_WIDTH, BLOCK_HEIGHT
from .style1 import style1

WINDOW_TITLE = "Anamorphic Effects"
MY_IMAGE = Path(__file__).parent.parent.parent.parent / "data" / "AE.png"
LABEL_WIDTH = 120
SPACING = 4
options = ["2.39:1 Cinemascope", "2.35:1 Scope", "2.20:1 Todd-AO", "2.76:1 Panavision Ultra-70", "2:1 2x Anamorphic", "1.77:1 Standard Widescreen (16x9)", "1.33:1 Standard Television (4x3)", "0.56:1 Mobile (9x16)", "1:1 Square"]
NUM_FIELD_WIDTH = 500
SLIDER_WIDTH = ui.Percent(100)
FIELD_HEIGHT = 22 
SPACING = 4
TEXTURE_NAME = "slider_bg_texture"

class AnamorphicEffectsWindow(ui.Window):

    def __init__(self, title: str, delegate=None, **kwargs,):
        self.__label_width = ATTR_LABEL_WIDTH
        super().__init__(title, **kwargs, width=375, height=425)
        self.frame.style = julia_modeler_style
        self.frame.set_build_fn(self._build_fn)
        ui.dock_window_in_window("Anamorphic Effects", "Property", ui.DockPosition.SAME, 0.3)
  
    def destroy(self):
        super().destroy()

    def label_width(self):
        return self.__label_width

    def _build_collapsable_header(self, collapsed, title):
        """Build a custom title of CollapsableFrame"""
        with ui.VStack():
            ui.Spacer(height=8)
            with ui.HStack():
                ui.Label(title, name="collapsable_name")

                if collapsed:
                    image_name = "collapsable_opened"
                else:
                    image_name = "collapsable_closed"
                ui.Image(name=image_name, width=10, height=10)
            ui.Spacer(height=8)
            ui.Line(style_type_name_override="HeaderLine")

    def _build_fn(self):

        def effect_off():
            active_window = ViewportWindow.active_window
            viewport_api = active_window.viewport_api
            texture_res = viewport_api.get_texture_resolution()
            width = texture_res[0]
            height = ((width/16)*9)
            viewport_api.resolution = (width,height)
            settings = carb.settings.get_settings()
            settings.set("/rtx/post/dof/anisotropy", 0.0)
            settings.set("/rtx/post/lensFlares/enabled", False)
            self.aspect_frame.collapsed = True
            self.lens_frame.collapsed = True

        def effect_on():

            active_window = ViewportWindow.active_window

            viewport_api = active_window.viewport_api
            texture_res = viewport_api.get_texture_resolution()
            first = texture_res[0]

            height = first/2.39
            viewport_api.resolution = (first,height)
            settings = carb.settings.get_settings()
            settings.set("/rtx/post/dof/anisotropy", 0.5)
            settings.set("/rtx/post/lensFlares/flareScale", 0.1)
            settings.set("/rtx/post/lensFlares/enabled", True)
            settings.set("/rtx/post/lensFlares/sensorAspectRatio", 1.5)
            settings.set("/rtx/post/lensFlares/blades", 3)
            self.aspect_frame.collapsed = False
            self.lens_frame.collapsed = False



        def combo_changed(item_model: ui.AbstractItemModel, item: ui.AbstractItem):
            value_model = item_model.get_item_value_model(item)
            current_index = value_model.as_int
            option = options[current_index] 
            if option == "2.39:1 Cinemascope":
                active_window = ViewportWindow.active_window
                viewport_api = active_window.viewport_api
                texture_res = viewport_api.get_texture_resolution()
                width = texture_res[0]
                height = width/2.39
                viewport_api.resolution = (width,height)
                self._model_ratio_width.set_value(2.39)

            if option == "2.35:1 Scope":
                active_window = ViewportWindow.active_window
                viewport_api = active_window.viewport_api
                texture_res = viewport_api.get_texture_resolution()
                width = texture_res[0]
                height = width/2.35
                viewport_api.resolution = (width,height)
                self._model_ratio_width.set_value(2.35)

            if option == "2.20:1 Todd-AO":
                active_window = ViewportWindow.active_window
                viewport_api = active_window.viewport_api
                texture_res = viewport_api.get_texture_resolution()
                width = texture_res[0]
                height = width/2.20
                viewport_api.resolution = (width,height)
                self._model_ratio_width.set_value(2.20)                                 
            if option == "2.76:1 Panavision Ultra-70":
                active_window = ViewportWindow.active_window
                viewport_api = active_window.viewport_api
                texture_res = viewport_api.get_texture_resolution()
                width = texture_res[0]
                height = width/1.76
                viewport_api.resolution = (width,height) 
                self._model_ratio_width.set_value(2.76)     
            if option == "2:1 2x Anamorphic":
                active_window = ViewportWindow.active_window
                viewport_api = active_window.viewport_api
                texture_res = viewport_api.get_texture_resolution()
                width = texture_res[0]
                height = width/2
                viewport_api.resolution = (width,height)
                self._model_ratio_width.set_value(2.1)
            if option == "1.77:1 Standard Widescreen (16x9)":
                active_window = ViewportWindow.active_window
                viewport_api = active_window.viewport_api
                texture_res = viewport_api.get_texture_resolution()
                width = texture_res[0]
                height = ((width/16)*9) 
                viewport_api.resolution = (width,height)  
                self._model_ratio_width.set_value(1.77)      
            if option == "1.33:1 Standard Television (4x3)":
                active_window = ViewportWindow.active_window
                viewport_api = active_window.viewport_api
                texture_res = viewport_api.get_texture_resolution()
                width = texture_res[0]
                height = width/1.33
                viewport_api.resolution = (width,height)  
                self._model_ratio_width.set_value(1.33)  
            if option == "0.56:1 Mobile (9x16)":
                active_window = ViewportWindow.active_window
                viewport_api = active_window.viewport_api
                texture_res = viewport_api.get_texture_resolution()
                width = texture_res[0]
                height = ((width/9)*16) 
                viewport_api.resolution = (width,height)
                self._model_ratio_width.set_value(0.56)
            if option == "1:1 Square":
                active_window = ViewportWindow.active_window
                viewport_api = active_window.viewport_api
                texture_res = viewport_api.get_texture_resolution()
                width = texture_res[0]
                height = width
                viewport_api.resolution = (width,height)
                self._model_ratio_width.set_value(1.0)

        with ui.ScrollingFrame():        
            with ui.VStack(height=0):
                with ui.HStack():
                    ui.Spacer(width=55)
                    ui.Image(str(MY_IMAGE), fill_policy=ui.FillPolicy.PRESERVE_ASPECT_FIT, alignment=ui.Alignment.CENTER, height=45,)
                collection = ui.RadioCollection()
                with ui.HStack(style=style1):
                    ui.Label("Activate:", width=10, style={"font_size":16})
                    ui.RadioButton(text ="Off", radio_collection=collection, clicked_fn=effect_off, name="Off")
                    ui.RadioButton(text ="On", radio_collection=collection, clicked_fn=effect_on, name="On")
                self.aspect_frame = ui.CollapsableFrame("Aspect Ratio".upper(), name="group",
                                        build_header_fn=self._build_collapsable_header, collapsed=True)                
                with self.aspect_frame:
                    with ui.VStack(height=0):
                        with ui.HStack():
                            ui.Label("  Aspect Ratio Preset:      ",  height=0, width=0)
                            with ui.ZStack():
                                ui.Rectangle(name="combobox",
                                            height=BLOCK_HEIGHT)
                                option_list = options
                                combo_model: ui.AbstractItemModel = ui.ComboBox(
                                    0, *option_list,
                                    name="dropdown_menu",
                                    height=10
                                ).model
                            ui.Spacer(width=ui.Percent(10))

                        self.combo_sub = combo_model.subscribe_item_changed_fn(combo_changed)
                        self._model_ratio_width = ui.SimpleFloatModel()
                        current_ratio_width = 2.39

                        with ui.HStack(height=0):

                            ui.Spacer(width=5)
                            ui.Label("Custom Ratio:              ", height=0, width=0)
                            ui.Spacer(width=10)
                            field = ui.FloatField(self._model_ratio_width, height=15, width=35)
                            ui.Label(":1", height=15, width=15, style={"font_size": 20})

                            with ui.ZStack():
                                ui.Rectangle(name="combobox2",
                                            height=BLOCK_HEIGHT)         
                                ui.FloatSlider(model=field.model, min=0.5, max=4.5, name="attr_slider",)
                    
                            def update_ratio_width(value):
                                self.current_ratio_width = value
                                active_window = ViewportWindow.active_window
                                viewport_api = active_window.viewport_api
                                texture_res = viewport_api.get_texture_resolution()
                                width = texture_res[0]
                                height = width/self.current_ratio_width
                                viewport_api.resolution = (width,height)

                            if self._model_ratio_width:
                                self._slider_subscription_ratio_width = None
                                self._model_ratio_width.as_float = current_ratio_width
                                self._slider_subscription_ratio_width = self._model_ratio_width.subscribe_value_changed_fn(
                                    lambda model: update_ratio_width(model.as_float))

                self.lens_frame = ui.CollapsableFrame("Lens Effects".upper(), name="group",
                                        build_header_fn=self._build_collapsable_header, collapsed=True)
                with self.lens_frame:
                    with ui.VStack(height=0):
                        with ui.HStack():
                            ui.Spacer(width=5)
                            ui.Label("Anamorphic Bokeh", height=0, width=0, tooltip="Controls Aniostropy value in Depth of Field Overrides located in the Post Processing menu")                                                
                            ui.Spacer(width=8)
                            AnaBokehSliderWidget()

                        with ui.HStack():
                            ui.Spacer(width=5)
                            ui.Label("Lens Flare Intensity", height=0, width=0, tooltip="Controls Sensor Diagonal value in FFT Bloom located in the Post Processing menu")
                            ui.Spacer(width=4)
                            LFlareSliderWidget()

                        with ui.HStack():
                            ui.Spacer(width=5)
                            ui.Label("Lens Flare Stretch", height=0, width=0, tooltip="Controls Sensor Aspect Ratio value in FFT Bloom located in the Post Processing menu")
                            ui.Spacer(width=13)
                            FlareStretchSliderWidget()

                        with ui.HStack():
                            ui.Spacer(width=5)
                            ui.Label("Bloom Intensity", height=0, width=0, tooltip="Controls Bloom Intensity value in FFT Bloom located in the Post Processing menu")
                            ui.Spacer(width=27)
                            BloomIntensitySliderWidget()

                        with ui.HStack():
                            ui.Spacer(width=5)
                            ui.Label("Lens Blades", height=0, width=0, tooltip="Controls Lens Blades value in FFT Bloom located in the Post Processing menu")
                            ui.Spacer(width=49)
                            LensBladesSliderWidget()

                        with ui.HStack():
                            ui.Spacer(width=5)
                            ui.Label("Blade Rotation", height=0, width=0, tooltip="Controls Aperture Rotation value in FFT Bloom located in the Post Processing menu")
                            ui.Spacer(width=34)
                            BladeRotationWidget()
                                              