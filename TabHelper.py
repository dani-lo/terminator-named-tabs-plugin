from gi.repository import Gtk

import terminatorlib.plugin as plugin

from terminatorlib.util import dbg, err
from terminatorlib.config import Config

from terminatorlib.paned import Paned, HPaned, VPaned
from terminatorlib.window import Window
from terminatorlib.terminal import Terminal
from terminatorlib.notebook import Notebook, TabLabel
from terminatorlib.factory import Factory
from terminatorlib.util import err, dbg, enumerate_descendants, make_uuid


from xml.etree.ElementTree import parse
from xml.etree import ElementTree

from os.path import splitext, isfile, exists, join
from os import listdir, makedirs, linesep



CONFIG_DISPLAY_NAME = 'Tab Helper'
CONFIG_NEW_NAMED_TAB_TITLE = 'named tab - new'

TERMINATOR_EVENT_ACTIVATE = 'activate'
TERMINATOR_EVENT_CLICKED = 'clicked'
TERMINATOR_EVENT_DESTROY = 'destroy'
TERMINATOR_EVENT_DELETE = 'delete_event'

AVAILABLE = ['TabHelper']

CONFIG_PROFILE_WINDOW_KEY = 'window0'
CONFIG_PROFILE_CHILD_KEY = 'child0'

#######################

BUTTON_OK = 'OK'
BUTTON_CANCEL = 'Cancel'

# TERMINAL_NUMBER_VARIABLE = 'terminalNumber'
# CHANGE_DIRECTORY_COMMAND = 'cd "%s"'
# EXPORT_TERMINAL_COMMAND = 'export %s=%d'

EVENT_ACTIVATE = 'activate'
EVENT_CLICKED = 'clicked'
DESTROY_EVENT = 'destroy'
DELETE_EVENT = 'delete_event'

class TabHelper(plugin.MenuItem):
    capabilities = ['terminal_menu']

    def __init__(self):

        self.plugin_name = self.__class__.__name__
    
    def callback(self, menuitems, menu, terminal):
        """
        Click call back invoked from Terminator when user right clicks window
        @param menuitems: List of menu items, that will be displayed. Mutable
        @param menu: GTK menu instance
        @param terminal Terminal class instance pased from erminator
        """

        plugin_menu_item = Gtk.MenuItem(CONFIG_DISPLAY_NAME)
        plugin_submenu = Gtk.Menu()

        plugin_menu_item.set_submenu(plugin_submenu)

        plugin_submenu.append(self.create_named_tab_submenu_item(terminal))

        menuitems.append(plugin_menu_item)

    def create_named_tab_submenu_item(self, terminal):
        """
        @param terminal: Terminal class instance pased from terminator
        """

        save_item = Gtk.ImageMenuItem(CONFIG_NEW_NAMED_TAB_TITLE)

        image = Gtk.Image()
        image.set_from_icon_name(Gtk.STOCK_FLOPPY, Gtk.IconSize.MENU)

        save_item.set_image(image)
        save_item.connect(TERMINATOR_EVENT_ACTIVATE, self.new_named_tab_callback, terminal)

        return save_item

    
    def new_named_tab_callback(self, _, terminal):
        """
        Called by gtk, if user clicked the new named tab menu item.
        @param _: full menu item; not used
        @param terminal: The terminal this context menu item belongs to.
        """

        tab_title = input_box(title = "New tab title") 

        terminal_window = terminal.get_toplevel()

        if not terminal_window.is_child_notebook():

            maker = Factory()
            maker.make('Notebook', window=terminal_window)
        
        terminal_window.show()
        terminal_window.present()

        tab_metadata = {
            "label": tab_title
        }

        if tab_title == None:
            terminal_window.get_child().newtab()
        else:
            terminal_window.get_child().newtab(metadata = tab_metadata)
        

"""
input_box - written by https://github.com/camillo
"""
def input_box(title='Input Box', message='', default_text='', modal=True):
    
    win = InputBoxDialog(message, default_text, modal=modal)
    win.set_title(title)
    win.show()
    
    Gtk.main()

    return win.ret


"""
InputBoxDialog - written by https://github.com/camillo
"""
class InputBoxDialog(Gtk.Dialog):
    
    def __init__(self, message='', default_text='', modal=True):
        
        Gtk.Dialog.__init__(self)
        
        self.connect(DESTROY_EVENT, self.quit)
        self.connect(DELETE_EVENT, self.quit)
        
        if modal:
            self.set_modal(True)
        
        box = Gtk.VBox(spacing=10)
        box.set_border_width(10)
        
        self.vbox.pack_start(box, True, True, 0)
        
        box.show()

        if message:
            label = Gtk.Label(message)
            box.pack_start(label, True, True, 0)
            label.show()

        self.entry = Gtk.Entry()
        self.entry.connect(EVENT_ACTIVATE, self.click)
        self.entry.set_text(default_text)

        box.pack_start(self.entry, True, True, 0)
        
        self.entry.show()
        self.entry.grab_focus()
        
        button = Gtk.Button(BUTTON_OK)
        button.connect(EVENT_CLICKED, self.click)
        button.set_can_default(True)
        
        self.action_area.pack_start(button, True, True, 0)
        
        button.show()
        button.grab_default()
        button = Gtk.Button(BUTTON_CANCEL)
        button.connect(EVENT_CLICKED, self.quit)
        button.set_can_default(True)
        
        self.action_area.pack_start(button, True, True, 0)
        
        button.show()

        self.ret = None

    def quit(self, *_):
        
        self.hide()
        self.destroy()
        Gtk.main_quit()

    def click(self, *_):
        
        self.ret = self.entry.get_text()
        self.quit()