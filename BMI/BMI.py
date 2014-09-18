#!/usr/bin/python
#
#-------------------------------------------------------------------------------
# Name:    BMI
#
# Author:  Steve Pavlin
#
# Created: September 09, 2014
#-------------------------------------------------------------------------------

# Imports

import pylab
from math import sqrt

"""BMIGraph class, this class takes a body.dat file and prepares a graph of the
points along with a linear regression line. Calculates normal and "formula" BMI for the given data."""

class BMIGraph(object):

    def __init__(self, fileName):
        # The file name of the BMI data to read.
        self.fileName = fileName
      
        # A dictionary of the BMI data in the file. Sorted using Person # - [List of Data].
        self.bmiData = {}
        
        
        # A list of (x, y) coordinates in the form of tuples.
        # self.coordinates[0] is the list for the normal BMI calculations and self.coordinates[1] is the Formula BMI calculations.
        self.coordinates = [[], []]
    
        
        # A list of two dictionaries of the least of squares operations needed.
        # self.losCalculations[0] is the dictionary for the normal BMI calculations and self.losCalculations[1] is for the Formula BMI calculations. A dictionary is used for the ease of finding values using a string.
        self.losCalculations = [{}, {}]


    def readFile(self):
        # Open the data file.
        dataFile = open(self.fileName, 'r')

        person = 0
        for data in dataFile.readlines():
            # Add a persons data to the dictionary.
            self.bmiData[person] = data.split()
            person += 1

        
        # After reading the file into self.bmiData, calculate the (x, y) points.
        self.calculatePoints()


    # Returns a persons normal BMI.
    def calculateNormalBMI(self, personNumber):
        
        # Loop to find the data at personNumber.
        for person in self.bmiData.keys():


            if person == personNumber:
                # Fetch the data
                personData = self.bmiData[person]
                
                # Fetch the necessary variables needed to calculate BMI.
                weight = float(personData[22])
                # Weight must be converted to metres according to the formula.
                height = float(personData[23]) / 100

                # Return the BMI calculation.
                return (weight / (height ** 2))


    # Returns a persons formula BMI.
    def calculateFormulaBMI(self, personNumber): 
        
        # Loop to find the data at personNumber.
        for person in self.bmiData.keys():
            
              
            if person == personNumber:
                # Fetch the data.
                personData = self.bmiData[person]
            
                # Fetch the necessary variables needed to calculate formula BMI.
                chestDiameter = float(personData[4])
                chestDepth = float(personData[3])
                bitrochantericDiameter = float(personData[2])
                wristGirth = float(personData[20])
                ankleGirth = float(personData[19])
                height = float(personData[23])
                
                # Return the BMI calculation.
                return -110 + (1.34 * chestDiameter) + (1.54 * chestDepth) + (1.20 * bitrochantericDiameter) + (1.11 * wristGirth) + (1.15 * ankleGirth) + (0.177 * height) 


    # Returns a persons weight.
    def getPersonWeight(self, personNumber):
        # Find the person.
        for person in self.bmiData.keys():

            if person == personNumber:
                # Fetch the data
                personData = self.bmiData[person]
                # Return the 22nd variable in the list, which is weight.
                return personData[22]


    # Returns a persons age.
    def getPersonAge(self, personNumber):
        # Find the person.
        for person in self.bmiData.keys():

            if person == personNumber:
                # Fetch the data.
                personData = self.bmiData[person]
                # Return the 21st variable in the list, which is age.
                return personData[21]
        

    # Calculates the (x, y) values for the persons normal and formula BMI and adds it to the respective list.
    def calculatePoints(self):
        
        # Loop through people in bmiData.
        for personNumber in self.bmiData.keys():
            # Add a tuple to the normal BMI coordinates list containing a persons age (x) and normal BMI (y).
            self.coordinates[0].append((self.getPersonAge(personNumber), self.calculateNormalBMI(personNumber)))
            
            # Add a tuple to the formula BMI coordinates list containing a persons weight (x) and formula BMI (y). 
            self.coordinates[1].append((self.getPersonWeight(personNumber), self.calculateFormulaBMI(personNumber)))
        # Perform least of squares calculations using the points.
        self.performLosCalculations()

    """ Linear regression line methods """


    # Performs all the calculations needed for the linear regression line for normal and formula BMI.
    def performLosCalculations(self):
        
        # Perform the calculations for normal and "formula" BMI values, and add it to self.losCalculations.
        for bmiType in range(len(self.losCalculations)):

            # Save the current bmiType's data.
            bmiTypeData = self.losCalculations[bmiType]
            
            # Add each least of squares calculations to the dictionary for later use.
            bmiTypeData['SUM_X'] =  self.sumX(bmiType)
            bmiTypeData['SUM_Y'] = self.sumY(bmiType)
            bmiTypeData['SUM_XY'] =  self.sumXY(bmiType)
            bmiTypeData['SUM_XSQUARED'] = self.sumXSquared(bmiType)
            bmiTypeData['SUM_YSQUARED'] = self.sumYSquared(bmiType)
            bmiTypeData['NUMBER_OF_POINTS'] = self.getNumberOfPoints()


    # Returns the sum of all the x coordinates for the current dataset.
    def sumX(self, bmiType):
       
        # Counter
        totalX = 0
        for coordinate in self.coordinates[bmiType]:
            # Add the X coordinate from the tuple, which is at position [0].
            totalX += float(coordinate[0])
            
        return totalX

    # Returns the sum of all the y coordinates for the current dataset.
    def sumY(self, bmiType):
        
        # Counter
        totalY = 0
        for coordinate in self.coordinates[bmiType]:
            # Add the Y coordinate from the tuple, which is at position [1].
            totalY += float(coordinate[1])


        return totalY


    # Returns the sum of the products of XY for the current dataset.
    def sumXY(self, bmiType):
        
        # Counter.
        totalSumXY = 0
        for coordinate in self.coordinates[bmiType]:
            # Multiply the two coordinates together, and add it to the total.
            totalSumXY += float(coordinate[0]) * float(coordinate[1])

        return totalSumXY


    # Returns the sum of each x value squared.
    def sumXSquared(self, bmiType):

        # Counter.
        totalXSquared = 0
        for coordinate in self.coordinates[bmiType]:
            # Square the x term, and add it to the total.
            totalXSquared += float(coordinate[0]) ** 2

        return totalXSquared

    # Returns the sum of each y value squared.
    def sumYSquared(self, bmiType):

        # Counter
        totalYSquared = 0
        for coordinate in self.coordinates[bmiType]:
            # Square the y term, and add it to the total.
            totalYSquared += float(coordinate[1]) ** 2

        return totalYSquared


    # Return the amount of coordinates. Same for both sets of data.
    def getNumberOfPoints(self):
        return len(self.coordinates[0])



    # Use the math functions to find the slope and y intercept. Returns a tuple of (m, b).
    def calculateLine(self, points, sumXY, sumX, sumY, sumXSquared):
        # Solve for the slope(m).
        slope = ((points * sumXY) - (sumX * sumY)) / (points * sumXSquared - (sumX) ** 2)
        # Solve for the y intercept(b).
        intercept = (sumY - (slope * sumX)) / points
       
        # Return them both in a tuple.
        return (slope, intercept)


    # Returns the correlation coefficient using a formula.
    def calculateCorrelationCoefficient(self, points, sumXY, sumX, sumY, sumXSquared, sumYSquared):
        return (points * sumXY - (sumX * sumY)) / (sqrt((points * sumXSquared - (sumX ** 2)) * (points * sumYSquared - (sumY ** 2))))   
    
    
    
    # Find 2 points on the line so it can be graphed. lineData is the m and b values for the equation of the line.
    # Uses 0 as x1 and the max points on the graphs x value as x2. 
    def computeLinePoints(self, lineData):
        m = lineData[0]
        b = lineData[1]

        # Best x value choices for the line assuming no negative data.
        xOne = 0
        # Find the highest x value in the dataset. It will always lie in the formula dataset so use position 1.
        xTwo = max([float(x[0]) for x in self.coordinates[1]])

        # Find the corresponding y values to the x values using y=mx+b.
        yOne = (m * xOne) + b
        yTwo = (m * xTwo) + b

        # Return a tuple of two lists, the x points and the y points so it can be easily passed into pylab.plot().
        return ([xOne, xTwo], [yOne, yTwo])


    def graph(self):
        # Begin the data retrieval process
        self.readFile()


        # Graph the coordinates and line for normal BMI and Formula BMI.
        # Normal BMI would be at [0] while Formula BMI would be at [1].
        for bmiType in range(len(self.losCalculations)):
            
            # Save the dictionary of least of squares math calculations for the current dataset.
            bmiTypeData = self.losCalculations[bmiType]
            
            # Calculate m and b using the least of squares math calculations in the dictionary.
            lineEquation = self.calculateLine(bmiTypeData['NUMBER_OF_POINTS'], bmiTypeData['SUM_XY'], bmiTypeData['SUM_X'], bmiTypeData['SUM_Y'], bmiTypeData['SUM_XSQUARED'])

            
            # Compute the minimum and maximum points and draw the line.
            linePoints = self.computeLinePoints(lineEquation)

            # Generate a line name, line color, point name, and point color based on the current data set.

            # For normal BMI.
            if (bmiType == 0):
                lineName = 'Normal BMI line'
                lineColor = 'r'
                
                pointName = 'Normal BMI'
                pointColor = 'ro'
                

            # For Formula BMI.
            else:
                lineName = 'Formula BMI line'
                lineColor = 'b'  

                pointName = 'Formula BMI'
                pointColor = 'bo'          


            # Plot the current data's points. The long expression creates a list of the x or y values in the current data set.
            pylab.plot([float(x[0]) for x in self.coordinates[bmiType]], [float(x[1]) for x in self.coordinates[bmiType]], pointColor, label=pointName)

            # Plot the current data sets line.
            pylab.plot(linePoints[0], linePoints[1], lineColor)
            
            
            # Calculate and print the correlation coefficient for the current data.
            print('The correlation coefficient for the %s is %s' % (lineName, self.calculateCorrelationCoefficient(bmiTypeData['NUMBER_OF_POINTS'], bmiTypeData['SUM_XY'], bmiTypeData['SUM_X'], bmiTypeData['SUM_Y'], bmiTypeData['SUM_XSQUARED'], bmiTypeData['SUM_YSQUARED'])))



        # Add a legend.
        pylab.legend(loc='upper left', numpoints = 1)

        # Draw the graph.
        pylab.show()









# Create a BMIGraph object. 
myBMIGraph = BMIGraph('body.dat')

# Call graph() to graph the data.
myBMIGraph.graph()
