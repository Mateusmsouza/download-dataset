import logging

import pandas as pd
from csv import writer

from data.flickr import download_image_by_id

LOGGER = logging.getLogger('dataset')

class NeutralRowException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class FlickrService:

    def __init__(self) -> None:
        LOGGER.debug('Starting Flickr service')

    def __read_database(self) -> pd.DataFrame:
        return pd.read_csv('dataset-csv/flickr1_icassp2016_dataset.csv')
    
    def __is_positive(self, row) -> bool:
        ''' each row receives 3 votes for positive, negative or neutral.
            Neutral is excluded.
            If x >= 2 // x in [NEGATIVE, POSITIVE], image is considered x
        '''
        num_positive = row['Num_of_Positive']
        num_negative = row['Num_of_Negative']
        if num_positive >= 2:
            return True
        elif num_negative >= 2:
            return False
        raise NeutralRowException()
    
    def __create_csv_caption(self, photo_id, caption):
        data = [photo_id, caption]
        with open('dataset-photo-caption.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(data)
            f_object.close()

    def download_images(self):
        df_csv = self.__read_database()
        for _, row in df_csv.iterrows():
            try:
                sentiment = self.__is_positive(row)
                image_id = row['ImageID']
                caption = download_image_by_id(
                    photo_id=image_id,
                    save_on_dir=f'dataset-images/{sentiment}')
                self.__create_csv_caption(image_id, caption)
                break
            except NeutralRowException:
                # neutral images are not considered
                pass
