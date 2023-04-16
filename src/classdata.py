import templates as t

def parse(root_cu, class_name):
    die = None
    for d in root_cu.iter_DIEs():
        if d.tag == 'DW_TAG_class_type' and d.attributes['DW_AT_name'].value.decode() == class_name:
            die = d
    
    constr_list = []
    method_list = []
    for child in die.iter_children():
        if child.tag == 'DW_TAG_subprogram':
            i = ItemData(root_cu, child)
            if i.name == class_name:
                constr_list.append(i)
            else:
                method_list.append(i)
    return ClassData(class_name, constr_list, method_list)

# Find type by offset
def resolve_type(root_cu, t):
    if isinstance(t, bytes):
        return t.decode()
    
    for d in root_cu.iter_DIEs():
        if d.tag and 'type' in d.tag and d.offset == t:
            return resolve_type(root_cu, d.attributes['DW_AT_name'].value)

# Unified class for constructors and methods
class ItemData:
    def __init__(self, root_cu, die):
        self.name = die.attributes['DW_AT_name'].value.decode()
        
        children = [c for c in die.iter_children()][1:]
        self.args = []
        
        # resolve arg types
        for c in children:
            if c.tag == 'DW_TAG_formal_parameter':
                self.args.append(resolve_type(root_cu, c.attributes['DW_AT_type'].value))
    
    def constr_fn(self, i):
        if not self.args:
            return t.CONSTR_FN_NOARGS.format(class_name=self.name, i=i)
        else:
            a = self.both_args()
            return t.CONSTR_FN.format(
                class_name=self.name,
                i=i,
                fn_args=a[0],
                call_args=a[1]
            )
    
    def both_args(self):
        args = ''
        c_args = ''
        for i in range(len(self.args)):
            # add const to reinterpret cast
            a = self.args[i] if 'const' in self.args[i] else 'const ' + self.args[i]
            args += t.FN_ARG.format(type=a, i=i)
            c_args += t.FN_CALL_ARG.format(i=i)
        c_args = c_args[:-2] # cut out last ', '
        return (args, c_args)
    
    def constr_lst_item(self, i):
        return t.CONSTR_LIST_ITEM.format(
            size_args=self.size_args(),
            i=i
        )
    
    def size_args(self):
        if not self.args:
            return ''
        s = ''
        for a in self.args:
            s += t.SIZE_ARG.format(type=a)
        return s
    
    def method_fn(self, class_name):
        if not self.args:
            return t.METHOD_FN_NOARGS.format(class_name=class_name, method_name=self.name)
        else:
            a = self.both_args()
            return t.METHOD_FN.format(
                class_name=class_name,
                method_name=self.name,
                fn_args=a[0],
                call_args=a[1]
            )
    
    def method_lst_item(self):
        return t.METHOD_LIST_ITEM.format(
            size_args=self.size_args(),
            method_name=self.name
        )


# Root class for building class fuzzer
class ClassData:
    def __init__(self, name, constr_list, method_list):
        self.name = name
        self.constr_list = constr_list
        self.method_list = method_list
    
    def constr_fns(self):
        s = ''
        for i in range(len(self.constr_list)):
            s += self.constr_list[i].constr_fn(i) + '\n'
        return s
    
    def constr_lst(self):
        s = ''
        for i in range(len(self.constr_list)):
            s += self.constr_list[i].constr_lst_item(i)
        return s
    
    def method_fns(self):
        s = ''
        for m in self.method_list:
            s += m.method_fn(self.name) + '\n'
        return s
    
    def method_lst(self):
        s = ''
        for m in self.method_list:
            s += m.method_lst_item()
        return s
    
    def fuzzer(self, class_header):
        return t.CORE.format(
            class_header=class_header,
            class_name=self.name,
            constr_fns=self.constr_fns(),
            constr_list=self.constr_lst(),
            method_fns=self.method_fns(),
            method_list=self.method_lst(),
        )