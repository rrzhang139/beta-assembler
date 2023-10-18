class Parser:
    def __init__(self):
        pass
    
    def has_literal(self, opcode):
      """
      Check if the given opcode uses a literal.
      """
      if opcode.endswith("C") or opcode in ['BEQ', 'BNE', 'LD', 'LDR']:
          return True
      return False

    def parse_instruction(self, instruction):
        # Given an assembly instruction, parse it and return its components
        # E.g., "ADD(R1, R2, R3)" should return ("ADD", "R1", "R2", "R3")
        opcode, body = instruction.split("(")
        literal = self.has_literal(opcode)
        if len(body.split(",")) == 3:
            dest, src1, src2 = body.split(",")
            src2 = src2[:-1] # remove the trailing ')'
            return (opcode, dest.strip(), src1.strip(), src2.strip(), literal)
        elif len(body.split(",")) == 2:
            src1, src2 = body.split(",")
            src2 = src2[:-1] # remove the trailing ')'
            return (opcode, src1.strip(), src2.strip(), None, literal)
        else:
            return (opcode, None, None, None, literal)
      


