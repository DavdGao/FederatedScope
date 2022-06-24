



class ObjNode(object):
    def __init__(self):
        self.operator = None
        self.father = None
        self.children = list()

class JoinNode(object):
    def __init__(self, operator):
        self.operator = operator




class Ast(object):
    def __init__(self):
        self.root = None