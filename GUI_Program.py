import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import tensorflow as tf

class ImageClassifierApp:
    def __init__(self, root):
        self.root = root
        root.title("Image Classifier")

        # Load the pre-trained model (e.g., MobileNetV2)
        self.model = tf.keras.applications.MobileNetV2(weights='imagenet', input_shape=(224, 224, 3))

        # Setup GUI
        self.setup_gui()

    def setup_gui(self):
        # Button to upload image
        self.upload_btn = tk.Button(self.root, text='Upload Image', command=self.upload_image)
        self.upload_btn.pack()

        # Label to show image
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # Label to show classification
        self.classification_label = tk.Label(self.root, text='Classification Results')
        self.classification_label.pack()

    def upload_image(self):
        # Open file dialog to select image
        file_path = filedialog.askopenfilename()
        if file_path:
            # Open and resize the image
            image = Image.open(file_path)
            image = image.resize((1024, 1024))

            # Display the image
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

            # Classify the image
            self.classify_image(image)

    def classify_image(self, image):
        # Preprocess the image
        img_array = tf.keras.preprocessing.image.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0)  # Create a batch

        # Predict the class
        predictions = self.model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        # Get the class name
        class_name = tf.keras.applications.mobilenet_v2.decode_predictions(score.numpy(), top=1)[0][0][1]
        self.classification_label.config(text=f'Predicted Class: {class_name}')

def main():
    root = tk.Tk()
    app = ImageClassifierApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
