from PIL import Image
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

UPLOAD_FOLDER = r'C:\Users\shlom\PycharmProjects\day92_image_colour_group\static'  # Create this folder in your project directory
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Open an image file
image1 = Image.open('static/zwift_race.jpg')
image2 = Image.open('testrgb.png')

# Convert the image to RGB mode (if not already)
rgb_image = image2.convert('RGB')

# Convert the RGB image to a NumPy array
rgb_array = np.array(rgb_image)

# Convert to hex
hex_array = np.array([
    ["#{:02X}{:02X}{:02X}".format(r, g, b) for r, g, b in row]
    for row in rgb_array])

df = pd.DataFrame(hex_array)

# Flatten DataFrame to a 1D array for counting
Upload_image_flattened_colors = df.values.flatten()
print("FLATTENED COLORS")
print(Upload_image_flattened_colors)

def duplicate_colors(selected_picture):
    print(selected_picture)
    image1 = Image.open(f'static/{selected_picture}')

    # Convert the image to RGB mode (if not already)
    rgb_image = image1.convert('RGB')

    # Convert the RGB image to a NumPy array
    rgb_array = np.array(rgb_image)

    # Convert to hex
    hex_array = np.array([
        ["#{:02X}{:02X}{:02X}".format(r, g, b) for r, g, b in row]
        for row in rgb_array])

    df = pd.DataFrame(hex_array)

    # Flatten DataFrame to a 1D array for counting
    Upload_image_flattened_colors = df.values.flatten()
    print("FLATTENED COLORS")
    print(Upload_image_flattened_colors)
    print("function works")
    return Upload_image_flattened_colors


# Count occurrences of each unique HEX color


# Display duplicate color counts

# http://127.0.0.1:5000/
@app.route('/')
def home():
    # color_counts = pd.Series(flattened_colors).value_counts().reset_index()
    # color_counts = (
    #     pd.Series(Upload_image_flattened_colors)
    #     .value_counts(normalize=False)
    #     .rename_axis("HEX Color")
    #     .reset_index(name="Count")
    # )
    #
    # color_counts.columns = ["HEX Color", "Count"]
    # most_counted_colors = color_counts.head(11)
    #
    # color_table_html = most_counted_colors.to_html(classes='table table-striped', index=False)
    #
    # color_counts_df = pd.DataFrame({
    #     "HEX Color": ["#B7BDBB", "#507F93", "#B09685", "#82875F", "#B19786", "#83866B"],
    #     "Count": [1600, 1600, 1000, 800, 800, 600]})
    #
    # var = [111, 222, 555, 999]
    return render_template('table.html')


#  return render_template('index.html', var=color_counts_df["HEX Color"], var2=color_counts_df['Count'])


@app.route("/test", methods=['POST', 'GET'])
def show_color():

    if 'image' not in request.files:
        return "No file part", 400
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    if file:
        # Save the image to the specified upload folder

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        #CALL FUNCTION############

        #duplicate_colors(file.filename)
        print(file_path,file.filename)


        # Example: Process the image using PIL
        image = Image.open(file_path)
        print(image.filename)

        image = image.convert("L")  # Convert to grayscale as an example
        processed_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + file.filename)
        image.save(processed_path)


    flattened_colors = ['#2FC0C3', '#B29985', '#B19884', '#837C76', '#2FC0C3'] * 1000  # example
    color_counts = (
        pd.Series(duplicate_colors(file.filename))
        .value_counts()
        .rename_axis("HEX Color")
        .reset_index(name="Count")
    )


    #file=r'C:\Users\shlom\PycharmProjects\day92_image_colour_group\static\processed_chek_template.png'
    # loaded_picture_2=Image.open('zwift_race.jpg')

    # loaded_picture_2.show()

    return render_template('index_2.html', color_counts=color_counts.head(10), insert='',picture=file.filename)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return "No file part", 400
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    if file:
        # Save the image to the specified upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Example: Process the image using PIL
        image = Image.open(file_path)

        image = image.convert("L")  # Convert to grayscale as an example
        processed_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + file.filename)
        image.save(processed_path)

        return f"File uploaded and processed! Saved as {processed_path}", 200


if __name__ == '__main__':
    app.run(debug=True)

# shape = hex_array.shape
# size = hex_array.size
#
# # Print results
# print("HEX Array:\n", hex_array)
# print("\nShape:", shape)  # (Rows, Columns)
# print("Size:", size)  # Total number of elements
#
# array = np.zeros([100, 200, 3], dtype=np.uint8)
#
# array[:, :222] = [255, 128, 0]  # Orange left side
# array[:, 100:] = [0, 0, 255]  # Blue right side
#
# img = Image.fromarray(array)
# img.save('testrgb.png')
# img.show()


# Define the array and ensure it's a NumPy array with dtype=uint8
# array22 = np.array([[132, 131, 111],
#                     [132, 131, 111],
#                     [134, 131, 114]], dtype=np.uint8)
#
# # Convert to a grayscale image
# img22 = Image.fromarray(array22, mode='L')
#
# # Save and show the image
# img22_resized = img22.resize((100, 100), Image.NEAREST)  # You can change NEAREST to other resampling methods
#
# # Save and show the resized image
# img22_resized.save('picture_resized.png')
# img22_resized.show()


# chatgpt quastion
# \\color_counts = pd.Series(flattened colors).value_counts().reset_index() can i render to html file?
# # print(rgb_array)
# # print(rgb_array[11, 2])  # This will display a NumPy array of shape (height, width, 3)
# # print(rgb_image.size)
# print(rgb_image.show())  #zwift show
