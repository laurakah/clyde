import unittest
import dullBrain
import baseBrain

def fakeCallback():
	return

class DullBrainTestCase(unittest.TestCase):

	def setUp(self):
 		self.inputs = {"isCollision": fakeCallback, "getOrientation": fakeCallback, "getMovementDirection": fakeCallback}
 		self.outputs = {"setOrientation": fakeCallback, "setMovementDirection": fakeCallback, "move": fakeCallback}
 		self.b = dullBrain.DullBrain(self.inputs, self.outputs)

	def tearDown(self):
		return

	def testIsSubclass_ofBaseBrain(self):
		self.assertEqual(True, issubclass(dullBrain.DullBrain, baseBrain.BaseBrain))
		
	def testStep_doesNotRaiseNotImplementedException(self):
		self.b.step()
		self.assertTrue(True)
		
	def testIsFinished_doesNotRaiseNotImplementedException(self):
		self.b.isFinished()
		self.assertTrue(True)
		
	def testIsFinished_returnsFalse(self):
		self.assertEqual(False, self.b.isFinished())
	
	
if __name__ == '__main__':
	unittest.main()
