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
import matplotlib

"""BMIGraph class, this class takes a body.dat file and prepares a graph of the
points along with a linear regression line using matplotlib."""

class BMIGraph(object):

    def __init__(self, fileName):
        # The file name of data to read.
        self.fileName = fileName
        # A dictionary of the BMI data in the file. Sorted using Person # - [List of Data].
        self.bmiData = {}
        # A list of (x, y) coordinates in the form of tuples.
        # self.coordinates[0] is the list for the  easy calculations and self.coordinates[1] is the long BMI calculation
        self.coordinates = [[], []]
    
    def readFile(self):
        # Open the data file.
        dataFile = open(self.fileName, 'r')

        person = 0
        for data in dataFile.readlines():
            self.bmiData[person] = data.split()
            person += 1




    def calculateNormalBMI(self, personNumber):
        
        # Loop to find the data at personNumber.
        for person in self.bmiData.keys():


            if person == personNumber:
                # Fetch the data
                personData = self.bmiData[person]
                
                # Fetch the necessary variables needed to calculate BMI
                weight = int(float(personData[22]))
                # Weight must be converted to m for the formula
                height = int(float(personData[23])) / 100

                # Return the BMI calculation.
                
                return (weight / (height ** 2))


    def calculateFormulaBMI(self, personNumber): 
        
        # Loop to find the data at personNumber.
        for person in self.bmiData.keys():
            
              
            if person == personNumber:
                # Fetch the data.
                personData = self.bmiData[person]
            
                # Fetch the necessary variables needed to calculate BMI in floats, then cast to integers.
                chestDiameter = int(float(personData[4]))
                chestDepth = int(float(personData[3]))
                bitrochantericDiameter = int(float(personData[2]))
                wristGirth = int(float(personData[20]))
                ankleGirth = int(float(personData[19]))
                height = int(float(personData[23]))
                # Return the BMI calculation.

                return -110 + (1.34 * chestDiameter) + (1.54 * chestDepth) + (1.20 * bitrochantericDiameter) + (1.11 * wristGirth) + (1.15 * ankleGirth) + (0.177 * height) 


    def getPersonWeight(self, personNumber):
        # Find the person.
        for person in self.bmiData.keys():

            if person == personNumber:
                # Fetch the data
                personData = self.bmiData[person]
                # Return the 22nd variable in the list, which is weight.
                return personData[22]

    def getPersonAge(self, personNumber):
        # Find the person.
        for person in self.bmiData.keys():

            if person == personNumber:
                # Fetch the data.
                personData = self.bmiData[person]
                # Return the 21st variable in the list, which is age.
                return personData[21]
        

    def calculatePoints(self):
        
        # Loop through people in bmiData.

        for personNumber in self.bmiData.keys():
            # Add a tuple to the coordinates list containing the persons age (x) and normal BMI (y).
            self.coordinates[0].append((self.getPersonAge(personNumber), self.calculateNormalBMI(personNumber)))
            
            # Add a tuple to the coordinates list containing the persons weight (x) and formula BMI (y). 
            self.coordinates[1].append((self.getPersonWeight(personNumber), self.calculateFormulaBMI(personNumber)))
            
            
    """ Least of squares line methods """

       
    # Returns the sum of all the X coordinates (Age).
    def sumX(self):
       
        # Counter
        totalX = 0
        for coordinate in self.coordinates[1]:
            # Add the X coordinate from the tuple, which is at position [0].
            totalX += int(float(coordinate[0]))
            
        return totalX

    # Returns the sum of all the Y coordinates (BMI).
    def sumY(self):
        
        # Counter
        totalY = 0
        for coordinate in self.coordinates[1]:
            # Add the Y coordinate from the tuple, which is at position [1].
            totalY += int(float(coordinate[1]))


        return totalY


    # Returns the sum of the products of XY.
    def sumXY(self):
        
        # Counter.
        totalSumXY = 0
        for coordinate in self.coordinates[1]:
            # Multiply the two coordinates together, and add it to the total.
            totalSumXY += (int(float(coordinate[0])) * int(float(coordinate[1])))

        return totalSumXY


    def sumXSquared(self):

        # Counter.
        totalXSquared = 0
        for coordinate in self.coordinates[1]:
            # Square the x term, and add it to the total.
            totalXSquared += (int(float(coordinate[0])) ** 2)

        return totalXSquared

    def sumYSquared(self):

        # Counter
        totalYSquared = 0
        for coordinate in self.coordinates[1]:
            # Square the y term, and add it to the total.
            totalYSquared += (int(float(coordinate[1])) ** 2)

        return totalYSquared

    def getNumberOfPoints(self):
        # Return how many coordinates/points in the list.
        return len(self.coordinates[1])



    # Use the math functions to find the slope and y intercept. Returns a tuple of (m, b).
    def calculateLine(self):
        # Solve for the slope(m).
        slope = ((self.getNumberOfPoints() * self.sumXY()) - (self.sumX() * self.sumY())) / (self.getNumberOfPoints() * self.sumXSquared() - (self.sumX()) ** 2)# Solve for the y intercept(b).
        intercept = (self.sumY() - (slope * self.sumX())) / self.getNumberOfPoints()
        
        return (slope, intercept)



    def correlationCoefficient(self):
        return (self.getNumberOfPoints() - (self.sumX() * self.sumY()) / sqrt((self.getNumberOfPoints() * self.sumXSquared()) ** 2) * (self.getNumberOfPoints() * self.sumYSquared() - (self.sumY()) ** 2)) 


    # Find 2 points on the line so it can be graphed. lineData is the m and b values for the equation of the line.
    def computeLinePoints(self, lineData):
        m = lineData[0]
        b = lineData[1]

        # Best x value choices for the line assuming no negative data.
        xOne = 0
        # Find the highest x value in the formula dataset.
        xTwo = max([float(x[0]) for x in self.coordinates[1]])

        # Find the corrosponding y values to the x values using y=mx+b.
        yOne = (m * xOne) + b
        yTwo = (m * xTwo) + b

        # Return a tuple of two lists, the x points and the y points so it can be easily passed into pylab.plot().
        return ([xOne, xTwo], [yOne, yTwo])


    def debug(self):
        print(self.sumX())
        print(self.sumY())
        print(self.sumXY())
        print(self.sumXSquared())
        print(self.sumYSquared())
        print(self.getNumberOfPoints())


    def graph(self):
        # Loop through coordinates to construct two lists needed to pass into pylab.plot().
        normalXValues = []
        normalYValues = []

        formulaXValues = []
        formulaYValues = []

        # Gather the XY values of the normal BMI points.
        for coordinate in self.coordinates[0]:
            # Add the x coordinate to the x list.
            normalXValues.append(int(float(coordinate[0])))

            # Add the y coordinate to the y list.
            normalYValues.append(int(float(coordinate[1])))

        
        print(self.calculateLine())
      

        # Gather the XY values of the formula BMI points.
        for coordinate in self.coordinates[1]:
            # Add the x coordinate to the x list.
            formulaXValues.append(coordinate[0])
            # Add the y coordinate to the y list.
            formulaYValues.append(coordinate[1])

        
       # Calculate the equation of the line and compute two random points.

        linePoints = self.computeLinePoints(self.calculateLine())
        
        # Draw the normal BMI points.
        pylab.plot(normalXValues, normalYValues, 'ro', label='Normal BMI')
        # Draw the formula BMI points.
        pylab.plot(formulaXValues, formulaYValues, 'bo', label='Formula BMI')
        # Draw the line of best fit through the Formula BMI values.
        pylab.plot(linePoints[0], linePoints[1])


        # Add a legend.

        pylab.legend(loc='upper left', numpoints = 1)

        # Draw the graph.

        pylab.show()



testGraph = BMIGraph('body.dat')
testGraph.readFile()
testGraph.calculatePoints()

print (testGraph.debug())
testGraph.graph()
