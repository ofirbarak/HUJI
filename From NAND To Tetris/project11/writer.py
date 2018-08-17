class Writer:
    def __init__(self, outputfile):
        self.__outputfile = outputfile

    def write_push(self, variable, number):
        if variable == 'field':
            self.__outputfile.write('push this %s\n' % number)
        else:
            self.__outputfile.write('push %s %s\n' % (variable, number))

    def write_pop(self, variable, number):
        if variable == 'field':
            self.__outputfile.write('pop this %s\n' % number)
        else:
            self.__outputfile.write('pop %s %s\n' % (variable, number))

    def write_array(self):
        self.write_pop("pointer", 1)
        self.write_push("that", 0)

    def write_call(self, func_name, number):
        self.__outputfile.write('call %s %s\n' % (func_name, number))

    def write_func_dec(self, class_name, subrotinue_name, number):
        self.__outputfile.write('function %s.%s %d\n' % (class_name, subrotinue_name, number))

    def write_operation(self, op):
        if op == 'divide':
            self.write_call('Math.divide', 2)
        elif op == 'multiply':
            self.write_call('Math.multiply', 2)
        else:
            self.__outputfile.write('%s\n' % op)

    def write_start_label(self, label):
        self.__outputfile.write('label %s.start\n' % label)

    def write_end_label(self, label):
        self.__outputfile.write('label %s.end\n' % label)

    def write_method(self):
        self.write_push('argument', 0)
        self.write_pop('pointer', 0)

    def write_constructor(self, number):
        self.write_push('constant', number)
        self.write_call('Memory.alloc', 1)
        self.write_pop('pointer', 0)

    def write_goto(self, go):
        self.__outputfile.write('goto %s\n' % go)

    def write_return(self):
        self.__outputfile.write('return\n')

    def write_if_goto(self, go):
        self.__outputfile.write('if-')
        self.write_goto(go)

    def write_label(self, label):
        self.__outputfile.write('label %s\n' % label)