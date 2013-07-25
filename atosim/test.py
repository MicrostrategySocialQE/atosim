'''
Created on 2013-7-10

@author: xumingze
'''

import unittest
from atosim import Simulator
import atomac
import time
    
class Constants:
    bid = "com.apple.iphonesimulator"
    
class TestCase(unittest.TestCase):
    
    def setUp(self):
        
        unittest.TestCase.setUp(self)
        
    
    def tearDown(self):
#        atomac.terminateAppByBundleId(Constants.bid)
        unittest.TestCase.tearDown(self)
        
    def testInitSimClass(self):
        sim = Simulator()
        self.assertTrue(sim.isRunning())
        sim.quit()
        self.assertFalse(sim.isRunning())
        pass
    
    def testFindApp(self):
        sim = Simulator()

        app = sim.findAppsByName("Safari")
        self.assertTrue(app.__len__()>0)
                
    def testMenuOpts(self):
        sim = Simulator()
        sim.reset()
        app = sim.findAppsByName("Safari")
        self.assertTrue(app.__len__() > 0)
        sim.rotateToLeft()
        time.sleep(1)
        sim.rotateToRight()
        sim.enablePrinter()
        
    def testActivateEditModeForTaskManager(self):
        sim = Simulator()
        sim.toggleTaskManager()
        sim.activateEditMode('Safari')
        
    def DtestDrag(self):
        sim = Simulator()        
        app = sim.findAppsByName('Safari')[0]
        coord = app.getPosition()
        dest_coord = (coord[0]+200, coord[1])
        app.dragMouseButtonLeft(coord, dest_coord)
    
    def testLaunchApp(self):
        sim = Simulator()
        sim.launchApp("Safari")
            
    if __name__ == '__main__':
        unittest.main()    
        
        