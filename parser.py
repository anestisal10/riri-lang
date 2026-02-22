from dataclasses import dataclass

class ASTNode:
    line: int = 1
    column: int = 0

# --- AST Node Definitions ---
@dataclass
class Number(ASTNode):
    value: int
    line: int = 1
    column: int = 0

@dataclass
class String(ASTNode):
    value: str
    line: int = 1
    column: int = 0

@dataclass
class BinOp(ASTNode):
    left: any
    op: str
    right: any
    line: int = 1
    column: int = 0

# --- NEW NODES ---
@dataclass
class Assign(ASTNode):
    name: str
    value: any
    line: int = 1
    column: int = 0

@dataclass
class Var(ASTNode):
    name: str
    line: int = 1
    column: int = 0

@dataclass
class If(ASTNode):
    condition: any
    true_branch: list
    false_branch: list
    line: int = 1
    column: int = 0

@dataclass
class While(ASTNode):
    condition: any
    body: list
    line: int = 1
    column: int = 0

@dataclass  
class FunctionCall(ASTNode):
    name: str
    args: list
    line: int = 1
    column: int = 0

@dataclass
class FunctionDef(ASTNode):
    name: str
    args: list
    body: list
    line: int = 1
    column: int = 0

@dataclass
class ArrayDef(ASTNode):
    elements: list
    line: int = 1
    column: int = 0

@dataclass
class IndexAccess(ASTNode):
    target: any
    index: any
    line: int = 1
    column: int = 0


# --- Parser Class ---
class Parser:
    def __init__(self, tokens):
        # Convert to list so we can peek ahead
        self.tokens = list(tokens)
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def peek(self):
        """Look at the next token without consuming the current one."""
        peek_pos = self.pos + 1
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None

    def eat(self, token_type):
        if self.current_token and (self.current_token.type == token_type or self.current_token.value == token_type):
            self.advance()
        else:
            line = self.current_token.line if self.current_token else "EOF"
            col = self.current_token.column if self.current_token else "EOF"
            raise Exception(f"Syntax Error on line {line}, column {col}: Expected '{token_type}', but got '{self.current_token.type if self.current_token else 'EOF'}'")

    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return Number(token.value, token.line, token.column)
        
        elif token.type == 'STRING':
            self.eat('STRING')
            return String(token.value, token.line, token.column)
        
        # --- NEW: Handle Variable Access ---
        elif token.type == 'IDENTIFIER':
            line, col = token.line, token.column
            self.eat('IDENTIFIER')

            if self.current_token and self.current_token.type == '(':
                self.eat('(')
                args = []
                # Very simple argument parsing (handles 1 argument for now)
                if self.current_token.type != ')':
                    args.append(self.expression())
                self.eat(')')
                return FunctionCall(token.value, args, line, col)

            if self.current_token and self.current_token.type == '[':
                self.eat('[')
                index_expr = self.expression()
                self.eat(']')
                return IndexAccess(Var(token.value, line, col), index_expr, line, col)

            return Var(token.value, line, col)

        elif token.type == '[':
            line, col = token.line, token.column
            self.eat('[')
            elements = []
            if self.current_token and self.current_token.type != ']':
                elements.append(self.expression())
                while self.current_token and self.current_token.type == ',':
                    self.eat(',')
                    elements.append(self.expression())
            self.eat(']')
            return ArrayDef(elements, line, col)

        elif token.type == 'DEFINE':
            line, col = token.line, token.column
            self.eat('DEFINE')
            name = self.current_token.value
            self.eat('IDENTIFIER')

            if self.current_token and self.current_token.type == '(':
                self.eat('(')
                args = []
                
                if self.current_token.type != ')':
                    args.append(self.expression())
                self.eat(')')
                body = []
                while self.current_token and self.current_token.type != 'END':
                    body.append(self.statement())
                self.eat('END')
            
            return FunctionDef(name=name, args=args, body=body, line=line, column=col)

        elif token.type == '(':
            self.eat('(')
            node = self.expression()
            self.eat(')')
            return node
        
        line = token.line if token else "EOF"
        col = token.column if token else "EOF"
        raise Exception(f"Syntax Error on line {line}, column {col}: Invalid syntax at '{token.type if token else 'EOF'}'")

    def term(self):
        node = self.factor()
        while self.current_token and self.current_token.type in ('*', '/'):
            token = self.current_token
            self.eat(token.type) # Using type to eat * or /
            node = BinOp(left=node, op=token.type, right=self.factor(), line=token.line, column=token.column)
        return node

    def arithmetic(self):
        node = self.term()
        while self.current_token and self.current_token.type in ('+', '-'):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token.type, right=self.term(), line=token.line, column=token.column)
        return node
    
    def expression(self):
        node = self.arithmetic()
        # Check for comparison operators
        while self.current_token and self.current_token.type in ('>', '<'):
            token = self.current_token
            self.eat(token.type)
            # Compare the left side with the right side (recursively calling arithmetic)
            node = BinOp(left=node, op=token.type, right=self.arithmetic(), line=token.line, column=token.column)
        return node

    # --- NEW: Determine if it's Assignment or Expression ---
    def statement(self):
        # Check if we have "IDENTIFIER ="
        if (self.current_token.type == 'IDENTIFIER' and 
            self.peek() is not None and 
            self.peek().type == 'EQUALS'):
            
            var_name = self.current_token.value
            line, col = self.current_token.line, self.current_token.column
            
            self.eat('IDENTIFIER')
            self.eat('EQUALS')
            expr = self.expression()
            return Assign(name=var_name, value=expr, line=line, column=col)
        elif self.current_token.type == 'IF':
            line, col = self.current_token.line, self.current_token.column
            self.eat('IF')
            condition = self.expression()
            true_branch = []
            false_branch = []
            
            # Parse statements until we hit ELSE or END
            while self.current_token and self.current_token.type not in ('ELSE', 'END'):
                true_branch.append(self.statement())
            
            # Handle Optional ELSE (kotsif)
            if self.current_token.type == 'ELSE':
                self.eat('ELSE')
                while self.current_token and self.current_token.type != 'END':
                    false_branch.append(self.statement())
            
            self.eat('END') # Expect 'telos' to close the block
            return If(condition=condition, true_branch=true_branch, false_branch=false_branch, line=line, column=col)
        elif self.current_token.type == 'WHILE':
            line, col = self.current_token.line, self.current_token.column
            self.eat('WHILE')
            condition = self.expression()
            body = []
            
            
            # Parse statements until we hit ELSE or END
            while self.current_token and self.current_token.type not in ('END'):
                body.append(self.statement())
            
            
            self.eat('END') # Expect 'telos' to close the block
            return While(condition=condition, body=body, line=line, column=col)
        else:
            # Otherwise it's just a math expression (e.g., 5 + x)
            return self.expression()

    def parse(self):
        """Returns a list of statements"""
        statements = []
        while self.current_token is not None:
            statements.append(self.statement())
        return statements