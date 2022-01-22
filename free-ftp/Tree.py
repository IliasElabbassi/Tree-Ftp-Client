from re import S


class Node:
    def __init__(self, data, type=""):
        self.data = data
        self.type = type
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
    
    def getLevel(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level

    def print_tree(self):
        prefix = "_" * self.getLevel() * 3
        print(prefix +self.type+": "+self.data)
        if self.children:
            for child in self.children:
                child.print_tree()