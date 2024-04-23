from typing import Dict, List, Tuple
from pytest import raises
from math import asin, sqrt, sin, cos, pi
import matplotlib.pyplot as plt


class City:
    ...
    def __init__(self, city, country, attendees, latitude, longitude):
        self.city = city
        self.country = country
        self.attendees = attendees
        self.latitude = latitude
        self.longitude = longitude

        #checking the data type and limits of inputs

        if type(city) != str or type(country) != str:
            raise TypeError("City and/or country name has to be string.")
        if type(attendees) != int:
            raise TypeError("Number of attendees should be a positive integer.")
        if attendees < 0:
            raise ValueError("Number of attendees should be a positive integer.")
        if type(latitude)  != float and type(latitude) != int:
            raise TypeError("Latitude must be a float or integer between -90 to 90 degrees.")
        if latitude > 90 or latitude < -90:
            raise ValueError("Latitude must be a float or integer between -90 to 90 degrees.")
        if type(longitude)  != float and type(longitude) != int:
            raise TypeError("Longitude must be a float or integer between -180 to 180 degrees.")
        if longitude > 180 or longitude < -180:
            raise ValueError("Longitude must be a float or integer between -180 to 180 degrees.")

    def distance_to(self, other: 'City') -> float:
        """
        Returns the distance in km from the one city to the host city
        """
        d1 = sin((self.latitude-other.latitude)*pi/360)**2               #input in radians
        d2 = cos(other.latitude*pi/180)*cos(self.latitude*pi/180)*(sin((self.longitude-other.longitude)*pi/360))**2     #input in radians

        return 2*6371*asin(sqrt(d1 + d2))           #where radius of the Earth is 6371km

    def co2_to(self, other: 'City') -> float:
        """
        The total CO2 emitted by the researchers travelling from one city to the host city
        """
        d = self.distance_to(other)
        if d <= 1000:
            co2 = 200*d*self.attendees 

        if 1000 < d <= 8000:
            co2 = 250*d*self.attendees

        if d > 8000:
            co2 = 300*d*self.attendees

        return co2
        

class CityCollection:
    ...
    def __init__(self, list_of_cities):
        self.cities = list_of_cities

        if len(list_of_cities) == 0:          #check to see if list is empty
            raise ValueError("The list of cities is empty.")

        for i in list_of_cities:             #check to see if the individual cities are City objects
            if type(i) != City:
                raise TypeError("All entries must be City objects.") 


    def countries(self) -> List[str]:
        """
        Returns a list of unique countries that the cities in the collection belong to
        """
        unique_countries = []
        for i in self.cities:
            unique_countries.append(i.country)


        return list(set(unique_countries))

    def total_attendees(self) -> int:
        """
        Returns the number of all the attendees
        """
        total_attendees = []
        for i in self.cities:
            total_attendees.append(i.attendees)


        return sum(total_attendees)

    def total_distance_travel_to(self, city: City) -> float:
        """
        Returns the total distance travelled by all attendees
        """
        d = []
        for i in self.cities:
            d.append((City.distance_to(i,city))*i.attendees)
        

        return sum(d)

    def travel_by_country(self, city: City) -> Dict[str, float]:
        """
        Returns a dictionary mapping the attendees' country to the distance travelled
        by all the attendees from that country to the host city
        """
        distance_per_country = {}
        for i in self.cities:
            if i.country not in distance_per_country.keys():     #check for unique country
                distance_per_country[i.country] = 0
            distance_per_country[i.country] += i.attendees*i.distance_to(city)
        

        return distance_per_country


    def co2_by_country(self, city: City) -> Dict[str, float]:
        """
        Returns a dictionary mapping the attendees' country to the CO2 emitted
        by all the attendees from that country to the host city
        """
        co2_per_country = {}
        for i in self.cities:
            if i.country not in co2_per_country.keys():    #check for unique country
                co2_per_country[i.country] = 0
            co2_per_country[i.country] += i.co2_to(city)            #add co2 to country for multiple cities in one country
            

        return co2_per_country

    
    def total_co2(self, city: City) -> float:
        """
        Returns the total CO2 emitted by all attendees if the conference
        were held in this city
        """
        total_co2 = []
        for i in self.co2_by_country(city):
           total_co2.append(self.co2_by_country(city)[i])
        
        return sum(total_co2)


    def summary(self, city: City):
        """
        Outputs a summarative statement containing information if this city 
        were to be chosen as host
        """
        print("Host city: {} ({})".format(city.city,city.country))
        print("Total CO2: {:.0f} tonnes".format(self.total_co2(city)/1000))

        if city in self.cities:     #if the host city is in the CityCollection
            print("Total attendees travelling to Zurich from {} different cities: {}".format(len(self.cities)-1,self.total_attendees()-city.attendees))
        
        else:                       #if the host city is not in the CityCollection
            print("Total attendees travelling to Zurich from {} different cities: {}".format(len(self.cities)-1,self.total_attendees()))


    def sorted_by_emissions(self) -> List[Tuple[str, float]]:
        """
        Returns a sorted listed of city names and CO2 emissions in ascending order
        """
        sort_emissions = []

        for i in self.cities:
            sort_emissions.append((i.city, self.total_co2(i)))

        sort_emissions.sort(key=lambda x:x[1])
    

        return sort_emissions


    def plot_top_emitters(self, city: City, n: int, save: bool):
        """
        PLots the CO2 emissions per country
        """

        #checking correct inputs for function

        if n > len(CityCollection.countries(self)):
            raise ValueError("You are appearing to be plotting more countries than there are in the collection.")

        if type(n) != int:
            raise TypeError("The number of countries with the most emissions must be a positive integer.")

        if type(save) != bool:
            raise TypeError("You have to specific True or False (boolean) if you wish to save the file.")


        emissions_per_country = CityCollection.co2_by_country(self,city)
        emissions_per_country = sorted(emissions_per_country.items(), key = lambda x: x[1])
        countries = []
        emissions = []

        for i in emissions_per_country:
            countries.append(i[0])
            emissions.append(i[1]/1000)      #emissions in tonnes

        countries = countries[:-n-1:-1]
        countries.append("All other countries")
        emissions_data = emissions[:-n-1:-1]
        emissions_data.append(sum(emissions[:-n]))

        plt.figure()
        plt.bar(countries, emissions_data)
        plt.title("Total emissions from each country (Top {})".format(n))
        plt.ylabel("Total emissions (tonnes CO2)")
        plt.xticks()

        if save == True:
            s = ("_".join(city.city.split())).lower()
            plt.savefig("{}.png".format(s))

        plt.show()
