class Attribute(object):
    def __init__(self, attr_name, attr_type):
        self.attr_name = attr_name
        self.attr_type = attr_type


class Schema(object):
    def __init__(self, attrs: list):
        self.attrs = attrs
        self.attr_map = {}
        for i in range(len(attrs)):
            self.attr_map[attrs[i].attr_name] = i

    def get_attr(self, attr_name: str):
        return self.attrs[self.attr_map[attr_name]]

    def get_attrs(self, attr_names: list):
        return [get_attr(attr_name) for attr in attr_names]