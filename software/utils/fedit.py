from PyQt4 import QtGui
from widgets.editor import TextEditor, DragDropEditor
from widgets.tile import tile


def add_tile(workspace):
    new_tile = tile(workspace.currentWidget(), 30, 30)
