Real-Time Music Recommendation System using MongoDB, Apache Kafka, Flask and spark

Extracting MFCC Features from Audio Files
This script extracts Mel-frequency cepstral coefficients (MFCC) features from audio files using the librosa library and saves them to a CSV file.

Overview
The script performs the following steps:

Extract MFCC Features:
It reads audio files from the specified directory.
For each audio file, it loads the audio using librosa, computes the MFCC features, and appends them to a list along with the file name.
It skips any files that are not in the .mp3 format.

Save to CSV:
It converts the list of MFCC features into a Pandas DataFrame.
It saves the DataFrame to a CSV file.

Requirements:
Python 3.x
librosa
pandas
tqdm

Usage:
Ensure you have the required Python libraries installed:

bash
Copy code
pip install librosa pandas tqdm
Set the audio_path variable to the directory containing the audio files.

Run the script:

bash
Copy code
python extract_mfcc.py
The MFCC features will be extracted and saved to a CSV file named MFCC_features.csv in the current directory.


STEP 2:
Merging Audio Metadata with MFCC Features
This script merges audio metadata from filtered_metadata.csv with MFCC features from MFCC_features_no_zeros.csv, based on the common numeric part of the audio_file and track_id columns.

Overview
The script performs the following steps:

Reading and Cleaning MFCC Features:
It reads the MFCC_features.csv file into a Pandas DataFrame.
It removes leading zeros from the audio_file column.
It saves the modified DataFrame to a new CSV file named MFCC_features_no_zeros.csv.

Merging Datasets:
It reads the filtered_metadata.csv and MFCC_features_no_zeros.csv files into Pandas DataFrames.
It extracts the numeric part from the audio_file column and creates a new column named audio_numeric.
It merges the two DataFrames based on the audio_numeric and track_id columns using an inner join.
It drops the audio_numeric column as it's no longer needed.
It saves the merged DataFrame to a new CSV file named merged_data.csv.

Requirements
Python 3.x
pandas

Usage
Ensure you have the required Python libraries installed:

bash
Copy code
pip install pandas
Run the script:

bash
Copy code
python merge_data.py
The merged data will be saved to a new CSV file named merged_data.csv in the current directory.

Step2 part2
Merging Audio Metadata with MFCC Features
This script merges audio metadata from filtered_metadata.csv with MFCC features from MFCC_features_no_zeros.csv, based on the common numeric part of the audio_file and track_id columns.

Overview
The script performs the following steps:

Reading and Cleaning MFCC Features:
It reads the filtered_metadata.csv and MFCC_features_no_zeros.csv files into Pandas DataFrames.
It extracts the numeric part from the audio_file column and creates a new column named audio_numeric.
Merging Datasets:
It merges the two DataFrames based on the audio_numeric and track_id columns using an inner join.
It drops the audio_numeric column as it's no longer needed.
It saves the merged DataFrame to a new CSV file named merged_data.csv.

Requirements
Python 3.x
pandas
Usage
Ensure you have the required Python libraries installed:

bash
Copy code
pip install pandas
Run the script:

bash
Copy code
python merge_data.py
The merged data will be saved to a new CSV file named merged_data.csv in the current directory.

STEP 3
Music Recommendation System with Apache Spark
This repository contains code for a Music Recommendation System implemented using Apache Spark, which utilizes machine learning techniques for clustering and recommendation.

Overview
The system performs the following steps:

Data Loading and Preprocessing:
Load music data from a CSV file into a Spark DataFrame.
Convert necessary columns to numeric types.
Filter out rows with null values in selected features.

Clustering:
Use K-means clustering algorithm to cluster music tracks based on selected features.
Perform hyperparameter tuning using a TrainValidationSplit.
Evaluate clustering performance using the Silhouette Score.
Determine the optimal number of clusters.

Recommendation Generation:
For each input track, recommend other tracks belonging to the same cluster.
Display recommended tracks for demonstration purposes.
Spark Session Management:

Initialize and stop the Spark session.
Requirements
Python 3.x
Apache Spark
pandas
matplotlib
Usage
Ensure you have Apache Spark installed and configured.
Install required Python packages using pip install -r requirements.txt.
Place your music dataset in CSV format named merged_data.csv in the project directory.
Run the Python script music_recommendation_system.py.
View the recommended tracks printed in the console.

Step 4
Real-Time Music Recommendation System using Apache Kafka and Flask
This repository contains code for a real-time music recommendation system implemented using Apache Kafka for streaming and Flask for serving recommendations on a web page.

Overview
The system consists of two main components:

Producer (producer.py):
The producer utilizes Apache Spark to perform clustering on music data and generates music recommendations.
KafkaProducer sends the recommendations to a Kafka topic (music_recommendations).

Consumer (consumer.py):
The consumer reads recommendations from the Kafka topic (music_recommendations) and serves them to a Flask web application.
The Flask application allows users to view real-time music recommendations on a web page.Real-Time Music Recommendation System using Apache Kafka and Flask
This repository contains code for a real-time music recommendation system implemented using Apache Kafka for streaming and Flask for serving recommendations on a web page.

Overview
The system consists of two main components:

Producer (producer.py):

The producer utilizes Apache Spark to perform clustering on music data and generates music recommendations.
KafkaProducer sends the recommendations to a Kafka topic (music_recommendations).
Consumer (consumer.py):

The consumer reads recommendations from the Kafka topic (music_recommendations) and serves them to a Flask web application.
The Flask application allows users to view real-time music recommendations on a web page.

Requirements
Python 3.x
Apache Kafka
Apache Spark
Flask
pyspark
kafka-pythonReal-Time Music Recommendation System using Apache Kafka and Flask
This repository contains code for a real-time music recommendation system implemented using Apache Kafka for streaming and Flask for serving recommendations on a web page.

Overview
The system consists of two main components:

Producer (producer.py):

The producer utilizes Apache Spark to perform clustering on music data and generates music recommendations.
KafkaProducer sends the recommendations to a Kafka topic (music_recommendations).
Consumer (consumer.py):

The consumer reads recommendations from the Kafka topic (music_recommendations) and serves them to a Flask web application.
The Flask application allows users to view real-time music recommendations on a web page.
Requirements
Python 3.x
Apache Kafka
Apache Spark
Flask
pyspark
kafka-python

Usage
Start Apache Kafka server.

Run the producer script to generate music recommendations:

bash
Copy code
python producer.py
Run the consumer script to serve recommendations on a web page:

bash
Copy code
python consumer.py
Access the Flask web application in your browser at http://localhost:5001.

View real-time music recommendations on the home page.
Usage
Start Apache Kafka server.

Run the producer script to generate music recommendations:

bash
Copy code
python producer.py
Run the consumer script to serve recommendations on a web page:

bash
Copy code
python consumer.py
Access the Flask web application in your browser at http://localhost:5001.

View real-time music recommendations on the home page.
Requirements
Python 3.x
Apache Kafka
Apache Spark
Flask
pyspark
kafka-python
Usage
Start Apache Kafka server.

Run the producer script to generate music recommendations:

bash
Copy code
python producer.py
Run the consumer script to serve recommendations on a web page:

bash
Copy code
python consumer.py
Access the Flask web application in your browser at http://localhost:5001.

View real-time music recommendations on the home page.

SUMMARY
This repository contains code for a Music Recommendation System implemented using Apache Spark. The system leverages machine learning techniques for clustering and recommendation.

Features:
Data Preprocessing: Load music data from CSV files, convert columns to numeric types, and filter out null values.
Clustering: Utilize K-means clustering algorithm for grouping music tracks based on selected features.
Recommendation Generation: Generate recommendations by recommending tracks within the same cluster as the input track.
Evaluation: Evaluate clustering performance using the Silhouette Score.
Visualization: Visualize Silhouette Scores to determine the optimal number of clusters.
Spark Session Management: Initialize and stop the Spark session.

Usage:
Ensure Apache Spark is installed and configured.
Install required Python packages using pip install -r requirements.txt.
Place the music dataset in CSV format named merged_data.csv in the project directory.
Run the Python script music_recommendation_system.py.
View the recommended tracks printed in the console.

Requirements:
Python 3.x
Apache Spark
pandas
matplotlib




