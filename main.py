import sys
import subprocess
import gi
import time
import os
import requests
from PIL import Image
from gi.repository import GLib, Gtk, GdkPixbuf, Gdk

gi.require_version("Gtk", "4.0")

class Chitra(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.chitra.screenshot")
        GLib.set_application_name("Test")

    def do_activate(self):
        self.window = Gtk.ApplicationWindow(application=self, title="Chitra")
        self.window.set_default_size(400, 300)

        # Creating Title
        lbl = Gtk.Label(label="Capture it with Chitra!!")
        lbl.set_markup("<span font='20' weight='bold'>Capture it with Chitra!!</span>")

        # Creating a button for selecting rectangular screenshot
        btn = Gtk.Button(label="Select Area")
        btn.connect("clicked", self.select_area)

        # Button for capturing full window screenshot
        btn2 = Gtk.Button(label="Select Window")
        btn2.connect("clicked", self.capture_full_screen)

        # Creating a vertical box to hold all the widgets
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.set_halign(Gtk.Align.CENTER)
        vbox.set_valign(Gtk.Align.CENTER)

        # Adding widgets to vbox container
        vbox.append(lbl)
        vbox.append(btn)
        vbox.append(btn2)

        self.window.set_child(vbox)
        self.window.present()

    # Selecting particular area for screenshot
    def select_area(self, widget):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        save_path = f"$HOME/Pictures/mypicture_{timestamp}.jpg"

        # Expand the tilde and environment variables to the full path
        save_path = os.path.expandvars(save_path)

        # Run the command to save the screenshot and copy it to the clipboard
        subprocess.run(f"maim -s {save_path} | tee {save_path} | xclip -selection clipboard -t image/png", shell=True)
        self.show_image(save_path)

    # Capturing full screen screenshot
    def capture_full_screen(self, widget):
        print("Capturing Full Screen")

        if self.window is not None:
            self.window.hide()

            # Use GLib timeout to delay the screenshot capture
            GLib.timeout_add(500, self.take_screenshot)

    # Adding a timestamp to hide the app
    def take_screenshot(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        save_path = f"$HOME/Pictures/full_screenshot_{timestamp}.png"

        # Expand the tilde and environment variables to the full path
        save_path = os.path.expandvars(save_path)

        # Run maim to capture the full screen
        subprocess.run(f"maim {save_path} | tee {save_path} | xclip -selection clipboard -t image/png", shell=True)

        print(f"Full screen screenshot saved to {save_path}")
        self.show_image(save_path)

        # Show the window again
        if self.window is not None:
            self.window.show()

        return False

    # Post screenshot customization
    def customizeScreenshot(self, save_path):
        image = Image.open(save_path)
        image = image.resize((1,1))
        dominant_color = image.getpixel((0,0))
        return f"rgb({dominant_color[0]}, {dominant_color[1]}, {dominant_color[2]})"

    # Displaying the image in new window
    def show_image(self, save_path):
        image_window = Gtk.Window(title="Selected Image")
        image_window.set_default_size(800, 750)

        # Save the image with the background
        image_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        image_container.set_name("image-container")
        image_container.set_halign(Gtk.Align.CENTER)
        image_container.set_valign(Gtk.Align.CENTER)
        image_container.get_style_context().add_class("custom-bg")

        try:
            # Load image
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(save_path)
            image = Gtk.Image.new_from_pixbuf(pixbuf)
            image.set_size_request(500, 450)
            image.get_style_context().add_class("main-img")

            image_container.append(image)
            image_window.set_child(image_container)

        except Exception as e:
            print(f"Failed to load image: {e}")

        dominant_color = self.customizeScreenshot(save_path)
        self.apply_css(image_window, dominant_color)
        image_window.present()
        self.save_image_with_background(save_path, dominant_color)
        self.further_action(save_path, dominant_color)

    # Function to save the background picture
    def save_image_with_background(self, save_path, dominant_color):
        image = Image.open(save_path)
        bg_image = Image.new('RGB', (image.width + 80, image.height + 80), dominant_color)

        # Paste the original image onto the background image
        bg_image.paste(image, (40, 40))

        save_path_with_bg = save_path.replace('.jpg', '_with_bg.jpg')
        bg_image.save(save_path_with_bg)
        print(f"Image with background saved to {save_path_with_bg}")
        return save_path_with_bg
    
    # Function to save background picture in clipboard
    def copy_the_shot(self, save_path):
        try:
            subprocess.run(f"xclip -selection clipboard -t image/png -i {save_path}", shell=True)
            print(f"Copied {save_path} to clipboard")
        except Exception as e:
            print(f"Failed to copy image to clipboard: {e}")


    # Last outro screen to save a screen or to copy it to clipboard
    def further_action(self, save_path, dominant_color):
        self.dialog_window = Gtk.ApplicationWindow(application=self, title="Further Actions?")
        self.dialog_window.set_default_size(300, 200)

        # Declaring buttons
        lbl = Gtk.Label(label="Save Your Screenshot")
        btn = Gtk.Button(label="Save")
        btn.connect("clicked", lambda widget: self.save_image_with_background(save_path, dominant_color))

        btn2 = Gtk.Button(label="Copy")
        btn2.connect("clicked", lambda widget: self.copy_the_shot(save_path))

        btn3 = Gtk.Button(label="Get a link")
        btn3.connect("clicked", lambda widget: self.get_sharable_link(save_path))

        # Container for storing the buttons
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.append(btn)
        hbox.append(btn2)
        hbox.append(btn3)

        # Container for label and buttons
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)
        vbox.set_halign(Gtk.Align.CENTER)
        vbox.set_valign(Gtk.Align.CENTER)
        vbox.append(lbl)
        vbox.append(hbox)

        self.dialog_window.set_child(vbox)
        self.dialog_window.present()

    # Function to upload image and get sharable link
    def get_sharable_link(self, save_path):
        url = "https://0x0.st"
        with open(save_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
            if response.status_code == 200:
                sharable_link = response.text.strip()
                print(f"Sharable link: {sharable_link}")
                self.show_link_dialog(sharable_link)
            else:
                print("Failed to upload image")

    # Function to show sharable link in a dialog
    def show_link_dialog(self, link):
        link_dialog = Gtk.MessageDialog(
            transient_for=self.dialog_window,
            modal=True,
            buttons=Gtk.ButtonsType.OK,
            message_type=Gtk.MessageType.INFO,
            text="Sharable Link",
        )
        link_dialog.set_markup(link)
        link_dialog.connect("response", self.on_link_dialog_response)
        link_dialog.show()

    def on_link_dialog_response(self, dialog, response_id):
        dialog.destroy()


    # Applying CSS
    def apply_css(self, widget, bg_color):
        css = f"""
            .custom-bg {{
                display: flex;
                justify-content: center;
            }}
            .main-img {{
                background-color: {bg_color};
                padding: 20px;
                box-shadow: 0px 0px 10px black;
            }}
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode('utf-8'))

        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    # Function to copy the screenshot (currently not implemented)
    def copy_the_shot(self, widget):
        print("Copying the shot (functionality not implemented)")

app = Chitra()
exit_status = app.run(sys.argv)
print(exit_status)
sys.exit(exit_status)
