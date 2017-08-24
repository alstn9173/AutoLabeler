class Widget :
    widget_data = []
    def __init__(self):
        self.widget_data['index'] = 0
        self.widget_data['class'] = 0
        self.widget_data['package'] = 0
        self.widget_data['content-desc'] = 0
        self.widget_data['checkable'] = 0
        self.widget_data['checked'] = 0
        self.widget_data['clickable'] = 0
        self.widget_data['enabled'] = 0
        self.widget_data['focusable'] = 0
        self.widget_data['focused'] = 0
        self.widget_data['scrollable'] = 0
        self.widget_data['long-clickable'] = 0
        self.widget_data['password'] = 0
        self.widget_data['selected'] = 0
        self.widget_data['bounds'] = 0
        self.widget_data['resource-id'] = 0
        self.widget_data['instance'] = 0

    # parse the input xml line and save each data
    def set_data(self, line):
        self.parse_data(line)

    def parse_data(self, line):
        b = 0