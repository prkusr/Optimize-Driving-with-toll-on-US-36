============================********************************************========================================
								Optimize Driving with toll on US 36
============================********************************************========================================
								BY: Vibhor Mishra and Prasanna Kumar
################################################################################################################


Project Description
______________________

Suppose a user has to drive US 36 every single day either from Denver to Boulder or in the reverse direction. This utility provides the information of how much user can spend for reaching at a particular time.

Eg., a user might have to spend at most $1.50 to reach within 25 minutes, $1 to reach within 35 minutes, $0.50 to reach within 45 minutes. This output is presented in the form of graph plotted with Delay vs Cost of the journey.

The real time traffic conditions are scraped from http://cotrip.org/ about the delay on different segments(toll exits) of highway and using the toll information, the code optimizes and suggests users the segments they should take the toll lane and which segments they should drive on a regular lane.

_______________________________________________________________________________________________________________________________________________________________________________________________


To run the code, one should have following python modules installed:
1) matplotlib
2) gurobi
3) Python library like json,urllib2

To fetch the realtime traffic info, ptyhon libraries are used through which we call the url with specific routId desginated for each source and destiantion pair, get the json response, parse it, extract required info and use it for ILP formaulation.

Here is the flow of the program:

1) user is asked to pick the source, destination and via-highway.
2) the realtime traffic information is fetched from : http://www.cotrip.org/highways/ for the given source,destination and highway. The informaiton feteched is basically the delay time on different segments of the highway.
3) Toll cost is statically stored as it's not required to be fetched each time the progrma is run.
4) using this real time info and toll cost of the express toll lane specific for each segment, we formaulate ILP and solve it using gurobi optimizer.
5) we initialize the cost constraint with lowest toll cost of a segment and increment it by 2 in each iteration to get the plot of delay time vs cost.
6) show the plot to user thourgh which he can make a better decision about tradeoff between cost and delay he want to incur on his travel.


ILP formulation:
-----------------

Example : For "A" source to "D" destination, following is the real time information we fetch from cotrip.org:
	Segment		   NormalTravelTime 	Delay		Toll
==========================================================
1) 'B to C' (s0) |		10mins		|	4mins	|	$4 
2) 'C to D'	(s1) |		15min		|	2mins	|	$6
3) 'E to F'	(s2) |		8mins		|	5mins	|	$8


Initialize tollCost = min(4,6,8) = 4
Maximum_Cost = sum(4,6,8) = 18

while tollCost <= Maximum_Cost

	Objective: Minimize s0*4 + s1*2 + s2*5
	subject to:
			4*(1-s0) + 6*(1-s1) + 8*(1-s2) <= tollCost
			s0, s1, s2 => Binary Integers
			
	save result in output array.
	Based on result compute delay and cost.
	cost_x -> append(cost)
	delay_y -> append(delay)
	
	Increment tollcost by 2: tollCost = tollCost +2
	
	
Plot cost_x and delay_y.


-------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------



