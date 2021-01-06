#!/usr/bin/python3
import os
import csv
import sys
import time
import math
import struct
import numpy as np
import pandas as pd
from csv import reader
from csv import writer
from csv import DictReader
import tkinter as tk
from tkinter import ttk
import datetime as datetime

from sinkingFund import *
from interestCalc import *
from capitalRecovery import*

#############################################
root = tk.Tk()
root.title("Laser Pointer GUI Version 0.0.1")
#root.geometry("1200x750")
root.geometry("1200x900")
column_size = 60
row_size = 25

################## Globals ##################

#################### Create Labels ####################
Lasermode_label     = tk.Label(root, text="Laser\nMode")
xcoord_label        = tk.Label(root, text="XCoord")
ycoord_label        = tk.Label(root, text="YCoord")
xwidth_label        = tk.Label(root, text="XWidth")
ywidth_label        = tk.Label(root, text="YWidth")
pwm_label          = tk.Label(root, text="PWM\n(%Mod)")
target_detect_label = tk.Label(root, text="Target\nDetect")
target_lock_label   = tk.Label(root, text="Target\nLock")
target_dispo_label  = tk.Label(root, text="Target\nDispo")
target_dist_label   = tk.Label(root, text="Target\nDistance")

mv_laserX_label     = tk.Label(root, text="x coord")
mv_laserY_label     = tk.Label(root, text="y coord")
mv_laserZ_label     = tk.Label(root, text="z coord")
mv_targetX_label    = tk.Label(root, text="x coord")
mv_targetY_label    = tk.Label(root, text="y coord")
mv_targetZ_label    = tk.Label(root, text="distance")
mv_targetMood_label = tk.Label(root, text="mood")

Targetmode_label    = tk.Label(root, text="Target\nMode")
xc_label            = tk.Label(root, text="XCoord")
yc_label            = tk.Label(root, text="YCoord")
detect_label        = tk.Label(root, text="Target\nDetect")
dist_label          = tk.Label(root, text="Target\nDist")
dispo_label         = tk.Label(root, text="Target\nDispo")
lock_label          = tk.Label(root, text="Target\nLock")
pel_label           = tk.Label(root, text="PEL")

##### Not Used ####
# inst_label          = tk.Label(root, text="Instance")
# set_pwr_label       = tk.Label(root, text="Pwr Off")
# create_laser_label  = tk.Label(root, text="DISARMED")
# create_target_label = tk.Label(root, text="NONE")
# spon_label          = tk.Label(root, text="Pwr On")
# spoff_label         = tk.Label(root, text="Pwr Off")
# lsron_label         = tk.Label(root, text="Lsr On")
# lsroff_label        = tk.Label(root, text="Lsr Off")
# dot_label           = tk.Label(root, text="Dot Off")
# square_label        = tk.Label(root, text="Sqr Off")
# move2_label         = tk.Label(root, text="Move 2\nTarget")

######### Power and ON/OFF Labels ##########
set_pwr_label = tk.StringVar()
set_pwr_label_text = tk.StringVar()
set_pwr_label_text.set("UNSET")
set_pwr_label = tk.Label(root, textvariable=set_pwr_label_text, width=8)
set_pwr_label.grid(row=1, column=2)

set_onoff_label = tk.StringVar()
set_onoff_label_text = tk.StringVar()
set_onoff_label_text.set("LSR OFF")
set_onoff_label = tk.Label(root, textvariable=set_onoff_label_text, width=8)
set_onoff_label.grid(row=0, column=2)

set_pel_label = tk.StringVar()
set_pel_label_text = tk.StringVar()
set_pel_label_text.set("pel coeff")
set_pel_label = tk.Label(root, textvariable=set_pel_label_text, width=8)
set_pel_label.grid(row=4, column=2)

############ Classes ###########
class LaserPointer:
    def __init__(self,xcoord=1,ycoord=1,pwm=0):
        self.xcoord     = xcoord
        self.ycoord     = ycoord
        self.pwm        = pwm
        self.lasertuple = (xcoord,ycoord,pwm)
        self.laserlist = [xcoord,ycoord,pwm]
        print("{0} : {1} : {2} \n".format(self.xcoord,
                        self.ycoord,self.pwm))

        def __del__(self):
            print("Laser destructor called")

        def cloneLaser(self,laser1):
            print("Creating Laser\n")
            laser = LaserPointer()
            laser.xcoord     = laser1.xcoord
            laser.ycoord     = laser1.ycoord
            laser.pwm        = laser1.pwm
            return laser

        def getlaserlist(self,laser):
            print("{0}".format(laser.laserlist))
            return laser.laserlist

class TargetClass:
    def __init__(self,instance,xloc=1,yloc=1,dist=0.01,disp='U',pel=0):
        if dist <= 0: dist = 0.1
        self.name = "%s:" % (instance)
        self.instance = instance
        self._as_parameter_ = instance
        self.xloc     = xloc
        self.yloc     = yloc
        self.dist     = dist
        self.disp     = disp
        self.pel      = pel
        globals()['PEL_1'] = self.pel
        self.targettuple = (instance,xloc,yloc,dist,disp,pel)
        self.targetlist = [instance,xloc,yloc,dist,disp,pel]
        # print("{0} : {1} : {2} : {3} : {4}\n".format(self.xloc,
        #                 self.yloc,self.dist,self.disp,self.pel))

        def __del__(self):
            print("Target destructor called")

class TargetMonitor:
    def __init__(self,master,instance,num=1):
        self.name = "%s" % (instance)
        self.num = num if num >=1 else 1
        self.laser = GLOBAL_LASER
        self.ambLight = GLOBAL_AMBIENTLIGHT
        self._as_parameter_ = instance
        # self.frame = tk.Label(master)
        self.frame = tk.Frame(master)
        self.targList = [[TargetClass(i)] for i in range(num)]

        for a in range(12):
            self.frame.grid_columnconfigure(a,  minsize=column_size)
            # self.frame.grid_rowconfigure(a,  minsize=1)


###############################################################
################# TargetMonitor Declarations ##################
#### We can create multiple TargetMonitor objects by changing
#### array size and making object declarations accordingly.

## Array Size
tm = [0]
# tm = [0, 0, 0, 0]

## Object Declarations, must match array size
tm[0] = TargetMonitor(root, 1, 1)
# tm[1] = TargetMonitor(root, 2)
# tm[2] = TargetMonitor(root, 3)
# tm[3] = TargetMonitor(root, 4)

# entry_text = tk.StringVar()
# entry = tk.Entry(root, textvariable=entry_text)
# new_text = "Example text"
# entry_text.set(new_text)

#################################################################
############### Button Declarations ################
create_laser_button = tk.Button(text="Laser On",
                    command=lambda: lp_lsron_cmd(), width=13)
lsr_off_btn = tk.Button(text="Laser Off",
                    command=lambda: lp_lsroff_cmd(GLOBAL_LASER), width=13)
set_pwr_btn = tk.Button(text="Set DAC0 V",
                    command=lambda: lp_lsr_set_pwr_cmd(GLOBAL_LASER), width=13)
lsr_fire_btn = tk.Button(text="FIRE",
                    command=lambda: lp_fire_cmd(GLOBAL_LASER), width=13)
lsr_blank_btn = tk.Button(text="Blank Laser",
                    command=lambda: lp_lsr_blank_cmd(GLOBAL_LASER), width=13)
lsr_unblank_btn = tk.Button(text="Unblank Laser",
                    command=lambda: lp_lsr_unblank_cmd(GLOBAL_LASER), width=13)
lsr_pwrup_btn = tk.Button(text="DAC0 V Inc",
                    command=lambda: lp_laserPwrInc(GLOBAL_LASER), width=13)
lsr_pwrdwn_btn = tk.Button(text="DAC0 V Dec",
                    command=lambda: lp_laserPwrDec(GLOBAL_LASER), width=13)

# track_target_button = tk.Button(text="Track Target",
#                     command=lambda: lp_track_target_cmd(GLOBAL_TARGET,GLOBAL_LASER), width=13)
# end_track_target_button = tk.Button(text="Stop Track",
#                     command=lambda: lp_end_track_target_cmd(), width=13)
scan_target_button = tk.Button(text="Scan Target",
                    command=lambda: lp_scan_target_cmd(GLOBAL_TARGET,GLOBAL_LASER), width=13)
stop_scan_button = tk.Button(text="Stop Scan",
                    command=lambda: lp_stop_scan_cmd(GLOBAL_TARGET,GLOBAL_LASER), width=13)
move_laser_to_point_button = tk.Button(text="Move Laser",
                    command=lambda: lp_moveLaserToPoint(GLOBAL_LASER,
                    int(movelsrX.get()),int(movelsrY.get())), width=10)

create_target_button = tk.Button(text="Create Target 1",
                    command=lambda:  t_create_target_cmd(), width=13)
destroy_target_button = tk.Button(text="Destroy Target 1",
                    command=lambda:  t_destroy_target_cmd(GLOBAL_TARGET), width=13)
move_target_btn = tk.Button(text="Move Target",
                    command=lambda: t_moveTarget(GLOBAL_TARGET), width=10)
global_target_btn = tk.Button(text="Set Target",
                    command=lambda: t_setGlobalTarget(GLOBAL_TARGET), width=13)
change_target_mood_btn = tk.Button(text="Mood Change",
                    command=lambda: t_change_target_mood_cmd(GLOBAL_TARGET), width=13)
# draw_dot_button = tk.Button(text="Draw Dot",
#                     command=lambda: lp_draw_dot_cmd(GLOBAL_TARGET,GLOBAL_LASER), width=13)

create_laser_button.grid(           row=0,  column=0)
lsr_off_btn.grid(                   row=0,  column=1)
set_pwr_btn.grid(                   row=1,  column=0)
lsr_pwrup_btn.grid(                 row=2,  column=0)
lsr_pwrdwn_btn.grid(                row=3,  column=0)
lsr_fire_btn.grid(                  row=4,  column=0)
lsr_blank_btn.grid(                 row=5,  column=0)
lsr_unblank_btn.grid(               row=6,  column=0)

move_laser_to_point_button.grid(    row=4,  column=4)
scan_target_button.grid(            row=4,  column=1)
stop_scan_button.grid(              row=5,  column=1)
# track_target_button.grid(           row=4,  column=2)
# end_track_target_button.grid(       row=5,  column=2)
create_target_button.grid(          row=10, column=0)
destroy_target_button.grid(         row=11, column=0)
global_target_btn.grid(             row=12, column=0)
change_target_mood_btn.grid(        row=13, column=0)
move_target_btn.grid(               row=13, column=4)

#### Command Button Options -- Do Not Use ####
# draw_dot_button.grid(               row=10,  column=0)
# create_target_button.frame.grid(    row=5,  column=0)
# move_target_btn.frame.grid(         row=5,  column=0)
# change_target_mood_btn.frame.grid(  row=6,  column=0)
# draw_dot_button.frame.grid(         row=7,  column=0)
# scan_target_button.frame.grid(      row=8,  column=0)
# stop_scan_button.frame.grid(        row=9,  column=0)
# move2_target_button.frame.grid(     row=10, column=0)
# track_target_button.frame.grid(     row=11, column=0)
# end_track_target_button.frame.grid( row=12, column=0)
####################################################
################ Entry Declarations ################

lsrset = tk.StringVar()
lsrup = tk.StringVar()
lsrdwn = tk.StringVar()
pelset = tk.StringVar()

movelsrX = tk.StringVar()
movelsrY = tk.StringVar()
movelsrZ = tk.StringVar()

movetarX = tk.StringVar()
movetarY = tk.StringVar()
movetarZ = tk.StringVar()
tarmood = tk.StringVar()

lsrset_entry = tk.Entry(root, textvariable=lsrset, width=10)
lsrup_entry  = tk.Entry(root, textvariable=lsrup,  width=10)
lsrdwn_entry = tk.Entry(root, textvariable=lsrdwn, width=10)
pelset_entry = tk.Entry(root, textvariable=pelset, width=10)

movelsrX_entry = tk.Entry(root, textvariable=movelsrX, width=10)
movelsrY_entry = tk.Entry(root, textvariable=movelsrY, width=10)
movelsrZ_entry = tk.Entry(root, textvariable=movelsrZ, width=10)

movetarX_entry = tk.Entry(root, textvariable=movetarX, width=10)
movetarY_entry = tk.Entry(root, textvariable=movetarY, width=10)
movetarZ_entry = tk.Entry(root, textvariable=movetarZ, width=10)
tarmood_entry  = tk.Entry(root, textvariable=tarmood,  width=10)

lsrset.set(0.00)
lsrup.set(1.0)
lsrdwn.set(1.0)
pelset.set(25.0)

movelsrX.set(32000)
movelsrY.set(32000)
movelsrZ.set(0.0)
movetarX.set(40000)
movetarY.set(40000)
movetarZ.set(5.0)
tarmood.set('S')

lsrset_entry.grid   (row=1,  column=1)
lsrup_entry.grid    (row=2,  column=1)
lsrdwn_entry.grid   (row=3,  column=1)
pelset_entry.grid   (row=5,  column=2)

movelsrX_entry.grid (row=4,  column=5)
movelsrY_entry.grid (row=4,  column=6)
movelsrZ_entry.grid (row=4,  column=7)
movetarX_entry.grid (row=13, column=5)
movetarY_entry.grid (row=13, column=6)
movetarZ_entry.grid (row=13, column=7)
tarmood_entry.grid  (row=13, column=8)

################ Functions and Commands ################

################### Laser Button Commands ####################
def lp_lsron_cmd():
    print("Testing Laser On Command")
    laser = LaserPointer()
    laser = centerLaser(laser)
    set_onoff_label_text.set("LSR ON")
    # print("{0} : {1} : {2} \n".format(laser.xcoord,
    #                 laser.ycoord,laser.pwm))
    setFireFlag()
    setReactFlag()
    setScanFlag()
    setTrackFlag()
    setLaserMode_Label(7) # INIT
    setLaserX_Label(laser,1)
    setLaserY_Label(laser,1)
    setLaserXWidth_Label(laser,1)
    setLaserYWidth_Label(laser,1)
    setLaserPWM_Label(laser,0) # 0.1 % pwm
    setLaserTDetect_Label(laser,0)
    setLaserTLock_Label(laser,0)
    setLaserTDist_Label(laser,0)
    setLaserTDisp_Label(laser,0)
    globals()['GLOBAL_LASER'] = laser
    return laser

def lp_lsroff_cmd(laser):
    print("Laser Off")
    laser = blankLaser(laser)
    laser = centerLaser(laser)
    set_onoff_label_text.set("LSR OFF")
    setFireFlag()
    setReactFlag()
    setScanFlag()
    setTrackFlag()
    setLaserMode_Label(0) # OFF
    setLaserX_Label(laser,0)
    setLaserY_Label(laser,0)
    setLaserXWidth_Label(laser,0)
    setLaserYWidth_Label(laser,0)
    setLaserPWM_Label(laser,0) # 0.1 % pwm
    setLaserTDetect_Label(laser,0)
    setLaserTLock_Label(laser,0)
    setLaserTDist_Label(laser,0)
    setLaserTDisp_Label(laser,0)
    globals()['GLOBAL_LASER'] = laser
    return laser
    del laser

def lp_lsr_set_pwr_cmd(laser):
    laser.pwm = float(lsrset.get())
    set_pwr_label_text.set("SET")
    print("Laser Power set to: {:.2f}".format(laser.pwm)) # DBPRINT
    globals()['GLOBAL_LASER'] = laser
    return laser

def lp_fire_cmd(laser):
    print("Firing Laser")
    setLaserX_Label(laser,1)
    setLaserY_Label(laser,1)
    setLaserXWidth_Label(laser,1)
    setLaserYWidth_Label(laser,1)
    setLaserMode_Label(2) # FIRE
    set_pwr_label_text.set("SET")
    clearFireFlag()
    while(FIRE_FLAG == 0):
        laser.pwm = float(lsrset.get())
        setLaserPWM_Label(laser,2)
        ## code here for DAC0 output
        root.update_idletasks()
        root.update()
    laser.pwm = 0.0
    setLaserPWM_Label(laser,1)
    if TRACK_FLAG == 0:
        setLaserMode_Label(3) # TRACK
    elif SCAN_FLAG == 0:
        setLaserMode_Label(4) # SCAN
    else:
        setLaserMode_Label(6) # BLANK
    globals()['GLOBAL_LASER'] = laser
    return laser

def lp_lsr_blank_cmd(laser):
    laser = blankLaser(laser)
    globals()['GLOBAL_LASER'] = laser
    return laser

def lp_lsr_unblank_cmd(laser):
    laser = unBlankLaser(laser)
    globals()['GLOBAL_LASER'] = laser
    return laser

def lp_laserPwrInc(laser):
    laser.pwm += float(lsrup.get())
    lsrset.set(laser.pwm)
    setLaserPWM_Label(laser,1)
    globals()['GLOBAL_LASER'] = laser
    return laser

def lp_laserPwrDec(laser):
    laser.pwm -= float(lsrdwn.get())
    lsrset.set(laser.pwm)
    globals()['GLOBAL_LASER'] = laser
    return laser

def lp_stop_scan_cmd(target,laser):
    print("\nScan stopped")
    laser = blankLaser(laser)
    setScanFlag()
    setReactFlag()
    setFireFlag()
    laser.xcoord = target.xloc
    laser.ycoord = target.yloc
    setup_laser_labels(laser)
    if TRACK_FLAG == 0:
        setLaserMode_Label(3) # TRACK
    else:
        setLaserMode_Label(6) # BLANK
    globals()['GLOBAL_LASER'] = laser
    return laser

def lp_scan_target_cmd(target,laser):
    print("\nTesting scan_target_cmd")
    clearScanFlag()
    clearReactFlag()
    # laser = unBlankLaser(laser)
    lsrset.set(laser.pwm)
    setLaserPWM_Label(laser,1)
    target.pel += (float(pelset.get()) * float(lsrset.get()))
    globals()['PEL_1'] = target.pel
    setTar_PEL_Label(target,2)
    while(SCAN_FLAG == 0):
        laser.xcoord = target.xloc
        laser.ycoord = target.yloc
        setLaserMode_Label(4) # SCAN
        setLaserX_Label(laser,1)
        setLaserY_Label(laser,1)
        setWidthLabels(target,laser)
        #scanTargetBox(target,laser)
        root.update_idletasks()
        root.update()
    if TRACK_FLAG == 0:
        setLaserMode_Label(3) # TRACK
    else:
        setLaserMode_Label(1) # ARM
    laser.pwm = 0.0
    lsrset.set(laser.pwm)
    target.pel += (50 * float(lsrset.get()))
    globals()['PEL_1'] = target.pel
    setTar_PEL_Label(target,2)
    setup_target_labels(target)
    setup_laser_labels(laser)
    globals()['GLOBAL_LASER'] = laser
    globals()['GLOBAL_TARGET'] = target
    return laser

def lp_end_track_target_cmd():
    setTrackFlag()
    if SCAN_FLAG == 0:
        setLaserMode_Label(4) # SCAN
    else:
        setLaserMode_Label(1) # ARM

def lp_track_target_cmd(target,laser):
    clearTrackFlag()
    while(TRACK_FLAG == 0):
        laser.xcoord = target.xloc
        laser.ycoord = target.yloc
        setLaserMode_Label(3) # TRACK
        setup_laser_labels(laser)
        setWidthLabels(target,laser)
        root.update_idletasks()
        root.update()
    if SCAN_FLAG == 0:
        setLaserMode_Label(4) # SCAN
    elif FIRE_FLAG == 0:
        setLaserMode_Label(2) # FIRE
    else:
        setLaserMode_Label(1) # ARM
    setLaserTLock_Label(laser,0)
    setLaserTDetect_Label(laser,0)
    setTar_Lock_Label(target,0)
    globals()['GLOBAL_LASER'] = laser
    return laser

def lp_moveLaserToPoint(laser,xp,yp):
    laser.xcoord = xp
    laser.ycoord = yp
    print("x: {:.2f}\ty: {:.2f}".format(laser.xcoord,laser.ycoord))
    setup_laser_labels(laser)
    globals()['GLOBAL_LASER'] = laser
    return laser

def lp_move2_target_cmd(target,laser):
    print("\nTesting move2_target_cmd")
    laser.xcoord = target.xloc
    laser.ycoord = target.yloc
    setLaserMode_Label(1) # ARM
    setLaserX_Label(laser,1)
    setLaserY_Label(laser,1)
    setLaserXWidth_Label(laser,1)
    setLaserYWidth_Label(laser,1)
    setLaserPWM_Label(laser,1)
    globals()['GLOBAL_LASER'] = laser
    globals()['GLOBAL_TARGET'] = target
    print("Laser:\t{0} : {1} : {2}\n".format(laser.xcoord,
                    laser.ycoord,laser.pwm))
    print("{0} : {1} : {2} : {3} : {4}\n".format(target.xloc,
                    target.yloc,target.dist,target.disp,target.pel))
    return laser

def lp_draw_dot_cmd(target,laser):
    print("Testing lp_draw_dot_cmd")
    setTrackFlag()
    laser = centerLaser(laser)
    laser = blankLaser(laser)
    setLaserMode_Label(2) # FIRE
    setLaserX_Label(laser,1)
    setLaserY_Label(laser,1)
    setLaserXWidth_Label(laser,0)
    setLaserYWidth_Label(laser,0)
    setLaserPWM_Label(laser,1)
    setLaserTDisp_Label(target,0)
    setLaserTDist_Label(target,0)
    print("Dot:\t{0} : {1} : {2} \n".format(laser.xcoord,
                    laser.ycoord,laser.pwm))
    globals()['GLOBAL_LASER'] = laser
    return laser

################### Target Button Commands ###################
def t_create_target_cmd():
    print("Creating New Target\n")
    target = TargetClass(1)
    globals()['PEL_1'] = target.pel
    globals()['GLOBAL_TARGET'] = target
    setTar_Mode_Label(target,1)
    return target

def t_destroy_target_cmd(target):
    print("Target go BOOM!!\n")
    target.xloc = 0
    target.yloc = 0
    target.dist = 1.0
    target.disp = 'U'
    target.pel = 0.0
    globals()['PEL_1'] = target.pel
    setTar_PEL_Label(target,2)
    setup_target_labels(target)
    globals()['GLOBAL_TARGET'] = target
    setLaserTDist_Label(target,0)
    setLaserTDisp_Label(target,0)
    return target
    del target

def t_setGlobalTarget(target):
    print("Setting Global to Target's value\n")
    target.xloc = 37654
    target.yloc = 36342
    target.dist = 5.2
    target.disp = 'F'
    target.pel = 12
    globals()['PEL_1'] = target.pel
    setup_target_labels(target)
    globals()['GLOBAL_TARGET'] = target
    return target

def t_moveTarget(target):
    print("Setting Global to Target's value\n")
    target.xloc = int(movetarX.get())
    target.yloc = int(movetarY.get())
    target.dist = float(movetarZ.get())
    target.disp = tarmood.get()
    target.disp = 'B'
    setup_target_labels(target)
    globals()['GLOBAL_TARGET'] = target
    return target

def t_change_target_mood_cmd(target):
    print("Target becomes agressive!!")
    target.xloc = 3745
    target.yloc = 4457
    target.dist = 3.7
    target.disp = 'A'
    # target.pel = 25
    # globals()['PEL_1'] = target.pel
    setup_target_labels(target)
    # print("{0} : {1} : {2} : {3} : {4}\n".format(target.xloc,
    #                 target.yloc,target.dist,target.disp,target.pel))
    globals()['GLOBAL_TARGET'] = target
    return target

# ### Start of Construction Zone Pylon ####
#
# def t_moveTargetRandy(laser,num):
#     laser.xcoord = math.floor(XMAX/2)
#     laser.ycoord = math.floor(YMAX/2)
#     globals()['GLOBAL_LASER'] = laser
#     return laser
#
# ### End of Construction Zone Pylon ####

####################################################
########### Laser Scanners and Trackers ############

def getScanWidth(target,cameramax,scanWidth,betadeg):
    base = (2*(cameramax*scanWidth*math.tan(betadeg)/(target.dist)))
    print("scan size: {0:.0f} pixels\n".format(base)); ## DBPRINT
    return base

def calculateBoxCorners(target,laser):
    xw = math.floor(getScanWidth(target,XMAX,3.0,CAMERA_VIEW_ANGLE))
    yw = math.floor(getScanWidth(target,YMAX,1.5,CAMERA_VIEW_ANGLE))
    globals()['XWIDTH'] = xw
    globals()['YWIDTH'] = yw
    x0 = laser.xcoord - (xw * 0.5)
    y0 = laser.ycoord - (yw * 0.5)
    xf = laser.xcoord + (xw * 0.5)
    yf = laser.ycoord + (yw * 0.5)
    x0 = XMIN if(x0 < XMIN) else x0
    y0 = YMIN if(y0 < YMIN) else y0
    xf = XMAX if (xf > XMAX) else xf
    yf = YMAX if (yf > YMAX) else yf
    print("{0:.2f}\n".format(x0))
    print("{0:.2f}\n".format(y0))
    print("{0:.2f}\n".format(xf))
    print("{0:.2f}\n".format(yf))
    cornerArray = [x0,y0,xf,yf,xw,yw]
    return cornerArray

def scanTargetBox(target,laser):
    carr = calculateBoxCorners(target,laser)
    laser.xcoord = carr[0]
    laser.ycoord = carr[1]
    while (SCAN_FLAG == 0):
        for laser.ycoord in range (math.floor(carr[3])):
            laser.ycoord +=1
            for laser.xcoord in range (math.floor(carr[2])):
                laser.xcoord +=1
            root.update_idletasks()
            root.update()
        root.update_idletasks()
        root.update()
    globals()['GLOBAL_LASER'] = laser
    return laser

def laserReactToTarget(target, laser):
    print("Laser react to Target\n")
    clearReactFlag()
    while(REACT_FLAG==0):
        print("TEST")
        ## add code that makes laser
        ## read target mood and react accordingly
    globals()['GLOBAL_LASER'] = laser
    return laser

##############################################
################ Flag Togglers ###############
def setTrackFlag():
    globals()['TRACK_FLAG'] = 1
    return TRACK_FLAG
def clearTrackFlag():
    globals()['TRACK_FLAG'] = 0
    return TRACK_FLAG
def setScanFlag():
    globals()['SCAN_FLAG'] = 1
    return SCAN_FLAG
def clearScanFlag():
    globals()['SCAN_FLAG'] = 0
    return SCAN_FLAG
def setReactFlag():
    globals()['REACT_FLAG'] = 1
    return REACT_FLAG
def clearReactFlag():
    globals()['REACT_FLAG'] = 0
    return REACT_FLAG
def setFireFlag():
    globals()['FIRE_FLAG'] = 1
    return FIRE_FLAG
def clearFireFlag():
    globals()['FIRE_FLAG'] = 0
    return FIRE_FLAG

#####################################################
############## Blanking and Centering ###############
def blankLaser(laser):
    print("Blanking Laser")
    setFireFlag()
    globals()['GLOBAL_BLANKER_PWM'] = laser.pwm
    laser.pwm = 0.0
    lsrset.set(laser.pwm)
    # setLaserPWM_Label(laser,1)
    set_pwr_label_text.set("UNSET")
    globals()['GLOBAL_LASER'] = laser
    setLaserMode_Label(6) # BLANK
    return laser

def unBlankLaser(laser):
    laser.pwm = GLOBAL_BLANKER_PWM
    lsrset.set(laser.pwm)
    set_pwr_label_text.set("SET")
    print("Unblanking Laser, pwm = {:.3f}".format(laser.pwm))
    if SCAN_FLAG == 0:
        setLaserMode_Label(4) # SCAN
    else:
        setLaserMode_Label(1) # ARM
    globals()['GLOBAL_LASER'] = laser
    return laser

def centerLaser(laser):
    laser.xcoord = math.floor(XMAX/2)
    laser.ycoord = math.floor(YMAX/2)
    globals()['GLOBAL_LASER'] = laser
    return laser

# def createLaser(xcoord,ycoord,pwm):
#     print("Creating Laser\n")
#     laser = LaserPointer(xcoord,ycoord,pwm)
#     globals()['GLOBAL_LASER'] = laser
#     return laser

###############################################
################ Label Setters ################
def setup_laser_labels(laser):
    setLaserMode_Label(1)
    setLaserX_Label(laser,1)
    setLaserY_Label(laser,1)
    setLaserXWidth_Label(laser,1)
    setLaserYWidth_Label(laser,1)
    setLaserPWM_Label(laser,1)
    setLaserTLock_Label(laser,1)
    setLaserTDetect_Label(laser,1)

def setup_target_labels(target):
    if target.instance == 1:
        setTar_Mode_Label(target,1)
        setTar_X_Label(target,1)
        setTar_Y_Label(target,1)
        setTar_Detect_Label(target,1)
        setTar_Dist_Label(target,1)
        setTar_Disp_Label(target,1)
        setTar_Lock_Label(target,1)
        setTar_PEL_Label(target,1)
        setLaserTDist_Label(target,1)
        setLaserTDisp_Label(target,1)
#     elif target.instance == 2:
#         # setT2_Mode_Label(target,1)
#         setT2_X_Label(target,1)
#         setT2_Y_Label(target,1)
#         setT2_Detect_Label(target,1)
#         setT2_Dist_Label(target,1)
#         setT2_Disp_Label(target,1)
#         setT2_Lock_Label(target,1)
#         setT2_PEL_Label(target,1)
#     elif target.instance == 3:
#         # setT3_Mode_Label(target,1)
#         setT3_X_Label(target,1)
#         setT3_Y_Label(target,1)
#         setT3_Dist_Label(target,1)
#         setT3_Detect_Label(target,1)
#         setT3_Disp_Label(target,1)
#         setT3_PEL_Label(target,1)
#
def setWidthLabels(target,laser):
    globals()['XWIDTH'] = math.floor(getScanWidth(target,XMAX,3.0,CAMERA_VIEW_ANGLE))
    globals()['YWIDTH'] = math.floor(getScanWidth(target,YMAX,1.5,CAMERA_VIEW_ANGLE))
    setLaserXWidth_Label(laser,1)
    setLaserYWidth_Label(laser,1)

def setLaserMode_Label(num):
    if (num == 0):
        lchan_mode_label_text.set("OFF")
    elif (num == 1):
        lchan_mode_label_text.set("ARM")
    elif (num == 2):
        lchan_mode_label_text.set("FIRE")
    elif (num == 3):
        lchan_mode_label_text.set("TRACK")
    elif (num == 4):
        lchan_mode_label_text.set("SCAN")
    elif (num == 5):
        lchan_mode_label_text.set("TRK/SCN")
    elif (num == 6):
        lchan_mode_label_text.set("BLANK")
    elif (num == 7):
        lchan_mode_label_text.set("INIT")
    elif (num == 8):
        lchan_mode_label_text.set("UNUSED")

def setLaserX_Label(laser,num):
    if (num == 0):
        lchan_xcoord_label_text.set(0)
    elif (num == 1):
        lchan_xcoord_label_text.set("{0}".format(laser.xcoord))
    elif (num == 2):
        lchan_xcoord_label_text.set("{0}".format(int(movelsrX.get())))
    elif (num == 3):
        lchan_xcoord_label_text.set("NaN")

def setLaserY_Label(laser,num):
    if (num == 0):
        lchan_ycoord_label_text.set(0)
    elif (num == 1):
        lchan_ycoord_label_text.set("{0}".format(laser.ycoord))
    elif (num == 2):
        lchan_ycoord_label_text.set("{0}".format(int(movelsrY.get())))
    elif (num == 3):
        lchan_ycoord_label_text.set("NaN")

def setLaserXWidth_Label(laser,num):
    if (num == 0):
        lchan_xwidth_label_text.set(1)
    elif(num == 2):
        lchan_xwidth_label_text.set("{0}".format(XWIDTH))
    if((SCAN_FLAG==0)&(num==1)):
        lchan_xwidth_label_text.set("{0}".format(XWIDTH))
    else:
        lchan_xwidth_label_text.set(1)

def setLaserYWidth_Label(laser,num):
    if (num == 0):
        lchan_ywidth_label_text.set(1)
    elif(num == 2):
        lchan_ywidth_label_text.set("{0}".format(YWIDTH))
    if((SCAN_FLAG==0)&(num==1)):
        lchan_ywidth_label_text.set("{0}".format(YWIDTH))
    else:
        lchan_ywidth_label_text.set(1)

def setLaserPWM_Label(laser,num):
    if (num == 0):
        lchan_pwm_label_text.set("{0}".format(0))
    elif (num == 1):
        lchan_pwm_label_text.set("{:.3f}".format(laser.pwm))
    elif (num == 2):
        lchan_pwm_label_text.set("{0}".format(lsrset.get()))
    elif (num == 3):
        lchan_pwm_label_text.set("{0}".format(1.0))

def setLaserTDetect_Label(laser,num):
    if (num == 0):
        lchan_tdetect_label_text.set("NONE")
    elif (num == 1):
        lchan_tdetect_label_text.set(1)
    elif (num == 2):
        lchan_tdetect_label_text.set(2)
    elif (num == 3):
        lchan_tdetect_label_text.set(3)

def setLaserTLock_Label(laser,num):
    if (num == 0):
        lchan_tlock_label_text.set("NONE")
    elif (num == 1):
        lchan_tlock_label_text.set("LOCKED")
    elif (num == 2):
        lchan_tlock_label_text.set("UNLOCK")
    elif (num == 3):
        lchan_tlock_label_text.set(" ")

def setLaserTDisp_Label(target,num):
    if (num == 0):
        lchan_tdispo_label_text.set('U') # Unspecified
    elif (num == 1):
        lchan_tdispo_label_text.set("{0}".format(target.disp))
    elif (num == 2):
        lchan_tdispo_label_text.set("O") # Owner
    elif (num == 3):
        lchan_tdispo_label_text.set("C") # Child
    elif (num == 4):
        lchan_tdispo_label_text.set("P") # Pet

def setLaserTDist_Label(target,num):
    if (num == 0):
        lchan_tdist_label_text.set(0)
    elif (num == 1):
        lchan_tdist_label_text.set("{0}".format(target.dist))
        # lchan_tdist_label_text.set("{0}".format(tchan_1_tdist_label_text.get()))
    elif (num == 2):
        lchan_tdist_label_text.set("OOB")
    elif (num == 3):
        lchan_tdist_label_text.set("NaN")

def setTar_Mode_Label(target,num):
    if target.instance == 1:
        if (num == 0):
            tchan_1_mode_label_text.set("NONE")
        elif (num == 1):
            tchan_1_mode_label_text.set("ACTIVE")
        elif (num == 2):
            tchan_1_mode_label_text.set("PERP")
        elif (num == 3):
            tchan_1_mode_label_text.set("MASTER")
        elif (num == 4):
            tchan_1_mode_label_text.set("LADY")
        elif (num == 5):
            tchan_1_mode_label_text.set("ADMIN")
        elif (num == 6):
            tchan_1_mode_label_text.set("CHILD")
        elif (num == 7):
            tchan_1_mode_label_text.set("GONE")
    elif target.instance == 2:
        if (num == 0):
            tchan_2_mode_label_text.set("NONE")
        elif (num == 1):
            tchan_2_mode_label_text.set("ACTIVE")
        elif (num == 2):
            tchan_2_mode_label_text.set("PERP")
        elif (num == 3):
            tchan_2_mode_label_text.set("MASTER")
        elif (num == 4):
            tchan_2_mode_label_text.set("LADY")
        elif (num == 5):
            tchan_2_mode_label_text.set("ADMIN")
        elif (num == 6):
            tchan_2_mode_label_text.set("CHILD")
        elif (num == 7):
            tchan_2_mode_label_text.set("GONE")
    elif target.instance == 3:
        if (num == 0):
            tchan_3_mode_label_text.set("NONE")
        elif (num == 1):
            tchan_3_mode_label_text.set("ACTIVE")
        elif (num == 2):
            tchan_3_mode_label_text.set("PERP")
        elif (num == 3):
            tchan_3_mode_label_text.set("MASTER")
        elif (num == 4):
            tchan_3_mode_label_text.set("LADY")
        elif (num == 5):
            tchan_3_mode_label_text.set("ADMIN")
        elif (num == 6):
            tchan_3_mode_label_text.set("CHILD")
        elif (num == 7):
            tchan_3_mode_label_text.set("GONE")

def setTar_X_Label(target,num):
    if target.instance == 1:
        if (num == 0):
            tchan_1_xcoord_label_text.set(0)
        elif (num == 1):
            tchan_1_xcoord_label_text.set("{0}".format(target.xloc))
        elif (num == 2):
            tchan_1_xcoord_label_text.set("OOB")
        elif (num == 3):
            tchan_1_xcoord_label_text.set("NaN")
    elif target.instance == 2:
        if (num == 0):
            tchan_2_xcoord_label_text.set(0)
        elif (num == 1):
            tchan_2_xcoord_label_text.set("{0}".format(target.xloc))
        elif (num == 2):
            tchan_2_xcoord_label_text.set("OOB")
        elif (num == 3):
            tchan_2_xcoord_label_text.set("NaN")
    elif target.instance == 3:
        if (num == 0):
            tchan_3_xcoord_label_text.set(0)
        elif (num == 1):
            tchan_3_xcoord_label_text.set("{0}".format(target.xloc))
        elif (num == 2):
            tchan_3_xcoord_label_text.set("OOB")
        elif (num == 3):
            tchan_3_xcoord_label_text.set("NaN")

def setTar_Y_Label(target,num):
    if target.instance == 1:
        if (num == 0):
            tchan_1_ycoord_label_text.set("{0}".format(0))
        elif (num == 1):
            tchan_1_ycoord_label_text.set("{0}".format(target.yloc))
        elif (num == 2):
            tchan_1_ycoord_label_text.set("OOB")
        elif (num == 3):
            tchan_1_ycoord_label_text.set("NaN")
    elif target.instance == 2:
        if (num == 0):
            tchan_2_ycoord_label_text.set("{0}".format(0))
        elif (num == 1):
            tchan_2_ycoord_label_text.set("{0}".format(target.yloc))
        elif (num == 2):
            tchan_2_ycoord_label_text.set("OOB")
        elif (num == 3):
            tchan_2_ycoord_label_text.set("NaN")
    elif target.instance == 3:
        if (num == 0):
            tchan_3_ycoord_label_text.set(0)
        elif (num == 1):
            tchan_3_ycoord_label_text.set("{0}".format(target.xloc))
        elif (num == 2):
            tchan_3_ycoord_label_text.set("OOB")
        elif (num == 3):
            tchan_3_ycoord_label_text.set("NaN")

def setTar_Detect_Label(target,num):
    if target.instance == 1:
        if (num == 0):
            tchan_1_tdetect_label_text.set("NO")
        elif (num == 1):
            tchan_1_tdetect_label_text.set("{0}".format(lchan_tdetect_label_text.get()))
        elif (num == 2):
            tchan_1_tdetect_label_text.set("{0}".format(2))
        elif (num == 3):
            tchan_1_tdetect_label_text.set("{0}".format(3))
    elif target.instance == 2:
        if (num == 0):
            tchan_2_tdetect_label_text.set("NO")
        elif (num == 1):
            tchan_2_tdetect_label_text.set("{0}".format(lchan_tdetect_label_text.get()))
        elif (num == 2):
            tchan_2_tdetect_label_text.set("{0}".format(2))
        elif (num == 3):
            tchan_2_tdetect_label_text.set("{0}".format(3))
    elif target.instance == 3:
        if (num == 0):
            tchan_3_tdetect_label_text.set("NO")
        elif (num == 1):
            tchan_3_tdetect_label_text.set("{0}".format(lchan_tdetect_label_text.get()))
        elif (num == 2):
            tchan_3_tdetect_label_text.set("{0}".format(2))
        elif (num == 3):
            tchan_3_tdetect_label_text.set("{0}".format(3))

def setTar_Dist_Label(target,num):
    if target.instance == 1:
        if (num == 0):
            tchan_1_tdist_label_text.set("NO")
        elif (num == 1):
            tchan_1_tdist_label_text.set("{0}".format(target.dist))
        elif (num == 2):
            tchan_1_tdist_label_text.set("{0}".format(2))
        elif (num == 3):
            tchan_1_tdist_label_text.set("{0}".format(3))
    elif target.instance == 2:
        if (num == 0):
            tchan_2_tdist_label_text.set("NO")
        elif (num == 1):
            tchan_2_tdist_label_text.set("{0}".format(target.dist))
        elif (num == 2):
            tchan_2_tdist_label_text.set("{0}".format(2))
        elif (num == 3):
            tchan_2_tdist_label_text.set("{0}".format(3))
    elif target.instance == 3:
        if (num == 0):
            tchan_3_tdist_label_text.set("NO")
        elif (num == 1):
            tchan_3_tdist_label_text.set("{0}".format(target.dist))
        elif (num == 2):
            tchan_3_tdist_label_text.set("{0}".format(2))
        elif (num == 3):
            tchan_3_tdist_label_text.set("{0}".format(3))

def setTar_Disp_Label(target,num):
    if target.instance == 1:
        if (num == 0):
            tchan_1_tdispo_label_text.set("NO")
        elif (num == 1):
            tchan_1_tdispo_label_text.set("{0}".format(target.disp))
        elif (num == 2):
            tchan_1_tdispo_label_text.set("{0}".format(2))
        elif (num == 3):
            tchan_1_tdispo_label_text.set("{0}".format(3))
    elif target.instance == 2:
        if (num == 0):
            tchan_2_tdispo_label_text.set("NO")
        elif (num == 1):
            tchan_2_tdispo_label_text.set("{0}".format(target.disp))
        elif (num == 2):
            tchan_2_tdispo_label_text.set("{0}".format(2))
        elif (num == 3):
            tchan_2_tdispo_label_text.set("{0}".format(3))
    elif target.instance == 3:
        if (num == 0):
            tchan_3_tdispo_label_text.set("NO")
        elif (num == 1):
            tchan_3_tdispo_label_text.set("{0}".format(target.disp))
        elif (num == 2):
            tchan_3_tdispo_label_text.set("{0}".format(2))
        elif (num == 3):
            tchan_3_tdispo_label_text.set("{0}".format(3))

def setTar_Lock_Label(target,num):
    if target.instance == 1:
        if (num == 0):
            tchan_1_tlock_label_text.set("NO")
        elif (num == 1):
            tchan_1_tlock_label_text.set("{0}".format(lchan_tlock_label_text.get()))
        elif (num == 2):
            tchan_1_tlock_label_text.set("{0}".format(2))
        elif (num == 3):
            tchan_1_tlock_label_text.set("{0}".format(3))
    elif target.instance == 2:
        if (num == 0):
            tchan_2_tlock_label_text.set("NO")
        elif (num == 1):
            tchan_2_tlock_label_text.set("{0}".format(lchan_tlock_label_text.get()))
        elif (num == 2):
            tchan_2_tlock_label_text.set("{0}".format(2))
        elif (num == 3):
            tchan_2_tlock_label_text.set("{0}".format(3))
    elif target.instance == 3:
        if (num == 0):
            tchan_3_tlock_label_text.set("NO")
        elif (num == 1):
            tchan_3_tlock_label_text.set("{0}".format(lchan_tlock_label_text.get()))
        elif (num == 2):
            tchan_3_tlock_label_text.set("{0}".format(2))
        elif (num == 3):
            tchan_3_tlock_label_text.set("{0}".format(3))

def setTar_PEL_Label(target,num):
    if target.instance == 1:
        if (num == 0):
            tchan_1_tpel_label_text.set("NO")
        elif (num == 1):
            tchan_1_tpel_label_text.set("{0}".format(target.pel))
        elif (num == 2):
            tchan_1_tpel_label_text.set("{0}".format(PEL_1))
        elif (num == 3):
            tchan_1_tpel_label_text.set("{0}".format(1))
    elif target.instance == 2:
        if (num == 0):
            tchan_2_tpel_label_text.set("NO")
        elif (num == 1):
            tchan_2_tpel_label_text.set("{0}".format(target.pel))
        elif (num == 2):
            tchan_1_tpel_label_text.set("{0}".format(PEL_2))
        elif (num == 3):
            tchan_1_tpel_label_text.set("{0}".format(2))
    elif target.instance == 3:
        if (num == 0):
            tchan_3_tpel_label_text.set("NO")
        elif (num == 1):
            tchan_3_tpel_label_text.set("{0}".format(target.pel))
        elif (num == 2):
            tchan_1_tpel_label_text.set("{0}".format(PEL_3))
        elif (num == 3):
            tchan_3_tpel_label_text.set("{0}".format(3))

#################################################################
##################### Label Declarations ########################

######### Channel Labels for Lasers and Targets ##########
# # lchan_title     = tk.StringVar()
lchan_mode      = tk.StringVar()
lchan_xcoord    = tk.StringVar()
lchan_ycoord    = tk.StringVar()
lchan_xwidth    = tk.StringVar()
lchan_ywidth    = tk.StringVar()
lchan_pwm       = tk.StringVar()
lchan_tdetect   = tk.StringVar()
lchan_tlock     = tk.StringVar()
lchan_tdispo    = tk.StringVar()
lchan_tdist     = tk.StringVar()

# lchan_title_label_text = tk.StringVar()
# lchan_title_label_text.set("Laser 1:")
# lchan_title_label = tk.Label(root, textvariable=lchan_title_label_text, width=8)
# lchan_title_label.grid(row=1, column=3)

lchan_mode_label_text = tk.StringVar()
lchan_mode_label_text.set("safe")
lchan_mode_label = tk.Label(root, textvariable=lchan_mode_label_text, width=8)
lchan_mode_label.grid(row=1, column=4)

lchan_xcoord_label_text = tk.StringVar()
lchan_xcoord_label_text.set("0")
lchan_xcoord_label = tk.Label(root, textvariable=lchan_xcoord_label_text, width=8)
lchan_xcoord_label.grid(row=1, column=5)

lchan_ycoord_label_text = tk.StringVar()
lchan_ycoord_label_text.set("0")
lchan_ycoord_label = tk.Label(root, textvariable=lchan_ycoord_label_text, width=8)
lchan_ycoord_label.grid(row=1, column=6)

lchan_xwidth_label_text = tk.StringVar()
lchan_xwidth_label_text.set("0")
lchan_xwidth_label = tk.Label(root, textvariable=lchan_xwidth_label_text, width=8)
lchan_xwidth_label.grid(row=1, column=7)

lchan_ywidth_label_text = tk.StringVar()
lchan_ywidth_label_text.set("0")
lchan_ywidth_label = tk.Label(root, textvariable=lchan_ywidth_label_text, width=8)
lchan_ywidth_label.grid(row=1, column=8)

lchan_pwm_label_text = tk.StringVar()
lchan_pwm_label_text.set("0.1")
lchan_pwm_label = tk.Label(root, textvariable=lchan_pwm_label_text, width=8)
lchan_pwm_label.grid(row=1, column=9)

lchan_tdetect_label_text = tk.StringVar()
lchan_tdetect_label_text.set("None")
lchan_tdetect_label = tk.Label(root, textvariable=lchan_tdetect_label_text, width=8)
lchan_tdetect_label.grid(row=1, column=10)

lchan_tlock_label_text = tk.StringVar()
lchan_tlock_label_text.set("UL")
lchan_tlock_label = tk.Label(root, textvariable=lchan_tlock_label_text, width=8)
lchan_tlock_label.grid(row=1, column=11)

lchan_tdispo_label_text = tk.StringVar()
lchan_tdispo_label_text.set("U")
lchan_tdispo_label = tk.Label(root, textvariable=lchan_tdispo_label_text, width=8)
lchan_tdispo_label.grid(row=1, column=12)

lchan_tdist_label_text = tk.StringVar()
lchan_tdist_label_text.set("0")
lchan_tdist_label = tk.Label(root, textvariable=lchan_tdist_label_text, width=8)
lchan_tdist_label.grid(row=1, column=13)

# tchan_1_title    = tk.StringVar()
tchan_1_mode     = tk.StringVar()
tchan_1_xcoord   = tk.StringVar()
tchan_1_ycoord   = tk.StringVar()
tchan_1_xwidth   = tk.StringVar()
tchan_1_ywidth   = tk.StringVar()
tchan_1_pwm      = tk.StringVar()
tchan_1_tdetect  = tk.StringVar()
tchan_1_tdist    = tk.StringVar()
tchan_1_tdispo   = tk.StringVar()
tchan_1_tlock    = tk.StringVar()
tchan_1_tpel     = tk.StringVar()

# tchan_1_title_label_text = tk.StringVar()
# tchan_1_title_label_text.set("Target 1:")
# tchan_1_title_label = tk.Label(root, textvariable=tchan_1_title_label_text, width=8)
# tchan_1_title_label.grid(row=4, column=3)

tchan_1_mode_label_text = tk.StringVar()
tchan_1_mode_label_text.set("safe")
tchan_1_mode_label = tk.Label(root, textvariable=tchan_1_mode_label_text, width=8)
tchan_1_mode_label.grid(row=10, column=4)

tchan_1_xcoord_label_text = tk.StringVar()
tchan_1_xcoord_label_text.set("0")
tchan_1_xcoord_label = tk.Label(root, textvariable=tchan_1_xcoord_label_text, width=8)
tchan_1_xcoord_label.grid(row=10, column=5)

tchan_1_ycoord_label_text = tk.StringVar()
tchan_1_ycoord_label_text.set("0")
tchan_1_ycoord_label = tk.Label(root, textvariable=tchan_1_ycoord_label_text, width=8)
tchan_1_ycoord_label.grid(row=10, column=6)

tchan_1_tdetect_label_text = tk.StringVar()
tchan_1_tdetect_label_text.set("NONE")
tchan_1_tdetect_label = tk.Label(root, textvariable=tchan_1_tdetect_label_text, width=8)
tchan_1_tdetect_label.grid(row=10, column=7)

tchan_1_tdist_label_text = tk.StringVar()
tchan_1_tdist_label_text.set("0")
tchan_1_tdist_label = tk.Label(root, textvariable=tchan_1_tdist_label_text, width=8)
tchan_1_tdist_label.grid(row=10, column=8)

tchan_1_tdispo_label_text = tk.StringVar()
tchan_1_tdispo_label_text.set("U")
tchan_1_tdispo_label = tk.Label(root, textvariable=tchan_1_tdispo_label_text, width=8)
tchan_1_tdispo_label.grid(row=10, column=9)

tchan_1_tlock_label_text = tk.StringVar()
tchan_1_tlock_label_text.set("NO")
tchan_1_tlock_label = tk.Label(root, textvariable=tchan_1_tlock_label_text, width=8)
tchan_1_tlock_label.grid(row=10, column=10)

tchan_1_tpel_label_text = tk.StringVar()
tchan_1_tpel_label_text.set("100")
tchan_1_tpel_label = tk.Label(root, textvariable=tchan_1_tpel_label_text, width=8)
tchan_1_tpel_label.grid(row=10, column=11)

# tchan_2_title       = tk.StringVar()
# tchan_2_mode        = tk.StringVar()
# tchan_2_xcoord      = tk.StringVar()
# tchan_2_ycoord      = tk.StringVar()
# tchan_2_xwidth      = tk.StringVar()
# tchan_2_ywidth      = tk.StringVar()
# tchan_2_pwm         = tk.StringVar()
# tchan_2_tdetect     = tk.StringVar()
# tchan_2_tdist       = tk.StringVar()
# tchan_2_tdispo      = tk.StringVar()
# tchan_2_tlock       = tk.StringVar()
# tchan_2_tpel        = tk.StringVar()
#
# tchan_2_title_label_text = tk.StringVar()
# tchan_2_title_label_text.set("Target 2:")
# tchan_2_title_label = tk.Label(root, textvariable=tchan_2_title_label_text,)
# tchan_2_title_label.grid(row=5, column=3)
#
# tchan_2_mode_label_text = tk.StringVar()
# tchan_2_mode_label_text.set("safe")
# tchan_2_mode_label = tk.Label(root, textvariable=tchan_2_mode_label_text,)
# tchan_2_mode_label.grid(row=5, column=4)
#
# tchan_2_xcoord_label_text = tk.StringVar()
# tchan_2_xcoord_label_text.set("0")
# tchan_2_xcoord_label = tk.Label(root, textvariable=tchan_2_xcoord_label_text,)
# tchan_2_xcoord_label.grid(row=5, column=5)
#
# tchan_2_ycoord_label_text = tk.StringVar()
# tchan_2_ycoord_label_text.set("0")
# tchan_2_ycoord_label = tk.Label(root, textvariable=tchan_2_ycoord_label_text,)
# tchan_2_ycoord_label.grid(row=5, column=6)
#
# tchan_2_tdetect_label_text = tk.StringVar()
# tchan_2_tdetect_label_text.set("0")
# tchan_2_tdetect_label = tk.Label(root, textvariable=tchan_2_tdetect_label_text,)
# tchan_2_tdetect_label.grid(row=5, column=7)
#
# tchan_2_tdist_label_text = tk.StringVar()
# tchan_2_tdist_label_text.set("0")
# tchan_2_tdist_label = tk.Label(root, textvariable=tchan_2_tdist_label_text,)
# tchan_2_tdist_label.grid(row=5, column=8)
#
# tchan_2_tdispo_label_text = tk.StringVar()
# tchan_2_tdispo_label_text.set("U")
# tchan_2_tdispo_label = tk.Label(root, textvariable=tchan_2_tdispo_label_text,)
# tchan_2_tdispo_label.grid(row=5, column=9)
#
# tchan_2_tlock_label_text = tk.StringVar()
# tchan_2_tlock_label_text.set("NO")
# tchan_2_tlock_label = tk.Label(root, textvariable=tchan_2_tlock_label_text,)
# tchan_2_tlock_label.grid(row=5, column=10)
#
# tchan_2_tpel_label_text = tk.StringVar()
# tchan_2_tpel_label_text.set("100")
# tchan_2_tpel_label = tk.Label(root, textvariable=tchan_2_tpel_label_text,)
# tchan_2_tpel_label.grid(row=5, column=11)
#
# tchan_3_title    = tk.StringVar()
# tchan_3_mode     = tk.StringVar()
# tchan_3_xcoord   = tk.StringVar()
# tchan_3_ycoord   = tk.StringVar()
# tchan_3_xwidth   = tk.StringVar()
# tchan_3_ywidth   = tk.StringVar()
# tchan_3_pwm      = tk.StringVar()
# tchan_3_tdetect  = tk.StringVar()
# tchan_3_tdist    = tk.StringVar()
# tchan_3_tdispo   = tk.StringVar()
# tchan_3_tlock    = tk.StringVar()
# tchan_3_tpel     = tk.StringVar()
#
# tchan_3_title_label_text = tk.StringVar()
# tchan_3_title_label_text.set("Target 3:")
# tchan_3_title_label = tk.Label(root, textvariable=tchan_3_title_label_text,)
# tchan_3_title_label.grid(row=6, column=3)
#
# tchan_3_mode_label_text = tk.StringVar()
# tchan_3_mode_label_text.set("safe")
# tchan_3_mode_label = tk.Label(root, textvariable=tchan_3_mode_label_text,)
# tchan_3_mode_label.grid(row=6, column=4)
#
# tchan_3_xcoord_label_text = tk.StringVar()
# tchan_3_xcoord_label_text.set("0")
# tchan_3_xcoord_label = tk.Label(root, textvariable=tchan_3_xcoord_label_text,)
# tchan_3_xcoord_label.grid(row=6, column=5)
#
# tchan_3_ycoord_label_text = tk.StringVar()
# tchan_3_ycoord_label_text.set("0")
# tchan_3_ycoord_label = tk.Label(root, textvariable=tchan_3_ycoord_label_text,)
# tchan_3_ycoord_label.grid(row=6, column=6)
#
# tchan_3_tdetect_label_text = tk.StringVar()
# tchan_3_tdetect_label_text.set("0")
# tchan_3_tdetect_label = tk.Label(root, textvariable=tchan_3_tdetect_label_text,)
# tchan_3_tdetect_label.grid(row=6, column=7)
#
# tchan_3_tdist_label_text = tk.StringVar()
# tchan_3_tdist_label_text.set("0")
# tchan_3_tdist_label = tk.Label(root, textvariable=tchan_3_tdist_label_text,)
# tchan_3_tdist_label.grid(row=6, column=8)
#
# tchan_3_tdispo_label_text = tk.StringVar()
# tchan_3_tdispo_label_text.set("U")
# tchan_3_tdispo_label = tk.Label(root, textvariable=tchan_3_tdispo_label_text,)
# tchan_3_tdispo_label.grid(row=6, column=9)
#
# tchan_3_tlock_label_text = tk.StringVar()
# tchan_3_tlock_label_text.set("NO")
# tchan_3_tlock_label = tk.Label(root, textvariable=tchan_3_tlock_label_text,)
# tchan_3_tlock_label.grid(row=6, column=10)
#
# tchan_3_tpel_label_text = tk.StringVar()
# tchan_3_tpel_label_text.set("100")
# tchan_3_tpel_label = tk.Label(root, textvariable=tchan_3_tpel_label_text,)
# tchan_3_tpel_label.grid(row=6, column=11)

#####################################################
################ The Label Generator ################
for a in range(30):
#     root.grid_columnconfigure(a,  minsize=column_size)
#     root.grid_rowconfigure(a,  minsize=row_size)
#
    Lasermode_label.grid(   row=0, column=4)
    xcoord_label.grid(      row=0, column=5)
    ycoord_label.grid(      row=0, column=6)
    xwidth_label.grid(      row=0, column=7)
    ywidth_label.grid(      row=0, column=8)
    pwm_label.grid(         row=0, column=9)
    target_detect_label.grid(row=0, column=10)
    target_lock_label.grid( row=0, column=11)
    target_dispo_label.grid(row=0, column=12)
    target_dist_label.grid( row=0, column=13)

    Targetmode_label.grid(  row=9, column=4)
    xc_label.grid(          row=9, column=5)
    yc_label.grid(          row=9, column=6)
    detect_label.grid(      row=9, column=7)
    dist_label.grid(        row=9, column=8)
    dispo_label.grid(       row=9, column=9)
    lock_label.grid(        row=9, column=10)
    pel_label.grid(         row=9, column=11)

    # set_pwr_label.grid(     row=1,  column=2)
    mv_laserX_label.grid(   row=3,  column=5)
    mv_laserY_label.grid(   row=3,  column=6)
    mv_laserZ_label.grid(   row=3,  column=7)

    mv_targetX_label.grid(   row=12,  column=5)
    mv_targetY_label.grid(   row=12,  column=6)
    mv_targetZ_label.grid(   row=12,  column=7)
    mv_targetMood_label.grid(row=12,  column=8)

    # create_laser_label.grid(row=1, column=1)
    # create_target_label.grid(row=2, column=1)
    # spon_label.grid(        row=3, column=1)
    # spoff_label.grid(       row=4, column=1)
    # lsron_label.grid(       row=5, column=1)
    # lsroff_label.grid(      row=6, column=1)
    # dot_label.grid(         row=7, column=1)
    # square_label.grid(      row=8, column=1)
    # move2_label.grid(       row=9, column=1)

# lc[0].frame.grid(row=0, column=3, rowspan=5, columnspan=12)
tm[0].frame.grid(row=7, column=3, rowspan=5, columnspan=12)

root.update()
root.mainloop()

#### Construction Zone Pylon ####

#### End of Construction Zone Pylon ####

