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

# Load the image
img = Image.open(os.getcwd()+'\chapter1.jpg')

# Convert image to numpy array
img_array = np.array(img)

# Ensure we don't go over the 255 limit for pixel values after addition
clipped_img_array = np.clip(img_array + generated_number, 0, 255)

# Convert the modified array back to an image
new_img = Image.fromarray(clipped_img_array.astype('uint8'))

# Save the new image with converted pixels
output_image_path = os.getcwd()+'\chapter1out.jpg'
new_img.save(output_image_path)

# Calculate the sum of the red channel values in the new image
sum_red_values = np.sum(clipped_img_array[:, :, 0])

# Output the sum of the red channel values
print(sum_red_values)