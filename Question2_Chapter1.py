from PIL import Image
import numpy as np
import time
import os
print(os.getcwd())


# Calculate the current time and the generated number according to the provided algorithm
current_time = int(time.time())
generated_number = (current_time % 100) + 50
if generated_number % 2 == 0:
    generated_number += 10
print(generated_number)
# Load the image
original_image = Image.open(os.getcwd()+'/chapter1.jpg')
total_r = 0
def increase_rgb(image, value):
    # Split the image into channels
    r, g, b = image.split()
    print(r)
    # Convert channels to "L" mode which has pixel values 0-255
    r, g, b = r.point(lambda i: i + value), g.point(lambda i: i + value), b.point(lambda i: i + value)
    # Merge the channels back
    return Image.merge("RGB", (r, g, b))


# Apply the increase to the RGB values using the generated number
modified_image = increase_rgb(original_image, generated_number)
# Save the new image with converted pixels
output_image_path = os.getcwd()+'/chapter1.jpg'
modified_image.save(output_image_path)
width, height = modified_image.size
for y in range(height):
    for x in range(width):
        # Get the original pixel values (r, g, b)
        r,g,b = modified_image.getpixel((x, y))
        total_r = total_r + r
# Calculate the sum of the red channel values in the new image
#sum_red_values = np.sum(clipped_img_array[:, :, 0])

# Output the sum of the red channel values
print(total_r)