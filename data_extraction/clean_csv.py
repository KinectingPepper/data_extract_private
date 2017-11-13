import os
import pandas as pd

import matplotlib.pyplot as plt
import basics

# function that 'Tries to' extract the exercise from a given csvfile.
# saveloc = the location where the extracted csv is  to be saved.
# csvfile = the raw csvfile that will be extracted from.
# oef = the exercise that is performed in the csvfile (1 through 3)


def cleancsv(saveloc, csvfile, oef):
    if(isinstance(csvfile, type(' '))):
        file, T, person = basics.GetPerson(csvfile, -1)
    elif(isinstance(csvfile, type(pd.DataFrame()))):
        starttime = basics.GetSeconds(csvfile.time[0])
        endtime = basics.GetSeconds(csvfile.time[len(csvfile) - 1])
        T = endtime - starttime
        file_ = csvfile
        person = 0
    else:
        print('no correct input')
        return

    handL = file[file.jointName == 'HandLeft']
    handR = file[file.jointName == 'HandRight']
    joints = len(file.jointName.unique())
    handL = handL.reset_index(drop=True)
    handR = handR.reset_index(drop=True)
    xl = basics.GetJoint(file, 'x', 'HandLeft')
    yl = basics.GetJoint(file, 'y', 'HandLeft')
    zl = basics.GetJoint(file, 'z', 'HandLeft')
    xr = basics.GetJoint(file, 'x', 'HandRight')
    yr = basics.GetJoint(file, 'y', 'HandRight')
    zr = basics.GetJoint(file, 'z', 'HandRight')

    if(len(handL) == 0):
        newfile = file
        newfile.to_csv(saveloc)
        return
    T /= len(handL)
    timeframe = [T * x for x in range(0, len(handL))]

    for x in range(0, len(xl)):
        xl[x] *= -1

    deltatime = 0.25
    # get delta and remove padding
    dxl = basics.CalcDelta(xl, timeframe, deltatime)
    dxl = dxl[1:len(dxl) - 2]
    dxr = basics.CalcDelta(xr, timeframe, deltatime)
    dxr = dxr[1:len(dxr) - 2]
    dyl = basics.CalcDelta(yl, timeframe, deltatime)
    dyl = dyl[1:len(dyl) - 2]
    dyr = basics.CalcDelta(yr, timeframe, deltatime)
    dyr = dyr[1:len(dyr) - 2]
    dzl = basics.CalcDelta(zl, timeframe, deltatime)
    dzl = dzl[1:len(dzl) - 2]
    dzr = basics.CalcDelta(zr, timeframe, deltatime)
    dzr = dzr[1:len(dzr) - 2]
    REL = len(xl) / len(dxl)

    t = [deltatime * x for x in range(0, len(dxl))]
    treshold = 0.1 / 2
    for x in range(0, len(dxl)):
        if(dxl[x] - treshold < 0 and dxl[x] + treshold > 0):
            dxl[x] = 0
        if(dxr[x] - treshold < 0 and dxr[x] + treshold > 0):
            dxr[x] = 0
        if(dyl[x] - treshold < 0 and dyl[x] + treshold > 0):
            dyl[x] = 0
        if(dyr[x] - treshold < 0 and dyr[x] + treshold > 0):
            dyr[x] = 0
        if(dzl[x] - 0.01 < 0 and dzl[x] + 0.0 > 0):
            dzl[x] = 0
        if(dzr[x] - 0.01 < 0 and dzr[x] + 0.01 > 0):
            dzr[x] = 0
    note = -1
    dxllow = False
    dxrlow = False
    dxrhigh = False
    dxlhigh = False
    dxrllow = False
    dxrlhigh = False
    average = 0
    # check delta and actual height tresholds
    for x in range(0, len(yl)):
        average += (yl[x] + yr[x])
    avg = average / (len(yl) + len(xl))
    if(oef != 3):
        for x in range(len(dxl) - 1, 0, -1):
            c = int(x * REL)
            if(dyl[x] < 0 and not dxllow and (((yl[c] > avg)))):
                dxllow = True
            if(dyl[x] > 0 and dxllow):
                dxlhigh = True
            if(dyr[x] < 0 and not dxrlow and ((yr[c] > avg))):
                dxrlow = True
            if(dyr[x] > 0 and dxrlow and 1):
                dxrhigh = True
            if(dyr[x] < 0 and dyl[x] < 0 and dxrhigh and dxlhigh and (yr[c] > avg) and (yl[c] > avg)):
                dxrllow = True
            if(dyr[x] > 0 and dyl[x] > 0 and dxrllow):
                dxrlhigh = True
            if(dyr[x] == 0 and dyl[x] == 0 and dxrlhigh):
                i = int(x * REL)
                while((yr[i] > avg or yl[i] > avg)):
                    i -= 1
                    if(i == 0):
                        break
                while((yr[i - 1] < yr[i] or yr[i - 2] < yr[i]or yr[i - 3] < yr[i]or yr[i - 4] < yr[i]or yr[i - 5] < yr[i])or(yl[i - 1] < yl[i] or yl[i - 2] < yl[i]or yl[i - 3] < yl[i]or yl[i - 4] < yl[i]or yl[i - 5] < yl[i])):
                    i -= 1
                    if(i == 0):
                        break

                note = int(i / REL)
                note -= 0
                if(note < 0):
                    note = 0
                break
    else:
        for x in range(len(dxl) - 1, 3, -1):
            if(dxl[x] < 0 and not dxllow):
                dxllow = True
            if(dxl[x] > 0 and dxllow and not dxlhigh):
                dxlhigh = True
            if(dxr[x] < 0 and not dxrlow):
                dxrlow = True
            if(dxr[x] > 0 and dxrlow and not dxrhigh):
                dxrhigh = True
            if(dxr[x] < 0 and dxl[x] < 0 and dxrhigh and dxlhigh):
                dxrllow = True
            if(dxr[x] > 0 and dxl[x] > 0 and dxrllow):
                dxrlhigh = True
            if(dxr[x] == 0 and dxl[x] == 0 and dxrlhigh):
                note = int(x)
                if(note < 0):
                    note = 0
                break

    note *= deltatime
    note = int(note)
    T1 = file.time[0]
    T1 = basics.NewTime(T1, note)
    c = -1
    for x in range(0, len(file.time)):
        if((T1[:8] in file.time[x])):
            c = x
            break

    newfile = file[c:]
    newfile = newfile.reset_index(drop=True)
    # From front to back
    handL = newfile[newfile.jointName == 'HandLeft']
    handR = newfile[newfile.jointName == 'HandRight']
    handL = handL.reset_index(drop=True)
    handR = handR.reset_index(drop=True)
    for x in range(0, len(handL.y)):
        if(oef != 3):
            yl = basics.GetJoint(newfile, 'y', 'HandLeft')
            yr = basics.GetJoint(newfile, 'y', 'HandRight')
        else:
            yl = basics.GetJoint(newfile, 'x', 'HandLeft')
            yl = [x * -1 + 1 for x in yl]
            yr = basics.GetJoint(newfile, 'x', 'HandRight')
            yr = [x + 1 for x in yr]
    assert(len(handL) != 0)
    T = basics.GetSeconds(
        handL.time[len(handL) - 1]) - basics.GetSeconds(handL.time[0])
    T /= len(handL)
    timeframe = [T * x for x in range(0, len(handL))]

    #######
    # Get and treshold Deltas
    deltatime = 0.25

    dyl = basics.CalcDelta(yl, timeframe, deltatime)
    dyl = dyl[1:len(dyl) - 2]
    dyr = basics.CalcDelta(yr, timeframe, deltatime)
    dyr = dyr[1:len(dyr) - 2]
    REL = len(yl) / len(dyl)
    t = [deltatime * x for x in range(0, len(dyl))]
    if(oef != 3):
        treshold = 0.1 / 2
    else:
        treshold = 0.05 / 2
    for x in range(0, len(dyl)):
        if(dyl[x] - treshold < 0 and dyl[x] + treshold > 0):
            dyl[x] = 0
        if(dyr[x] - treshold < 0 and dyr[x] + treshold > 0):
            dyr[x] = 0

    #######
    # Get Top (75%) and bottom (80%)
    hdyl = basics.GetHeight(dyl, 4, 1)
    hdyl = hdyl * 0.75 if hdyl > 0 else hdyl * 1.25

    if(oef == 3):
        hyl = basics.GetHeight(yl, 10, 1)
        hyl *= 0.9
    else:
        hyl = basics.GetHeight(yl, 4, 0)
        hyl = hyl * 0.75 if hyl > 0 else hyl * 1.25

    lyl = basics.GetLow(yl, 4, 0)
    lyl = lyl * 0.75 if lyl < 0 else lyl * 1.25
    if(oef == 3):
        hyr = basics.GetHeight(yr, 10, 1)
        hyr *= 0.9
    else:
        hyr = basics.GetHeight(yr, 4, 0)
        hyr = hyr * 0.75 if hyl > 0 else hyr * 1.25
    hdyr = basics.GetHeight(dyr, 4, 1)
    hdyr = hdyr * 0.75 if hdyr > 0 else hdyr * 1.25
    lyr = basics.GetLow(yr, 4, 0)
    lyr = lyr * 0.9 if lyr < 0 else lyr * 1.1
    dlyr = basics.GetLow(dyr, 3, 1)
    dlyr = dlyr * 0.8 if dlyr < 0 else dlyr * 1.2
    dlyl = basics.GetLow(dyl, 3, 1)
    dlyl = dlyl * 0.8 if dlyl < 0 else dlyl * 1.2
    #######
    # Set start and end point
    done = False
    while(1):
        dyrlhigh = False
        dyrllow = False
        dyrhigh = False
        dyrlow = False
        dylhigh = False
        dyllow = False
        rlow = 0.0
        llow = 0.0
        y = 0
        note = (len(dyl))
        for x in range(1, len(dyl)):
            if(dyl[x] > hdyl and dyr[x] > hdyr and not dyrlhigh):
                # print(['lr_up',x*deltatime])
                y = x - 1
                while((dyl[y] != 0 or dyr[y] != 0)and y > 1):
                    y -= 1
                while((yl[int((y) * REL)] > lyl or yr[int((y) * REL)] > lyr)and y > 1):
                    y -= 1
                while((yl[int((y - 1) * REL)] < yl[int(y * REL)] or yr[int((y - 1) * REL)] < yr[int(y * REL)])and y > 1):
                    y -= 1
                if(y == 1):
                    y = 0
                dyrlhigh = True
            if(dyl[x] < 0 and dyr[x] < 0 and dyrlhigh and not dyrllow and dlyr >= dyr[x] and dlyl >= dyl[x]):
                # print(['lr_down',x*deltatime])
                dyrllow = True
            if(dyl[x] > hdyl and not dylhigh and dyrllow and (yl[int(x * REL)] > hyl or yl[int((x + 1) * REL)] > hyl)):
                # print(['l_up',x*deltatime])
                dylhigh = True
                rlow += yr[int((x) * REL)]
            elif(dyl[x] < 0 and dylhigh and not dyllow):
                # print(['l_down',x*deltatime])
                dyllow = True
                rlow += yr[int((x) * REL)]
            elif(dyr[x] > hdyr and not dyrhigh and dyrllow and (yr[int(x * REL)] > hyr or yr[int((x + 1) * REL)] > hyr)):
                # print(['r_up',x*deltatime])
                llow += yl[int((x) * REL)]
                dyrhigh = True
            elif(dyr[x] < 0 and dyrhigh and not dyrlow):
                # print(['r_down',x*deltatime])
                llow += yl[int((x) * REL)]
                dyrlow = True
            if(dyl[x] == 0 and dyr[x] == 0 and dyllow and dyrlow):
                while((yl[int(x * REL)] > lyl or yr[int(x * REL)] > lyr)and x < len(dyl) - 2):
                    x += 1
                while((yl[int((x - 1) * REL)] > yl[int(x * REL)] or yr[int((x - 1) * REL)] > yr[int(x * REL)] or yl[int((x - 1) * REL)] > yl[int((x + 1) * REL - 1)] or yr[int((x - 1) * REL)] > yr[int((x + 1) * REL - 1)])and x < len(dyl) - 2):
                    x += 1
                if(x == len(dyl) - 2):
                    x += 1
                note = x + 1
                print(['done', x * deltatime])
                break
        if(dyrlhigh or done):
            break
        elif(done == False):
            done = True
            hdyl = basics.GetHeight(dyl, 4, 1)
            hdyr = basics.GetHeight(dyr, 4, 1)
            hdyl = hdyl * 0.75 if hdyl > 0 else hdyl * 1.25
            hdyr = hdyr * 0.75 if hdyr > 0 else hdyr * 1.25

    #########
    # Create the timestamps
    if(note < len(dyl)):
        T2 = basics.NewTime(newfile.time[0], (note * deltatime))
    else:
        T2 = newfile.time[len(newfile) - 1]
    c = -1
    for x in range(0, len(newfile.time)):
        if((T2[:8] in newfile.time[x])and(newfile.time[x][9] >= T2[9])):
            c = x + 1
            break

    T2 = basics.NewTime(newfile.time[0], (y * deltatime))
    c2 = -1
    for x in range(0, len(newfile.time)):
        if((T2[:8] in newfile.time[x])):
            if(newfile.time[x][9] > T2[9] and x != 0):
                c2 = x - 1
                break
            else:
                c2 = x
                break

    #########
    # get rid of some starting peaks
    yl = yl[int(c2 / joints):int(c / joints)]
    yr = yr[int(c2 / joints):int(c / joints)]
    c3 = 0
    for i in range(0, len(yl)):
        if(yl[i + 1] < yl[i] or yr[i + 1] < yr[i]):
            c3 += 1
        else:
            break
    c3 = int(c3 * joints)

    ########
    # recut the csvfile
    newfile2 = newfile[c2 + c3:c]
    newfile2 = newfile2.reset_index(drop=True)

    if(len(newfile2) > 0):
        newfile2.to_csv(saveloc)
    else:
        newfile.to_csv(saveloc)

    debug = False
    if(debug):
        timeframe2 = [T * x for x in range(0, len(yl))]
        t2 = [deltatime * x for x in range(0, len(dyl))]
        print([dxllow, dxlhigh], [dxrlow, dxrhigh], [dxrllow, dxrlhigh])
        print(REL)
        print(avg)
        print(y)
        print(note)
        print(T1)
        plt.plot(timeframe2, yl, 'r-', timeframe2, yr, 'b-')
        plt.show()
        plt.plot(t2, dyl, 'r-', t2, dyr, 'b-')
        plt.show()
        plt.close()

# Function that compares a list of files by creating a graph of the xyz coörds
# files = list of locations from csvfiles to compare
# saveloc = the location for the image of the graph to be saved


def compare(files, saveloc):
    l = len(files)
    plt.figure(figsize=(int(20 * l), 30))
    for i in range(0, len(files)):
        file, t, person = basics.GetPerson(files[i], -1)
        assert(len(file) > 0)
        handL = file[file.jointName == 'HandLeft']
        if(len(handL) == 0):
            continue
        handL = handL.reset_index(drop=True)
        xl = basics.GetJoint(file, 'x', 'HandLeft')
        yl = basics.GetJoint(file, 'y', 'HandLeft')
        zl = basics.GetJoint(file, 'z', 'HandLeft')
        xr = basics.GetJoint(file, 'x', 'HandRight')
        yr = basics.GetJoint(file, 'y', 'HandRight')
        zr = basics.GetJoint(file, 'z', 'HandRight')
        t /= len(handL)
        timeframe = [t * x for x in range(0, len(handL))]
        plt.subplot(l, 3, 3 * i + 1)
        plt.plot(timeframe, xl, 'r-', timeframe, xr, 'g-')
        plt.subplot(l, 3, 3 * i + 2)
        plt.plot(timeframe, yl, 'r-', timeframe, yr, 'g-')
        plt.subplot(l, 3, 3 * i + 3)
        plt.plot(timeframe, zl, 'r-', timeframe, zr, 'g-')
    plt.savefig(saveloc)
    plt.close()


# used by GetPart to obtain cutting borders
def RecursiveLoop(values, start, end, low, sink):
    while(values[start] > low and start != 0):
        start -= 1
    while(values[end] > low and end != len(values) - 1):
        end += 1
    done = False
    while(not done):
        i = 0
        done = True
        if(start >= 10):
            i = start - 10
        else:
            i = 0
        for j in range(start, i, -1):
            if(values[j] < values[start] - sink):
                start = j
                done = False
    done = False
    while(not done):
        i = 0
        done = True
        if(end <= len(values) - 10):
            i = end + 10
        else:
            i = len(values) - 1

        for j in range(end, i, 1):
            if(values[j] < values[end] - sink):
                end = j
                done = False
    return start, end

# Used by getpart to assemble a list containing information


def GetList(l, r, hl, hr):
    coords = list()
    for i in range(0, len(l)):
        if(l[i] > hl and r[i] > hr):
            coords.append([1, i])
        elif(l[i] > hl and not r[i] > hr):
            coords.append([2, i])
        elif(not l[i] > hl and r[i] > hr):
            coords.append([3, i])

    numberlist = list()
    j = 1
    start = coords[0][1]
    lasttime = coords[0][1]
    timedifference = int(len(l) / 20)
    for i in range(1, len(coords)):
        if(coords[i][0] != coords[i - 1][0] or coords[i][1] > lasttime + timedifference):
            numberlist.append([coords[i - 1][0], j, start, coords[i - 1][1]])
            start = coords[i][1]
            lasttime = coords[i][1]
            j = 1
        else:
            j += 1
            lasttime = coords[i][1]
    numberlist.append([coords[i - 1][0], j, start, coords[i - 1][1]])

    numbertresholdmultiplier = 5
    numbertreshold = numberlist[0][1]
    i = 1
    while(i != len(numberlist)):
        if(numberlist[i][1] > numbertreshold):
            numbertreshold = numberlist[i][1]
            i = 0
        elif(numberlist[i][1] < int(numbertreshold / numbertresholdmultiplier)):
            numberlist.pop(i)
            i = i - 1 if i > 0 else 0
        else:
            i += 1
    # remove duplicates
    i = 0
    j = 0
    while(i < len(numberlist)):
        while(j < len(numberlist)):
            if(numberlist[i][0] == numberlist[j][0] and i != j):
                if(numberlist[j][1] >= numberlist[i][1]):
                    numberlist.pop(i)
                    i = -1
                    break
                else:
                    numberlist.pop(j)
                    j = 0
                    continue
            j += 1
        i += 1
    return numberlist

# Function that extracts a given part from an excercise
# csvfile = input file from which a specific section will be returned
# oef = the sort of excercise [1,2 or 3]
# nr = the part of the excersice ['l','r','lr']

# return the part of the csvfile consisting of the requested part


def GetPart(csvfile, oef, nr):
    if(isinstance(csvfile, type(' '))):
        file, T, person = basics.GetPerson(csvfile, -1)
    elif(isinstance(csvfile, type(pd.DataFrame()))):
        starttime = basics.GetSeconds(csvfile.time[0])
        endtime = basics.GetSeconds(csvfile.time[len(csvfile) - 1])
        T = endtime - starttime
        file_ = csvfile
        person = 0
    else:
        print('invalid input')
        return
    # Get Left and Right hand
    joints = len(file.jointName.unique())

    if(oef != 3):
        l = basics.GetJoint(file, 'y', 'HandLeft')
        r = basics.GetJoint(file, 'y', 'HandRight')
    else:
        l = basics.GetJoint(file, 'x', 'HandLeft')
        l = [x * -1 + 1 for x in l]
        r = basics.GetJoint(file, 'x', 'HandRight')
        r = [x + 1 for x in r]

    if(oef != 3):
        hl = basics.GetHeight(l, 20, 1) * 0.8
        hr = basics.GetHeight(r, 20, 1) * 0.8
        ll = basics.GetLow(l, 30, 1) * 0.8
        lr = basics.GetLow(r, 30, 1) * 0.8
    else:
        hl = basics.GetHeight(l, 20, 1) * 0.9
        hr = basics.GetHeight(r, 20, 1) * 0.9
        ll = basics.GetLow(l, 50, 1) * 1.15
        lr = basics.GetLow(r, 50, 1) * 1.15

    # get all coords
    numberlist = GetList(l, r, hl, hr)

    nrtohand = {1: 'lr', 2: 'l', 3: 'r'}
    start = 0
    end = len(l) - 1
    if(oef != 3):
        sink = 0.02
    else:
        sink = 0.01
    double = False
    for i in numberlist:
        if(nrtohand[i[0]] != nr):
            continue
        if(double):
            print("more than one matching curve")
        double = True
        start = i[2]
        end = i[3]
        startL = start
        startR = start
        endL = end
        endR = end
        startL, endL = RecursiveLoop(l, startL, endL, ll, sink)
        startR, endR = RecursiveLoop(r, startR, endR, lr, sink)
        if(nr == 'l'):
            start = startL
            end = endL
        elif(nr == 'r'):
            start = startR
            end = endR
        else:
            start = startL if startL > startR else startR
            end = endL if endL > endR else endR
    # revert x transformation
    if(oef == 3):
        for i in range(0, len(l)):
            l[i] = (l[i] - 1) * -1
        for i in range(0, len(r)):
            r[i] = (r[i] - 1)

    if(start == 0 and end == len(l) - 1):
        print(['error start and end full file'])
        return file

    newfile = file[int(start * joints):int((end + 1) * joints)]
    return newfile
