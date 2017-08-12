import unittest
import theseusBrain
import baseRoomDetectionBrain

class TheseusBrainTestCase(unittest.TestCase):
	
	def setUp(self):
		return
		
	def tearDown(self):
		return
		
	def testTheseusBrain_extendsBaseBrain(self):
		self.assertEqual(True, issubclass(theseusBrain.TheseusBrain, baseRoomDetectionBrain.BaseRoomDetectionBrain))
	

if __name__ == "__main__":
	unittest.main()