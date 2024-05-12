import librosa
import pandas as pd
import os
from tqdm import tqdm

def extract_mfcc(audio_path):
    mfcc_features = []
    for file in tqdm(os.listdir(audio_path)):
        if file.endswith('.mp3'):
            try:
                audio, sr = librosa.load(os.path.join(audio_path, file))
                mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
                mfcc_features.append([file, mfcc])
            except Exception as e:
                print(f"Error processing {file}: {e}. Skipping...")
    return mfcc_features

def save_to_csv(mfcc_features, csv_file):
    df = pd.DataFrame(mfcc_features, columns=['audio_file', 'mfcc'])
    df.to_csv(csv_file, index=False)

audio_path = 'sample_audio(20gb)'
mfcc_features = extract_mfcc(audio_path)
save_to_csv(mfcc_features, 'MFCC(20GB)_features.csv')

