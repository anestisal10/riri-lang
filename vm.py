class VirtualMachine:
    def __init__(self, instructions, constants):
        self.instructions = instructions
        self.constants = constants
        self.stack = []
        self.env = {}
        self.ip = 0  # Instruction Pointer
        self.output_buffer = []

    def run(self):
        while self.ip < len(self.instructions):
            opcode, arg = self.instructions[self.ip]
            self.ip += 1
            
            if opcode == "LOAD_CONST":
                self.stack.append(self.constants[arg])
                
            elif opcode == "STORE_NAME":
                val = self.stack.pop()
                self.env[arg] = val
                
            elif opcode == "LOAD_NAME":
                if arg not in self.env:
                    raise Exception(f"VM Error: Variable '{arg}' not found!")
                self.stack.append(self.env[arg])
                
            elif opcode == "ADD":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left + right)
                
            elif opcode == "SUB":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left - right)
                
            elif opcode == "MUL":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left * right)
                
            elif opcode == "DIV":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left / right)
                
            elif opcode == "GT":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(1 if left > right else 0)
                
            elif opcode == "LT":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(1 if left < right else 0)
                
            elif opcode == "BUILD_LIST":
                new_list = []
                # Pop arguments in reverse order to maintain list order
                for _ in range(arg):
                    new_list.insert(0, self.stack.pop())
                self.stack.append(new_list)
                
            elif opcode == "BINARY_SUBSCR":
                index = self.stack.pop()
                target = self.stack.pop()
                self.stack.append(target[int(index)])
                
            elif opcode == "PRINT":
                val = self.stack.pop()
                print(val)
                self.output_buffer.append(str(val))
                
            elif opcode == "INPUT":
                prompt = self.stack.pop()
                val = input(prompt)
                try:
                     self.stack.append(float(val))
                except:
                     self.stack.append(val)
                
            elif opcode == "JUMP_IF_FALSE":
                cond = self.stack.pop()
                if not cond:
                    self.ip = arg
                    
            elif opcode == "JUMP_ABSOLUTE":
                self.ip = arg
                
            else:
                raise Exception(f"VM Error: Unknown OpCode '{opcode}'")
                
        return "\n".join(self.output_buffer) + "\n" if len(self.output_buffer) > 0 else ""
