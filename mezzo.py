import streamlit as st
import random
from PIL import Image, ImageDraw

# Streamlit app title
st.title('Halftone Gradient Generator')

# Create columns for the UI and Image display
col1, col2 = st.columns([1, 3])  # Adjusts for 20% UI, 80% output ratio

# Slider parameters
with col1:
    min_diameter = st.slider('Min Dot Diameter', min_value=2, max_value=20, value=4, step=1)
    max_diameter = st.slider('Max Dot Diameter', min_value=2, max_value=40, value=16, step=1)
    max_spacing = st.slider('Max Spacing', min_value=5, max_value=100, value=50, step=5)
    randomness = st.slider('Randomness Factor', min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Image dimensions
width, height = 3800, 2800

def generate_image(min_diam, max_diam, max_space, randomness_factor, width, height):
    # Create a white background image
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Starting position
    x = 0

    # The change in space per step
    space_increase_per_step = max_space / width
    diameter_decrease_per_step = (max_diam - min_diam) / width

    # Draw circles
    while x < width:
        y = 0
        current_spacing = min_diam + int(x * space_increase_per_step)
        current_diameter = max_diam - int(x * diameter_decrease_per_step)  # Decreasing the diameter as x increases
        while y < height:
            # Apply randomness to the position
            random_offset_x = random.uniform(-randomness_factor, randomness_factor) * current_spacing
            random_offset_y = random.uniform(-randomness_factor, randomness_factor) * current_spacing
            # Ensure that the dot stays within the image bounds
            final_x = min(max(0, x + random_offset_x), width - current_diameter)
            final_y = min(max(0, y + random_offset_y), height - current_diameter)
            # Draw the circle
            draw.ellipse((final_x - current_diameter / 2, final_y - current_diameter / 2, final_x + current_diameter / 2, final_y + current_diameter / 2), fill='black')
            # Increase the y position by the current spacing
            y += current_spacing
        
        # Increase x position by the current spacing
        x += current_spacing

    return image

# Display the image in the second column
image = generate_image(min_diameter, max_diameter, max_spacing, randomness, width, height)
with col2:
    st.image(image, caption='Halftone Gradient', use_column_width=True)
