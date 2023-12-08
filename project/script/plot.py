import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Constants
MOTOR_NAME = "M2100F"
ROCKET_LENGTH = 2300
MAX_ALTITUDE = 10000
MIN_ALTITUDE = 0
ALTITUDE_INCREMENTS = 1000
MAX_VERTICAL_MOTION = 400
MIN_VERTICAL_MOTION = -100
VERTICAL_MOTION_INCREMENTS = 50
FLIGHT_PROFILE_CSV_FILE_PATH = "project\data\Flight_Profile.csv"
STABILITY_CSV_FILE_PATH = "project\data\Stability_vs_time.csv"
THURST_CURVE_CSV = "project\data\AeroTech_M2100G.csv"
AVERAGE_THRUST = 2173.6

rename_dict = {"# Time (s)": "Time (s)"}


def plot_Stability():
    """Plot Stability data."""
    df = pd.read_csv(STABILITY_CSV_FILE_PATH)
    df.rename(columns=rename_dict, inplace=True)

    df_cleaned = df.dropna(subset=["Stability margin calibers (​)"])
    df_cleaned["stability margin percentage"] = (
        (df_cleaned["CP location (mm)"] - df_cleaned["CG location (mm)"])
        / ROCKET_LENGTH
        * 100
    )

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(
        df_cleaned["Time (s)"],
        df_cleaned["Stability margin calibers (​)"],
        "k-",
        label="Stability(cal)",
    )
    ax2 = ax1.twinx()
    ax2.plot(
        df_cleaned["Time (s)"],
        df_cleaned["CP location (mm)"],
        "r--",
        label="CP location (mm)",
    )
    ax2.plot(
        df_cleaned["Time (s)"],
        df_cleaned["CG location (mm)"],
        "b--",
        label="CG location (mm)",
    )

    ax1.set_xlabel("TIME (s)")
    ax1.set_ylabel("STABILITY (cal)")
    ax2.set_ylabel("LOCATION (mm)")
    ax1.set_xlim(0, df["Time (s)"].max())
    ax1.grid(True)

    # Combine legends from ax1 and ax2
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="upper right")

    fig.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.title(f"{MOTOR_NAME} Motor - Stability(cal) vs Time(s)")
    plt.show()


def plot_Flight_Profile():
    """Plot Flight Profile data."""
    df = pd.read_csv(FLIGHT_PROFILE_CSV_FILE_PATH)
    df.rename(columns=rename_dict, inplace=True)

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot Altitude
    ax1.plot(df["Time (s)"], df["Altitude (ft)"], "k:", label="Altitude (ft)")
    ax1.set_xlabel("TIME (s)")
    ax1.set_ylabel("ALTITUDE (ft)")
    ax1.set_xlim(0, df["Time (s)"].max())
    ax1.set_ylim(MIN_ALTITUDE, MAX_ALTITUDE)
    ax1.set_yticks(range(MIN_ALTITUDE, MAX_ALTITUDE + 1, ALTITUDE_INCREMENTS))
    ax1.grid(True)

    # Plot Vertical velocity and Vertical acceleration on the same axis, ax2
    ax2 = ax1.twinx()
    ax2.plot(
        df["Time (s)"],
        df["Vertical velocity (m/s)"],
        "k--",
        label="Vertical velocity (m/s)",
    )
    ax2.plot(
        df["Time (s)"],
        df["Vertical acceleration (m/s²)"],
        "k-",
        label="Vertical acceleration (m/s²)",
    )
    ax2.set_ylabel("VERTICAL VELOCITY (m/s); VERTICAL ACCELERATION (m/s²)", labelpad=15)
    ax2.set_ylim(MIN_VERTICAL_MOTION, MAX_VERTICAL_MOTION)
    ax2.set_yticks(
        np.arange(
            MIN_VERTICAL_MOTION,
            MAX_VERTICAL_MOTION + 1,
            VERTICAL_MOTION_INCREMENTS,
        )
    )

    # Combine legends from ax1 and ax2
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="upper right")

    plt.title(f"{MOTOR_NAME} Motor - Vertical Motion vs Time")
    fig.tight_layout()  # Adjust layout to fit labels
    plt.show()


def plot_Thrust_Curve():
    df = pd.read_csv(THURST_CURVE_CSV, skiprows=3)

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(df["Time (s)"], df["Thrust (N)"], "k", label="Thrust (N)")
    ax1.set_xlabel("TIME (s)")
    ax1.set_ylabel("THRUST (N)")

    ax1.set_xlim(0)
    ax1.set_ylim(0)
    # ax1.set_ylim(0, df["Thrust (N)"].max())

    plt.axhline(y=AVERAGE_THRUST, color="k", linestyle="--")
    plt.text(
        df["Time (s)"].max() - 0.5,
        AVERAGE_THRUST,
        f"Average {AVERAGE_THRUST}N",
        verticalalignment="bottom",
        color="k",
    )

    plt.title(f"{MOTOR_NAME} Motor - Thrust Curve")
    fig.tight_layout()  # Adjust layout to fit labels
    plt.show()


# def plot_CD_Override_text():


def main():
    plot_Thrust_Curve()
    plot_Stability()
    plot_Flight_Profile()


if __name__ == "__main__":
    main()
