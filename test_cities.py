from cities import City, CityCollection
from utils import read_attendees_file
import pytest
from pytest import raises, approx
import math


zurich = City('Zurich', 'Switzerland', 52, 47.22, 8.33)
san_francisco = City('San Francisco', 'United States', 71, 37.77, -122.41)
greenwich = City('London', 'United Kingdom', 15, 51.48, 0)
los_angeles = City("Los Angeles", "United States", 298, 34, -118.24)

collection = CityCollection([zurich, san_francisco, greenwich, los_angeles])


def test_distance():
    result = zurich.distance_to(san_francisco)
    expected = 9375

    assert result == approx(expected, rel = 0.01)   #giving a tolerance to account for rounding 


def test_co2():
    result = zurich.co2_to(san_francisco)
    expected = 146245428

    assert result == approx(expected, rel = 0.01)   #giving a tolerance to account for rounding 


def test_total_attendees():
    result = collection.total_attendees()
    expected = 436

    assert result == expected


def test_total_distance_travel_to():
    result = collection.total_distance_travel_to(zurich)
    expected = 3516917

    assert result == approx(expected, rel = 0.01)

def test_total_co2():
    result = collection.total_co2(zurich)
    expected = 1053925728

    assert result == approx(expected, rel = 0.01)

def test_co2_to():
    distance = zurich.distance_to(san_francisco)
    result = zurich.co2_to(san_francisco)/(distance*zurich.attendees)
    expected = 300

    assert result == approx(expected, rel = 0.01)

def test_co2_edge_case():
    """
    Testing when two cities are approximately 1000km apart
    """
    phoenix = City("Phoenix", "United States", 2, 33.45, -112.08)              
    distance = math.floor(phoenix.distance_to(san_francisco)/1000)*1000         #(=1000)
    def co2_to_test(self, other: 'City') -> float:
        """
        The total CO2 emitted by the researchers travelling from one city to the host city
        """
        d = math.floor(self.distance_to(other)/1000)*1000                      #(=1000)
        if d <= 1000:
            co2 = 200*d*self.attendees 

        if 1000 < d <= 8000:
            co2 = 250*d*self.attendees

        if d > 8000:
            co2 = 300*d*self.attendees

        return co2

    result = co2_to_test(phoenix,san_francisco)/(distance*phoenix.attendees)
    expected = 200

    assert result == approx(expected, rel = 0.01)


def test_sorted_by_emissions():

    result = collection.sorted_by_emissions()
    expected = [('Los Angeles', approx(196112780, rel=0.01)), ('San Francisco', approx(218597803, rel=0.01)), ('London', approx(975610986, rel = 0.01)), ('Zurich', approx(1053925728, rel=0.01))]
    assert [tuples[0] for tuples in result] == [tuples[0] for tuples in expected]
    assert approx([tuples[1] for tuples in result], rel=0.001) == [tuples[1] for tuples in expected]




############################################################################      NEGATIVE TESTS      #######################################################################################

def test_inputs():
    with pytest.raises(TypeError):
        wrong_city_type = City(468, "Test Nation", 60, 80, -90)

    with pytest.raises(TypeError):
        wrong_country_type = City("Test", 1e6, 99, 80, -90)

    with pytest.raises(TypeError):
        wrong_attendees_type = City("Test", "Test Nation", "-48", 80, -90)
    
    with pytest.raises(ValueError):
        wrong_attendees_negative = City("Test", "Test Nation", -48, 80, -90)

    with pytest.raises(TypeError):
        wrong_latitude_type = City(468, "Test Nation", 60, "80", -90)

    with pytest.raises(ValueError):
        wrong_latitude_type = City("Test", "Test Nation", 60, 160, -90)

    with pytest.raises(TypeError):
        wrong_longitude_type = City(468, "Test Nation", 60, 80, "-90")

    with pytest.raises(ValueError):
        wrong_longtitude_type = City("Test", "Test Nation", 60, 160, -1500)

def test_plot_n_value():
    with pytest.raises(ValueError):
        collection.plot_top_emitters(zurich, 10, False)

    with pytest.raises(TypeError):
        collection.plot_top_emitters(zurich, "10", False)

def test_plot_sav():
    with pytest.raises(ValueError):
        collection.plot_top_emitters(zurich, 10, "False")

def test_list_of_cities():
    with pytest.raises(ValueError):
        empty_list_of_cities = CityCollection([])

    with pytest.raises(TypeError):
        wrong_list_of_cities = CityCollection([zurich, "zurich", san_francisco])

    
         
    
















