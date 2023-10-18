class SymbolTable:
    def __init__(self):
        self.symbol_table = {
            f'R{i}': i for i in range(32)
        }
    
    def add_symbol(self, symbol, value):
        self.symbol_table[symbol] = value