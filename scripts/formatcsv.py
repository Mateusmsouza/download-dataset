'''
create a CSV'''
import os
from csv import writer

import pandas as pd


RESTAURANT_DATASET = 'dataset-csv/restaurant_reviews.tsv'
IMAGES_FOLDER = 'dataset-images'

def __append_to_csv(image_path, review, sentiment):
        data = [image_path, review, sentiment]
        with open('dataset-visualsentiment-restaurant.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(data)
            f_object.close()


if __name__ == '__main__':
    df = pd.read_csv(RESTAURANT_DATASET, delimiter='\t', quoting=3)
    dataset_images_positive_path = f'{IMAGES_FOLDER}/positive'
    dataset_images_negative_path = f'{IMAGES_FOLDER}/negative'

    dataset_images_positive_list = os.listdir(dataset_images_positive_path)
    dataset_images_negative_list = os.listdir(dataset_images_negative_path)

    __append_to_csv('image_path', 'review', 'sentiment')
    for _, row in df.iterrows():
        sentiment = 'positive' if row['Liked'] == 1 else 'negative'

        if sentiment == 'positive':
            path = f'{dataset_images_positive_path}/{dataset_images_positive_list.pop()}'
        else:
            path = f'{dataset_images_negative_path}/{dataset_images_negative_list.pop()}'
        __append_to_csv(path, row['Review'], sentiment)