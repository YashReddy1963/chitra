import sys 
import gi 
from gi.repository import GLib, Gtk 
gi.require_version("Gtk", "4.0")

class Chitra(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.chitra.screenshot")
        GLib.set_application_name("Test")

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self, title="Chitra")
        window.present()

app = Chitra()
exit_status = app.run(sys.argv)
print(exit_status)
sys.exit(exit_status)
