import cv2
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
from scipy.interpolate import splprep, splev
matplotlib.use('TkAgg')


def create_air_ball(image_size, num_air_balls):
    image = np.zeros((image_size, image_size), dtype=np.uint8)

    for _ in range(num_air_balls):
        ball_center = (np.random.randint(20, image_size - 20), np.random.randint(20, image_size - 20))
        ball_axes = (np.random.randint(5, 20), np.random.randint(4,18))
        angle = (np.random.randint(0, 180))
        if ball_axes[0] < ball_axes[1]:
            proportion = ball_axes[0] / ball_axes[1]
        else:
            proportion = ball_axes[1] / ball_axes[0]
        print(f"Proportion: {proportion:.2f}")
        cv2.ellipse(image, ball_center, ball_axes, angle, 0, 360, 255, -1)

    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()



#  This function helps to calculate the length of the line
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance


def create_scratch(image_size, num_scratches):
    image = np.zeros((image_size, image_size), dtype=np.uint8)

    for _ in range(num_scratches):
        start = (np.random.randint(10, image_size - 20), np.random.randint(10, image_size - 20))
        end = (np.random.randint(10, image_size - 20), np.random.randint(10, image_size - 20))
        distance = calculate_distance(start, end)
        if distance > 2:
            proportion = 2 / distance
        else:
            proportion = distance / 2
        print(f"Proportion: {proportion:.10f}") # The function will return the number with up to 10 digits after the point
        cv2.line(image, start, end, 255, 2)

    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()

def create_stain():
        # Generate noisy points (same as before)
        num_points = 10  # const
        theta = np.linspace(0, 2 * np.pi, num_points)
        radius = 4  # const
        x_points = radius * np.cos(theta)
        y_points = radius * np.sin(theta)
        noise = np.random.normal(0, 1.5, num_points)
        x_points += noise
        y_points += noise

        # Fit a spline curve through the points
        tck, u = splprep([x_points, y_points], s=0)
        u_new = np.linspace(u.min(), u.max(), 100)
        x_fit, y_fit = splev(u_new, tck)

        # Calculate the area of the ellipse
        a = radius
        b = radius
        area_ellipse = np.pi * a * b

        # Calculate the positive area of the shaded region
        positive_area_shaded_region = np.trapz(np.maximum(y_fit, 0), x_fit)

        # Calculate the percentage
        percentage_inside_ellipse = abs((positive_area_shaded_region / area_ellipse) * 100)

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Plot the filled shape (shaded region)
        ax.fill(x_fit, y_fit, facecolor='gray', alpha=0.5, label='Shaded Region')

        # Plot the ellipse
        ellipse = Ellipse((0, 0), 2 * a, 2 * b, color='red', fill=False, linestyle='--', label='Ellipse')
        ax.add_patch(ellipse)

        # Set axis limits
        ax.set_xlim(-radius - 10, radius + 10)
        ax.set_ylim(-radius - 10, radius + 10)

        # Hide axes
        ax.axis('off')

        # Display the percentage inside the ellipse
        ax.text(0, -radius - 2, f"Percentage inside ellipse: {percentage_inside_ellipse:.2f}%", ha='center')

        # Show the plot
        plt.legend()
        plt.show()

# ---------------------------------Main Running Code----------------------------------------------------------------
try:
    image_size = 1000  # const
    defect_type = input("Please select the defect:\n"
                        "(1) Air-ball\n"
                        "(2) Scratch\n"
                        "(3) Stain\n"
                        "the number you chose: ")
    defect_type = int(defect_type)

    if defect_type == 1:
        amount = input("Please enter the amount of air-balls: ")
        create_air_ball(image_size, int(amount))
    elif defect_type == 2:
        amount = input("Please enter the amount of Scratches: ")
        create_scratch(image_size, int(amount))
    elif defect_type == 3:
        create_stain()
    else:
        print("Invalid number")
except ValueError:
    print("Invalid input. Please enter a valid number.")
