#! /usr/bin/env python
import gi
gi.require_version ('Astroid', '0.1')
gi.require_version ('Gtk', '3.0')

from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Astroid

from syntax_highlight import SyntaxHighlight

class SyntaxHighlightPlugin (GObject.Object, Astroid.ThreadViewActivatable, SyntaxHighlight):
  object = GObject.property (type = GObject.Object)
  thread_view = GObject.property (type = Gtk.Box)

  def do_activate (self):
    print ('syntax: activated', __file__)

  def do_deactivate (self):
    print ('syntax: deactivated')

  def do_filter_part (self, text, html, mime_type, is_patch):
    return SyntaxHighlight.do_filter_part (self, text, html, mime_type, is_patch)


print ('syntax: plugin loaded')

