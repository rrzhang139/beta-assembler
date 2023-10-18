class Code:
    def __init__(self):
        # Initialize any mappings from mnemonic to opcode here
        self.opcode_mapping = {
          'ADD':   0b100000,
          'ADDC':  0b110000,
          'AND':   0b101000,
          'ANDC':  0b111000,
          'BEQ':   0b11101,
          'BNE':   0b11110,
          'CMPEQ': 0b100100,
          'CMPEQC':0b110100,
          'CMPLE': 0b100110,
          'CMPLEC':0b110110,
          'CMPLT': 0b100101,
          'CMPLTC':0b110101,
          'DIV':   0b100011,
          'DIVC':  0b110011,
          'JMP':   0b11011,
          'LD':    0b11000,
          'LDR':   0b11111,
          'MUL':   0b100010,
          'MULC':  0b110010,
          'OR':    0b101001,
          'ORC':   0b111001,
          'SHL':   0b101100,
          'SHLC':  0b111100,
          'SHR':   0b101101,
          'SHRC':  0b111101,
          'SRA':   0b101110,
          'SRAC':  0b111110,
          'SUB':   0b100001,
          'SUBC':  0b110001,
          'ST':    0b11001,
          'XOR':   0b101010,
          'XORC':  0b111010
      }

    def translate_opcode(self, opcode):
        # Translate the opcode into its binary representation
        return self.opcode_mapping.get(opcode, None)

    def translate_operand(self, operand, symbol_table, literal=False):
        # Translate the operand into its binary representation, use symbol table if necessary
        
        # Check if operand is a symbol in the symbol table
        if operand in symbol_table:
            # if its a register 
            if operand.startswith('R'):
              return symbol_table[operand]
            # if its a label?????
            operand = int(symbol_table[operand])
        
        # If it's not a symbol or label, it must be a literal
        if literal:
          try:
              value = int(operand)
              return self.sign_extend_to_16(value)
          except ValueError:
              pass  # not a literal
        
        raise ValueError(f"Invalid operand: {operand}. It's neither a known register, a defined symbol, nor a literal.")


    def sign_extend_to_16(self, value):
      """
      Sign extend the given value to 16 bits.
      """
      # Convert the value to binary and remove the '0b' prefix
      binary_repr = bin(value & 0xFFFF)[2:]

      # Ensure the literal does not exceed 16 bits
      assert len(binary_repr) <= 16, "Literal exceeds 16-bit limit"

      # Identify the bit width by finding the sign change position
      for i in range(len(binary_repr) - 1, 0, -1):
          if binary_repr[i] != binary_repr[i-1]:
              bit_width = i + 1
              break
      else:
          bit_width = 1  # This is the case when all bits are the same

      # Sign extend the value
      msb = binary_repr[0]
      while len(binary_repr) < 16:
          binary_repr = msb + binary_repr

      return int(binary_repr, 2)