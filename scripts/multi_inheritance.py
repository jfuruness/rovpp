class ROV:
    def proc(self):
        self.gao()
        self.valid()

    def valid(self):
        print("ROV valid")

    def gao(self):
        print("ROV gao")

class NonLite:
    def gao(self):
        print("non lite gao")

class V2:
    def proc(self):
        self.gao()
        self.valid()

    def valid(self):
        print("ROV valid")
    def gao(self):
        print("V2 gao")

class V3(ROV, V2):
    pass

V3().proc()
