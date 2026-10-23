
import math
import matplotlib.pyplot as plt

print("===== JEE PHYSICS LAB =====")
print("Projectile Motion Simulator\n")

# Get inputs

while True:
    speed = float(input("Enter initial speed (m/s): "))
    angle = float(input("Enter launch angle (degrees): "))

    if speed > 0 and 0 < angle < 90:
        break

    print("Invalid input. Speed must be positive")
    print("and angle must be between 0 and 90 degrees.")


gravity = 9.8
angle_rad = math.radians(angle)

# Calculate motion
flight_time = 2 * speed * math.sin(angle_rad) / gravity
max_height = (speed**2 * math.sin(angle_rad)**2) / (2 * gravity)
horizontal_range = speed**2 * math.sin(2 * angle_rad) / gravity

# Display results
print("\n===== RESULTS =====")
print(f"Time of flight: {flight_time:.2f} seconds")
print(f"Maximum height: {max_height:.2f} metres")
print(f"Horizontal range: {horizontal_range:.2f} metres")

# Generate points along the trajectory
times = [
    i * flight_time / 100
    for i in range(101)
]

x_positions = [
    speed * math.cos(angle_rad) * t
    for t in times
]

y_positions = [
    speed * math.sin(angle_rad) * t
    - 0.5 * gravity * t**2
    for t in times
]

# Plot the trajectory
plt.figure(figsize=(9, 5))
plt.plot(x_positions, y_positions, label="Projectile path")
plt.axhline(0, color="black", linewidth=0.8)

plt.title("JEE Physics Lab - Projectile Motion")
plt.xlabel("Horizontal distance (m)")
plt.ylabel("Vertical height (m)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
