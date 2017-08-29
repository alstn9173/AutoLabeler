class TensorOutput:
    def __init__(self, boundary, identified_class, accuracy):
        self.boundary = boundary
        self.identified_class = identified_class
        self.accuracy = accuracy

    def set_boundary(self, boundary):
        self.boundary = boundary

    def set_class(self, identified_class):
        self.identified_class = identified_class

    def set_accuracy(self, accuracy):
        self.accuracy = accuracy

    def get_boundary(self):
        return self.boundary

    def get_class(self):
        return self.identified_class

    def get_accuracy(self):
        return self.accuracy
