'''
Created on 2013-7-10

@author: xumingze
'''
import atomac
import time
from atomac.AXClasses import NativeUIElement

class Simulator:
    '''
    Simulator class - Command manipulations of iphone simulator
    '''
    
    bid = "com.apple.iphonesimulator"
    pageSlider = "Page*of*"
    def __init__(self):
        self.launch()

        
    def _get_sim_window(self):
        sim = atomac.getAppRefByBundleId(self.bid)
        windows = sim.windows(match = 'iOS Simulator*')
        if windows:
            return windows[0]
        else:
            raise Exception("Cannot get simulator window.")
    def _get_first_window(self):
        sim = atomac.getAppRefByBundleId(self.bid)
        windows = sim.windows()
        if windows:
            return sim.windows()[0]
        else:
            raise Exception("Cannot get simulator window")
    
    def launch(self):
        if self.isRunning():
            self.sim = atomac.getAppRefByBundleId(self.bid)
            return self.sim
        else:
            atomac.launchAppByBundleId(self.bid)
            init_time = time.time()
            timeout = 20
            thinktime = 0.2
            
            while(time.time() - init_time < timeout):
                sim = atomac.getAppRefByBundleId(self.bid)
                if sim.windows():
                    self.sim = sim
                    return self.sim
                time.sleep(thinktime)
            raise Exception("Simulator launching time out!")
    
    def quit(self):
        if self.isRunning():
            atomac.terminateAppByBundleId(self.bid)
            while(self.isRunning()):
                time.sleep(0.5)       
            return True
        else:
            return False
        
    def home(self):
        win = self._get_sim_window()
        elems = self.waitFor(win, AXDescription = 'Home')
        if elems:
            elems[0].Press()
            time.sleep(0.5)
        return win
    
    def tapHomeBtn(self):
        win = self._get_sim_window()
        win.menuItem('Hardware', 'Home').Press()
        
    def doubleTapHomeBtn(self):
        win = self._get_sim_window()
        win.menuItem('Hardware', 'Home').Press()
        win.menuItem('Hardware', 'Home').Press()
        
    def lock(self):
        win = self._get_sim_window()
        win.menuItem(4,9).Press()
    
    def unlock(self):
        win = self._get_sim_window()
        btn = self.waitFor(win, AXTitle='slide to unlock')
        if btn:
            btn[0].Press()
            return True
        else:
            return False
    
    def homeSlideToLeft(self):
        win = self.home()
        sliders = self.waitFor(win, AXRole='AXSlider', AXTitle='Page*of*')
        if not sliders:
            return False
        slider = sliders[0]
        page_info = slider.AXTitle.split(' ')
        current_page = page_info[1]
        if current_page == "1":
            return False
        else:
            slider.Decrement()
            return True

    
    def homeSlideToRight(self):
        win = self.home()
        
        slider = self.waitFor(win, AXRole='AXSlider', AXTitle='Page*of*')[0]
        if not slider:
            return False
        page_info = slider.AXTitle.split(' ')
        current_page = page_info[1]
        total_page = page_info[3]
        if current_page == total_page:
            return False
        else:
            slider.Increment()
            return True
    
    def _navToFirstPage(self):
        if self.waitFor(AXTitle = self.pageSlider):
            while(True):
                if not self.homeSlideToLeft():
                    break
        else:
            self.home()
            self.lock()
            self.unlock()
        
    def waitFor(self, base_elem = None, timeout = 2, thinktime = 0.01,  **kwargs):
        if base_elem:
            win = base_elem
        else:
            win = self.sim.windows()[0]
        init_time = time.time()
        while(time.time() - init_time < timeout):
            elem = win.findAll(**kwargs)
            if elem:
                return elem
            time.sleep(thinktime)
        return []
                
          

    
    
    def search(self):
        '''
        It's in todo list
        '''
    
    def isRunning(self):
        try:
            atomac.getAppRefByBundleId(self.bid)   
            return True 
        except:
            return False
        
    def activate(self, elem):
        elem.activate()

        
    def reset(self):
        win = self._get_sim_window()
        win.menuItem(1,4).Press()
        winPopup = self._get_first_window()
        resetBtn = winPopup.buttons(match = 'Reset')
        if resetBtn:
            resetBtn[0].Press()
            return True
        else:
            return False
    

    

    
    def rotateToLeft(self):
        win = self._get_sim_window()
        win.menuItem('Hardware', 'Rotate Left').Press()
    
    def rotateToRight(self):
        win = self._get_sim_window()
        win.menuItem('Hardware', 'Rotate Right').Press()
    
    def enablePrinter(self):
        win = self._get_sim_window()
        win.menuItem('File', 'Open Printer Simulator').Press()
        
    def shake(self):
        win = self._get_sim_window()
        win.menuItem('Hardware', 'Shake Gesture')
        
    def getPosition(self):
        win = self._get_sim_window()
        return win.AXPostion
    
    def getSize(self):
        win = self._get_sim_window()
        return win.AXSize
    
    def getFGApp(self):
        '''
        get the app running in foreground
        '''
        return self._get_sim_window()
        
    def findAppsByName(self, name = None):
        '''
        Application related api
        '''
        win = self._get_sim_window()
        self._navToFirstPage()
        while(True):        
            
            apps = self.waitFor(win, timeout = 2, AXTitle = name)
            if apps:
                return apps
            else:
                if not self.homeSlideToRight():
                    break
        return []    
    
    def toggleTaskManager(self):
        '''
        Application related api
        '''
        win = self._get_sim_window()
        elems = self.waitFor(win, AXDescription = 'Home')
        if not elems:
            raise "Cannot find home button!"
        elem = elems[0]
        cord = self._get_touch_point(elem)
        elem.doubleClickMouse(cord)
        

    def activateEditMode(self, name):
        '''
        Application related api
        Find apps first, if multiple apps are found, only click frist app.
        '''
        apps = self.findAppsByName(name)   
        if apps:
            app = apps[0]
            cord = self._get_touch_point(app)
            app.clickMouseButtonLeft(cord, interval = 2)
            return True
        else:
            return False
            

    def _get_touch_point(self, elem):
        position = elem.AXPosition
        size = elem.AXSize
        x = position[0]+size[0]/2
        y = position[1]+size[1]/2
        return (x,y)
    
    def launchApp(self, name):
        apps = self.findAppsByName(name)
        if apps:
            time.sleep(0.5)
            apps[0].Press()
        else:
            raise Exception("Cannot find the app!")

    
                

    
    
        

    


    

        
if __name__ == "__main__":
    sim = Simulator()
#    sim.quit()
#    sim.launch()
#    app = sim.findAppsByName('Usher')[0]
    app = sim.getFGApp()
    sim.activate(app)
    coord = app.AXPosition
    size = app.AXSize
    src_coord = (coord[0]+size[0]/2,coord[1]+size[1]/2)
    dest_coord = (coord[0]+300, coord[1]+size[1]/2)
    src_coord = (906, 535)
    dest_coord = (748, 333)
    
    
    app.dragMouseButtonLeft(src_coord, dest_coord, interval = 0.5)
#    app.clickMouseButtonLeft(src_coord)

    pass
            

