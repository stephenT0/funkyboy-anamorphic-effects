import omni.ext
import omni.ui as ui
from .window import AnamorphicEffectsWindow, WINDOW_TITLE

class FunkyboyAnamorphicEffectsExtension(omni.ext.IExt):
    def on_startup(self, ext_id): 
        self._menu_path = f"Window/{WINDOW_TITLE}"
        self._window = AnamorphicEffectsWindow(WINDOW_TITLE, self._menu_path)
        self._menu = omni.kit.ui.get_editor_menu().add_item(self._menu_path, self._on_menu_click, True)


    def on_shutdown(self):
        omni.kit.ui.get_editor_menu().remove_item(self._menu)
        if self._window is not None:
            self._window.destroy()
            self._window = None


    def _on_menu_click(self, menu, toggled):
        if toggled:
            if self._window is None:
                self._window = AnamorphicEffectsWindow(WINDOW_TITLE, self._menu_path)
            else:
                self._window.show()
        else:
            if self._window is not None:
                self._window.hide()

