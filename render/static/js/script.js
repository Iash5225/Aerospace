document.addEventListener("DOMContentLoaded", function () {
  // Attach event listeners to your buttons
  document
    .getElementById("flightProfileBtn")
    .addEventListener("click", function () {
      window.location.href = "/flight_profile/";
    });

  document
    .getElementById("dragCoefficientBtn")
    .addEventListener("click", function () {
      window.location.href = "/drag_coefficient/";
    });

  document
    .getElementById("stabilityTimeBtn")
    .addEventListener("click", function () {
      window.location.href = "/stability_time/";
    });

  document
    .getElementById("motorThrustCurveBtn")
    .addEventListener("click", function () {
      window.location.href = "/motor_thrust_curve/";
    });
});
