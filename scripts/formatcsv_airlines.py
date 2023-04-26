'''
create a CSV'''
import os
from csv import writer

import pandas as pd


AIRLINE_DATASET = 'dataset-csv/airline_reviews.csv'
IMAGES_FOLDER = 'dataset-images'

def __append_to_csv(image_path, review, sentiment):
        data = [image_path, review, sentiment]
        with open('dataset-visual_sentiment-airlines.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(data)
            f_object.close()


if __name__ == '__main__':
    df = pd.read_csv(AIRLINE_DATASET, delimiter=',')
    __append_to_csv('image_path', 'review', 'sentiment')
    dataset_images_positive_path = f'{IMAGES_FOLDER}/positive'
    dataset_images_negative_path = f'{IMAGES_FOLDER}/negative'

    dataset_images_positive_list = os.listdir(dataset_images_positive_path)
    dataset_images_negative_list = os.listdir(dataset_images_negative_path)

    for _, row in df.iterrows():
        
        sentiment = row['airline_sentiment']
        
        negative_used_images = []

        if sentiment == 'positive':
            image_id = dataset_images_positive_list.pop()
            path = f'{dataset_images_positive_path}/{image_id}/{image_id}_medium.jpg'
            __append_to_csv(path, row['text'], sentiment)
        elif sentiment == 'negative':
            if not dataset_images_negative_list:
                 # if we have used all negatives images, reset the array
                 dataset_images_negative_list = negative_used_images

            image_id = dataset_images_negative_list.pop()
            path = f'{dataset_images_negative_path}/{image_id}/{image_id}_medium.jpg'
            negative_used_images.append(image_id)
            __append_to_csv(path, row['text'], sentiment)