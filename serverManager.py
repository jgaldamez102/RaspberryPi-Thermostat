req_fields = ['temp','key']
from LFSR import LFSRencrypt
keys = LFSRencrypt()
class serverManager():
    def __init__(self):
        print('Server Initializing')
        #checks if the temp value being asked is valid
    def _temp_range_checker(self,temp_entry):
        if isinstance(temp_entry,dict):
            t = keys[temp_entry['key']]^temp_entry['temp']
            if(t>=60) and (t<=100):
                return 1
            else:
                return -1

        return 0

    def set_temp(self,temp_entry):
        st = self._temp_range_checker(temp_entry)
        if(st==1):
            print('')
            print("Changing Desired Temperature")
            return temp_entry['temp'],temp_entry['key'],'Temp Changed'
        elif(st==-1):
            print('')
            print("Invalid Data from HTTP Request! Temp Unchanged")
            return None,None,'Invalid! Temp must be between 60 and 100 inclusive'
        elif(not st):
            return None,None,'Invalid Data! Temp must be between 60 and 100 inclusive'

