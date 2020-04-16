#######################################
#######################################
# NETWORK ADJUSTMENT LIBRARY FOR PLOTS
# Sébastien Guillaume (HEIG-VD)
# Daniel Willi (swisstopo)
# 2019
#######################################
#######################################

import numpy as np
import matplotlib.pyplot as plt

class Point:
        
    def __init__(self,id):
        self.id = id
        self.ipl_id = -1
        self.east = 0
        self.north = 0
        self.height = 0
        self.planiFix = 0
        self.heightFix = 0
        self.displ_east = 0
        self.displ_north = 0
        self.displ_height = 0
        self.ellipse_a = 0
        self.ellipse_b = 0
        self.ellipse_azi = 0
        self.fiab_NA = 0
        self.fiab_NB = 0
        self.fiab_azi = 0
        
    def printId(self):
        print('id = {}'.format(self.id))

    def printCoord(self):
        print('id = {} East = {:0.4f}  North = {:0.4f}  Height = {:0.4f}'.format(self.id,self.east,self.north,self.height))


class Observation:
        
    def __init__(self,id1,id2,type_obs):
        self.id1 = id1
        self.id2 = id2
        self.type_obs = type_obs
        
    def printObservation(self):
        print('{}->{} : {}'.format(self.id1,self.id2,self.type_obs))


def findIdFromIplID(points,ipl_id):
    for key,value in points.items():
        if value.ipl_id == ipl_id:
            return value.id

def plotPoints(points,options):
    
    #PLOT POINTS
    for key, value in points.items():
        pts_no = key
        y = value.east
        x = value.north
        if value.planiFix == '0':
            plt.plot(y,x,'s',color='black',markersize=7)
        if value.planiFix == '1':
            plt.plot(y,x,'o',color='blue',markersize=5)

        textOffset = options['textOffset'][0]
        fontSize = options['fontSize'][0]
        plt.text(y+textOffset,x+textOffset,pts_no,fontSize=fontSize)  
        
        plt.axis('equal')
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.grid(True)
        plt.xlabel(r'$E_{MN95}$ [m]',fontsize=14)
        plt.ylabel(r'$N_{MN95}$ [m]',fontsize=14)


def plotObservations(points,observations,options):
            
    #PLOT OBSERVATIONS
    for obs in observations:
        type = obs.type_obs
        sta = obs.id1
        vis = obs.id2
        sta_y = points[sta].east
        sta_x = points[sta].north
        vis_y = points[vis].east
        vis_x = points[vis].north
        D_y = vis_y-sta_y
        D_x = vis_x-sta_x        
        
        if type == 'RI':
            plt.plot([sta_y,sta_y+D_y*0.7],[sta_x,sta_x+D_x*0.7],'black',lineWidth=1)
            plt.plot([sta_y+D_y*0.7,sta_y+D_y*1.0],[sta_x+D_x*0.7,sta_x+D_x*1.0],'black',lineStyle='--',lineWidth=1)
   
        if type == 'DP':
            plt.plot([sta_y,sta_y+D_y*1],[sta_x,sta_x+D_x*1],'black',lineStyle='--',lineWidth=0.5)
            plt.plot([sta_y+D_y*0.2,sta_y+D_y*0.4],[sta_x+D_x*0.2,sta_x+D_x*0.4],'black',lineWidth=2.5)
            
            
        plt.axis('equal')
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.grid(True)
        plt.xlabel(r'$E_{MN95}$ [m]',fontsize=14)
        plt.ylabel(r'$N_{MN95}$ [m]',fontsize=14)
    
    
def plotPrecision(points,options):
    
    for key, value in points.items():
        pts_no = key
        pt_y = value.east
        pt_x = value.north
    
        f = options['scalePrecision'][0]
        theta = np.linspace(0,2*np.pi,50)
        R=[[np.cos(value.ellipse_azi*np.pi/200),np.sin(value.ellipse_azi*np.pi/200)],
           [-np.sin(value.ellipse_azi*np.pi/200),np.cos(value.ellipse_azi*np.pi/200)]]
        
        y0 = f*value.ellipse_b*np.cos(theta)
        x0 = f*value.ellipse_a*np.sin(theta)
        
        vec_yx = np.vstack((y0,x0))
        rot_yx = np.matmul(R,vec_yx)
        
        y = rot_yx[0,:] + pt_y
        x = rot_yx[1,:] + pt_x
        plt.plot(y,x,color='b')

        ax1_y_1 = 0.8*f*value.ellipse_a*np.sin(value.ellipse_azi*np.pi/200) + pt_y
        ax1_x_1 = 0.8*f*value.ellipse_a*np.cos(value.ellipse_azi*np.pi/200) + pt_x
        ax1_y_2 = 1.2*f*value.ellipse_a*np.sin(value.ellipse_azi*np.pi/200) + pt_y
        ax1_x_2 = 1.2*f*value.ellipse_a*np.cos(value.ellipse_azi*np.pi/200) + pt_x
        ax2_y_1 = 0.8*f*value.ellipse_b*np.sin((100+value.ellipse_azi)*np.pi/200) + pt_y
        ax2_x_1 = 0.8*f*value.ellipse_b*np.cos((100+value.ellipse_azi)*np.pi/200) + pt_x
        ax2_y_2 = 1.2*f*value.ellipse_b*np.sin((100+value.ellipse_azi)*np.pi/200) + pt_y
        ax2_x_2 = 1.2*f*value.ellipse_b*np.cos((100+value.ellipse_azi)*np.pi/200) + pt_x
        plt.plot([ax1_y_1,ax1_y_2],[ax1_x_1,ax1_x_2],color='b')
        plt.plot([ax2_y_1,ax2_y_2],[ax2_x_1,ax2_x_2],color='b')
        
        plt.axis('equal')
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.grid(True)
        plt.xlabel(r'$E_{MN95}$ [m]',fontsize=14)
        plt.ylabel(r'$N_{MN95}$ [m]',fontsize=14)
        


def plotReliability(points,options):
    
    for key, value in points.items():
        pts_no = key
        pt_y = value.east
        pt_x = value.north
    
        f = options['scaleReliability'][0]
        R=[[np.cos(value.fiab_azi*np.pi/200),np.sin(value.fiab_azi*np.pi/200)],
           [-np.sin(value.fiab_azi*np.pi/200),np.cos(value.fiab_azi*np.pi/200)]]
        
        y0 = [f*value.fiab_NB,f*value.fiab_NB,-f*value.fiab_NB,-f*value.fiab_NB,f*value.fiab_NB]
        x0 = [f*value.fiab_NA,-f*value.fiab_NA,-f*value.fiab_NA,f*value.fiab_NA,f*value.fiab_NA]
        
        vec_yx = np.vstack((y0,x0))
        rot_yx = np.matmul(R,vec_yx)
        
        y = rot_yx[0,:] + pt_y
        x = rot_yx[1,:] + pt_x
        plt.plot(y,x,color='g')

#        ax1_y_1 = 0.8*f*value.fiab_NA*np.sin(value.fiab_azi*np.pi/200) + pt_y
#        ax1_x_1 = 0.8*f*value.fiab_NA*np.cos(value.fiab_azi*np.pi/200) + pt_x
#        ax1_y_2 = 1.2*f*value.fiab_NA*np.sin(value.fiab_azi*np.pi/200) + pt_y
#        ax1_x_2 = 1.2*f*value.fiab_NA*np.cos(value.fiab_azi*np.pi/200) + pt_x
#        ax2_y_1 = 0.8*f*value.fiab_NB*np.sin((100+value.fiab_azi)*np.pi/200) + pt_y
#        ax2_x_1 = 0.8*f*value.fiab_NB*np.cos((100+value.fiab_azi)*np.pi/200) + pt_x
#        ax2_y_2 = 1.2*f*value.fiab_NB*np.sin((100+value.fiab_azi)*np.pi/200) + pt_y
#        ax2_x_2 = 1.2*f*value.fiab_NB*np.cos((100+value.fiab_azi)*np.pi/200) + pt_x
#        plt.plot([ax1_y_1,ax1_y_2],[ax1_x_1,ax1_x_2],color='g')
#        plt.plot([ax2_y_1,ax2_y_2],[ax2_x_1,ax2_x_2],color='g')
        
        plt.axis('equal')
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.grid(True)
        plt.xlabel(r'$E_{MN95}$ [m]',fontsize=14)
        plt.ylabel(r'$N_{MN95}$ [m]',fontsize=14)
        
                
        
def plotDisplacements(points,options):
    
    for key, value in points.items():
        pts_no = key
        pt_y = value.east
        pt_x = value.north
    
        f = options['scaleDisplacement'][0]
                
        dy = value.displ_east
        dx = value.displ_north
        #plt.quiver(pt_y,pt_x,dy,dx,color='red', scale_units='xy',units='xy', angles='xy',scale=1/f)
        plt.plot([pt_y,pt_y+dy*f],[pt_x,pt_x+dx*f],color='red',linewidth=2)
        
        if np.sqrt(dy**2+dx**2)>0.000001:
            angle = np.arctan2(dy,dx)*180/np.pi
            plt.plot(pt_y+dy*f,pt_x+dx*f,marker=(3,0,-angle),color='red',markersize=10)
            
        plt.axis('equal')
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.grid(True)
        plt.xlabel(r'$E_{MN95}$ [m]',fontsize=14)
        plt.ylabel(r'$N_{MN95}$ [m]',fontsize=14)
            
        
######################
###### READ IPL ######
######################
        
# my_int equals int but returns 0 in case of an empty string
# or an string with only blanks
def my_int(my_string):
    my_string.replace(' ','')
    if len(my_string) == 0:
        return 0
    if len(my_string) == 1:
        if ord(my_string) == 32:
            return 0
    nb_spaces = 0
    for car in my_string:
        if ord(car) == 32:
            nb_spaces = nb_spaces + 1
    if nb_spaces == len(my_string):
        return 0
    return int(float(my_string))


#####################################
###### HIER ANPASSEN
#####################################

def readIpl(path):
    fname = path
    
    
    # fname root
    fname_root = fname.split(".")
    
    
    lines = [line.rstrip('\n') for line in open(fname)]
    ##with open(fname) as f:
    ##    lines = f.readlines()
    
    title1 = lines[0]
    title2 = lines[1]
    net_type = lines[2][0:8]
    
    if net_type != "LAGENETZ" and net_type != "RESEAU P":
        print("Program does only work with LAGENETZ")
        temp = input("Press ENTER to end...")
        sys.exit()
    
    i = 7
    
    point_name_per_index = {}
    point_index_per_number = {}
    point_coordinates = []
    
    points = {}
    
    ## PUNKTE
    nb_pt = 0
    while True:
        # end of the point section
        if lines[i].strip() == "MESSUNGEN":
            break
        
        # read point type
        point_fix = lines[i][0]
        point_name = lines[i][1:17]
        point_name = point_name.strip()
        point_numb = int(lines[i][19:27])
        point_east = float(lines[i][27:41])
        point_north = float(lines[i][41:55])
        
        i = i + 1
    
        if point_name == "PLOT":
            continue
        
        cur_point = Point(point_name)
        cur_point.planiFix = point_fix
        cur_point.ipl_id = point_numb
        cur_point.east = point_east
        cur_point.north = point_north
        points.update({cur_point.id:cur_point})
    
    i = i + 1
    observations = []
    ## MESSUNGEN
    while True:
        # end of the point section
        if lines[i].strip() == "VERSCHIEBUNGEN":
            break
        
        pt1 = my_int(lines[i][2:10])
        pt2 = my_int(lines[i][10:18])
        gnss = my_int(lines[i][33:34])
        dist = my_int(lines[i][39:40])
        hz = my_int(lines[i][46:48])
        v = my_int(lines[i][78:80])
        
        id1 = findIdFromIplID(points,pt1)
        id2 = findIdFromIplID(points,pt2)
        if dist>0:
            type_obs = 'DP'
        elif hz > 0:
            type_obs = 'RI'
                
        cur_obs = Observation(id1,id2,type_obs)
        observations.append(cur_obs)
        
        i = i+1
    
    i = i + 1
    ## VERSCHIEBUNGEN
    while True:
        # end of the point section
        if lines[i].strip() == "ELLIPSEN":
            break
        
        pt1 = my_int(lines[i][2:10])
        dx   = float(lines[i][10:20])/1000
        dy   = float(lines[i][20:30])/1000
        
        id1 = findIdFromIplID(points,pt1)
        points[id1].displ_east = dx
        points[id1].displ_north = dy
        
        i = i+1
    
    i = i + 1
    ## ELLIPSEN
    while True:
        # end of the point section
        if lines[i].strip() == "ZUVERLAESSIGKEIT":
            break
        
        pt1 = my_int(lines[i][2:10])
        a   = float(lines[i][10:20])/1000
        b   = float(lines[i][20:30])/1000
        azi   = float(lines[i][30:40])
        
        id1 = findIdFromIplID(points,pt1)
        points[id1].ellipse_a = a
        points[id1].ellipse_b = b
        points[id1].ellipse_azi = azi
        
        i = i+1
    
    i = i + 1
    ## ZUVERLAESSIGKEIT
    while True:
        # end of the point section
        if lines[i].strip() == "ENDE":
            break
        
        pt1 = my_int(lines[i][2:10])
        NA   = float(lines[i][10:20])/1000
        NB   = float(lines[i][20:30])/1000
        azi   = float(lines[i][30:40])
    
        id1 = findIdFromIplID(points,pt1)
        points[id1].fiab_NA = NA
        points[id1].fiab_NB = NB
        points[id1].fiab_azi = azi
            
        i = i+1        
        
    return points,observations