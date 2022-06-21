from federatedscope.db.model.sqlschedule_pb2 import AttributeType

MAX_INT = 2147483647
MIN_INT = -2147483648


class Attribute(object):
    def __init__(self, attr):
        self.name = attr['name']
        if attr['type'].lower() == "int":
            self.type = AttributeType.INT
            if 'min' in attr:
                self.min_value = attr['min']
            else:
                self.min_value = -2147483648
            if 'max' in attr:
                self.max_value = attr['max']
            else:
                self.max_value = 2147483647
            if 'delta' in attr:
                self.delta = attr['delta']
            else:
                self.delta = 1
        else:
            self.type = AttributeType.STRING

    def __str__(self):
        if self.type == AttributeType.INT:
            return "%s:%s:%d:%d:%d" % (self.name, AttributeType.Name(self.type), self.min_value, self.max_value, self.delta)
        else:
            return "%s:%s" % (self.name, AttributeType.Name(self.type))


class Schema(object):
    def __init__(self, schema_str: str):
        attrs = eval(schema_str.strip())
        self._attrs = []
        for attr in attrs:
            if 'name' not in attr:
                raise ValueError("No name in attribute definition")
            if 'type' not in attr:
                raise ValueError("No type in attribute definition")
            self._attrs.append(Attribute(attr))
        self._attr_map = {}
        for i in range(len(attrs)):
            self._attr_map[attrs[i]['name']] = i

    def get_attr_by_name(self, attr_name: str):
        return self._attrs[self._attr_map[attr_name]]

    def get_attr_by_id(self, attr_id: int):
        return self._attrs[attr_id]

    def get_attrs_by_name(self, attr_names: list):
        return [self.get_attr_by_name(attr_name) for attr_name in attr_names]

    def get_attrs_by_id(self, attr_ids: list):
        return [self.get_attr_by_id(attr_id) for attr_id in attr_ids]

    def attr_names(self):
        return [attr.name for attr in self._attrs]

    def attrs(self):
        return self._attrs

    def __str__(self):
        return "|".join([str(attr) for attr in self._attrs])
