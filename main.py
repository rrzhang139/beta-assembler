from parser import Parser
from code import Code
from symbol_table import SymbolTable

def main(input_file, output_file):
    parser = Parser()
    code = Code()
    symbol_table = SymbolTable()

    with open(input_file, 'r') as infile:
        # First pass: symbols
        for line in infile:
          # Checks if this line is a symbol
          if line.__contains__('='):
            # Adds the symbol to the symbol table
            symbol, value = line.strip().split('=')
            symbol_table.add_symbol(symbol.strip(), value.strip())
          elif line.__contains__(':'):
             # Adds the label to the symbol table
            label, value = line.strip().split(':')
            symbol_table.add_symbol(label.strip(), value.strip())

    
    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile:
        # Second pass: converting assembly to machine code
        for line in infile:
            # Skip empty lines, symbol intialization, and labels
            if line.__contains__('=') or line.__contains__(':') or line.strip() == '':
              continue
            
            # Parse the instruction into its components
            parsed_instruction = parser.parse_instruction(line.strip())

            # Translate each component into binary
            opcode, ra, rb, rc, literal = parsed_instruction
            binary_opcode = code.translate_opcode(opcode)
            binary_ra = code.translate_operand(ra, symbol_table.symbol_table)
            binary_rb = code.translate_operand(rb, symbol_table.symbol_table, literal)

            # Combine these into a single 32-bit instruction (for Beta ISA)
            binary_instruction = None
            if rc:
              binary_rc = code.translate_operand(rc, symbol_table.symbol_table)
              if literal:
                literal_operand = binary_rb
                binary_instruction = (binary_opcode << 26) | (binary_rc << 21) | (binary_ra << 16) | (literal_operand)
              else:
                binary_instruction = (binary_opcode << 26) | (binary_rc << 21) | (binary_ra << 16) | (binary_rb << 11)
            else: # It's a Jump instruction (0x1B)
              binary_instruction = (binary_opcode << 26) | (binary_rc << 21) | (binary_ra << 16)
            # print(binary_instruction.to_bytes(4))
            data = binary_instruction.to_bytes(4)
            hex_representation = ''.join(f'{byte:02x}' for byte in data)
            print(hex_representation)
            # Write the binary instruction to the output file
            outfile.write(binary_instruction.to_bytes(4, byteorder='little'))
# 1100 0000 0011 1111
if __name__ == "__main__":
    main('input.asm', 'output.bin')
