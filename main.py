from optimal_number_of_drones import OptimalNumberOfDrones
from optimal_drone_path import OptimalPath
from gsd_calculation import GSD

class MainClass:
    def __init__(self):
        self.optimal_number_of_drones = OptimalNumberOfDrones()
        self.optimal_drone_path = OptimalPath()
        self.gsd_calculation = GSD()

if __name__ == "__main__":
    main = MainClass()