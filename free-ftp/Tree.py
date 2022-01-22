class Node:
    def __init__(self, data):
        self.data = data
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
        print(prefix + self.data)
        if self.children:
            for child in self.children:
                child.print_tree()