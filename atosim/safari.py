'''
Created on Jul 15, 2013

@author: xumingze
'''
from simulator import Simulator

class Safari:
    def __init__(self):
        sim = Simulator()
        sim.launchApp("Safari")
        self.win = sim._get_sim_window()
        pass
    
    def forward(self):
        self.win.findAll(AXTitle="Forward")[0].Press()
        pass
    
    def back(self):
        self.win.findAll(AXTitle="Back")[0].Press()
        pass
    
    def goToAddress(self, url):
        try:
            address = self.win.findAll(AXTitle="Address")[0]
            address.Press()
            clear = self.win.findAll(AXTitle="Clear text")[0]
            clear.Press()
            address.sendKeys(url)
            self.win.findAll(AXTitle="go")[-1].Press()
            return True
        except:
            return False 

    
    def search(self, str):
        
        try:
            if not str:
                return False
            search = self.win.findAll(AXValue="Search")[0]
            search.Press()
            search.sendKeys(str)
            self.win.findAll(AXTitle="search")[-1].Press()
            return True
        except:
            return False            
    
    def refresh(self):
        self.win.findAll(AXTitle="reload")[0].Press()
        pass

if __name__ == '__main__':
    s = Safari()
    s.search("askbot")
    