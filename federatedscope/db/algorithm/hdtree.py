class RangeTree(object):
    def __init__(self):
        self.children = []
        self.range = None
        self.layer = None
        self.height = None

    @staticmethod
    def factory(min, max, delta, fanout):
        root = RangeTree().construct(min, max, 0, delta, fanout)
        return root

    def construct(self, min, max, layer, delta, fanout):
        self.range = (min, max)
        self.layer = layer
        self.height = 1
        if max - min + 1 > delta:
            step_size = int((max - min + 1) / fanout)
            if step_size == 0: step_size = 1
            cur_min, cur_max = min, min + step_size - 1
            while cur_min <= max:
                if cur_max >= max: cur_max = max
                child = RangeTree().construct(cur_min, cur_max, layer + 1, delta, fanout)
                if self.height < child.height + 1: self.height = child.height + 1 
                self.children.append(child)
                cur_min, cur_max = cur_min + step_size, cur_max + step_size
        return self

    def decompose_interval(self, min, max):
        if min <= self.range[0] and self.range[1] <= max:
            return [(self.layer, self.range)]
        ret = []
        for child in self.children:
            if min <= child.range[0] <= max or min <= child.range[1] <= max:
                ret += child.decompose_interval(min, max)
        return ret
    
    def get_ranges(self, value):
        ret = [None] * self.height
        node = self
        while node != None:
            ret[node.layer] = node.range
            next_node = None
            for child in node.children:
                if child.range[0] <= value <= child.range[1]:
                    next_node = child
                    break
            node = next_node
        return ret