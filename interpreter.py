import lexer
import parser as prsr
import argparse
from dataclasses import dataclass
import time
import io
import compiler
from vm import VirtualMachine

class TimeoutException(Exception):
    pass

@dataclass
class NativeFunction:
    func: callable

class Evaluator:
    def __init__(self, timeout=None):
        self.start_time = time.time()
        self.timeout = timeout

    def evaluate(self, node, env):
        if self.timeout and time.time() - self.start_time > self.timeout:
            raise TimeoutException(f"Execution exceeded timeout of {self.timeout} seconds.")

        # 1. Handle Numbers and Primitives
        if isinstance(node, prsr.Number):
            return float(node.value)
        
        if isinstance(node, prsr.String):
            return node.value

        if isinstance(node, prsr.ArrayDef):
            return [self.evaluate(element, env) for element in node.elements]
            
        if isinstance(node, prsr.IndexAccess):
            target = self.evaluate(node.target, env)
            index = self.evaluate(node.index, env)
            
            if not isinstance(target, list):
                raise Exception(f"Runtime Error on line {node.line}, column {node.column}: Target is not accessible by index.")
                
            try:
                # Ensure integer index
                return target[int(index)]
            except Exception as e:
                raise Exception(f"Runtime Error on line {node.line}, column {node.column}: Array index out of bounds or invalid ({e}).")

        # 2. Handle Binary Operations
        if isinstance(node, prsr.BinOp):
            left_val = self.evaluate(node.left, env)
            right_val = self.evaluate(node.right, env)

            if node.op == '+': return left_val + right_val
            elif node.op == '-': return left_val - right_val
            elif node.op == '*': return left_val * right_val
            elif node.op == '/': return left_val / right_val
            elif node.op == '>': return 1 if left_val > right_val else 0
            elif node.op == '<': return 1 if left_val < right_val else 0
        
        # 3. Handle Assignment (Save to env)
        if isinstance(node, prsr.Assign):
            value = self.evaluate(node.value, env)
            env[node.name] = value
            return value

        # 4. Handle Variable Access (Read from env)
        if isinstance(node, prsr.Var):
            if node.name in env:
                if isinstance(env[node.name], NativeFunction):
                    return env[node.name].func
                return env[node.name]
            else:
                raise Exception(f"Runtime Error on line {node.line}, column {node.column}: Monkey Lord PITIS is angry! Variable '{node.name}' not defined.")
            
        if isinstance(node, prsr.FunctionDef):
            # Store the function definition in the environment
            env[node.name] = node
            return None # Function definitions don't return a value
            
        if isinstance(node, prsr.FunctionCall):
            func_value = env.get(node.name)
            
            if not func_value:
                raise Exception(f"Runtime Error on line {node.line}, column {node.column}: Function '{node.name}' not defined.")
            
            # Evaluate arguments
            arg_values = [self.evaluate(arg, env) for arg in node.args]
            
            if isinstance(func_value, prsr.FunctionDef):
                local_env = env.copy() # Create a new environment for the function call
                for param, val in zip(func_value.args, arg_values):
                    local_env[param.name] = val
                for stmt in func_value.body:
                    self.evaluate(stmt, local_env)
                return None

            # Check if it's a native function
            if isinstance(func_value, NativeFunction):
                return func_value.func(*arg_values)
            else:
                raise Exception(f"Runtime Error on line {node.line}, column {node.column}: '{node.name}' is not a callable function.")
        
        if isinstance(node, prsr.If):
            # Evaluate the condition (Non-zero is true)
            condition = self.evaluate(node.condition, env)
            
            if condition:
                # Execute all statements in the true branch
                for stmt in node.true_branch:
                    self.evaluate(stmt, env)
            else:
                # Execute all statements in the false branch
                for stmt in node.false_branch:
                    self.evaluate(stmt, env)
            return None # If statements don't return a value
        
        if isinstance(node, prsr.While):
            # Evaluate the condition (Non-zero is true)
            condition = self.evaluate(node.condition, env)
            
            while condition:
                # Execute all statements in the true branch
                for stmt in node.body:
                    self.evaluate(stmt, env)
                # Re-evaluate the condition after executing the body
                condition = self.evaluate(node.condition, env)
            return None # If statements don't return a value

        raise Exception(f"Unknown node type: {type(node)}")

def run(text, timeout=None, capture_output=False, use_vm=False, debug_vm=False):
    # 1. Lexing
    tokens = lexer.lexer(text)
    
    # 2. Parsing (Get a list of statements)
    p = prsr.Parser(tokens)
    statements = p.parse()
    
    # Setup output capture
    output_buffer = io.StringIO() if capture_output else None
    
    if use_vm:
        instructions, constants = compiler.compile_ast(statements)
        
        if debug_vm:
            debug_str = "--- BYTECODE GENERATED ---\n"
            for i, (op, arg) in enumerate(instructions):
                debug_str += f"{str((i)).zfill(3)} {op:<15} {arg if arg is not None else ''}\n"
            debug_str += f"Constants pool: {constants}\n"
            debug_str += "--- EXECUTING OPCODES ---\n"
            
            if capture_output:
                print(debug_str, file=output_buffer)
            else:
                print(debug_str)
                
        machine = VirtualMachine(instructions, constants)
        output = machine.run()
        
        if capture_output:
            # We append the VM's buffered print statements
            print(output, file=output_buffer, end="")
            return output_buffer.getvalue()
        return

    def builtin_print(*args, **kwargs):
        if capture_output:
            print(*args, file=output_buffer, **kwargs)
        else:
            print(*args, **kwargs)
            
    def builtin_input(prompt):
        if capture_output:
            raise Exception("Input is not supported in non-interactive mode. Monkey Lord PITIS is angry!")
        return float(input(prompt))
    
    # 3. Interpreting
    evaluator = Evaluator(timeout=timeout)
    env = {
        'fwnakse': NativeFunction(builtin_print), 
        'skalise': NativeFunction(builtin_input)
    } # This is your memory/variable storage
    
    for stmt in statements:
        evaluator.evaluate(stmt, env)
            
    if capture_output:
        return output_buffer.getvalue()

def _generate_mermaid_node(node, lines, counter):
    node_id = f"node_{counter[0]}"
    counter[0] += 1
    
    if isinstance(node, prsr.Number):
        lines.append(f'{node_id}["Number({node.value})"]')
    elif isinstance(node, prsr.String):
        lines.append(f'{node_id}["String({node.value})"]')
    elif isinstance(node, prsr.Var):
        lines.append(f'{node_id}["Variable({node.name})"]')
    elif isinstance(node, prsr.ArrayDef):
        lines.append(f'{node_id}["ArrayDef"]')
        for val in node.elements:
            val_id = _generate_mermaid_node(val, lines, counter)
            lines.append(f'{node_id} -->|Element| {val_id}')
    elif isinstance(node, prsr.IndexAccess):
        lines.append(f'{node_id}["IndexAccess"]')
        target_id = _generate_mermaid_node(node.target, lines, counter)
        index_id = _generate_mermaid_node(node.index, lines, counter)
        lines.append(f'{node_id} -->|Target| {target_id}')
        lines.append(f'{node_id} -->|Index| {index_id}')
    elif isinstance(node, prsr.BinOp):
        lines.append(f'{node_id}["BinOp({node.op})"]')
        left_id = _generate_mermaid_node(node.left, lines, counter)
        right_id = _generate_mermaid_node(node.right, lines, counter)
        lines.append(f'{node_id} --> {left_id}')
        lines.append(f'{node_id} --> {right_id}')
    elif isinstance(node, prsr.Assign):
        lines.append(f'{node_id}["Assign({node.name})"]')
        val_id = _generate_mermaid_node(node.value, lines, counter)
        lines.append(f'{node_id} --> {val_id}')
    elif isinstance(node, prsr.If):
        lines.append(f'{node_id}["If Statement"]')
        cond_id = _generate_mermaid_node(node.condition, lines, counter)
        lines.append(f'{node_id} -->|Condition| {cond_id}')
        
        true_block_id = f"node_{counter[0]}"; counter[0] += 1
        lines.append(f'{true_block_id}["True Branch"]')
        lines.append(f'{node_id} -->|Then| {true_block_id}')
        for stmt in node.true_branch:
            stmt_id = _generate_mermaid_node(stmt, lines, counter)
            lines.append(f'{true_block_id} --> {stmt_id}')
            
        if node.false_branch:
            false_block_id = f"node_{counter[0]}"; counter[0] += 1
            lines.append(f'{false_block_id}["False Branch"]')
            lines.append(f'{node_id} -->|Else| {false_block_id}')
            for stmt in node.false_branch:
                stmt_id = _generate_mermaid_node(stmt, lines, counter)
                lines.append(f'{false_block_id} --> {stmt_id}')
    elif isinstance(node, prsr.While):
        lines.append(f'{node_id}["While Loop"]')
        cond_id = _generate_mermaid_node(node.condition, lines, counter)
        lines.append(f'{node_id} -->|Condition| {cond_id}')
        
        body_block_id = f"node_{counter[0]}"; counter[0] += 1
        lines.append(f'{body_block_id}["Loop Body"]')
        lines.append(f'{node_id} -->|Do| {body_block_id}')
        for stmt in node.body:
            stmt_id = _generate_mermaid_node(stmt, lines, counter)
            lines.append(f'{body_block_id} --> {stmt_id}')
    elif isinstance(node, prsr.FunctionCall):
        lines.append(f'{node_id}["Call({node.name})"]')
        for arg in node.args:
            arg_id = _generate_mermaid_node(arg, lines, counter)
            lines.append(f'{node_id} -->|Arg| {arg_id}')
    elif isinstance(node, prsr.FunctionDef):
        lines.append(f'{node_id}["Def({node.name})"]')
        for arg in node.args:
            arg_id = _generate_mermaid_node(arg, lines, counter)
            lines.append(f'{node_id} -->|Param| {arg_id}')
        body_id = f"node_{counter[0]}"; counter[0] += 1
        lines.append(f'{body_id}["Body"]')
        lines.append(f'{node_id} -->|Do| {body_id}')
        for stmt in node.body:
            stmt_id = _generate_mermaid_node(stmt, lines, counter)
            lines.append(f'{body_id} --> {stmt_id}')
    else:
        lines.append(f'{node_id}["Unknown Node"]')
        
    return node_id

def visualize_ast(text):
    tokens = lexer.lexer(text)
    p = prsr.Parser(tokens)
    statements = p.parse()
    
    counter = [0]
    lines = ["```mermaid", "graph TD"]
    
    root_id = f"node_{counter[0]}"
    counter[0] += 1
    lines.append(f'{root_id}["Program"]')
    
    for stmt in statements:
        stmt_id = _generate_mermaid_node(stmt, lines, counter)
        lines.append(f'{root_id} --> {stmt_id}')
        
    lines.append("```")
    return "\n".join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="name of the file to interpret")
    parser.add_argument("--vm", action="store_true", help="Execute using Bytecode Virtual Machine")
    parser.add_argument("--debug-vm", action="store_true", help="Print VM Bytecode")
    args = parser.parse_args()
    
    if not args.file.startswith("PITIS"):
        raise ValueError("Only files starting with 'PITIS' are allowed, all praise monkey lord PITIS!")
    
    text = open(args.file).read()
    
    # Run the interpreter sequence
    run(text, use_vm=args.vm, debug_vm=args.debug_vm)
