#!/usr/bin/python
#
#-------------------------------------------------------------------------------
# Name:    Adventure Game
#
# Author:  BMI
#
# Created: September 09, 2014
#-------------------------------------------------------------------------------

# Imports

"""BMIGraph class, this class takes a body.dat file and prepares a graph of the
points along with a linear regression line using matplotlib."""

class BMIGraph(object):

    def __init__(self, fileName):
        # The file name of data to read.
        self.fileName = fileName
        # A dictionary of the BMI data in the file. Sorted using Person # - [List of Data].
        self.bmiData = {}
        # A list of (x, y) coordinates in the form of tuples.
        self.coordinates = []
    
    def readFile(self):
        # Open the data file.
        dataFile = open(self.fileName, 'r')

        person = 0
        for data in dataFile.readlines():
            self.bmiData[person] = data.split()
            person += 1

        print(self.bmiData[506][21])

    def calculatePersonBMI(self, personNumber): 
        
        # Loop to find the data at personNumber.
        for person in self.bmiData.keys():
            
              
            if person == personNumber:
                # Fetch the data.
                personData = self.bmiData[person]
            
                # Fetch the necessary variables needed to calculate BMI round the float, then cast to integers.
                chestDiameter = int(round(float(personData[4])))
                chestDepth = int(round(float(personData[3])))
                bitrochantericDiameter = int(round(float(personData[2])))
                wristGirth = int(round(float(personData[20])))
                ankleGirth = int(round(float(personData[19])))
                height = int(round(float(personData[23])))
                # Return the BMI calculation.

                return (-110 + (1.34 * chestDiameter) + (1.54 * chestDepth) + (1.20 * bitrochantericDiameter) + (1.11 * wristGirth) + (1.15 * ankleGirth) + (0.177 * height)) 


    def getPersonAge(self, personNumber):
        # Find the persons height
        for person in self.bmiData.keys():

            if person == personNumber:
                # Fetch the data.
                personData = self.bmiData[person]
                # Return the 21st variable in the list, which is height.
                return personData[21]
        

    def calculatePoints(self):
        
        # Loop through people in bmiData.

        for personNumber in self.bmiData.keys():
            # Add a tuple to the coordinates list containing the persons age (x) and BMI (y).
            self.coordinates.append((self.getPersonAge(personNumber), self.calculatePersonBMI(personNumber)))
            
            
    """ Least of squares line methods """

       
    # Returns the sum of all the X coordinates (Age).
    def sumX(self):
       
        # Counter
        totalX = 0
        for coordinate in self.coordinates:
            # Add the X coordinate from the tuple, which is at position [0].
            totalX += int(float(coordinate[0]))
            
        return totalX

    # Returns the sum of all the Y coordinates (BMI).
    def sumY(self):
        
        # Counter
        totalY = 0
        for coordinate in self.coordinates:
            # Add the Y coordinate from the tuple, which is at position [1].
            totalY += int(float(coordinate[1]))


        return totalY


    # Returns the sum of the products of XY
    def sumXY(self):
        pass

testGraph = BMIGraph('body.dat')
testGraph.readFile()
testGraph.calculatePoints()
print(testGraph.sumX())
print(testGraph.sumY())
