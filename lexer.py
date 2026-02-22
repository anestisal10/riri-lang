from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: any = None
    line: int = 1
    column: int = 0

def lexer(text):
    text_iter = iter(text)
    current_char = next(text_iter, None)
    
    line = 1
    column = 1
    
    def advance():
        nonlocal current_char, line, column
        if current_char == '\n':
            line += 1
            column = 1
        else:
            column += 1
        current_char = next(text_iter, None)

    while current_char is not None:
        # Ignore whitespace
        if current_char.isspace():
            advance()
            continue
            
        start_col = column
        
        # Handle numbers
        if current_char.isdigit():
            num_str = ""
            while current_char is not None and current_char.isdigit():
                num_str += current_char
                advance()
            yield Token('NUMBER', int(num_str), line, start_col)
            
        elif current_char == '"':
            id_str = ""
            advance() # skip opening quote
            while current_char is not None and (current_char.isalnum() or current_char == " ") and current_char != '"':
                id_str += current_char
                advance()
            if current_char == '"':
                advance() # Consume closing quote
            yield Token('STRING', id_str, line, start_col)
        
        # --- Handle Identifiers (Variable names) ---
        elif current_char.isalpha():
            id_str = ""
            while current_char is not None and current_char.isalnum():
                id_str += current_char
                advance()
            
            if id_str == "if":
                yield Token('IF', None, line, start_col)
            elif id_str == "kotsif":
                yield Token('ELSE', None, line, start_col)
            elif id_str == "miaou":      
                yield Token('END', None, line, start_col)
            elif id_str == "skarfalwnontas":
                yield Token('WHILE', None, line, start_col)
            elif id_str == "banana":
                yield Token('DEFINE', None, line, start_col)
            else:
                yield Token('IDENTIFIER', id_str, line, start_col)

        # --- Handle Assignment Operator ---
        elif current_char == '=':
            yield Token('EQUALS', '=', line, start_col)
            advance()

        # Handle operators and brackets
        elif current_char in '+-*/()<>[],':
            yield Token(current_char, None, line, start_col)
            advance()
        
        else:
            # Skip unknown characters or raise error
            raise ValueError(f"Lexical Error on line {line}, column {column}: Unknown character '{current_char}'")
            advance()