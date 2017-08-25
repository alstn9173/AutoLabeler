##############
# COMPLETE!!!#
##############
class Widget :
    def __init__(self, xml):
        self.xml = xml
        self.widget_data = []
        self.tag_name = ['index',       'text',         'class',
                         'package',     'content-desc', 'checkable',
                         'checked',     'enabled',      'focusable',
                         'focused',     'scrollable',   'long-clickable',
                         'password',    'selected',     'bounds',
                         'resource-id', 'instance']

        for i in range(0, len(self.tag_name)):
            self.widget_data.append('')

    # Set tag information
    def set_widget_data(self, tag, value):
        index = self.widget_data.index(tag)
        self.widget_data[index] = value

    # Returns tag information
    def get_widget_data(self, tag):
        index = self.widget_data.index(tag)
        return self.widget_data[index]

    # A method that returns what tag an index comes in as input.
    def what_tag_assigned_this_index(self, index):
        return self.tag_name[index]