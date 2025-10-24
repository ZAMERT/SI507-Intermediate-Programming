import numpy as np
import json
import os
import random
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.path import Path
random.seed(17)
import requests
from collections import Counter
import re

class DetroitDistrict:
    """
    A class representing a district in Detroit with attributes related to historical redlining.
    coordinates,holcGrade,holcCol or,id,description should be load from the redLine data file
    if cache is not available

    Parameters 
    ------------------------------
    coordinates : list of lists, 2D List, not list of list of list
        Coordinates defining the district boundaries from the json file
        Note that some districts are non-contiguous, which may
        effect the structure of this attribute

    holcGrade : str
        The HOLC grade of the district.

    id : str
        The identifier for the district, the HOLC ID.

    description : str, optional
        Qualitative description of the district.

    holcColor : str, optional
        A string represent the color of the holcGrade of the district

    randomLat : float, optional
        A random latitude within the district (default is None).

    randomLong : float, optional
        A random longitude within the district (default is None).

    medIncome : int, optional
        Median household income for the district, to be filled later (default is None).
        
    censusTract : str, optional
        Census tract code for the district (default is None).


    Attributes
    ------------------------------
    self.coordinates 
    self.holcGrade 
    holcColor : str
        The color representation of the HOLC grade.
        • Districts with holc grade A should be assigned the color 'darkgreen'
        • Districts with holc grade B should be assigned the color 'cornflowerblue'
        • Districts with holc grade C should be assigned the color 'gold'
        • Districts with holc grade D should be assigned the color 'maroon'
        If there is no input for holcColor, it should be generated based on the holcGrade and the rule above.

    self.id 
    self.description 
    self.randomLat 
    self.randomLong 
    self.medIncome 
    self.censusTract 


    """
    Grade_Color_Map = {
        "A": "darkgreen", 
        "B": "cornflowerblue", 
        "C": "gold",
        "D": "maroon"
    }
    
    def __init__(self, coordinates, holcGrade, id, description, holcColor = None, randomLat=None, randomLong=None, medIncome=None, censusTract=None):
        self.coordinates = coordinates
        self.holcGrade = holcGrade
        self.id = id
        self.description = description
        self.holcColor = holcColor or self.Grade_Color_Map.get(holcGrade)
        self.randomLat = randomLat
        self.randomLong = randomLong
        self.medIncome = medIncome
        self.censusTract = censusTract



class RedLines:
    """
    A class to manage and analyze redlining district data.

    Attributes
    ----------
    districts : list of DetroitDistrict
        A list to store instances of DetroitDistrict.

    """

    def __init__(self,cacheFile = None):
        """
        Initializes the RedLines class without any districts.
        assign districts attribute to an empty list
        """
        self.districts = []
        if cacheFile:
            self.loadCache(cacheFile)
        

    def createDistricts(self, fileName):
        """
        Creates DetroitDistrict instances from redlining data in a specified file.
        Based on the understanding in step 1, load the file,parse the json object, 
        and create 238 districts instance.
        Finally, store districts instance in a list, 
        and assign the list to be districts attribute of RedLines.

        Parameters
        ----------
        fileName : str
            The name of the file containing redlining data in JSON format.

        Hint
        ----------
        The data for description attribute could be from  
        one of the dict key with only number.

        """
        f = open(fileName)
        data = json.load(f)
        f.close()
        features = data.get("features") # Get the item from the dict with the key "features"
        districts = [] # Define an empty list for storing the districts instance.
        for feature in features:
            geom = feature.get("geometry")
            prop = feature.get("properties")
            coordinates = []
            coords = geom.get("coordinates")
            for point in coords[0][0]: # Three layers.
                coordinates.append(point) # Extract coordinates.
            
            holcGrade = prop.get("holc_grade")
            id = prop.get("holc_id")
            desc = prop.get("area_description_data")
            description  = desc.get("8")
            
            d = DetroitDistrict(coordinates, holcGrade, id, description) # Initialize the district instance.
            districts.append(d)
        
        self.districts = districts

    def plotDistricts(self):
        """
        Plots the districts using matplotlib, displaying each district's location and color.
        Name it redlines_graph.png and save it to the current directory. 
        """
        fig, ax = plt.subplots()
        for d in self.districts:
            ax.add_patch(matplotlib.patches.Polygon(d.coordinates, 
                                                    closed = True, 
                                                    facecolor = d.holcColor, 
                                                    edgecolor = "black"))
            ax.autoscale()
        plt.rcParams["figure.figsize"] = (15, 15)
        plt.show()
        plt.savefig("redlines_graph.png")
        plt.close()

    def generateRandPoint(self):
        """
        Generates a random point within the boundaries of each district.

        This method creates a mesh grid of points covering the geographical area of interest
        and then selects a random point within the boundary of each district.

        Attributes
        ----------
        self.districts : list of DetroitDistrict
            The list of district instances in the RedLines class.

        Note
        ----
        The random point is assigned as the randomLat and randomLong  for each district.
        This method assumes the 'self.districts' attribute has been populated with DetroitDistrict instances.

        """
        xgrid = np.arange(-83.5, -82.8, .004)
        ygrid = np.arange(42.1, 42.6, .004)
        xmesh, ymesh = np.meshgrid(xgrid, ygrid)
        
        points = np.vstack((xmesh.flatten(), ymesh.flatten())).T
        
        for d in self.districts:
            vertices = np.asarray(d.coordinates, dtype = float) # Convert to numpy array
            p = Path(vertices)
            grid = p.contains_points(points)
            point = points[random.choice((np.where(grid)[0]).tolist())]
            print(d, " : ", point)
            d.randomLong = float(point[0])
            d.randomLat = float(point[1])

        
    def fetchCensus(self):

        """
        Fetches the census tract for each district in the list of districts using the FCC API.

        This method iterates over the all districts in `self.districts`, retrieves the census tract 
        for each district based on its random latitude and longitude, and updates the district's 
        `censusTract` attribute.

        Note
        ----
        The method fetches data from "https://geo.fcc.gov/api/census/area" and assumes that 
        `randomLat` and `randomLong` attributes of each district are already set.

        The function `fetch` is an internal helper function that performs the actual API request.

        In the api call, check if the response.status_code is 200.
        If not, it might indicate the api call made is not correct, check your api call parameters.

        If you get status_code 200 and other code alternativly, it could indicate the fcc webiste is not 
        stable. Using a while loop to make anther api request in fetch function, until you get the correct result. 

        Important
        -----------
        The order of the API call parameter has to follow the following. 
        'lat': xxx,'lon': xxx,'censusYear': xxx,'format': 'json' Or
        'lat': xxx,'lon': xxx,'censusYear': xxx

        """
        def fetch(lat, lon, year = 2010): # Use 2010 since later we will use data in year 2018. 
            url = "https://geo.fcc.gov/api/census/area"
            parameters = {
                'lat': lat,
                'lon': lon,
                'censusYear': year,
                'format': 'json'
            }
            while True: # Use a while loop to make sure that we get the API response with status_code 200.
                try:
                    response = requests.get(url, params = parameters)
                    if response.status_code == 200:
                        data = response.json()
                        FIPS = data["results"][0]["block_fips"]
                        return FIPS[2:11] # Extract the census tract from the FIPS code.
                except Exception:
                    continue
        
        for d in self.districts:
            census_Tract = fetch(d.randomLat, d.randomLong)
            d.censusTract = census_Tract 

    def fetchIncome(self):

        """
        Retrieves the median household income for each district based on the census tract.

        This method requests income data from the ACS 5-Year Data via the U.S. Census Bureau's API 
        for the year 2018. It then maps these incomes to the corresponding census tracts and updates 
        the median income attribute of each district in `self.districts`.

        Note
        ----
        The method assumes that the `censusTract` attribute for each district is already set. It updates 
        the `medIncome` attribute of each district based on the fetched income data. If the income data 
        is not available or is negative, the median income is set to 0.

        """
        url = "https://api.census.gov/data/2018/acs/acs5"
        parameters = {
            "get": "B19013_001E",
            "for": "tract:*",
            "in": "state:26"
        }
        
        try:
            response = requests.get(url, params = parameters)
            if response.status_code == 200:
                data = response.json()
        except Exception as e:
            return
        
        income_dict = {}
        df = data[1:] # The first row is the header.
        for row in df:
            income = float(row[0]) # Change the format from string to float.
            if income < 0:
                income = 0
            county = row[2]
            tract = row[3]
            key = county + tract
            income_dict[key] = income
        
        for d in self.districts:
            d.medIncome = income_dict.get(d.censusTract)
        
        
        
    def cacheData(self, fileName):
        """
        Saves the current state of district data to a file in JSON format.
        Using the __dict__ magic method on each district instance, and save the 
        result of it to a list.
        After creating the list, dump it to a json file with the inputted name.
        You should name the cache file as redlines_cache.json

        Parameters
        ----------
        filename : str
            The name of the file where the district data will be saved.
        """
        district_dict_list = []
        for d in self.districts:
            district_dict_list.append(d.__dict__)
        
        f = open(fileName, mode = "w")
        json.dump(district_dict_list, f, indent = 4) # Indent 4 for better readability.
        f.close()
        

    def loadCache(self, fileName):
        """
        Loads district data from a cache JSON file if it exists.

        Parameters
        ----------
        fileName : str
            The name of the file from which to load the district data.
            You should name the cache file as redlines_cache.json

        Returns
        -------
        bool
            True if the data was successfully loaded, False otherwise.
        """
        try:
            f = open(fileName) # The mode is by default "r".
            data = json.load(f)
            f.close()
            self.districts = []
            for d in data:
                district = DetroitDistrict(
                    d.get("coordinates"),
                    d.get("holcGrade"),
                    d.get("id"),
                    d.get("description"),
                    d.get("randomLat"),
                    d.get("randomLong"),
                    d.get("medIncome"), 
                    d.get("censusTract")
                )
                self.districts.append(district)
            return True
        except Exception:
            return False
                

    def calcIncomeStats(self):
        """
        Use np.median and np.mean to
        Calculates the mean and median of median household incomes for each district grade (A, B, C, D).

        This method computes the mean and median incomes for districts grouped by their HOLC grades.
        The results are stored in a list following the pattern: [AMean, AMedian, BMean, BMedian, ...].
        After your calculations, you need to round the result to the closest whole int.
        Relate reading https://www.w3schools.com/python/ref_func_round.asp


        Returns
        -------
        list
            A list containing mean and median income values for each district grade in the order A, B, C, D.
        """
        grades = {
            "A": [],
            "B": [],
            "C": [],
            "D": [],
        }
        results = []
        for d in self.districts:
            grades[d.holcGrade].append(d.medIncome)
        
        for grade in ["A", "B", "C", "D"]:
            mean_income = round(np.mean(grades[grade]))
            median_income = round(np.median(grades[grade]))
            results.append(mean_income)
            results.append(median_income)
        
        return results
            


    def findCommonWords(self):
        """
        Analyzes the qualitative descriptions of each district category (A, B, C, D) and identifies the
        10 most common words unique to each category.

        This method aggregates the qualitative descriptions for each district category, splits them into
        words, and computes the frequency of each word. It then identifies and returns the 10 most 
        common words that are unique to each category, excluding common English filler words.

        Returns
        -------
        list of lists
            A list containing four lists, each list containing the 10 most common words for each 
            district category (A, B, C, D). The first list should represent grade A, and second for grade B,etc.
            The words should be in the order of their frequency.

        Notes
        -----
        - Common English filler words such as 'the', 'of', 'and', etc., are excluded from the analysis.
        - The method ensures that the common words are unique across the categories, i.e., no word 
        appears in more than one category's top 10 list.
        - Regular expressions could be used for word splitting to accurately capture words from the text.
        - Counter from collections could also be used.

        """
        # List of common filler words to exclude, you could add more if needed.
        filler_words = set(['the', 'of', 'and', 'in', 'to', 'a', 'is', 'for', 'on', 'that'])

        grades = {
            "A": "",
            "B": "",
            "C": "",
            "D": "",
        }
        
        for d in self.districts:
            grades[d.holcGrade] += " " + d.description.lower() # Use lower for easy later counting.
        
        grade_counts = {}
        
        for grade, grade_description in grades.items():
            words = re.findall(r"[a-z]+", grade_description) # Use the regular expression to extract words.
            filtered_words = [word for word in words if word not in filler_words]
            grade_counts[grade] = Counter(filtered_words) # Count the frequency of each word.
        
        used_words = set() # To track words already used in previous grades.
        unique_common_words = []
        for grade in ["A", "B", "C", "D"]:
            most_common = []
            for word, _ in grade_counts[grade].most_common():
                if word not in used_words:
                    most_common.append(word)
                    used_words.add(word) # Set uses "add" to add new item.
                if len(most_common) == 10:
                    break
            unique_common_words.append(most_common)
        
        return unique_common_words
    
    def calcRank(self):
        """
        Calculates and assigns a rank to each district based on median income.

        This method sorts the districts in descending order of their median income and then assigns
        a rank to each district, with 1 being the highest income district.

        Note
        ----
        The rank is assigned based on the position in the sorted list, so the district with the highest
        median income gets a rank of 1, the second-highest gets 2, and so on. Ties are not accounted for;
        each district will receive a unique rank.

        Important:
        If you do the extra credit, you need to edit the __init__ of DetroitDistrict adding another arg "rank" with
        default value to be None. Not doing so might cause the load cache method to fail if you use the ** operator in load cache. 

        Attribute 
        ----
        rank

        """
        

        pass

    def calcPopu(self):
        """
        Fetches and calculates the percentage of Black or African American residents in each district.

        This method fetch the total and Black populations for each census tract in Michigan from 
        the U.S. Census Bureau's API, like the median income data.  It then calculates the percentage of Black residents in each tract
        and assigns this value to the corresponding district percent attribute.

        Note
        ----
        The method assumes that the census tract IDs in the district data match those used by the Census Bureau.
        The percentage is rounded to two decimal places. If the Black population is zero, the percentage is set to 0. 
        Elif the total population is zero, the percentage is set to 1.

        Important:
        If you do the extra credit, you need to edit the __init__ of DetroitDistrict adding another arg "percent" with
        default value to be None. Not doing so might cause the load cache method to fail if you use the ** operator in load cache. 


        Attribute 
        ----
        percent

        """
        pass


    def comment(self):
        '''
        Look at the
        districts in each category, A, B, C and D. Are there any trends that you see? Share 1 paragraph of your
        findings. And a few sentences(more than 50 words) about how this exercise did or did not change your understanding of
        residential segregation. Print you thought in the method.
        '''
        print("")


# Use main function to test your class implementations.
# Feel free to modify the example main function.
def main():
    myRedLines = RedLines()
    myRedLines.createDistricts('redlines_data.json')
    myRedLines.plotDistricts()
    myRedLines.generateRandPoint()
    myRedLines.fetchCensus()
    myRedLines.fetchIncome()
    myRedLines.calcRank()  # Assuming you have this method
    myRedLines.calcPopu()  # Assuming you have this method
    myRedLines.cacheData('redlines_cache.json')
    myRedLines.loadCache('redlines_cache.json')
    # Add any other function calls as needed

if __name__ == '__main__':
    main()


