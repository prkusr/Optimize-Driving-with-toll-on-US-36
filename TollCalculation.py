import time;
import datetime;

class Toll(object):    
    
    #Eastbound   Boulder, McCaslin, Interlocken, Wadsworth, Church Ranch, Sheridan, Federal, I-25
    tollMatrixE =[[0.25,    0.25,       0.25,       0.25,       0.25,       0.25,      0.25,   0],  #12:00 AM 3:00 AM
                  [0.25,    0.25,       0.25,       0.25,       0.25,       0.25,      0.25,   0],  #3:00 AM 5:00 AM
                  [0.25,    0.25,       0.25,       0.25,       0.25,       0.25,      0.25,   0.7], #5:00 AM 6:00 AM
                  [0.25,    0.25,       0.25,       0.25,       0.25,       0.35,      0.25,   2.3], #6:00 AM 6:45 AM
                  [0.35,    0.35,       0.25,       0.25,       0.35,       0.5,       0.25,   4.2], #6:45 AM 7:15 AM
                  [0.65,    0.50,       0.35,       0.35,       0.50,       1.00,      0.75,   4.65],#7:15 AM 8:15 AM
                  [0.35,    0.35,       0.25,       0.25,       0.35,       0.50,      0.25,   4.2], #8:15 AM 8:45 AM
                  [0.25,    0.25,       0.25,       0.25,       0.25,       0.50,      0.25,   1.65],#8:45 AM 10:00 AM
                  [0.25,    0.25,       0.25,       0.25,       0.25,       0.35,      0.25,   0],  #10:00 AM 12:00 PM
                  [0.25,    0.25,       0.25,       0.25,       0.25,       0.35,      0.25,   0],  #12:00 PM 3:00 PM
                  [0.50,    0.35,       0.25,       0.25,       0.50,       0.50,      0.25,   0],  #3:00 PM 3:30 PM
                  [0.50,    0.50,       0.35,       0.35,       0.50,       0.65,      0.60,   0],  #3:30 PM 4:30 PM
                  [0.65,    0.50,       0.50,       0.35,       0.50,       0.65,      0.60,   0],  #4:30 PM 6:00 PM
                  [0.50,    0.35,       0.35,       0.25,       0.50,       0.50,      0.25,   0],  #6:00 PM 7:00 PM
                  [0.25,    0.25,       0.25,       0.25,       0.25,       0.35,      0.25,   0],  #7:00 PM 12:00 AM
                  [0.25,    0.25,       0.25,       0.25,       0.25,       0.35,      0.25,   0]]  #Weekends All Day (Sat-Sun)
    
    # Westbound   I-25,  Federal,    Sheridan, Church Ranch, Wadsworth, Interlocken, McCaslin Boulder
    tollMatrixW =[[0.70,    0.25,       0.50,       0.25,       0.25,       0.25,      0.25,   0.25], #12:00 AM 3:00 AM
                  [0.00,    0.25,       0.50,       0.25,       0.25,       0.25,      0.25,   0.25], #3:00 AM 5:00 AM
                  [0.00,    0.25,       0.50,       0.25,       0.25,       0.25,      0.25,   0.25], #5:00 AM 6:00 AM
                  [0.00,    0.25,       0.50,       0.25,       0.25,       0.25,      0.25,   0.35], #6:00 AM 6:45 AM
                  [0.00,    0.35,       0.50,       0.25,       0.25,       0.25,      0.35,   0.35], #6:45 AM 7:15 AM
                  [0.00,    0.50,       0.75,       0.50,       0.35,       0.35,      0.50,   0.65], #7:15 AM 8:15 AM
                  [0.00,    0.35,       0.50,       0.25,       0.25,       0.25,      0.35,   0.35], #8:15 AM 8:45 AM
                  [0.00,    0.25,       0.50,       0.25,       0.25,       0.25,      0.25,   0.25], #8:45 AM 10:00 AM
                  [0.00,    0.25,       0.50,       0.25,       0.25,       0.25,      0.25,   0.25], #10:00 AM 12:00 PM
                  [0.00,    0.25,       0.50,       0.25,       0.25,       0.25,      0.25,   0.25], #12:00 PM 3:00 PM
                  [0.70,    0.35,       0.50,       0.25,       0.25,       0.25,      0.25,   0.25], #3:00 PM 3:30 PM
                  [2.00,    0.50,       0.60,       0.25,       0.25,       0.25,      0.25,   0.35], #3:30 PM 4:30 PM
                  [2.65,    0.50,       0.60,       0.35,       0.25,       0.35,      0.35,   0.50], #4:30 PM 6:00 PM
                  [4.65,    0.35,       0.50,       0.25,       0.25,       0.25,      0.25,   0.25], #6:00 PM 7:00 PM
                  [2.00,    0.25,       0.50,       0.25,       0.25,       0.25,      0.25,   0.25], #7:00 PM 12:00 AM
                  [0.70,    0.25,       0.50,       0.25,       0.25,       0.25,      0.25,   0.25]] #Weekends All Day (Sat-Sun)
    
    def __init__(self):
        
        self.col = {};            
        self.col[u'Boulder (US-36)'] = [0,7];
        self.col[u'McCaslin Blvd'] = [1,6];
        self.col[u'Interlocken Blvd'] = [2,5];
        self.col[u'Wadsworth Blvd'] = [3,4];
        self.col[u'Church Ranch Blvd'] = [4,3];
        self.col[u'Sheridan Blvd'] = [5,2];
        self.col[u'Federal Blvd'] = [6,1];
        self.col[u'I-25'] = [7,0];
        
        self.rows = [];
        self.rows.append([0,3]);    #12:00 AM 3:00 AM
        self.rows.append([3,5]);    #3:00 AM 5:00 AM
        self.rows.append([5,6]);    #5:00 AM 6:00 AM
        self.rows.append([6,6.75]); #6:00 AM 6:45 AM
        self.rows.append([6.75,7.25]);  #6:45 AM 7:15 AM
        self.rows.append([7.25,8.25]);  #7:15 AM 8:15 AM
        self.rows.append([8.25,8.75]);  #8:15 AM 8:45 AM
        self.rows.append([8.75,10]);    #8:45 AM 10:00 AM
        self.rows.append([10,12]);      #10:00 AM 12:00 PM
        self.rows.append([12,15]);      #12:00 PM 3:00 PM
        self.rows.append([15,15.5]);    #3:00 PM 3:30 PM
        self.rows.append([15.5,16.5]);  #3:30 PM 4:30 PM
        self.rows.append([16.5,18]);    #4:30 PM 6:00 PM
        self.rows.append([18,19]);      #6:00 PM 7:00 PM
        self.rows.append([19,23.99]);   #7:00 PM 12:00 AM
        self.rows.append([0,23.99]);    #Weekends All Day (Sat-Sun)
        
        self.row_TimeItr = None;
        
        self.currLocalTime = datetime.datetime(2016, 12, 12, 4, 55, 39, 442000);#datetime.datetime.now();        
        
        self.day = self.currLocalTime.strftime('%a');
        
        self.tollVal = [];
        self.segmentIndex = 0;
            
    
    def computeSegmentToll(self, src_index, dest_index, travelTime, direction):
                        
        self.tollVal.append(0);  
        currTime = round(self.currLocalTime.hour + self.currLocalTime.minute/60.0, 2);
                               
        if self.row_TimeItr is None:
            self.row_TimeItr = 0;
            if self.day in ['Sun', 'Sat']:
                self.row_TimeItr  = 15 #Point to the last row in TollMatrix as it corresponds to weekends toll rates.
            else:
                for r in self.rows:
                    if r[0] <= currTime and currTime < r[1]:
                        break;
                    self.row_TimeItr  +=1;
        else:
            if self.day not in ['Sun', 'Sat'] and self.row_TimeItr  == 15:
                for r in self.rows:
                    if r[0] <= currTime and currTime < r[1]:
                        break;
                    self.row_TimeItr  +=1;
            elif self.day not in ['Sun', 'Sat'] and currTime >= self.rows[self.row_TimeItr][1]:
                self.row_TimeItr = (self.row_TimeItr + 1)%14;
            elif self.day in ['Sun', 'Sat']:
                self.row_TimeItr  = 15 #Point to the last row in TollMatrix as it corresponds to weekends toll rates.
        
        print 'currLocalTime: [',self.currLocalTime, '], day: [',self.day,'], row_TimeItr: [',self.row_TimeItr,']';
        
        tollMat = [[]];
        if ~direction: #Eastbound
            tollMat = self.tollMatrixE;
        else:
            tollMat = self.tollMatrixW; #Westbound
            
        tollVal = 0;
        for i in range(src_index,dest_index):
            tollVal += tollMat[self.row_TimeItr][i];
        
        self.currLocalTime = self.currLocalTime + datetime.timedelta(minutes=travelTime);   
        self.day = self.currLocalTime.strftime('%a');    
        return tollVal                
        
    def getToll(self, data):
        
        try: 
            direction = 0;  # 0=>Eastbound, 1=>Westbound
            segments = [];
            shouldSortReverse = False;
            orderedSegmentIndex = [];
            tollSegmentMap = {};
            for i in range(0,len(data)):
                splitSeg = data[i][0].split(' to ');
                splitSeg = [splitSeg[0].strip(' |.'), splitSeg[1].strip(' |.')];
                orderedSegmentIndex.append((self.col[splitSeg[0]][0], i));
                segments.append(splitSeg);
            
            print 'Splitted segments: ',segments
            
            if self.col[segments[0][0]][0] > self.col[segments[0][1]][0]:
                shouldSortReverse = True;
                direction = 1;
            
            orderedSegmentIndex = sorted(orderedSegmentIndex, key=lambda orderedSegmentIndex:orderedSegmentIndex[0], reverse=shouldSortReverse);
            
            print 'Ordered segments: ',orderedSegmentIndex
                        
            for seg_ind in orderedSegmentIndex:
                segmentStart = segments[seg_ind[1]][0];
                segmentEnd = segments[seg_ind[1]][1];
            
                src_index = self.col[segmentStart][direction];
                dest_index = self.col[segmentEnd][direction];     
                
                print 'Computing toll: [%s] to [%s]' % (segmentStart, segmentEnd);
                
                toll = self.computeSegmentToll(src_index, dest_index, data[seg_ind[1]][1], direction);
                tollSegmentMap[data[seg_ind[1]][0]] = toll;
                                
                
            return tollSegmentMap;    
        
        except KeyError as err:
            print 'getToll:: Error - Source/Destination not found in toll database: ',err
            return;