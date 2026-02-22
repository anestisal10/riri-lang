import parser as prsr

class Compiler:
    def __init__(self):
        self.instructions = []
        self.constants = []

    def compile(self, node):
        if isinstance(node, prsr.Number):
            if node.value not in self.constants:
                self.constants.append(node.value)
            idx = self.constants.index(node.value)
            self.emit("LOAD_CONST", idx)
            
        elif isinstance(node, prsr.String):
            if node.value not in self.constants:
                self.constants.append(node.value)
            idx = self.constants.index(node.value)
            self.emit("LOAD_CONST", idx)
            
        elif isinstance(node, prsr.Var):
            self.emit("LOAD_NAME", node.name)
            
        elif isinstance(node, prsr.Assign):
            self.compile(node.value)
            self.emit("STORE_NAME", node.name)
            
        elif isinstance(node, prsr.BinOp):
            self.compile(node.left)
            self.compile(node.right)
            
            if node.op == '+': self.emit("ADD")
            elif node.op == '-': self.emit("SUB")
            elif node.op == '*': self.emit("MUL")
            elif node.op == '/': self.emit("DIV")
            elif node.op == '>': self.emit("GT")
            elif node.op == '<': self.emit("LT")
            
        elif isinstance(node, prsr.ArrayDef):
            for element in node.elements:
                self.compile(element)
            self.emit("BUILD_LIST", len(node.elements))
            
        elif isinstance(node, prsr.IndexAccess):
            self.compile(node.target)
            self.compile(node.index)
            self.emit("BINARY_SUBSCR")
            
        elif isinstance(node, prsr.If):
            self.compile(node.condition)
            self.emit("JUMP_IF_FALSE", 0) # Placeholder
            jump_idx = len(self.instructions) - 1
            
            for stmt in node.true_branch:
                self.compile(stmt)
                
            if node.false_branch:
                self.emit("JUMP_ABSOLUTE", 0) # Placeholder
                jump_abs_idx = len(self.instructions) - 1
                
                # Patch the false jump
                self.instructions[jump_idx] = ("JUMP_IF_FALSE", len(self.instructions))
                
                for stmt in node.false_branch:
                    self.compile(stmt)
                    
                # Patch absolute jump
                self.instructions[jump_abs_idx] = ("JUMP_ABSOLUTE", len(self.instructions))
            else:
                self.instructions[jump_idx] = ("JUMP_IF_FALSE", len(self.instructions))
                
        elif isinstance(node, prsr.While):
            loop_start = len(self.instructions)
            self.compile(node.condition)
            
            self.emit("JUMP_IF_FALSE", 0) # Placeholder
            jump_idx = len(self.instructions) - 1
            
            for stmt in node.body:
                self.compile(stmt)
            
            self.emit("JUMP_ABSOLUTE", loop_start)
            # Patch exit jump
            self.instructions[jump_idx] = ("JUMP_IF_FALSE", len(self.instructions))
            
        elif isinstance(node, prsr.FunctionCall):
            if node.name == "fwnakse":
                for arg in node.args:
                    self.compile(arg)
                self.emit("PRINT")
            elif node.name == "skalise":
                self.compile(node.args[0])
                self.emit("INPUT")
            else:
                 raise NotImplementedError(f"Function calls to custom '{node.name}' not supported in Bytecode VM yet!")
                 
        else:
            raise Exception(f"Compiler Error: Unknown Node {type(node)}")

    def emit(self, opcode, arg=None):
        self.instructions.append((opcode, arg))

def compile_ast(statements):
    compiler = Compiler()
    for stmt in statements:
        compiler.compile(stmt)
    return compiler.instructions, compiler.constants
