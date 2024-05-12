from time import sleep
from kafka import KafkaProducer
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans
from pyspark.ml import Pipeline
from pyspark.sql.types import DoubleType
from sklearn.metrics import adjusted_rand_score
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.ml.tuning import TrainValidationSplit, ParamGridBuilder
import pandas as pd

# Initialize Spark session
spark = SparkSession.builder \
    .appName("MusicRecommendationProducer") \
    .getOrCreate()

# Load the dataset
df = spark.read.csv("merged_data.csv", header=True, inferSchema=True)

# Convert 'duration' column to numeric
df = df.withColumn("duration", df["duration"].cast(DoubleType()))

# Convert 'genre_top_Blues' column to numeric
df = df.withColumn("genre_top_Blues", col("genre_top_Blues").cast(DoubleType()))

# Filter out rows with null values in selected features
selected_features = ['duration', 'listens', 'interest', 'genre_top_Blues', 'genre_top_Classical', 'genre_top_Country', 'genre_top_Easy Listening', 'genre_top_Electronic', 'genre_top_Experimental', 'genre_top_Folk', 'genre_top_Hip-Hop', 'genre_top_Instrumental', 'genre_top_International', 'genre_top_Jazz', 'genre_top_Old-Time / Historic', 'genre_top_Pop', 'genre_top_Rock', 'genre_top_Soul-RnB', 'genre_top_Spoken']
df_filtered = df.na.drop(subset=selected_features)

# Count the number of distinct clusters
num_clusters = df_filtered.select('track_id').distinct().count()

# Check if the number of clusters is greater than one
if num_clusters > 1:
    # Initialize an empty dictionary to store silhouette scores
    silhouette_scores = {}

    # Range of cluster numbers to test
    num_clusters_range = range(2, 21)

    # Create a VectorAssembler to assemble features into a vector
    assembler = VectorAssembler(inputCols=selected_features, outputCol="features")

    # Create a StandardScaler to normalize the features
    scaler = StandardScaler(inputCol="features", outputCol="scaledFeatures", withMean=True, withStd=True)

    # Define the evaluator
    evaluator = ClusteringEvaluator()

    for k in num_clusters_range:
        # Define the K-means clustering model
        kmeans = KMeans(featuresCol="scaledFeatures", k=k, seed=42)

        # Create a pipeline to chain feature transformation, scaling, and K-means model
        pipeline = Pipeline(stages=[assembler, scaler, kmeans])

        # Define a parameter grid for hyperparameter tuning
        param_grid = ParamGridBuilder().build()

        # Create a TrainValidationSplit
        train_val_split = TrainValidationSplit(estimator=pipeline,
                                               estimatorParamMaps=param_grid,
                                               evaluator=evaluator,
                                               trainRatio=0.8)  # 80% of the data will be used for training

        # Fit the TrainValidationSplit to the data
        tv_model = train_val_split.fit(df_filtered)

        # Get the best model from the TrainValidationSplit
        best_model = tv_model.bestModel

        # Apply the best model to the data to get cluster assignments
        predictions = best_model.transform(df_filtered)

        # Evaluate clustering by computing Silhouette score
        silhouette_score = evaluator.evaluate(predictions)

        # Store silhouette score for this cluster number
        silhouette_scores[k] = silhouette_score

    # Proceed with the original code after determining the optimal number of clusters

    # Define the K-means clustering model with the best number of clusters
    best_k = max(silhouette_scores, key=silhouette_scores.get)
    kmeans = KMeans(featuresCol="scaledFeatures", k=best_k, seed=42)

    # Create a pipeline to chain feature transformation, scaling, and K-means model
    pipeline = Pipeline(stages=[assembler, scaler, kmeans])

    # Fit the pipeline to the data
    model = pipeline.fit(df_filtered)

    # Make predictions
    predictions = model.transform(df_filtered)

    # Convert the DataFrame to Pandas DataFrame
    true_labels = df_filtered.select('track_id').toPandas()
    predicted_labels = predictions.select('track_id', 'prediction').toPandas()

    # Merge true labels and predicted labels based on track_id
    merged_labels = pd.merge(true_labels, predicted_labels, on='track_id')

    # Evaluate the best model using evaluation metrics
    silhouette_score = evaluator.evaluate(predictions)

    # Function to generate recommendations
    def generate_recommendations():
        input_track_ids = df_filtered.select("track_id").limit(10).rdd.flatMap(lambda x: x).collect()
        recommendations = {"track_ids": input_track_ids}  # Dummy recommendations for demonstration
        return recommendations

    # Initialize Kafka producer
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    # Function to produce recommendations and send them to Kafka topic
    def produce_recommendations():
        while True:
            recommendations = generate_recommendations()
            # Send recommendations to Kafka topic
            producer.send('music_recommendations', json.dumps(recommendations).encode('utf-8'))
            print("Recommendations sent to Kafka topic")
            sleep(5)  # Adjust sleep time as needed

    # Start Kafka producer
    produce_recommendations()

else:
    print("Error: Number of clusters must be greater than one.")

# Stop Spark session
spark.stop()

