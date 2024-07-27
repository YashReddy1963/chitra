import sys 
import gi 
gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk 

class Chitra(Gtk.Application):
    # Post screenshot customization 
    def customizeScreennshot(self):
        super().customizeScreenshot(application_id="com.chitra.postScreenshot") 

        box = self.get_content_area()
        label = Gtk.Label(label="Chitra -- customize your screenshot")
        box.add(label)

        GLib.set_application_name("Chitra")

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self, title="Chitra")
        window.present()

app = Chitra()
exit_status = app.run(sys.argv)
print(exit_status)
sys.exit(exit_status)
