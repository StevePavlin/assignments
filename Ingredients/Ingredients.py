#!/usr/bin/python
#
#-------------------------------------------------------------------------------
# Name:    Ingredients
#
# Author:  Steve Pavlin
#
# Created: September 04, 2014
#-------------------------------------------------------------------------------

""" Ingredient class. This class allows for ingredient objects to be created
    with a name and the amount of calories it contains per 100g. """

class Ingredient(object):

    def __init__(self, name, calorieCount):
        self.name = name
        self.calorieCount = calorieCount


""" IngredientList class. This class is contains a database in the form of a list
    that stores Ingredient objects. """

class IngredientList(object):

    def __init__(self):
        # Initialize a list to store Ingredient objects.
        self.database = []

    def add(self, ingredient):
        # Add the specified object to the list.
        self.database.append(ingredient)

    def find(self, ingredientName):
        for ingredient in self.database:
            # Check each objects name instance variables against the specified ingredients name to find.
            if ingredient.name == ingredientName:
                # If found, return the objects calories per 100g.
                return ingredient.calorieCount
        
        # Returned only if the specified object with the name specified does not exist.
        return -1

    def readList(self, fileName):
        # Open a file based on the fileName input.
        dataFile = open(fileName, 'r')


        for line in dataFile.readlines():
            # Perform a split to easily access the data in list format.
            ingredientData = line.split()

            # ingredientData[0] will always be the ingredients name.
            # ingredientData[1] will always be the ingredients calorie count per 100g.

            # Create a new Ingredient object with the data.
            ingredient = Ingredient(ingredientData[0], int(ingredientData[1]))
            # Add it to the database
            self.add(ingredient)
            
        dataFile.close()

    
    def count(self, fileName):
        # Open a file based on the fileName input.
        dataFile = open(fileName, 'r')

        # Initialize a counter to count the total calories for this recipe.
        totalCalorieCount = 0

        for line in dataFile.readlines():
            # Perform a split to easily access the data in list format.
            ingredientData = line.split()

            # ingredientData[0] will always be the ingredients name.
            # ingredientData[1] will always be the ingredients gram count.

            """ Divide the gram count by 100 to find a ratio to its calorie count per 100.
            Multiply that ratio by the ingredients calorie count by calling find() """
            calories = (int(ingredientData[1]) / 100) * self.find(ingredientData[0])
            totalCalorieCount += calories

        dataFile.close()
        return totalCalorieCount

# Create a list object.
testList = IngredientList()

# Read in each value.
testList.readList('table.dat')

# Test for method count should return 1634.1.
print(testList.count('pasta.txt'))

# Test for method find should return 191.
print(testList.find('spaghetti'))

# Test for method add should return 5.
testIngredient = Ingredient('test', 5)
testList.add(testIngredient)
print(testList.find('test'))
