import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import unittest
from src.signal_generation.signal_generator import generate_signal

class TestSignalGenerator(unittest.TestCase):
    def test_generate_signal_no_trades(self):
        result = generate_signal("FIL-USD")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
