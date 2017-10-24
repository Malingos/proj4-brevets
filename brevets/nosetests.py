import acp_times
import arrow
import nose
#from nose.readthedocs.io/en/latest/usage.html, still doesn't work? (says ran 0 tests?)
#results = nose.main()
#nose.main()
testControl=[0, 200,300, 1100]
testMax = [200,200,1000,1000]
#4 test cases: test 0, test when control = distance, test when control < distance, test when control > distance but within multiplier
#expectedOpen = ["2017-01-01T08:00","2017-01-01T13:53","",""]#0 shift, 13:53 shift, 41:00 shift
#expectedClose = ["","","",""]
#for purposes of test, ignore timezone shifts, so add 8 hours to expected results
start = arrow.get("2017-01-01T00:00")
expectedOpen = [start.isoformat(), start.shift(minutes=+833).isoformat(),start.shift(hours=+17).isoformat(), start.shift(hours=+41).isoformat()]
expectedClose = [start.shift(hours=+9).isoformat(), start.shift(minutes=+1290).isoformat(), start.shift(hours=+28).isoformat(), start.shift(hours=+83).isoformat()]
#function names should be test_something_something
#methods from acp_times:
#shiftTimezone(arrowISO, timezoneVar)
#open_time(control_dist_km, brevet_dist_km, brevet_start_timeISO)
#close_time(control_dist_km, brevet_dist_km, brevet_start_timeISO)
def test_open():
    i=0
    for result in expectedOpen:
#        print(acp_times.open_time(testControl[i],testMax[i],start)
#        print(result)
        assert(acp_times.open_time(testControl[i], testMax[i], start) == result)
#            print(".")
#        
#        else:
#            print("x")
        i+=1

def test_close():
    i=0
    for result in expectedClose:
        assert(acp_times.close_time(testControl[i], testMax[i], start) == result)
#            print(".")
#        else:
#            print("x")
        i+=1
        
