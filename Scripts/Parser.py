class Parser:
    def __init__(self, xml):
        self.xml = xml          # xml code
        self.lines = []         # List that stores xml code line by line
        self.tag_name = ['index', 'text', 'class', 'package',
                         'content-desc', 'checkable', 'checked',
                         'clickable', 'enabled', 'focusable',
                         'focused', 'scrollable', 'long-clickable',
                         'password', 'selected', 'bounds',
                         'resource-id', 'instance']

    #   -- xml_line_separator --
    # This method separate xml code line by line.
    # This method works like this:
    # [input]   xml = <something1="", ...><something2="", ...>...<some="", ...>
    # [call]    xml_line_seperator()
    # [result]  lines = [<something1="", ...>,
    #                    <something2="", ...>,
    #                    <some="", ...>]
    def xml_line_separator(self):
        start_index = 0
        d_quote_skipper = False     # To ignore all characters in the double quote

        for string_index in range(0, len(self.xml)):
            one_character = self.xml[string_index]

            if ~d_quote_skipper:
                if one_character == '<':
                    start_index = string_index
                elif one_character == '>':
                    self.lines.append(self.xml[start_index:string_index])

            if one_character == '\"':
                d_quote_skipper = ~d_quote_skipper

    #   -- xml_tag_separator --
    # This method separates each of the given tags from a separated xml line.
    # This method works like this:
    # [input]   line = <This="method" works="like this">
    # [call]    xml_tag_seperator(line, 'works')
    # [return]  'like this'
    def xml_tag_separator(self, line, tag_name):
        tag = line[line.find(tag_name):]
        tag = tag[tag.find('=') + 2:]
        tag = tag[:tag.find('"')]

        if tag_name == 'bounds':
            tag = tag.replace(',', ' ').replace('[', '').replace(']', ' ').strip().split(' ')

        return tag

    #   -- parser --
    # Read one line of xml code, divide each one,
    # and save it in the widget instance.
    # [input]   line = <This="method" works="like this">
    # [call]    parser()
    # [result]  set_of_widget = [  This <- method,
    #                              works <- like this ]
    def parser(self):
        self.xml_line_separator()

        set_of_widget = []     # List that stores all the widgets currently displayed on the screen

        for line in self.lines:
            widget_list = {}

            for tag_index in range(0, len(self.tag_name)):
                widget_list[self.tag_name[tag_index]] = self.xml_tag_separator(line, self.tag_name[tag_index])

            if widget_list['clickable'] == 'true':
                set_of_widget.append(widget_list)

        return set_of_widget

    #   -- print_xml --
    # Print the current xml code.
    def print_xml(self):
        for line in self.lines:
            print(line)
