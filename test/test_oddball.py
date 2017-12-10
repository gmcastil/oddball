import unittest
from oddball import oddball

class TestParseInstruction(unittest.TestCase):
    """Verify that source lines are parsed correctly with and without labels"""

    def test_accumulator(self):
        "Test accumulator addressing mode"
        instruction = 'rol a'
        expected = {'label' : None, 'mneumonic' : 'rol', 'operands' : 'a'}
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)
        # Now test with a label
        instruction = 'test_label:' + '    ' + instruction
        expected['label'] = 'test_label'
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)

    def test_relative(self):
        "Test relative addressing mode"
        instruction = 'bpl label'
        expected = {'label' : None, 'mneumonic' : 'bpl', 'operands' : 'label'}
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)
        # Now test with a label
        instruction = 'test_label:' + '    ' + instruction
        expected['label'] = 'test_label'
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)

    def test_implied(self):
        "Test implied addressing mode"
        instruction = 'brk'
        expected = {'label' : None, 'mneumonic' : 'brk', 'operands' : None}
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)
        # Now test with a label
        instruction = 'test_label:' + '    ' + instruction
        expected['label'] = 'test_label'
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)

    def test_immediate(self):
        "Test immediate addressing mode"
        instruction = 'adc #$44'
        expected = {'label' : None, 'mneumonic' : 'adc', 'operands' : '#$44'}
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)
        # Now test with a label
        instruction = 'test_label:' + '    ' + instruction
        expected['label'] = 'test_label'
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)

    def test_zp(self):
        "Test zero page addressing mode"
        instruction = 'adc $44'
        expected = {'label' : None, 'mneumonic' : 'adc', 'operands' : '$44'}
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)
        # Now test with a label
        instruction = 'test_label:' + '    ' + instruction
        expected['label'] = 'test_label'
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)

    def test_zp_x(self):
        "Test zero page X addressing mode"
        instruction = 'adc $44, x'
        expected = {'label' : None, 'mneumonic' : 'adc', 'operands' : '$44, x'}
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)
        # Now test with a label
        instruction = 'test_label:' + '    ' + instruction
        expected['label'] = 'test_label'
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)

    def test_abs(self):
        "Test absolute addressing mode"
        instruction = 'adc $4400'
        expected = {'label' : None, 'mneumonic' : 'adc', 'operands' : '$4400'}
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)
        # Now test with a label
        instruction = 'test_label:' + '    ' + instruction
        expected['label'] = 'test_label'
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)

    def test_abs_x(self):
        "Test absolute X addressing mode"
        instruction = 'adc $4400, x'
        expected = {'label' : None, 'mneumonic' : 'adc', 'operands' : '$4400, x'}
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)
        # Now test with a label
        instruction = 'test_label:' + '    ' + instruction
        expected['label'] = 'test_label'
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)

    def test_abs_y(self):
        "Test absolute Y addressing mode"
        instruction = 'adc $4400, y'
        expected = {'label' : None, 'mneumonic' : 'adc', 'operands' : '$4400, y'}
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)
        # Now test with a label
        instruction = 'test_label:' + '    ' + instruction
        expected['label'] = 'test_label'
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)

    def test_ind_x(self):
        "Test indirect X addressing mode"
        instruction = 'adc ($44, x)'
        expected = {'label' : None, 'mneumonic' : 'adc', 'operands' : '($44, x)'}
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)
        # Now test with a label
        instruction = 'test_label:' + '    ' + instruction
        expected['label'] = 'test_label'
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)

    def test_ind_y(self):
        "Test indirect Y addressing mode"
        instruction = 'adc ($44), y'
        expected = {'label' : None, 'mneumonic' : 'adc', 'operands' : '($44), y'}
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)
        # Now test with a label
        instruction = 'test_label:' + '    ' + instruction
        expected['label'] = 'test_label'
        result = oddball.parse_line(instruction)
        self.assertEqual(expected, result)

class TestParseAddress(unittest.TestCase):
    """Verify that addressing modes are inferred correctly from operands"""

    def test_accumulator(self):
        "Test accumulator addressing mode"
        operands = 'a'
        expected = 'acc'
        result = oddball.parse_addr_mode(operands)
        self.assertEqual(expected, result)

    def test_relative(self):
        "Test relative addressing mode"
        operands = 'test_label'
        expected = 'rel'
        result = oddball.parse_addr_mode(operands)
        self.assertEqual(expected, result)

    def test_implied(self):
        "Test implied addressing mode"
        operands = ''
        expected = 'imp'
        result = oddball.parse_addr_mode(operands)
        self.assertEqual(expected, result)

    def test_immediate(self):
        "Test immediate addressing mode"
        operands = '#$44'
        expected = 'imm'
        result = oddball.parse_addr_mode(operands)
        self.assertEqual(expected, result)

    def test_zp(self):
        "Test zero page addressing mode"
        operands = '$44'
        expected = 'zp'
        result = oddball.parse_addr_mode(operands)
        self.assertEqual(expected, result)

    def test_zp_x(self):
        "Test zero page X addressing mode"
        operands = '$44, x'
        expected = 'zp x'
        result = oddball.parse_addr_mode(operands)
        self.assertEqual(expected, result)

    def test_abs(self):
        "Test absolute addressing mode"
        operands = '$4400'
        expected = 'abs'
        result = oddball.parse_addr_mode(operands)
        self.assertEqual(expected, result)

    def test_abs_x(self):
        "Test absolute X addressing mode"
        operands = '$4400, x'
        expected = 'abs x'
        result = oddball.parse_addr_mode(operands)
        self.assertEqual(expected, result)

    def test_abs_y(self):
        "Test absolute Y addressing mode"
        operands = '$4400, y'
        expected = 'abs y'
        result = oddball.parse_addr_mode(operands)
        self.assertEqual(expected, result)

    def test_ind_x(self):
        "Test indirect X addressing mode"
        operands = '($44, x)'
        expected = 'ind x'
        result = oddball.parse_addr_mode(operands)
        self.assertEqual(expected, result)

    def test_ind_y(self):
        "Test indirect Y addressing mode"
        operands = '($44), y'
        expected = 'ind y'
        result = oddball.parse_addr_mode(operands)
        self.assertEqual(expected, result)


class TestLowerByte(unittest.TestCase):
    """Test that lower bytes are returned correctly"""
    def test_low_bytes(self):

        # Test one byte modes

        # Accumulator
        expected = ''
        low_byte_result = oddball.LOWER_BYTE['acc']('a')
        self.assertEqual(expected, low_byte_result)
        # Implied
        expected = ''
        low_byte_result = oddball.LOWER_BYTE['imp']('')
        self.assertEqual(expected, low_byte_result)

        # Test two byte modes

        # Relative
        expected = 'test_label'
        low_byte_result = oddball.LOWER_BYTE['rel']('test_label')
        self.assertEqual(expected, low_byte_result)

        # Immediate
        expected = '34'
        low_byte_result = oddball.LOWER_BYTE['imm']('#$34')
        self.assertEqual(expected, low_byte_result)

        # Zero page
        low_byte_result = oddball.LOWER_BYTE['zp']('$34')
        self.assertEqual(expected, low_byte_result)

        # Zero page, X
        low_byte_result = oddball.LOWER_BYTE['zp x']('$34,x')
        self.assertEqual(expected, low_byte_result)

        # Indirect, X
        low_byte_result = oddball.LOWER_BYTE['ind x']('($34,x)')
        self.assertEqual(expected, low_byte_result)

        # Indirect, Y
        low_byte_result = oddball.LOWER_BYTE['ind y']('($34),y')
        self.assertEqual(expected, low_byte_result)

        # Test three byte modes

        # Absolute
        low_byte_result = oddball.LOWER_BYTE['abs']('$1234')
        self.assertEqual(expected, low_byte_result)

        # Absolute, X
        low_byte_result = oddball.LOWER_BYTE['abs x']('$1234,x')
        self.assertEqual(expected, low_byte_result)

        # Absolute, Y
        low_byte_result = oddball.LOWER_BYTE['abs y']('$1234,y')
        self.assertEqual(expected, low_byte_result)

class TestUpperByte(unittest.TestCase):
    """Test that upper bytes are returned correctly"""


if __name__ == "__main__":
    unittest.main()
