class Exp:
    def __init__(self, type, exp1, op, exp2):
        self.type = type
        self.exp1 = exp1
        self.op = op
        self.exp2 = exp2

    def pp(self):
        self.exp1.pp()
        print(self.op, end="")
        if(self.exp2):
            self.exp2.pp()

    def value(self):
        new = self.calc_Mult()
        new = new.calc()
        if new.type=='num':
            return new.num
        else:
            return new.value()
    
    def calc_Mult(self):
        if(self.op =='*'):
            if(self.exp2.type == 'num'):
                return Num('num', self.exp1.num * self.exp2.num)
            else:
                return Exp('exp', Num('num',(int(self.exp1.num) * int(self.exp2.leftN()))), (self.exp2.op), (self.exp2.rightExp().calc_Mult()))
        else:
            if(self.exp2.type == 'num'):
                return Exp('exp', self.exp1, self.op, self.exp2)
            else:
                return Exp('exp', self.exp1, self.op, self.exp2.calc_Mult())

    def calc(self):
        if(self.op =='+'):
            if(self.exp2.type == 'num'):
                return Num('num', int(self.exp1.num) + int(self.exp2.num))
            else:
                return Exp('exp', Num('num',(int(self.exp1.num) + int(self.exp2.leftN()))), (self.exp2.op), (self.exp2.rightExp()))
        elif(self.op =='-'):
            if(self.exp2.type == 'num'):
                return Num('num', int(self.exp1.num) - int(self.exp2.num))
            else:
                return Exp('exp', Num('num',(int(self.exp1.num) - int(self.exp2.leftN()))), (self.exp2.op), (self.exp2.rightExp()))


    def leftN(self):
        return self.exp1.leftN()

    def rightExp(self):
        return self.exp2
         
class Num:
    def __init__(self, type, num):
        self.type = type
        self.num = num

    def pp(self):
        print(self.num, end="")

    def value(self):
        return int(self.num)
    
    def leftN(self):
        return int(self.num)
    
    def calc_Mult(self):
        return self

    def calc(self):
        return self