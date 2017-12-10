import unittest
import oddball

class TestOddballParseInstruction(unittest.TestCase):

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

if __name__ == "__main__":
    unittest.main()
