from sympy import symbols, lambdify, sqrt

# Define additional symbols
cr, ct, b, h, T, G, t, P, a, AR, lambda_ratio = symbols(
    'c_r c_t b h T G t P a AR lambda_ratio')

# Define the expressions based on the image provided
S_expr = 1/2 * (cr + ct) * b
AR_expr = b**2 / S_expr
lambda_expr = ct / cr

# Temperature equation as a function of altitude
T_expr = 59 - 0.00356 * h

# Pressure equation as a function of temperature
P_expr = 2116/144 * ((T + 459.7) / 518.6) ** 5.256

# Speed of sound equation as a function of temperature in Fahrenheit
a_expr = (1.4 * 1716.59 * (T + 460))**0.5

# Flutter velocity equation
# Fin flutter velocity expression
Vf_expr = a * sqrt(G / (1.337 * AR**3 * P *
                   (lambda_ratio + 1) / (2 * (AR + 2) * (t / cr)**3)))

# Create a callable function for fin flutter velocity
flutter_velocity_function = lambdify(
    (a, G, AR, P, lambda_ratio, t, cr), Vf_expr, modules='numpy')


# Create callable functions for temperature and pressure
temperature_function = lambdify(h, T_expr, modules='numpy')
pressure_function = lambdify(T, P_expr, modules='numpy')

# Create a callable function for the speed of sound
speed_of_sound_function = lambdify(T, a_expr, modules='numpy')

# Function to calculate temperature given the altitude


def calculate_temperature(altitude):
    return temperature_function(altitude)


# Function to calculate the speed of sound given the temperature

# Function to calculate pressure given the altitude
def calculate_speed_of_sound(temperature_fahrenheit):
    return speed_of_sound_function(temperature_fahrenheit)


def calculate_pressure(altitude):
    # First calculate the temperature at the given altitude
    temperature = calculate_temperature(altitude)
    # Then calculate the pressure using the temperature
    return pressure_function(temperature)

# Now we use the calculate_temperature function to find the temperature at a given altitude
# and then use it to find the speed of sound at that altitude


def calculate_speed_of_sound_at_altitude(altitude):
    temperature_at_altitude = calculate_temperature(altitude)
    return calculate_speed_of_sound(temperature_at_altitude)


def calculate_wing_area(cr_val, ct_val, b_val):
    return S_expr.subs({cr: cr_val, ct: ct_val, b: b_val})


def calculate_aspect_ratio(cr_val, ct_val, b_val):
    S_val = calculate_wing_area(cr_val, ct_val, b_val)
    return AR_expr.subs({cr: cr_val, ct: ct_val, b: b_val, S_expr: S_val})


def calculate_taper_ratio(cr_val, ct_val):
    return lambda_expr.subs({cr: cr_val, ct: ct_val})

# Function to calculate the fin flutter velocity


def calculate_flutter_velocity(altitude, shear_modulus, thickness, root_chord, tip_chord, semispan):
    aspect_ratio = calculate_aspect_ratio(
        cr_val=root_chord, ct_val=tip_chord, b_val=semispan)
    taper_ratio = calculate_taper_ratio(cr_val=root_chord, ct_val=tip_chord)
    pressure = calculate_pressure(altitude=altitude)
    speed_of_sound = calculate_speed_of_sound_at_altitude(altitude=altitude)
    Vf = Vf_expr.subs({
        a: speed_of_sound,
        G: shear_modulus,
        AR: aspect_ratio,
        P: pressure,
        lambda_ratio: taper_ratio,
        t: thickness,
        cr: root_chord
    })
    return Vf.evalf()


def main():

    # Example inputs
    cr_value = 9.75  # root chord length inch
    ct_value = 3.75  # tip chord length inch
    b_value = 4.75  # semi-span inch
    shear_modulus_example = 380000.0  # in psi, for example
    thickness_example = 0.125  # thickness of the wing in inch, for example
    altitude_example = 3000.0  # Altitude in feet

    # Calculate outputs
    wing_area = calculate_wing_area(cr_value, ct_value, b_value)
    aspect_ratio = calculate_aspect_ratio(cr_value, ct_value, b_value)
    taper_ratio = calculate_taper_ratio(cr_value, ct_value)

    temperature_at_altitude = calculate_temperature(
        altitude_example)  # Calculate temperature
    pressure_at_altitude = calculate_pressure(
        altitude_example)  # Calculate pressure

    speed_of_sound_at_altitude = calculate_speed_of_sound_at_altitude(
        altitude_example)  # Calculate speed of sound

    # Calculate fin flutter velocity
    flutter_velocity = calculate_flutter_velocity(
        altitude=altitude_example,
        shear_modulus=shear_modulus_example,
        thickness=thickness_example,
        root_chord=cr_value,
        tip_chord=ct_value,
        semispan=b_value
    )
    # Print the results
    print("Wing Area (S):", wing_area)
    print("Aspect Ratio (AR):", aspect_ratio)
    print("Taper Ratio (λ):", taper_ratio)

    # Print the results
    print(
        f"Temperature at altitude {altitude_example} feet: {temperature_at_altitude} °F")
    print(
        f"Pressure at altitude {altitude_example} feet: {pressure_at_altitude} lbs/ft²")

    # Print the results
    print(
        f"Speed of sound at altitude {altitude_example} feet: {speed_of_sound_at_altitude} feet/second")

    print(f"Flutter velocity = {flutter_velocity} feet/s")


if __name__ == "__main__":
    main()
