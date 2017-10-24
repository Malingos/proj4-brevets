"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

#def this_Function(control, boolean):
#    """
#    This function gets the speed based on the km count
#    """
#    #this will return the speed for opening or closing time
#    #if boolean is true, get open time, if false get close time
#    if(boolean):
#        if(control <= 200):
#            return 34
#        elif(control <= 400):
#            return 32
#        elif(control <= 600):
#            return 30
#        elif(control <= 1000):
#            return 28
#        else:
#            return 26
#    else:
#        if(control <= 600):
#            return 15
#        elif(control <= 1000):
#            return 11.428
#        else:
#            return 13.333
#def get_End(startTime,maxDist):
#    """
#    Returns the End Time in arrow, used if the end equals the control time because these have special times
#    """
#    #if(boolean):
#    #    if(maxDist == 200):
#    #    elif(maxDist == 300):
#    #    elif(maxDist == 400):
#    #    elif(maxDist == 600):
#    #    else:i
#    #else:
#    if(maxDist == 200):#13 hours 30 minutes
#        return startTime.shift(seconds=+48600)
#        #return arrow.get(startTime).timestamp + 48600
#    elif(maxDist == 300):#20 hours
#        return startTime.shift(seconds=+72000)
#        #return arrow.get(startTime).timestamp + 72000
#    elif(maxDist == 400):#24 + 3 hours
#        return startTime.shift(seconds=+97200)
#        #return arrow.get(startTime).timestamp + 97200
#    elif(maxDist == 600):#24 + 16 hours
#        return startTime.shift(seconds=+144000)
#        #return arrow.get(startTime).timestamp + 144000
#    else:#24*3 + 3 hours
#        return startTime.shift(seconds=+259200)
#        #return arrow.get(startTime).timestamp + 259200
###############################
#These were old methods, to be replaced with table driven coding(used to help me understand the logic)
###############################
#From article 9 time limits:
#0 - 200
#200 - 400
#400 - 600
#600 - 1000
timezone = 8
controldistances = [200,200,200,400]#can add more to tables if rules from article 9 change
#1000 - 1300? it's in the algorithm but not in the rules?
minSpeed = [15,15,15,11.428]#13.333 in algorithm, but 1300km not in rules?
maxSpeed = [34,32,30,28]#26 in algorithm, not in rules
maxTimes = [13.5,20,27,40,75]#200,300,400,600,1000, number of hours to shift until close
maxDistances = [200,300,400,600,1000]
maxDistMultiplier = 1.1#if multiplier for max distance changes
def shiftTimezone(arrowISO, timezoneVar):
    """
    Takes in an arrow ISO string and a timezone, and returns an arrow ISO that is shifted by the timezone variable
    """
    retval = arrow.get(arrowISO)
    retval = retval.shift(hours=+timezoneVar)
    return retval.isoformat()
def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    print("Starting open_time")
    print("Control: {}", control_dist_km)
    print("Max Distance: {}", brevet_dist_km)
    print("Start Time: {}", brevet_start_time)
    cyclingDistances = [0,0,0,0]
    #used to calculate opening times: Example#####################
    #450km 
    #[200,200,50,0]
    #max speeds:
    #[34,32,30,28]
    #200/34 + 200/32 + 50/30 + 0/28
    #this way if more things are added can simply add more to this cyclingDistances array
    #mySpeed = this_Function(control_dist_km, True)
    #thisDict = {200: 34, 400
    #times = ["13:30", "20:00", "27:00", "40:00", "75:00"]
    #control_dist_km = int(control_dist_km)
    #brevet_dist_km = float(brevet_dist_km)
    if (control_dist_km > brevet_dist_km and control_dist_km <= brevet_dist_km * maxDistMultiplier):
        control_dist_km = brevet_dist_km
    if (control_dist_km > brevet_dist_km * maxDistMultiplier or control_dist_km == 0):#dunno what to do if its higher, so just return the start i guess
        return shiftTimezone(brevet_start_time, timezone)
    i=0
    for entry in cyclingDistances:
        if(control_dist_km <= 0):
            break
        if(control_dist_km >= controldistances[i]):
            cyclingDistances[i] = controldistances[i]
            control_dist_km -= cyclingDistances[i]
        else:
            cyclingDistances[i] = control_dist_km
            control_dist_km = 0
        i+=1
    #now I have cycling distances filled out
    shift = 0
    i=0
    for entry in cyclingDistances:
       shift += entry/maxSpeed[i]
       i+=1
    shift = int(shift * 60)#hours -> minutes 
    return shiftTimezone(arrow.get(brevet_start_time).shift(minutes=+shift).isoformat(), timezone) 
        
#    thistime = control_dist_km/mySpeed
#    sometime = thistime
#    hournum = 0
#    i=0
#    while i in range (0, 2000):#didn't want to use while true, shouldn't be more than 2000 miles anyways
#        sometime -= 1
#        hournum += 1
#        if (sometime <= 1):
#            break
#        elif( sometime < 0 ):
#            sometime += 1
#            break
#    #after this loop sometime is just decimal point
#    minutes = sometime * 60 * 60
#    minutes = int(minutes)
#    hournum = hournum * 60 * 60
#    seconds = hournum + minutes
#    retval = arrow.get(brevet_start_time).shift(seconds)
#    #now i have number of seconds i can add to a timestamp
#    #timestamp = arrow.get(brevet_start_time).timestamp + seconds
#    #return arrow.get(timestamp).isoformat()
#    return retval.isoformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    print("Starting close_time")
    print("Control: {}", control_dist_km)
    print("Distance: {}", brevet_dist_km)
    print("Start: {}", brevet_start_time)
    #control_dist_km = int(control_dist_km)
    #brevet_dist_km = float(brevet_dist_km)
    cyclingDistances = [0,0,0,0]
    if (control_dist_km >= brevet_dist_km * maxDistMultiplier): #if distance is within the max distance multiplier of the maximum distance, for the purposes of the time returned they are the same
        control_dist_km = brevet_dist_km    
    if(control_dist_km == 0):#if its 0, add an hour
        return shiftTimezone(arrow.get(brevet_start_time).shift(hours=+1).isoformat(),timezone)
    if(control_dist_km == brevet_dist_km):#its max distance, lets find out which entry in the list it is
        i=0    
        for d in maxDistances:
            if(d == control_dist_km):
                break
            i+=1
        return shiftTimezone(arrow.get(brevet_start_time).shift(hours=+maxTimes[i]).isoformat(), timezone)
        
    #now we have the cases where its beginning and end
    #now basically do the same thing in opening times except with closing times
    i=0
    for entry in cyclingDistances:
        if(control_dist_km == 0):
            break
        if(control_dist_km >= controldistances[i]):
            cyclingDistances[i] = controldistances[i]
            control_dist_km -= controldistances[i]
        else:
            cyclingDistances[i] = control_dist_km
            control_dist_km = 0
        i+=1
    i=0
    shift = 0
    #now cyclingDistances is filledout, so just calculate based on speeds
    for speed in minSpeed:
        shift += cyclingDistances[i]/speed
        i+=1
    shift = int(shift * 60) #hours -> minutes
    #shift += int(timezone * 60)#timezone hours to minutes
    return shiftTimezone(arrow.get(brevet_start_time).shift(minutes=+shift).isoformat(), timezone)
#    arrowStart = arrow.get(brevet_start_time)
#    timestamp = 0
#    mySpeed = this_Function(control_dist_km, False)
#    if (control_dist_km == 0):
#        #timestamp = arrow.get(brevet_start_time).timestamp
#        #timestamp += 360
#        #return arrow.get(timestamp).isoformat()
#        arrowStart.shift(seconds=+360)
#        return arrowStart.isoformat()
#        #return arrow.get(int(arrow.get(brevet_start_time).timestamp()) + 360).isoformat()
#    if (control_dist_km >= brevet_dist_km):
#        return get_End(brevet_dist_km, arrowStart).isoformat()#uses "getEnd" method
#    thistime = control_dist_km/mySpeed
#    sometime = thistime
#    hournum = 0
#    while i in range (0, 2000):
#        sometime -= 1
#        hournum += 1
#        if (sometime <= 1):
#            break
#        elif( sometime < 0):
#            sometime += 1
#            break
#    minutes = sometime * 60 * 60
#    minutes = int(minutes)
#    hournum = hournum * 60 * 60
#    sec = hournum + minutes
#    arrowStart.shift(seconds=+sec)
#  
#    #timestamp = arrow.get(brevet_start_time).timestamp + seconds
#    return arrowStart.isoformat()#arrow.get(timestamp).isoformat()
