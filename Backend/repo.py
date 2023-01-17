import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from models import (
    GasPowerPlant,
    CoalPowerPlant,
    SolarPowerPlant,
    WindPowerPlant,
    HydroPowerPlant,
)
from weather_values import return_all_elements
from scipy.optimize import linprog


class Repo:

    static_y_values = [1, 2, 3, 4, 5]

    @classmethod
    def optimize(cls, defaulth="1", num=3, changed_values=[],  indicator=True):

        cost_functions = ''

        if indicator:
            cost_functions +='linear'
        else:
            cost_functions +='polynom'

        if len(changed_values) == 0:
            cost_functions +='_static'
        else:
            cost_functions +='_changed'


        list_obj, list_solar_wind = cls.get_list_objects(num)

        loads = pd.read_csv("predicted_values.csv")
        solar_wind_data = pd.read_csv("test_data.csv")
        solar_wind_data = solar_wind_data[["windspeed", "solarradiation"]].fillna(0)
        counter = 0
        obj = [1] * (num * 3)
        lhs_ineq = [[1] * (num * 3)]
        integrality = [2] * (num * 3)

        list_sum = {}
        for item in loads.values:

            solar_power = cls._calculate_solar(
                    solar_wind_data["solarradiation"][counter],
                    list_solar_wind[0].surface_panel,
                )

            wind_power = cls._calculate_wind(solar_wind_data["windspeed"][counter], 2)
            load = item[2] - (solar_power + wind_power)

            counter += 1

            # z = x1 + x2 + x3 + x4 + x5 + x6 prestavlja elektrane

            rhs_ineq = []
            bound_list = []

            for index, item in enumerate(list_obj):
                # lhs_ineq[0][index] = lhs_ineq[0][index] * item.power_max
                try:
                    bound_list.append((item.power_min, item.power_max))
                except:
                    bound_list.append((item.hydro_power_min, item.hydro_power_max))

                try:
                    if cost_functions == "linear_static":
                        if defaulth == "1":
                            obj[index] = obj[index] * Repo.return_linear_function(
                                True, "1", [], x=item.power_max
                            )
                        elif defaulth == "2":
                            obj[index] = obj[index] * Repo.return_linear_function(
                                True, "3", [], x=item.power_max
                            )

                        elif defaulth == "3":
                            co2 = Repo.return_linear_function(
                                True, "3", [], x=item.power_max
                            )
                            fuel_cost = Repo.return_linear_function(
                                True, "2", [], x=co2
                            )

                            obj[index] = obj[index] * (co2 + fuel_cost)

                    if cost_functions == "linear_changed":
                        if defaulth == "1":
                            obj[index] = obj[index] * Repo.return_linear_function(
                                False,
                                "1",
                                changed_values,
                                item.power_max,
                            )
                        elif defaulth == "2":

                            obj[index] = obj[index] * Repo.return_linear_function(
                                False, "3", changed_values, item.power_max
                            )
                        elif defaulth == "3":
                            co2 = Repo.return_linear_function(
                                False, "3", changed_values, item.power_max
                            )
                            fuel_cost = Repo.return_linear_function(
                                False, "2", changed_values, co2
                            )
                            obj[index] = obj[index] * (co2 + fuel_cost)

                    if cost_functions == "polynom_static":
                        if defaulth == "1":
                            obj[index] = obj[index] * Repo.return_polynom_function(
                                True,
                                "1",
                                [],
                                item.power_max,
                            )
                        elif defaulth == "2":
                            obj[index] = obj[index] * Repo.return_polynom_function(
                                True, "3", [], item.power_max
                            )
                        elif defaulth == "3":
                            co2 = Repo.return_polynom_function(
                                True, "3", [], item.power_max
                            )
                            fuel_cost = Repo.return_polynom_function(True, "2", [], co2)
                            obj[index] = obj[index] * (co2 + fuel_cost)

                    if cost_functions == "polynom_changed":
                        if defaulth == "1":
                            obj[index] = obj[index] * Repo.return_polynom_function(
                                True,
                                "1",
                                changed_values,
                                item.power_max,
                            )
                        elif defaulth == "2":

                            obj[index] = obj[index] * Repo.return_polynom_function(
                                True, "3", changed_values, item.power_max
                            )
                        elif defaulth == "3":
                            co2 = Repo.return_polynom_function(
                                True, "3", changed_values, item.power_max
                            )
                            fuel_cost = Repo.return_polynom_function(
                                True, "2", changed_values, co2
                            )
                            obj[index] = obj[index] * (co2 + fuel_cost)

                except:
                    obj[index] = obj[index] * 0

            rhs_ineq = [load]

            result = linprog(
                c=obj,
                A_eq=lhs_ineq,
                b_eq=rhs_ineq,
                bounds=bound_list,
                method="highs",
                integrality=integrality,
            )
            list_sum[counter] = result.x.tolist()
            list_sum[counter].append(solar_power)
            list_sum[counter].append(wind_power)

        return list_sum

    @classmethod
    def get_list_objects(cls, number):
        list = []
        scale = 5000 / number / 2
        lover_25 = scale * 0.75

        for item in range(number):
            gas = GasPowerPlant(item, "Gas" + str(item), 70, 75, 250, 500)

            coal = CoalPowerPlant(item, "Coal" + str(item), 60, 75, 500, 800)

            hydro = HydroPowerPlant(item, "Hydro" + str(item), 800, 1300)

            list.append(gas)
            list.append(coal)
            list.append(hydro)

        solar = SolarPowerPlant(item, "Solar" + str(item), 100, 275, 360)
        wind = WindPowerPlant(item, "Wind" + str(item), 15, 23, 11)
        list_renewable = []
        list_renewable.append(solar)
        list_renewable.append(wind)
        return list, list_renewable

    @classmethod
    def _calculate_1_x_function(cls):
        pass

    @classmethod
    def return_linear_function(cls, static: bool, graph, y_values, x):
        x_values = [0.2, 0.4, 0.6, 0.8, 1]
        if static:
            if graph == "1":
                y_values = [1, 0.5, 0.4, 0.3, 0.2]
                return Repo._calculate_linear_function(x_values, y_values, x)
            elif graph == "2":
                y_values = [1, 0.9, 0.8, 0.6, 0.2]
                return Repo._calculate_linear_function(x_values, y_values, x)
            else:
                y_values = [0.2, 0.3, 0.4, 0.64, 1]
                return Repo._calculate_linear_function(x_values, y_values, x)

        else:
            return Repo._calculate_linear_function(x_values, y_values, x)

    @classmethod
    def _calculate_linear_function(cls, x, y, predict_x):
        data = np.polyfit(x, y, 1)
        y_new = data[0] * predict_x + data[1]
        return y_new

    @classmethod
    def return_polynom_function(cls, static: bool, graph, y_values, x):
        x_values = [0.2, 0.4, 0.6, 0.8, 1]
        if static:
            if graph == "1":
                y_values = [1, 0.5, 0.4, 0.3, 0.2]
                return Repo._calculate_function(x_values, y_values, x)
            elif graph == "2":
                y_values = [1, 0.9, 0.8, 0.6, 0.2]
                return Repo._calculate_function(x_values, y_values, x)
            else:
                y_values = [0.2, 0.3, 0.4, 0.64, 1]
                return Repo._calculate_function(x_values, y_values, x)

        else:
            return Repo._calculate_function(x_values, y_values, x)

    @classmethod
    def correct_a_b_c_for_exponential_curve_fir(x_data, y_data):
        a = 1
        b = 1
        c = 1
        popt = curve_fit(lambda t, a, b, c: a * pow(t, 2) + b * t + c, x_data, y_data)
        return popt[0][0], popt[0][1], popt[0][2]

    @classmethod
    def _calculate_function(cls,x_data, y_data,x):

        a, b , c = Repo.correct_a_b_c_for_exponential_curve_fir(x_data,y_data)
        return a * pow(x,2) + b*x + c


    @classmethod
    def _calculate_solar(cls, solar_radiation, surface_area):
        # fiksna vrednost jer formula nesto cudna trebna da se pomnozi sve solarrad
        if  solar_radiation == 0:
            return 0
        # print(surface_area * 3 + (solar_radiation % 100))
        return surface_area * 5 + (solar_radiation % 100)

    @classmethod
    def _calculate_wind(cls, wind_speed, cross_section=1):
        # cross section je 1 ako se pomnozi daje maksimum oko 6000
        # print((1/2) * 1.29 * cross_section * pow(wind_speed, 3))
        return (1 / 2) * 1.29 * cross_section * pow(wind_speed, 3)
