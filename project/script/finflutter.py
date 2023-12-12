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

    def calculate_safety_factor(self, design_thickness, max_allowable_velocity):
            """
            Calculate the safety factor for a given thickness.
            
            Safety Factor = Max Allowable Velocity / Calculated Flutter Velocity

            :param design_thickness: Design thickness of the fin (in mm).
            :param max_allowable_velocity: Maximum allowable flutter velocity (in m/s).
            :return: Safety factor.
            """
            design_flutter_velocity = self.calculate_flutter_velocity(design_thickness)
            if max_allowable_velocity == 0:
                return float('inf')  # To avoid division by zero
            return design_flutter_velocity / max_allowable_velocity
    
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
        

    def plot_flutter_velocity(self, max_thickness, thickness_increments, design_thickness=None, max_velocity=None):
        thickness_list = np.arange(0, max_thickness + thickness_increments, thickness_increments)
        flutter_velocity_list = [self.calculate_flutter_velocity(thickness) for thickness in thickness_list]
        safety_factor_list = [self.calculate_safety_factor(thickness, max_velocity) for thickness in thickness_list]

        fig, ax1 = plt.subplots(figsize=(12, 6))

        color = 'tab:blue'
        ax1.set_xlabel('Thickness (mm)')
        ax1.set_ylabel('Flutter Velocity (m/s)', color=color)
        ax1.plot(thickness_list, flutter_velocity_list, label='Flutter Velocity', marker='o', color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        # Add max rocket velocity horizontal line
        if max_velocity is not None:
            ax1.axhline(y=max_velocity, color='purple', linestyle='--', linewidth=2, label=f'Max Rocket Velocity: {max_velocity}m/s')

        ax2 = ax1.twinx()
        color = 'tab:orange'
        ax2.set_ylabel('Safety Factor', color=color)
        # ax2.plot(thickness_list, safety_factor_list, label='Safety Factor', marker='x', color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        # Highlight design thickness and max thickness points if provided
        if design_thickness is not None:
            design_velocity = self.calculate_flutter_velocity(design_thickness)
            design_safety_factor = self.calculate_safety_factor(
                design_thickness, max_velocity)
            ax1.axvline(x=design_thickness, color='red', linestyle='--',
                        linewidth=2, label=f'Design Thickness: {design_thickness}mm')
            ax2.axhline(y=design_safety_factor, color='orange', linestyle='-.',
                        linewidth=2, label=f'Design Safety Factor: {design_safety_factor:.2f}')

        if max_velocity is not None:
            min_thickness_value = self.calculate_thickess(max_velocity)
            ax1.axvline(x=min_thickness_value, color='green', linestyle='--',
                        linewidth=2, label=f'Min Design Thickness: {min_thickness_value:.2f}mm')

        plt.title('Fin Flutter Analysis', y=1.05)  # Adjust the title position

        # Create a single legend for all lines
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper left')

        fig.tight_layout()  # Adjust layout to prevent clipping
        plt.grid(True)
        plt.show()
        
def main():
    # Create an instance of FinFlutter with the required parameters
    # Create an instance of FinFlutter with the required parameters
    fin_flutter = FinFlutter(
        altitude=3048,
        shear_modulus=5e9,
        root_chord=300,
        tip_chord=100,
        semi_span=140,
        speed_of_sound=346.06  # Example speed of sound
    )

    # User input for design thickness and max velocity
    design_thickness = float(input("Enter design thickness (in mm): "))
    max_velocity = float(input("Enter max rocket velocity (in m/s): "))

    # Calculate flutter velocity for design thickness
    design_flutter_velocity = fin_flutter.calculate_flutter_velocity(
        design_thickness)
    print(f"Design Flutter Velocity: {design_flutter_velocity:.2f} m/s")

    # Check if design flutter velocity is bigger than max velocity
    if design_flutter_velocity > max_velocity:
        print("The design is safe.")
    else:
        print("The design is not safe. Adjust thickness.")
        
    # Call the extended plotting function
    fin_flutter.plot_flutter_velocity(
        max_thickness=10, thickness_increments=0.1, design_thickness=design_thickness, max_velocity=max_velocity)


if __name__ == "__main__":
    main()
