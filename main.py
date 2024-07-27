import sys 
import subprocess
import gi 
import time
import os
from gi.repository import GLib, Gtk 
gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk

class Chitra(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.chitra.screenshot")
        GLib.set_application_name("Test")


    def do_activate(self):
        self.window = Gtk.ApplicationWindow(application=self, title="Chitra")
        self.window.set_default_size(400, 300)

        #Creating Title
        lbl = Gtk.Label(label="Capture it with Chitra!!")
        lbl.set_markup("<span font='20' weight='bold'>Capture it with Chitra!!</span>")

        #creating a button for selecting rectangular screenshot
        btn = Gtk.Button(label="Select Area")
        btn.connect("clicked",self.select_area)

        #button for capturing full window screenshot
        btn2 = Gtk.Button(label="Select Window")
        btn2.connect("clicked", self.capture_full_screen)

        #creaing a vertical box to hold all the widgets

        #creating a container to add multiple buttons, hbox == horizontal box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.set_halign(Gtk.Align.CENTER)
        vbox.set_valign(Gtk.Align.CENTER)

        #adding btn to vbox container
        vbox.append(lbl)
        vbox.append(btn)
        vbox.append(btn2)        


        self.window.set_child(vbox)
        self.window.present()

        

    #Selecting particular area for screenshot
    def select_area(self, widget):

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        save_path = f"$HOME/Pictures/mypicture_{timestamp}.jpg"
        
        # Expand the tilde to the full path
        save_path = os.path.expanduser(save_path)
        
        # Run the command to save the screenshot and copy it to the clipboard
        subprocess.run(f"maim -s {save_path} | tee {save_path} | xclip -selection clipboard -t image/png", shell=True)

    #Capturing full screen screenshot
    def capture_full_screen(self, widget):
        print("Capturing Full Screen")

        if self.window is not None:
            self.window.hide()
            
            # Use GLib timeout to delay the screenshot capture
            GLib.timeout_add(500, self.take_screenshot)

    #Adding a timestamp to hide the app
    def take_screenshot(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        save_path = f"$HOME/Pictures/full_screenshot_{timestamp}.png"

        # Expand the tilde to the full path
        save_path = os.path.expanduser(save_path)

        # Run maim to capture the full screen
        subprocess.run(f"maim {save_path}", shell=True)

        print(f"Full screen screenshot saved to {save_path}")

        # Show the window again
        if self.window is not None:
            self.window.show()

        return False
    
    # Post screenshot customization 
    def customizeScreenshot(self):

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


app = Chitra()
exit_status = app.run(sys.argv)
print(exit_status)
sys.exit(exit_status)
