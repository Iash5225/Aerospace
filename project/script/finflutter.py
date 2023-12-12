import numpy as np
import math


class FinFlutter:
    def __init__(self, altitude, shear_modulus, thickness, root_chord, tip_chord, semi_span, speed_of_sound=335, atmospheric_height=8077, std_atm_pressure=101325):
        self.altitude = altitude
        self.shear_modulus = shear_modulus
        self.thickness = thickness / 1000  # Convert mm to meters
        self.speed_of_sound = speed_of_sound
        self.atmospheric_height = atmospheric_height
        self.std_atm_pressure = std_atm_pressure

        self.semi_span = semi_span / 1000  # Convert mm to meters
        self.tip_chord = tip_chord / 1000  # Convert mm to meters
        self.root_chord = root_chord / 1000  # Convert mm to meters

        # Calculated Based on Inputs:
        # TODO
        # self.taper_ratio =

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
        wing_area = 0.5(self.root_chord+self.tip_chord)*self.semi_span
        return wing_area

    @property
    def aspect_ratio(self):
        aspect_ratio = math.pow(self.semi_span, 2)/self.wing_area
        return aspect_ratio

    @property
    def taper_ratio(self):
        taper_ratio = self.tip_chord/self.root_chord
        return taper_ratio
    
    @property
    def normalised_thickness(self):
        normalised_thickness = self.thickness/self.root_chord
        return normalised_thickness

    def calculate_flutter_velocity(self):
        exponent_part = np.exp(0.4 * self.altitude / self.atmospheric_height)
        first_sqrt_part = np.sqrt(self.shear_modulus/self.std_atm_pressure)
        second_sqrt_part = np.sqrt((2 + self.aspect_ratio) /
                                   (1 + self.taper_ratio))
        bracket_part = np.power(self.normalised_thickness/self.aspect_ratio,1.5)
        # bracket_part = (self.shear_modulus / self.std_atm_pressure) * ((2 + self.aspect_ratio) /
        #                                                                (1 + self.taper_ratio)) * (self.thickness / self.aspect_ratio)**1.5
        # flutter_velocity = 1.223 * self.speed_of_sound * \
        #     exponent_part * (bracket_part**1.3)
        flutter_velocity = 1.223 * self.speed_of_sound * exponent_part * first_sqrt_part * second_sqrt_part * bracket_part
        return flutter_velocity

    def calculate_safety_factor(self, desired_safety_factor):
        # Placeholder for safety factor calculation
        # You will need to implement the actual logic based on your safety requirements
        return desired_safety_factor

    # def calculate_aspect_ratio(self):
    #     return self.


# Example usage
if __name__ == "__main__":
    # Create an instance of FinFlutter with the required parameters
    fin_flutter = FinFlutter(
        altitude=3048,
        shear_modulus=5e9,
        thickness=4,
        aspect_ratio=0.7,
        taper_ratio=0.333
    )

    # Calculate flutter velocity
    velocity = fin_flutter.calculate_flutter_velocity()
    print(f"Flutter Velocity: {velocity:.2f} m/s")

    # Calculate safety factor (example value for desired_safety_factor provided)
    safety_factor = fin_flutter.calculate_safety_factor(
        desired_safety_factor=1.5)
    print(f"Safety Factor: {safety_factor}")
