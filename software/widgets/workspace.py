from PyQt4 import QtGui
from widgets.editor import TextEditor, DragDropEditor
from widgets.tile import tile, arrow
from utils import fedit


class Workspace(QtGui.QTabWidget):
    """ The main container widget which allows editing and viewing of files,
        status monitoring, and data visualisation. This widget can contain
        text and visual based file editing, visual and text based data
        review, and is displayed in a tab format.

        Widget is initialized with a single blank file
    """

    def add_file(self, file_path, index=0):

        """ Adds a file in the workspace, and allows editing via the drag
            and drop or text based editing windows

            file_path: The path to the file, with the extension
            index: The location of the tab to be inserted. If index
                   is equal to 0, the tab is added onto the end.
        """

        # Extract the extension and title from the file_path
        # If the file does not have an extension, both the title and extension
        # are equal to the name
        extension = file_path.split('.', 1)[-1]
        name = file_path.split('/')[-1]

        # Open text based files
        if extension in ('txt', 'py', 'upl'):
            added_file = TextEditor(name, extension, file_path)

            # Add a checker and updater to check for changes (saved vs. unsaved)
            added_file.textChanged.connect(lambda: self.save_state_change(False))

        # Open drag and drop based files
        elif extension == "pro":
            added_file = DragDropEditor(name, extension, file_path)
            f = open(file_path)
            for line in f:
                if line[0] == "#":
                    line = line.strip("\n")
                    params = line.split(" ")
                    new_tile = tile(added_file, int(params[1]), int(params[2]), int(params[3]))
                    new_tile.drawConnection.connect(added_file.drawArrow)
                    new_tile.fileChange.connect(lambda: self.save_state_change(False))
                elif line[0] == ">":
                    line = line.strip("\n")
                    params = line.split(" ")
                    new_arrow = arrow(int(params[1]), int(params[2]), int(params[3]), int(params[4]), int(params[5]), int(params[6]))
                    new_arrow.setParent(added_file)
                    new_arrow.lower()
                    new_arrow.show()
                    tiles = added_file.findChildren(tile)
                    for i in tiles:
                        if i.ref == int(params[5]) or i.ref == int(params[6]):
                            i.arrows.append(new_arrow)



        # Open new, untitled files
        elif extension == "untitled":
            added_file = TextEditor(name)
        else:
            QtGui.QMessageBox.question(self, 'Message',
                                       "Cannot open file")
            return None

        # Don't replicate the default name for a new, blank file
        if "untitled" in name:

            added_file.fileName = (added_file.fileName.split('.')[0] +
                                    str(self.num_of_untitled) + '.' + extension)
            self.num_of_untitled += 1

        # Add as a tab, at a certain index if indicated
        if index:
            self.insertTab(index, added_file, added_file.fileName)
            self.setCurrentIndex(index)
        else:
            self.addTab(added_file, added_file.fileName)
            self.setCurrentIndex(self.count() - 1)

    def save_state_change(self, isSaved):
        """ Adds or removes an asterisk from the current tab when text changes
            or the file is saved to denote to the user if their changes are
            currently saved.

            isSaved: If the file has become saved (True) or unsaved (False)
        """
        i = self.currentIndex()
        current_name = self.tabText(i)
        if isSaved and ('*' in current_name):
            self.setTabText(i, current_name[:-1])
            self.currentWidget().isSaved = True
        elif not isSaved and '*' not in current_name:
                self.setTabText(i, current_name + '*')
                self.currentWidget().isSaved = False

    def __init__(self):
        super(Workspace, self).__init__()

        # One of the only core components of the workspace itself
        # are the tabs along the top, defined below
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.removeTab)
        self.setMovable(True)

        # Set up initial tab as "untitled" and unsaved
        initial_file = DragDropEditor('untitled.pro')
        self.addTab(initial_file, initial_file.fileName)
        self.save_state_change(False)

        # Keep track of the "untitled" files
        self.num_of_untitled = 1

        # The layout in this widget is incredibly simple: a single window
        layout = QtGui.QGridLayout()
        self.setLayout(layout)

        self.show()
