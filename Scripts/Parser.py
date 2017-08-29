import widget


class Parser:
    def __init__(self, xml):
        self.xml = xml          # xml code
        self.lines = []         # List that stores xml code line by line
        self.tag_name = ['index', 'text', 'class', 'package',
                         'content-desc', 'checkable', 'checked',
                         'enabled', 'focusable', 'focused',
                         'scrollable', 'long-clickable', 'password',
                         'selected', 'bounds', 'resource-id', 'instance']
        self.set_of_widget = [] # List that stores all the widgets currently displayed on the screen

    #   -- xml_line_seperator --
    # This method works like this:
    # [input]   xml = <something1="", ...><something2="", ...>...<some="", ...>
    # [call]    xml_line_seperator()
    # [result]  lines = [<something1="", ...>,
    #                    <something2="", ...>,
    #                    <some="", ...>]
    def xml_line_seperator(self):
        start_index = 0

        for i in range(0, len(self.xml)):
            if self.xml[i] == '<':
                start_index = i
            if self.xml[i] == '>':
                self.lines.append(self.xml[start_index:i])

    #   -- xml_tag_seperator --
    # This method works like this:
    # [input]   line = <This="method" works="like this">
    # [call]    xml_tag_seperator(line, 'works')
    # [return]  'like this'
    def xml_tag_seperator(self, line, tag_name):
        tag = line[line.find(tag_name):]
        tag = tag[tag.find('=') + 2:]
        tag = tag[:tag.find('"')]

        if tag_name == 'boundary':
            tag = tag.replace(',', ' ').replace('[', '').replace(']', ' ').strip().split(' ')

        return tag

    #   -- --
    # Read one line of xml code, divide each one,
    # and save it in the widget instance.
    # [input]   line = <This="method" works="like this">
    # [call]    parser()
    # [result]  set_of_widgets = [  This = method,
    #                               works = like this ]
    def parser(self):
        for line in self.lines:
            w = widget.Widget(self.xml)

            for j in range(0, len(self.tag_name)):
                w.set_widget_data(self.tag_name[j],
                                  self.xml_tag_seperator(line, self.tag_name[j]))

            self.set_of_widget.append(w)

    def do_parsing(self):
        self.xml_line_seperator()
        self.parser()
        return self.set_of_widget

    #   -- print_xml --
    # Print the current xml code.
    def print_xml(self):
        for line in self.lines:
            print(line)
