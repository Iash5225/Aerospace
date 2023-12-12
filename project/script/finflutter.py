import numpy as np
import math
import matplotlib.pyplot as plt


class FinFlutter:
    def __init__(self, altitude: int, shear_modulus: float, root_chord: float, tip_chord: float, semi_span: float, speed_of_sound: float = 335, atmospheric_height: float = 8077, std_atm_pressure: float = 101325):
        self.altitude = altitude
        self.shear_modulus = shear_modulus
        self.speed_of_sound = speed_of_sound
        self.atmospheric_height = atmospheric_height
        self.std_atm_pressure = std_atm_pressure

        self.semi_span = semi_span / 1000  # Convert mm to meters
        self.tip_chord = tip_chord / 1000  # Convert mm to meters
        self.root_chord = root_chord / 1000  # Convert mm to meters

    def set_altitude(self, altitude: float):
        self.alitide = altitude

    def set_shear_modulus(self, shear_modulus):
        self.shear_modulus = shear_modulus

    def set_thickness(self, thickness):
        self.thickness = thickness

    def set_speed_of_sound(self, speed_of_sound):
        self.speed_of_sound = speed_of_sound

    def set_atmospheric_height(self, atmospheric_height):
        self.atmospheric_height = atmospheric_height

    def set_std_atm_pressure(self, std_atm_pressure):
        self.std_atm_pressure = std_atm_pressure

    def set_semi_span(self, semi_span):
        self.semi_span = semi_span

    def set_tip_chord(self, tip_chord):
        self.tip_chord = tip_chord

    @property
    def wing_area(self):
        wing_area = 0.5*(self.root_chord+self.tip_chord)*self.semi_span
        return wing_area

    @property
    def aspect_ratio(self):
        aspect_ratio = np.power(self.semi_span, 2)/self.wing_area
        return aspect_ratio

    @property
    def taper_ratio(self):
        taper_ratio = self.tip_chord/self.root_chord
        return taper_ratio

    def normalised_thickness(self, thickness):
        normalised_thickness = (thickness/1000)/self.root_chord
        return normalised_thickness

    def calculate_flutter_velocity(self, thickness):
        # Debug print statements to check intermediate values


        exponent_part = np.exp(0.4 * self.altitude / self.atmospheric_height)
        first_sqrt_part = np.sqrt(self.shear_modulus/self.std_atm_pressure)
        second_sqrt_part = np.sqrt((2 + self.aspect_ratio) /
                                   (1 + self.taper_ratio))
        bracket_part = np.power(self.normalised_thickness(
            thickness)/self.aspect_ratio, 3/2)
        flutter_velocity = 1.223 * self.speed_of_sound * exponent_part * \
            first_sqrt_part * second_sqrt_part * bracket_part
            
        # Debug print statements to check intermediate values
        # print(f"Exponent part: {exponent_part}")
        # print(f"First sqrt part: {first_sqrt_part}")
        # print(f"Second sqrt part: {second_sqrt_part}")
        # print(f"Bracket part: {bracket_part}")
        return flutter_velocity
    
    def calculate_thickess(self,flutter_velocity):
        first_exponent_part = np.exp(0.4 * self.altitude / self.atmospheric_height)
        first_sqrt_part = np.sqrt(self.shear_modulus/self.std_atm_pressure)
        second_sqrt_part = np.sqrt((2 + self.aspect_ratio) /
                                   (1 + self.taper_ratio))
        
        inside_exponent = 1.223 * self.speed_of_sound * first_exponent_part * \
            first_sqrt_part * second_sqrt_part
        
        overall_exponent = np.power(flutter_velocity/inside_exponent, 2/3)
        
        normalised_thickness = (overall_exponent*self.aspect_ratio)
        thickness = normalised_thickness * self.root_chord * 1000
        return thickness

    def calculate_safety_factor(self, desired_safety_factor):
        # Placeholder for safety factor calculation
        # You will need to implement the actual logic based on your safety requirements
        return desired_safety_factor
    
    def print_summary(self):
        print(f"Altitude: {self.altitude}")
        print(f"Shear modulus: {self.shear_modulus}")
        print(f"Standard atmospheric pressure: {self.std_atm_pressure}")
        
        print("\n")
        print(f"Root Chord: {self.root_chord}")
        print(f"Tip Chord: {self.tip_chord}")
        print(f"Aspect ratio: {self.aspect_ratio}")
        print(f"Taper ratio: {self.taper_ratio}")
        # print(f"Thickness: {thickness}")
        # print(f"Normalised Thickness: {self.normalised_thickness(thickness)}")
        
        print("\n")
        print(f"Speed of sound: {self.speed_of_sound}")
        print(f"Atmospheric height: {self.atmospheric_height}")
        
    def plot_flutter_velocity(self,max_thickness:int,thickness_incremenets:float):
        # 101 points from 0 to 10
        thickness_list = np.arange(
            0, max_thickness + thickness_incremenets, thickness_incremenets)
        
        flutter_velocity_list = [self.calculate_flutter_velocity(
            thickness) for thickness in thickness_list]
        
        # Plotting the results
        plt.figure(figsize=(10, 6))
        plt.plot(thickness_list, flutter_velocity_list, marker='o')
        
        # Setting minimum x and y limits to 0
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.title('Fin Flutter Velocity vs. Thickness')
        plt.xlabel('Thickness (mm)')
        plt.ylabel('Flutter Velocity (m/s)')
        plt.grid(True)
        plt.show()  
        
def main():
    # Create an instance of FinFlutter with the required parameters
    fin_flutter = FinFlutter(
        altitude=3048,
        shear_modulus=5e9,
        root_chord=300,
        tip_chord=100,
        semi_span=140,
    )

    # Calculate flutter velocity
    fin_flutter.set_speed_of_sound(346.06)
    velocity = fin_flutter.calculate_flutter_velocity(4)
    print(f"Flutter Velocity: {velocity:.2f} m/s")
    
    OR_max_velocity = 323
    thickness = fin_flutter.calculate_thickess(OR_max_velocity)
    print(
        f"thickness required to handle OR max velocity of {OR_max_velocity} is {thickness} mm")
    
    # fin_flutter.plot_flutter_velocity(6,0.1)

    # # Calculate safety factor (example value for desired_safety_factor provided)
    # safety_factor = fin_flutter.calculate_safety_factor(
    #     desired_safety_factor=1.5)
    # print(f"Safety Factor: {safety_factor}")


if __name__ == "__main__":
    main()
