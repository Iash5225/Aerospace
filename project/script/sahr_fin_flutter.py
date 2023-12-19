from sympy import symbols, lambdify, sqrt, exp

# Define symbols in one central place
cr, ct, b, h, H, T, G, t, P0, Cs0, B, lambda_ratio = symbols(
    'c_r c_t b h H T G t P_0 C_s0 B lambda_ratio')

# Expressions for wing area, aspect ratio, and taper ratio
S_expr = 1/2 * (cr + ct) * b
B_expr = b**2 / S_expr
lambda_expr = ct / cr
T_expr = t/cr

# Fin flutter velocity expression
Vf_expr = 1.223 * Cs0 * exp(0.4*h/H)*sqrt(G/P0) * \
    sqrt((2+B)/(1+lambda_ratio))*(T/B)**(3/2)

# Lambdify expressions for numerical calculations
normalised_thickness_function = lambdify((t, cr), T_expr, modules='numpy')
aspect_ratio_function = lambdify((cr, ct, b), B_expr, modules='numpy')
taper_ratio_function = lambdify((cr, ct), lambda_expr, modules='numpy')
flutter_velocity_lambdified = lambdify(
    (Cs0, h, H, G, P0, B, lambda_ratio, T), Vf_expr, modules='numpy')

# Now, you can call these lambdified functions in your main calculation functions


def calculate_normalised_thickness(thickness, root_chord):
    return normalised_thickness_function(thickness, root_chord)


def calculate_flutter_velocity(sea_level_speed_of_sound, altitude, atmospheric_scale_height, shear_modulus, sea_level_pressure, thickness, root_chord, tip_chord, semispan):
    aspect_ratio = aspect_ratio_function(root_chord, tip_chord, semispan)
    taper_ratio = taper_ratio_function(root_chord, tip_chord)
    normalised_thickness = calculate_normalised_thickness(thickness=thickness,root_chord=root_chord)

    flutter_velocity = flutter_velocity_lambdified(
        sea_level_speed_of_sound, altitude, atmospheric_scale_height, shear_modulus, sea_level_pressure, aspect_ratio, taper_ratio, normalised_thickness)

    return flutter_velocity

# Example usage in a 'main' function


def main():
    # Example input values
    altitude = 3000  # in feet
    shear_modulus = 380000  # in psi
    thickness = 0.125  # in inches
    root_chord = 9.75  # in inches
    tip_chord = 3.75  # in inches
    semispan = 4.75  # in inches
    sea_level_sound = 1100 # in ft/s
    sea_level_pressure = 14.7 # in psi
    atmospheric_scale_height = 26500 #ft
    

    # Perform calculations
    flutter_velocity = calculate_flutter_velocity(
        sea_level_sound, altitude, atmospheric_scale_height, shear_modulus, sea_level_pressure,thickness,root_chord,tip_chord,semispan)

    # Output results
    print(
        f"Flutter velocity at altitude {altitude} feet: {flutter_velocity} feet/second")


if __name__ == "__main__":
    main()
