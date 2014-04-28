import unittest
import modules.peech

class TestPeech(unittest.TestCase):

    def setUp(self):
        self.phenny = FakePhenny()

    def test_sci(self):
        self.tell_phenny('scientific')
        assert self.phenny.response is None

    def test_sca(self):
        self.tell_phenny('scatological')
        assert self.phenny.response is not None
    
    def tell_phenny(self, text):
        modules.peech.correct(self.phenny, FakeInput(text))

class FakePhenny:

    def __init__(self):
        self.response = None

    def reply(self, text):
        self.response = text

class FakeInput:

    def __init__(self, text):
        self.text = text

    def group(self):
        return self.text

    def nick(self):
        return 'testchild'

if __name__ == '__main__':
    unittest.main()
