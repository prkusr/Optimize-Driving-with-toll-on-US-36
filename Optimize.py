import matplotlib.pyplot as plt
from gurobipy import *
from webContent import *
import sys;
from TollCalculation import Toll; 

#                                Segment             ,    TIme , Delay
#scrapedData = [(u'Boulder (US-36) to Wadsworth Blvd',     10  ,   0), (u'Sheridan Blvd to I-25', 5, 0), (u'Wadsworth Blvd to Sheridan Blvd', 4, 4)]
#toll = [10, 23, 12];


#Get the real time data
scrapedData = scrapData();

print scrapedData

#Initialize Toll array with toll amount from above map.
t = Toll();
tollMap = t.getToll(scrapedData);
toll = [];
for i in range(0,len(scrapedData)):
    try:
        toll.append(tollMap[scrapedData[i][0]]);
    except:
        toll.append(0);

print toll;

x = [];
y = [];
segments = {};

initialDelay = sum(delay[2] for delay in scrapedData);

if initialDelay == 0:
    print 'Hurrah !! Take the highway as there is no delay on the highway.';
    sys.exit();

x.append(0);
y.append(initialDelay);

m = Model('RouteTimeCostOptimize');

for i in range(0,len(scrapedData)):
            segments[scrapedData[i][0]] = m.addVar(vtype=GRB.BINARY, name=scrapedData[i][0]);
            
m.setObjective(quicksum(scrapedData[i][2]*segments[scrapedData[i][0]] for i in range(0,len(scrapedData))), GRB.MINIMIZE);
            
min_cost = min(toll);
max_cost = sum(toll);

#sorted_toll_cost = sorted(toll);
tollCost = min_cost;

print "============================================================="  

while tollCost <= max_cost:      
    print 'Running ILP for tollCost: ', tollCost;
    try:                                                            
        
        # Add constraints
        constraint = m.addConstr(quicksum(toll[i]*(1-segments[scrapedData[i][0]]) for i in range(0,len(scrapedData))) <= tollCost , "cost");
        
        m.update();     
        
        m.params.OutputFlag = 0;
        
        m.optimize();
        #m.printAttr('X');
        
        if m.status == GRB.Status.OPTIMAL:
            temp_x = 0;
            temp_y = 0;
            i = 0;            
            for v in m.getVars():
                temp_x = temp_x + (1-v.x) * toll[i];
                temp_y = temp_y + v.x * scrapedData[i][2];
                print v.varName ,':', v.x
                i = i+1;
            x.append(temp_x);
            y.append(temp_y);    
            print 'Above solution for [Delay Time, Cost] : [%d, %0.2f]' % (m.objVal, temp_x);
            print "=============================================================\n"
        
        #print 'x: ',x,'\ny: ',y
        
        m.reset();
        m.remove(constraint);        
    
    except GurobiError:
        print('Error reported')
    
    #Incrementing maximum cost constraint by 2.
    tollCost +=0.5;


fig, ax1 = plt.subplots();

fig.canvas.set_window_title('Route Optimization');

print 'x: ',x,'\ny: ',y
plt.plot(x,y,'k+',x,y);

# Hide these grid behind plot objects
ax1.set_axisbelow(True)
ax1.set_title('Route Delay vs Cost Plot');
ax1.set_xlabel('Cost')
ax1.set_ylabel('Delay(secs)')

top = y[len(y)-1]*1.5;
bottom = 0.0
#ax1.set_ylim(bottom, top)
ax1.set_xlim(0, max_cost);
plt.show();