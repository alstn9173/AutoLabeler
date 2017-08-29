class Widget:
    def __init__(self, xml):
        self.xml = xml
        self.widget_data = {}

    # Set tag information
    def set_widget_data(self, tag, value):
        self.widget_data[tag] = value

    # Returns tag information
    def get_widget_data(self, tag):
        return self.widget_data[tag]