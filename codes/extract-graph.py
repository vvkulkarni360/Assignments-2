import cv2
import matplotlib.pyplot as plt
import pandas as pd
from pdf2image import convert_from_path
import numpy as np

# Function to extract ECG graphs from PDF images
def extract_ecg_from_pdf(pdf_file):
    # Extract images from PDF
    pages = convert_from_path(pdf_file, first_page=3, last_page=3)
   
    ecg_graphs = []  # List to store extracted ECG graphs

    for page in pages:
        # Convert page image to NumPy array
        page_image = np.array(page)

        # Process page image to identify and extract ECG graphs
        # Example: Identify ECG graphs based on size or pattern
        ecg_images = identify_ecg_images(page_image)

        # Append identified ECG graphs to the list
        ecg_graphs.extend(ecg_images)

    return ecg_graphs

# Function to identify ECG images within a page image
def identify_ecg_images(page_image):
        # Convert page image to grayscale
    gray_image = cv2.cvtColor(page_image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to create a binary image
    _, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract and separate each contour (assumed to be an ECG graph)
    ecg_images = []
    for contour in contours:
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Extract the contour as an ECG graph
        ecg_image = page_image[y:y+h, x:x+w]

        # Append the extracted ECG graph to the list
        ecg_images.append(ecg_image)

    return ecg_images

# Load PDF file and extract ECG graphs
pdf_file = '../pdf/graph-1-1.pdf'
ecg_graphs = extract_ecg_from_pdf(pdf_file)

# Process extracted ECG graphs
for i, ecg_graph in enumerate(ecg_graphs):
    # Process each ECG graph (e.g., convert to grayscale, plot, etc.)
    gray_image = cv2.cvtColor(ecg_graph, cv2.COLOR_BGR2GRAY)

    # Plot the extracted ECG graph
    plt.imshow(gray_image, cmap='gray')
    plt.axis('off')
    plt.title(f'ECG Graph {i+1}')
    plt.show()

    # Additional processing or analysis of the ECG graph can be done here
def analyze_ecg_abnormalities(ecg_data):
    # Convert ECG data to pandas DataFrame
    ecg_df = pd.DataFrame({'Time': range(len(ecg_data)), 'Voltage': ecg_data})

    # Compute statistics (e.g., mean, standard deviation)
    mean_voltage = ecg_df['Voltage'].mean()
    std_voltage = ecg_df['Voltage'].std()

    # Detect abnormalities based on threshold values
    abnormal_threshold_low = mean_voltage - 2 * std_voltage
    abnormal_threshold_high = mean_voltage + 2 * std_voltage

    # Identify abnormal voltage values
    abnormal_voltages = ecg_df[(ecg_df['Voltage'] < abnormal_threshold_low) | (ecg_df['Voltage'] > abnormal_threshold_high)]

    return abnormal_voltages


sample_ecg_data = np.random.normal(loc=0, scale=1, size=1000)  # Normal distribution
sample_ecg_data[300:400] += 3  # Add abnormality to the ECG data

# Analyze ECG data for abnormalities
abnormalities_df = analyze_ecg_abnormalities(sample_ecg_data)

# Display detected abnormalities
print("Detected Abnormalities:")
print(abnormalities_df)


#plot

plt.plot(sample_ecg_data, label='ECG Data')
plt.scatter(abnormalities_df['Time'], abnormalities_df['Voltage'], color='red', label='Abnormalities')
plt.xlabel('Time')
plt.ylabel('Voltage')
plt.title('ECG Data with Abnormalities')
plt.legend()
plt.show()


# Create a Pandas DataFrame with the extracted text
df = pd.DataFrame({'abnormalities_df': [abnormalities_df]})


csv_file = 'abnormalities_df.csv'
df.to_csv(csv_file, index=False)

print(f'DataFrame saved to {csv_file}')