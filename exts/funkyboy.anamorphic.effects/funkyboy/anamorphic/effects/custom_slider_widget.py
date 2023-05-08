# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
#
__all__ = ["CustomSliderWidget"]

from typing import Optional
import carb.settings
from omni.kit.viewport.window import ViewportWindow
import omni.ui as ui
from omni.ui import color as cl
from omni.ui import constant as fl
from .custom_base_widget import CustomBaseWidget

NUM_FIELD_WIDTH = 500
SLIDER_WIDTH = ui.Percent(100)
FIELD_HEIGHT = 22  # TODO: Once Field padding is fixed, this should be 18
SPACING = 4
TEXTURE_NAME = "slider_bg_texture"

class CustomSliderWidget(CustomBaseWidget):
    """A compound widget for scalar slider input, which contains a
    Slider and a Field with text input next to it.
    """

    def __init__(self,
                 model: ui.AbstractItemModel = None,
                 num_type: str = "float",
                 min=0.0,
                 max=1.0,
                 default_val=0.0,
                 display_range: bool = False,
                 **kwargs):
        self.__slider: Optional[ui.AbstractSlider] = None
        self.__numberfield: Optional[ui.AbstractField] = None
        self.__min = min
        self.__max = max
        self.__default_val = default_val
        self.__num_type = num_type
        self.__display_range = display_range

        # Call at the end, rather than start, so build_fn runs after all the init stuff
        CustomBaseWidget.__init__(self, model=model, **kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__slider = None
        self.__numberfield = None

    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        """The widget's model"""
        if self.__slider:
            return self.__slider.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """The widget's model"""
        self.__slider.model = value
        self.__numberfield.model = value

    def _on_value_changed(self, *args):
        """Set revert_img to correct state."""
        if self.__num_type == "float":
            index = self.model.as_float
        else:
            index = self.model.as_int
        self.revert_img.enabled = self.__default_val != index

    def _restore_default(self):
        """Restore the default value."""
        if self.revert_img.enabled:
            self.model.set_value(self.__default_val)
            self.revert_img.enabled = False

    def _build_display_range(self):
        """Builds just the tiny text range under the slider."""
        with ui.HStack():
            ui.Label(str(self.__min), alignment=ui.Alignment.LEFT, name="range_text")
            if self.__min < 0 and self.__max > 0:
                # Add middle value (always 0), but it may or may not be centered,
                # depending on the min/max values.
                total_range = self.__max - self.__min
                # subtract 25% to account for end number widths
                left = 100 * abs(0 - self.__min) / total_range - 25
                right = 100 * abs(self.__max - 0) / total_range - 25
                ui.Spacer(width=ui.Percent(left))
                ui.Label("0", alignment=ui.Alignment.CENTER, name="range_text")
                ui.Spacer(width=ui.Percent(right))
            else:
                ui.Spacer()
            ui.Label(str(self.__max), alignment=ui.Alignment.RIGHT, name="range_text")
        ui.Spacer(height=.75)

    def _build_body(self):
        """Main meat of the widget.  Draw the Slider, display range text, Field,
        and set up callbacks to keep them updated.
        """
        with ui.HStack(spacing=0):
            # the user provided a list of default values
            with ui.VStack(spacing=3, width=ui.Fraction(3)):
                with ui.ZStack():
                    # Put texture image here, with rounded corners, then make slider
                    # bg be fully transparent, and fg be gray and partially transparent
                    with ui.Frame(width=SLIDER_WIDTH, height=FIELD_HEIGHT,
                                  horizontal_clipping=True):
                        # Spacing is negative because "tileable" texture wasn't
                        # perfectly tileable, so that adds some overlap to line up better.
                        with ui.HStack(spacing=-12):
                            for i in range(50):  # tiling the texture
                                ui.Image(name=TEXTURE_NAME,
                                         fill_policy=ui.FillPolicy.PRESERVE_ASPECT_CROP,
                                         width=50,)

                    slider_cls = (
                        ui.FloatSlider if self.__num_type == "float" else ui.IntSlider
                    )
                    self.__slider = slider_cls(
                        height=FIELD_HEIGHT,
                        min=self.__min, max=self.__max, name="attr_slider"
                    )

                if self.__display_range:
                    self._build_display_range()

            with ui.VStack(width=ui.Fraction(1)):
                model = self.__slider.model
                model.set_value(self.__default_val)
                field_cls = (
                    ui.FloatField if self.__num_type == "float" else ui.IntField
                )

                # Note: This is a hack to allow for text to fill the Field space more, as there was a bug
                # with Field padding.  It is fixed, and will be available in the next release of Kit.
                with ui.ZStack():
                    # height=FIELD_HEIGHT-1 to account for the border, so the field isn't
                    # slightly taller than the slider
                    ui.Rectangle(
                        style_type_name_override="Field",
                        name="attr_field",
                        height=FIELD_HEIGHT - 1
                    )
                    with ui.HStack(height=0):
                        ui.Spacer(width=2)
                        self.__numberfield = field_cls(
                            model,
                            height=0,
                            style={
                                "background_color": cl.transparent,
                                "border_color": cl.transparent,
                                "padding": 4,
                                "font_size": fl.field_text_font_size,
                            },
                        )
                if self.__display_range:
                    ui.Spacer()

        model.add_value_changed_fn(self._on_value_changed)

class AnaBokehSliderWidget(CustomBaseWidget):
    """A compound widget for scalar slider input, which contains a
    Slider and a Field with text input next to it.
    """

    def __init__(self,
                 model: ui.AbstractItemModel = None,
                 num_type: str = "float",
                 min=0.0,
                 max=1.0,
                 default_val=0.5,
                 display_range: bool = False,
                 **kwargs):
        self.__slider: Optional[ui.AbstractSlider] = None
        self.__numberfield: Optional[ui.AbstractField] = None
        self.__min = min
        self.__max = max
        self.__default_val = default_val
        self.__num_type = num_type
        self.__display_range = display_range

        # Call at the end, rather than start, so build_fn runs after all the init stuff
        CustomBaseWidget.__init__(self, model=model, **kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__slider = None
        self.__numberfield = None

    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        """The widget's model"""
        if self.__slider:
            return self.__slider.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """The widget's model"""
        self.__slider.model = value
        self.__numberfield.model = value

    def _on_value_changed(self, *args):
        """Set revert_img to correct state."""
        if self.__num_type == "float":
            index = self.model.as_float
        else:
            index = self.model.as_int
        self.revert_img.enabled = self.__default_val != index

    def _restore_default(self):
        """Restore the default value."""
        if self.revert_img.enabled:
            self.model.set_value(self.__default_val)
            self.revert_img.enabled = False

    def _build_display_range(self):
        """Builds just the tiny text range under the slider."""
        with ui.HStack():
            ui.Label(str(self.__min), alignment=ui.Alignment.LEFT, name="range_text")
            if self.__min < 0 and self.__max > 0:
                # Add middle value (always 0), but it may or may not be centered,
                # depending on the min/max values.
                total_range = self.__max - self.__min
                # subtract 25% to account for end number widths
                left = 100 * abs(0 - self.__min) / total_range - 25
                right = 100 * abs(self.__max - 0) / total_range - 25
                ui.Spacer(width=ui.Percent(left))
                ui.Label("0", alignment=ui.Alignment.CENTER, name="range_text")
                ui.Spacer(width=ui.Percent(right))
            else:
                ui.Spacer()
            ui.Label(str(self.__max), alignment=ui.Alignment.RIGHT, name="range_text")
        ui.Spacer(height=.75)

    def _build_body(self):
        """Main meat of the widget.  Draw the Slider, display range text, Field,
        and set up callbacks to keep them updated.
        """
        with ui.HStack(spacing=0):
            # the user provided a list of default values
   
            with ui.VStack(spacing=3, width=ui.Fraction(3)):
                self._slider_model_anisotropy = ui.SimpleFloatModel()
                current_anisotropy = 0.5
                with ui.ZStack():
                    # Put texture image here, with rounded corners, then make slider
                    # bg be fully transparent, and fg be gray and partially transparent
                    with ui.Frame(width=SLIDER_WIDTH, height=FIELD_HEIGHT,
                                  horizontal_clipping=True):
                        # Spacing is negative because "tileable" texture wasn't
                        # perfectly tileable, so that adds some overlap to line up better.
                        with ui.HStack(spacing=-12):
                            for i in range(50):  # tiling the texture
                                ui.Image(name=TEXTURE_NAME,
                                         fill_policy=ui.FillPolicy.PRESERVE_ASPECT_CROP,
                                         width=50,)

                    slider_cls = (
                        ui.FloatSlider if self.__num_type == "float" else ui.IntSlider
                    )
                    self.__slider = slider_cls(self._slider_model_anisotropy, min=0.0, max=1.0, height=FIELD_HEIGHT, name="attr_slider")

                if self.__display_range:
                    self._build_display_range()


                def update_anisotropy(value):
                    current_anisotropy = value
                    settings = carb.settings.get_settings()
                    settings.set("/rtx/post/dof/anisotropy", float(current_anisotropy))

                if self._slider_model_anisotropy:
                    self._slider_subscription_anisotropy = None
                    self._slider_model_anisotropy.as_float = current_anisotropy
                    self._slider_subscription_anisotropy = self._slider_model_anisotropy.subscribe_value_changed_fn(
                        lambda model: update_anisotropy(model.as_float))
            with ui.VStack(width=ui.Fraction(1)):
                model = self.__slider.model
                model.set_value(self.__default_val)
                field_cls = (
                    ui.FloatField if self.__num_type == "float" else ui.IntField
                )

                # Note: This is a hack to allow for text to fill the Field space more, as there was a bug
                # with Field padding.  It is fixed, and will be available in the next release of Kit.
                with ui.ZStack():
                    # height=FIELD_HEIGHT-1 to account for the border, so the field isn't
                    # slightly taller than the slider
                    ui.Rectangle(
                        style_type_name_override="Field",
                        name="attr_field",
                        height=FIELD_HEIGHT - 1
                    )
                    with ui.HStack(height=0):
                        ui.Spacer(width=10)
                        self.__numberfield = field_cls(
                            model,
                            height=0,
                            style={
                                "background_color": cl.transparent,
                                "border_color": cl.transparent,
                                "padding": 4,
                                "font_size": fl.field_text_font_size,
                            },
                        )
                if self.__display_range:
                    ui.Spacer()

        model.add_value_changed_fn(self._on_value_changed)

class LFlareSliderWidget(CustomBaseWidget):
    """A compound widget for scalar slider input, which contains a
    Slider and a Field with text input next to it.
    """

    def __init__(self,
                 model: ui.AbstractItemModel = None,
                 num_type: str = "float",
                 min=0.0,
                 max=135.0,
                 default_val=60,
                 display_range: bool = False,
                 **kwargs):
        self.__slider: Optional[ui.AbstractSlider] = None
        self.__numberfield: Optional[ui.AbstractField] = None
        self.__min = min
        self.__max = max
        self.__default_val = default_val
        self.__num_type = num_type
        self.__display_range = display_range

        # Call at the end, rather than start, so build_fn runs after all the init stuff
        CustomBaseWidget.__init__(self, model=model, **kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__slider = None
        self.__numberfield = None

    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        """The widget's model"""
        if self.__slider:
            return self.__slider.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """The widget's model"""
        self.__slider.model = value
        self.__numberfield.model = value

    def _on_value_changed(self, *args):
        """Set revert_img to correct state."""
        if self.__num_type == "float":
            index = self.model.as_float
        else:
            index = self.model.as_int
        self.revert_img.enabled = self.__default_val != index

    def _restore_default(self):
        """Restore the default value."""
        if self.revert_img.enabled:
            self.model.set_value(self.__default_val)
            self.revert_img.enabled = False

    def _build_display_range(self):
        """Builds just the tiny text range under the slider."""
        with ui.HStack():
            ui.Label(str(self.__min), alignment=ui.Alignment.LEFT, name="range_text")
            if self.__min < 0 and self.__max > 0:
                # Add middle value (always 0), but it may or may not be centered,
                # depending on the min/max values.
                total_range = self.__max - self.__min
                # subtract 25% to account for end number widths
                left = 100 * abs(0 - self.__min) / total_range - 25
                right = 100 * abs(self.__max - 0) / total_range - 25
                ui.Spacer(width=ui.Percent(left))
                ui.Label("0", alignment=ui.Alignment.CENTER, name="range_text")
                ui.Spacer(width=ui.Percent(right))
            else:
                ui.Spacer()
            ui.Label(str(self.__max), alignment=ui.Alignment.RIGHT, name="range_text")
        ui.Spacer(height=.75)

    def _build_body(self):
        """Main meat of the widget.  Draw the Slider, display range text, Field,
        and set up callbacks to keep them updated.
        """
        with ui.HStack(spacing=0):
            # the user provided a list of default values
   
            with ui.VStack(spacing=3, width=ui.Fraction(3)):
                self._slider_model_sensor_size = ui.SimpleFloatModel()
                current_sensor_size = 60.0
                with ui.ZStack():
                    # Put texture image here, with rounded corners, then make slider
                    # bg be fully transparent, and fg be gray and partially transparent
                    with ui.Frame(width=SLIDER_WIDTH, height=FIELD_HEIGHT,
                                  horizontal_clipping=True):
                        # Spacing is negative because "tileable" texture wasn't
                        # perfectly tileable, so that adds some overlap to line up better.
                        with ui.HStack(spacing=-12):
                            for i in range(50):  # tiling the texture
                                ui.Image(name=TEXTURE_NAME,
                                         fill_policy=ui.FillPolicy.PRESERVE_ASPECT_CROP,
                                         width=50,)

                    slider_cls = (
                        ui.FloatSlider if self.__num_type == "float" else ui.IntSlider
                    )
                    self.__slider = slider_cls(self._slider_model_sensor_size, min=0.0, max=135.0, height=FIELD_HEIGHT, name="attr_slider")



                if self.__display_range:
                    self._build_display_range()


                def update_sensor_size(value):
                    current_sensor_size = value
                    settings = carb.settings.get_settings()
                    settings.set("/rtx/post/lensFlares/sensorDiagonal", float(current_sensor_size))

                if self._slider_model_sensor_size:
                    self._slider_subscription_sensor_size = None
                    self._slider_model_sensor_size.as_float = current_sensor_size
                    self._slider_subscription_sensor_size = self._slider_model_sensor_size.subscribe_value_changed_fn(
                        lambda model: update_sensor_size(model.as_float))
            with ui.VStack(width=ui.Fraction(1)):
                model = self.__slider.model
                model.set_value(self.__default_val)
                field_cls = (
                    ui.FloatField if self.__num_type == "float" else ui.IntField
                )

                # Note: This is a hack to allow for text to fill the Field space more, as there was a bug
                # with Field padding.  It is fixed, and will be available in the next release of Kit.
                with ui.ZStack():
                    # height=FIELD_HEIGHT-1 to account for the border, so the field isn't
                    # slightly taller than the slider
                    ui.Rectangle(
                        style_type_name_override="Field",
                        name="attr_field",
                        height=FIELD_HEIGHT - 1
                    )
                    with ui.HStack(height=0):
                        ui.Spacer(width=10)
                        self.__numberfield = field_cls(
                            model,
                            height=0,
                            style={
                                "background_color": cl.transparent,
                                "border_color": cl.transparent,
                                "padding": 4,
                                "font_size": fl.field_text_font_size,
                            },
                        )
                if self.__display_range:
                    ui.Spacer()

        model.add_value_changed_fn(self._on_value_changed)

class FlareStretchSliderWidget(CustomBaseWidget):
    """A compound widget for scalar slider input, which contains a
    Slider and a Field with text input next to it.
    """

    def __init__(self,
                 model: ui.AbstractItemModel = None,
                 num_type: str = "float",
                 min=0.01,
                 max=15.0,
                 default_val=1.5,
                 display_range: bool = False,
                 **kwargs):
        self.__slider: Optional[ui.AbstractSlider] = None
        self.__numberfield: Optional[ui.AbstractField] = None
        self.__min = min
        self.__max = max
        self.__default_val = default_val
        self.__num_type = num_type
        self.__display_range = display_range

        # Call at the end, rather than start, so build_fn runs after all the init stuff
        CustomBaseWidget.__init__(self, model=model, **kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__slider = None
        self.__numberfield = None

    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        """The widget's model"""
        if self.__slider:
            return self.__slider.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """The widget's model"""
        self.__slider.model = value
        self.__numberfield.model = value

    def _on_value_changed(self, *args):
        """Set revert_img to correct state."""
        if self.__num_type == "float":
            index = self.model.as_float
        else:
            index = self.model.as_int
        self.revert_img.enabled = self.__default_val != index

    def _restore_default(self):
        """Restore the default value."""
        if self.revert_img.enabled:
            self.model.set_value(self.__default_val)
            self.revert_img.enabled = False

    def _build_display_range(self):
        """Builds just the tiny text range under the slider."""
        with ui.HStack():
            ui.Label(str(self.__min), alignment=ui.Alignment.LEFT, name="range_text")
            if self.__min < 0 and self.__max > 0:
                # Add middle value (always 0), but it may or may not be centered,
                # depending on the min/max values.
                total_range = self.__max - self.__min
                # subtract 25% to account for end number widths
                left = 100 * abs(0 - self.__min) / total_range - 25
                right = 100 * abs(self.__max - 0) / total_range - 25
                ui.Spacer(width=ui.Percent(left))
                ui.Label("0", alignment=ui.Alignment.CENTER, name="range_text")
                ui.Spacer(width=ui.Percent(right))
            else:
                ui.Spacer()
            ui.Label(str(self.__max), alignment=ui.Alignment.RIGHT, name="range_text")
        ui.Spacer(height=.75)

    def _build_body(self):
        """Main meat of the widget.  Draw the Slider, display range text, Field,
        and set up callbacks to keep them updated.
        """
        with ui.HStack(spacing=0):
            # the user provided a list of default values
   
            with ui.VStack(spacing=3, width=ui.Fraction(3)):
                self._slider_model_flare = ui.SimpleFloatModel()
                current_flare = 1.5
                with ui.ZStack():
                    # Put texture image here, with rounded corners, then make slider
                    # bg be fully transparent, and fg be gray and partially transparent
                    with ui.Frame(width=SLIDER_WIDTH, height=FIELD_HEIGHT,
                                  horizontal_clipping=True):
                        # Spacing is negative because "tileable" texture wasn't
                        # perfectly tileable, so that adds some overlap to line up better.
                        with ui.HStack(spacing=-12):
                            for i in range(50):  # tiling the texture
                                ui.Image(name=TEXTURE_NAME,
                                         fill_policy=ui.FillPolicy.PRESERVE_ASPECT_CROP,
                                         width=50,)

                    slider_cls = (
                        ui.FloatSlider if self.__num_type == "float" else ui.IntSlider
                    )
                    self.__slider = slider_cls(self._slider_model_flare, min=0.01, max=15.0, height=FIELD_HEIGHT, name="attr_slider")



                if self.__display_range:
                    self._build_display_range()


                def update_flare(value):
                    current_flare = value
                    settings = carb.settings.get_settings()
                    settings.set("/rtx/post/lensFlares/sensorAspectRatio", float(current_flare))

                if self._slider_model_flare:
                    self._slider_subscription_flare = None
                    self._slider_model_flare.as_float = current_flare
                    self._slider_subscription_flare = self._slider_model_flare.subscribe_value_changed_fn(
                        lambda model: update_flare(model.as_float))
            with ui.VStack(width=ui.Fraction(1)):
                model = self.__slider.model
                model.set_value(self.__default_val)
                field_cls = (
                    ui.FloatField if self.__num_type == "float" else ui.IntField
                )

                # Note: This is a hack to allow for text to fill the Field space more, as there was a bug
                # with Field padding.  It is fixed, and will be available in the next release of Kit.
                with ui.ZStack():
                    # height=FIELD_HEIGHT-1 to account for the border, so the field isn't
                    # slightly taller than the slider
                    ui.Rectangle(
                        style_type_name_override="Field",
                        name="attr_field",
                        height=FIELD_HEIGHT - 1
                    )
                    with ui.HStack(height=0):
                        ui.Spacer(width=10)
                        self.__numberfield = field_cls(
                            model,
                            height=0,
                            style={
                                "background_color": cl.transparent,
                                "border_color": cl.transparent,
                                "padding": 4,
                                "font_size": fl.field_text_font_size,
                            },
                        )
                if self.__display_range:
                    ui.Spacer()

        model.add_value_changed_fn(self._on_value_changed)


class BloomIntensitySliderWidget(CustomBaseWidget):
    """A compound widget for scalar slider input, which contains a
    Slider and a Field with text input next to it.
    """

    def __init__(self,
                 model: ui.AbstractItemModel = None,
                 num_type: str = "float",
                 min=0.0,
                 max=0.5,
                 default_val=0.1,
                 display_range: bool = False,
                 **kwargs):
        self.__slider: Optional[ui.AbstractSlider] = None
        self.__numberfield: Optional[ui.AbstractField] = None
        self.__min = min
        self.__max = max
        self.__default_val = default_val
        self.__num_type = num_type
        self.__display_range = display_range

        # Call at the end, rather than start, so build_fn runs after all the init stuff
        CustomBaseWidget.__init__(self, model=model, **kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__slider = None
        self.__numberfield = None

    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        """The widget's model"""
        if self.__slider:
            return self.__slider.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """The widget's model"""
        self.__slider.model = value
        self.__numberfield.model = value

    def _on_value_changed(self, *args):
        """Set revert_img to correct state."""
        if self.__num_type == "float":
            index = self.model.as_float
        else:
            index = self.model.as_int
        self.revert_img.enabled = self.__default_val != index

    def _restore_default(self):
        """Restore the default value."""
        if self.revert_img.enabled:
            self.model.set_value(self.__default_val)
            self.revert_img.enabled = False

    def _build_display_range(self):
        """Builds just the tiny text range under the slider."""
        with ui.HStack():
            ui.Label(str(self.__min), alignment=ui.Alignment.LEFT, name="range_text")
            if self.__min < 0 and self.__max > 0:
                # Add middle value (always 0), but it may or may not be centered,
                # depending on the min/max values.
                total_range = self.__max - self.__min
                # subtract 25% to account for end number widths
                left = 100 * abs(0 - self.__min) / total_range - 25
                right = 100 * abs(self.__max - 0) / total_range - 25
                ui.Spacer(width=ui.Percent(left))
                ui.Label("0", alignment=ui.Alignment.CENTER, name="range_text")
                ui.Spacer(width=ui.Percent(right))
            else:
                ui.Spacer()
            ui.Label(str(self.__max), alignment=ui.Alignment.RIGHT, name="range_text")
        ui.Spacer(height=.75)

    def _build_body(self):
        """Main meat of the widget.  Draw the Slider, display range text, Field,
        and set up callbacks to keep them updated.
        """
        with ui.HStack(spacing=0):
            # the user provided a list of default values
   
            with ui.VStack(spacing=3, width=ui.Fraction(3)):
                self._slider_model_bloom = ui.SimpleFloatModel()
                current_bloom = 0.1
                with ui.ZStack():
                    # Put texture image here, with rounded corners, then make slider
                    # bg be fully transparent, and fg be gray and partially transparent
                    with ui.Frame(width=SLIDER_WIDTH, height=FIELD_HEIGHT,
                                  horizontal_clipping=True):
                        # Spacing is negative because "tileable" texture wasn't
                        # perfectly tileable, so that adds some overlap to line up better.
                        with ui.HStack(spacing=-12):
                            for i in range(50):  # tiling the texture
                                ui.Image(name=TEXTURE_NAME,
                                         fill_policy=ui.FillPolicy.PRESERVE_ASPECT_CROP,
                                         width=50,)

                    slider_cls = (
                        ui.FloatSlider if self.__num_type == "float" else ui.IntSlider
                    )
                    self.__slider = slider_cls(self._slider_model_bloom, min=0.0, max=0.5, height=FIELD_HEIGHT, name="attr_slider")



                if self.__display_range:
                    self._build_display_range()


                def update_bloom(value):
                    current_bloom = value
                    settings = carb.settings.get_settings()
                    settings.set("/rtx/post/lensFlares/flareScale", float(current_bloom))

                if self._slider_model_bloom:
                    self._slider_subscription_bloom = None
                    self._slider_model_bloom.as_float = current_bloom
                    self._slider_subscription_bloom = self._slider_model_bloom.subscribe_value_changed_fn(
                        lambda model: update_bloom(model.as_float))
            with ui.VStack(width=ui.Fraction(1)):
                model = self.__slider.model
                model.set_value(self.__default_val)
                field_cls = (
                    ui.FloatField if self.__num_type == "float" else ui.IntField
                )

                # Note: This is a hack to allow for text to fill the Field space more, as there was a bug
                # with Field padding.  It is fixed, and will be available in the next release of Kit.
                with ui.ZStack():
                    # height=FIELD_HEIGHT-1 to account for the border, so the field isn't
                    # slightly taller than the slider
                    ui.Rectangle(
                        style_type_name_override="Field",
                        name="attr_field",
                        height=FIELD_HEIGHT - 1
                    )
                    with ui.HStack(height=0):
                        ui.Spacer(width=10)
                        self.__numberfield = field_cls(
                            model,
                            height=0,
                            style={
                                "background_color": cl.transparent,
                                "border_color": cl.transparent,
                                "padding": 4,
                                "font_size": fl.field_text_font_size,
                            },
                        )
                if self.__display_range:
                    ui.Spacer()

        model.add_value_changed_fn(self._on_value_changed)


class LensBladesSliderWidget(CustomBaseWidget):
    """A compound widget for scalar slider input, which contains a
    Slider and a Field with text input next to it.
    """

    def __init__(self,
                 model: ui.AbstractItemModel = None,
                 num_type: str = "float",
                 min=3,
                 max=11,
                 default_val=6,
                 display_range: bool = False,
                 **kwargs):
        self.__slider: Optional[ui.AbstractSlider] = None
        self.__numberfield: Optional[ui.AbstractField] = None
        self.__min = min
        self.__max = max
        self.__default_val = default_val
        self.__num_type = num_type
        self.__display_range = display_range

        # Call at the end, rather than start, so build_fn runs after all the init stuff
        CustomBaseWidget.__init__(self, model=model, **kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__slider = None
        self.__numberfield = None

    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        """The widget's model"""
        if self.__slider:
            return self.__slider.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """The widget's model"""
        self.__slider.model = value
        self.__numberfield.model = value

    def _on_value_changed(self, *args):
        """Set revert_img to correct state."""
        if self.__num_type == "float":
            index = self.model.as_float
        else:
            index = self.model.as_int
        self.revert_img.enabled = self.__default_val != index

    def _restore_default(self):
        """Restore the default value."""
        if self.revert_img.enabled:
            self.model.set_value(self.__default_val)
            self.revert_img.enabled = False

    def _build_display_range(self):
        """Builds just the tiny text range under the slider."""
        with ui.HStack():
            ui.Label(str(self.__min), alignment=ui.Alignment.LEFT, name="range_text")
            if self.__min < 0 and self.__max > 0:
                # Add middle value (always 0), but it may or may not be centered,
                # depending on the min/max values.
                total_range = self.__max - self.__min
                # subtract 25% to account for end number widths
                left = 100 * abs(0 - self.__min) / total_range - 25
                right = 100 * abs(self.__max - 0) / total_range - 25
                ui.Spacer(width=ui.Percent(left))
                ui.Label("0", alignment=ui.Alignment.CENTER, name="range_text")
                ui.Spacer(width=ui.Percent(right))
            else:
                ui.Spacer()
            ui.Label(str(self.__max), alignment=ui.Alignment.RIGHT, name="range_text")
        ui.Spacer(height=.75)

    def _build_body(self):
        """Main meat of the widget.  Draw the Slider, display range text, Field,
        and set up callbacks to keep them updated.
        """
        with ui.HStack(spacing=0):
            # the user provided a list of default values
   
            with ui.VStack(spacing=3, width=ui.Fraction(3)):
                self._slider_model_blades = ui.SimpleIntModel()
                current_blades = 6  
                with ui.ZStack():
                    # Put texture image here, with rounded corners, then make slider
                    # bg be fully transparent, and fg be gray and partially transparent
                    with ui.Frame(width=SLIDER_WIDTH, height=FIELD_HEIGHT,
                                  horizontal_clipping=True):
                        # Spacing is negative because "tileable" texture wasn't
                        # perfectly tileable, so that adds some overlap to line up better.
                        with ui.HStack(spacing=-12):
                            for i in range(50):  # tiling the texture
                                ui.Image(name=TEXTURE_NAME,
                                         fill_policy=ui.FillPolicy.PRESERVE_ASPECT_CROP,
                                         width=50,)

                    slider_cls = (
                        ui.IntSlider if self.__num_type == "float" else ui.IntSlider
                    )
                    self.__slider = slider_cls(self._slider_model_blades, min=3, max=11, height=FIELD_HEIGHT, name="attr_slider")



                if self.__display_range:
                    self._build_display_range()


                def update_blades(value):
                    current_blades = value
                    settings = carb.settings.get_settings()
                    settings.set("/rtx/post/lensFlares/blades", int(current_blades))

                if self._slider_model_blades:
                    self._slider_subscription_blades = None
                    self._slider_model_blades.as_float = current_blades
                    self._slider_subscription_blades = self._slider_model_blades.subscribe_value_changed_fn(
                        lambda model: update_blades(model.as_int))
            with ui.VStack(width=ui.Fraction(1)):
                model = self.__slider.model
                model.set_value(self.__default_val)
                field_cls = (
                    ui.FloatField if self.__num_type == "float" else ui.IntField
                )

                # Note: This is a hack to allow for text to fill the Field space more, as there was a bug
                # with Field padding.  It is fixed, and will be available in the next release of Kit.
                with ui.ZStack():
                    # height=FIELD_HEIGHT-1 to account for the border, so the field isn't
                    # slightly taller than the slider
                    ui.Rectangle(
                        style_type_name_override="Field",
                        name="attr_field",
                        height=FIELD_HEIGHT - 1
                    )
                    with ui.HStack(height=0):
                        ui.Spacer(width=10)
                        self.__numberfield = field_cls(
                            model,
                            height=0,
                            style={
                                "background_color": cl.transparent,
                                "border_color": cl.transparent,
                                "padding": 4,
                                "font_size": fl.field_text_font_size,
                            },
                        )
                if self.__display_range:
                    ui.Spacer()

        model.add_value_changed_fn(self._on_value_changed)

class BladeRotationWidget(CustomBaseWidget):
    """A compound widget for scalar slider input, which contains a
    Slider and a Field with text input next to it.
    """

    def __init__(self,
                 model: ui.AbstractItemModel = None,
                 num_type: str = "float",
                 min=0.0,
                 max=100.0,
                 default_val=50.0,
                 display_range: bool = False,
                 **kwargs):
        self.__slider: Optional[ui.AbstractSlider] = None
        self.__numberfield: Optional[ui.AbstractField] = None
        self.__min = min
        self.__max = max
        self.__default_val = default_val
        self.__num_type = num_type
        self.__display_range = display_range

        # Call at the end, rather than start, so build_fn runs after all the init stuff
        CustomBaseWidget.__init__(self, model=model, **kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__slider = None
        self.__numberfield = None

    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        """The widget's model"""
        if self.__slider:
            return self.__slider.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """The widget's model"""
        self.__slider.model = value
        self.__numberfield.model = value

    def _on_value_changed(self, *args):
        """Set revert_img to correct state."""
        if self.__num_type == "float":
            index = self.model.as_float
        else:
            index = self.model.as_int
        self.revert_img.enabled = self.__default_val != index

    def _restore_default(self):
        """Restore the default value."""
        if self.revert_img.enabled:
            self.model.set_value(self.__default_val)
            self.revert_img.enabled = False

    def _build_display_range(self):
        """Builds just the tiny text range under the slider."""
        with ui.HStack():
            ui.Label(str(self.__min), alignment=ui.Alignment.LEFT, name="range_text")
            if self.__min < 0 and self.__max > 0:
                # Add middle value (always 0), but it may or may not be centered,
                # depending on the min/max values.
                total_range = self.__max - self.__min
                # subtract 25% to account for end number widths
                left = 100 * abs(0 - self.__min) / total_range - 25
                right = 100 * abs(self.__max - 0) / total_range - 25
                ui.Spacer(width=ui.Percent(left))
                ui.Label("0", alignment=ui.Alignment.CENTER, name="range_text")
                ui.Spacer(width=ui.Percent(right))
            else:
                ui.Spacer()
            ui.Label(str(self.__max), alignment=ui.Alignment.RIGHT, name="range_text")
        ui.Spacer(height=.75)

    def _build_body(self):
        """Main meat of the widget.  Draw the Slider, display range text, Field,
        and set up callbacks to keep them updated.
        """
        with ui.HStack(spacing=0):
            # the user provided a list of default values
   
            with ui.VStack(spacing=3, width=ui.Fraction(3)):
                self._slider_model_blade_rotation = ui.SimpleFloatModel()
                current_blade_rotation = 50.0 
                with ui.ZStack():
                    # Put texture image here, with rounded corners, then make slider
                    # bg be fully transparent, and fg be gray and partially transparent
                    with ui.Frame(width=SLIDER_WIDTH, height=FIELD_HEIGHT,
                                  horizontal_clipping=True):
                        # Spacing is negative because "tileable" texture wasn't
                        # perfectly tileable, so that adds some overlap to line up better.
                        with ui.HStack(spacing=-12):
                            for i in range(50):  # tiling the texture
                                ui.Image(name=TEXTURE_NAME,
                                         fill_policy=ui.FillPolicy.PRESERVE_ASPECT_CROP,
                                         width=50,)

                    slider_cls = (
                        ui.FloatSlider if self.__num_type == "float" else ui.IntSlider
                    )
                    self.__slider = slider_cls(self._slider_model_blade_rotation, min=0.0, max=100.0, height=FIELD_HEIGHT, name="attr_slider")



                if self.__display_range:
                    self._build_display_range()

                def update_blade_rotation(value):
                    current_blade_rotation = value
                    settings = carb.settings.get_settings()
                    settings.set("/rtx/post/lensFlares/apertureRotation", float(current_blade_rotation))

                if self._slider_model_blade_rotation:
                    self._slider_subscription_blade_rotation = None
                    self._slider_model_blade_rotation.as_float = current_blade_rotation
                    self._slider_subscription_blade_rotatation = self._slider_model_blade_rotation.subscribe_value_changed_fn(
                        lambda model: update_blade_rotation(model.as_float))

            with ui.VStack(width=ui.Fraction(1)):
                model = self.__slider.model
                model.set_value(self.__default_val)
                field_cls = (
                    ui.FloatField if self.__num_type == "float" else ui.IntField
                )

                # Note: This is a hack to allow for text to fill the Field space more, as there was a bug
                # with Field padding.  It is fixed, and will be available in the next release of Kit.
                with ui.ZStack():
                    # height=FIELD_HEIGHT-1 to account for the border, so the field isn't
                    # slightly taller than the slider
                    ui.Rectangle(
                        style_type_name_override="Field",
                        name="attr_field",
                        height=FIELD_HEIGHT - 1
                    )
                    with ui.HStack(height=0):
                        ui.Spacer(width=10)
                        self.__numberfield = field_cls(
                            model,
                            height=0,
                            style={
                                "background_color": cl.transparent,
                                "border_color": cl.transparent,
                                "padding": 4,
                                "font_size": fl.field_text_font_size,
                            },
                        )
                if self.__display_range:
                    ui.Spacer()

        model.add_value_changed_fn(self._on_value_changed)

class CustomRatioSliderWidget(CustomBaseWidget):
    """A compound widget for scalar slider input, which contains a
    Slider and a Field with text input next to it.
    """

    def __init__(self,
                 model: ui.AbstractItemModel = None,
                 num_type: str = "float",
                 min=0.5,
                 max=4.5,
                 default_val=2.39,
                 display_range: bool = False,
                 **kwargs):
        self.__slider: Optional[ui.AbstractSlider] = None
        self.__numberfield: Optional[ui.AbstractField] = None
        self.__min = min
        self.__max = max
        self.__default_val = default_val
        self.__num_type = num_type
        self.__display_range = display_range

        # Call at the end, rather than start, so build_fn runs after all the init stuff
        CustomBaseWidget.__init__(self, model=model, **kwargs)

    def destroy(self):
        CustomBaseWidget.destroy()
        self.__slider = None
        self.__numberfield = None

    @property
    def model(self) -> Optional[ui.AbstractItemModel]:
        """The widget's model"""
        if self.__slider:
            return self.__slider.model

    @model.setter
    def model(self, value: ui.AbstractItemModel):
        """The widget's model"""
        self.__slider.model = value
        self.__numberfield.model = value

    def _on_value_changed(self, *args):
        """Set revert_img to correct state."""
        if self.__num_type == "float":
            index = self.model.as_float
        else:
            index = self.model.as_int
        self.revert_img.enabled = self.__default_val != index

    def _restore_default(self):
        """Restore the default value."""
        if self.revert_img.enabled:
            self.model.set_value(self.__default_val)
            self.revert_img.enabled = False

    def _build_display_range(self):
        """Builds just the tiny text range under the slider."""
        with ui.HStack():
            ui.Label(str(self.__min), alignment=ui.Alignment.LEFT, name="range_text")
            if self.__min < 0 and self.__max > 0:
                # Add middle value (always 0), but it may or may not be centered,
                # depending on the min/max values.
                total_range = self.__max - self.__min
                # subtract 25% to account for end number widths
                left = 100 * abs(0 - self.__min) / total_range - 25
                right = 100 * abs(self.__max - 0) / total_range - 25
                ui.Spacer(width=ui.Percent(left))
                ui.Label("0", alignment=ui.Alignment.CENTER, name="range_text")
                ui.Spacer(width=ui.Percent(right))
            else:
                ui.Spacer()
            ui.Label(str(self.__max), alignment=ui.Alignment.RIGHT, name="range_text")
        ui.Spacer(height=.75)

    def _build_body(self):
        """Main meat of the widget.  Draw the Slider, display range text, Field,
        and set up callbacks to keep them updated.
        """
        with ui.HStack(spacing=0):
            
            
            # the user provided a list of default values
   
            with ui.VStack(spacing=3, width=ui.Fraction(3)):
                self._model_ratio_width = ui.SimpleFloatModel()
                current_ratio_width = 2.39
                
                
                with ui.ZStack():
                    field = ui.FloatField(self._model_ratio_width, height=15, width=35)
                    # Put texture image here, with rounded corners, then make slider
                    # bg be fully transparent, and fg be gray and partially transparent
                    with ui.Frame(width=SLIDER_WIDTH, height=FIELD_HEIGHT,
                                  horizontal_clipping=True):
                        # Spacing is negative because "tileable" texture wasn't
                        # perfectly tileable, so that adds some overlap to line up better.
                        with ui.HStack(spacing=-12):
                            
                            for i in range(5):  # tiling the texture
                                ui.Image(name=TEXTURE_NAME,
                                         fill_policy=ui.FillPolicy.PRESERVE_ASPECT_CROP,
                                         width=50,)

                    slider_cls = (
                        ui.FloatSlider if self.__num_type == "float" else ui.IntSlider
                    )
                    self.__slider = slider_cls(model=field.model, min=0.5, max=4.5, name="attr_slider")



                if self.__display_range:
                    self._build_display_range()

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

            with ui.VStack(width=ui.Fraction(1)):
                model = self.__slider.model
                model.set_value(self.__default_val)
                field_cls = (
                    ui.FloatField if self.__num_type == "float" else ui.IntField
                )

                # Note: This is a hack to allow for text to fill the Field space more, as there was a bug
                # with Field padding.  It is fixed, and will be available in the next release of Kit.
                with ui.ZStack():
                    # height=FIELD_HEIGHT-1 to account for the border, so the field isn't
                    # slightly taller than the slider
                    ui.Rectangle(
                        style_type_name_override="Field",
                        name="attr_field",
                        height=FIELD_HEIGHT - 1
                    )
                    with ui.HStack(height=0):
                        ui.Spacer(width=10)
                        self.__numberfield = field_cls(
                            model,
                            height=0,
                            style={
                                "background_color": cl.transparent,
                                "border_color": cl.transparent,
                                "padding": 4,
                                "font_size": fl.field_text_font_size,
                            },
                        )
                if self.__display_range:
                    ui.Spacer()

        model.add_value_changed_fn(self._on_value_changed)