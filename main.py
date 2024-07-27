import sys 
import gi 
gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk

class Chitra(Gtk.Application):
    # Post screenshot customization 
    def customizeScreenshot(self):
        super().customizeScreenshot(title="CHitra") 

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "Chitra - customize your screenshot"
        self.set_titlebar(header_bar)
        self.set_default_size(500, 400)

        # Textview 
        self.text_buffer = Gtk.TextBuffer()
        self.textView = Gtk.TextView(buffer=self.text_buffer)
        self.textView.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_buffer = self.textview.get_buffer()
        self.entry = Gtk.Entry("Chitra")
        self.entry.set_text("Chitra")


        GLib.set_application_name("Chitra")

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self, title="Chitra")
                # Adding a label heading to the app
        label = Gtk.Label(label="Chitra", xalign=20, yalign=20)
        label.set_markup("<span font='20' weight='bold'>Chitra</span> ") 

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=5)
                # Adding Picture Preview 
        picture = Gtk.Picture.new_for_filename('../../test-neofetch.png')
        picture.set_size_request(100, 200)

        hbox.append(label)
        hbox.append(picture)
        window.set_child(hbox)

        print(hbox)
        window.present()

app = Chitra()
exit_status = app.run(sys.argv)
print(exit_status)
sys.exit(exit_status)
