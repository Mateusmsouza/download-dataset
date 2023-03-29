import logging

import pandas as pd
from csv import writer
from flickrapi.exceptions import FlickrError

from data.flickr import download_image_by_id

LOGGER = logging.getLogger('dataset')

class NeutralRowException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class FlickrService:

    def __init__(self, max_negative=500, max_positive=500) -> None:
        self.__max_negative = 500
        self.__max_positive = 500
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
        nagetive_images_downloaded = 0
        positive_images_downloaded = 923
        df_csv = self.__read_database()
        for _, row in df_csv.iterrows():
            try:

                # improve count if necessary. Place it after actually downloading image
                if self.__is_positive(row):
                    sentiment = 'positive'
                    positive_images_downloaded += 1
                else:
                    sentiment = 'negative'
                    nagetive_images_downloaded += 1


                
                image_id = row['ImageID']
                caption = download_image_by_id(
                    photo_id=image_id,
                    save_on_dir=f'dataset-images/{sentiment}')
                self.__create_csv_caption(image_id, caption)
                
                if positive_images_downloaded >= self.__max_positive and nagetive_images_downloaded >= self.__max_negative:
                    LOGGER.info(
                        f'Total desired images collected. {self.__max_positive} positive images were asked '
                        f'and {self.__max_negative} negatives images were asked.')
                    LOGGER.info(f'Actually collected - positive: {positive_images_downloaded} and negative: {nagetive_images_downloaded}')
                    break
            except NeutralRowException:
                # neutral images are not considered
                pass
            except TypeError:
                LOGGER.error(f'medium or large image size from {image_id} could not be downloaded.')
            except FlickrError:
                LOGGER.error(f'Image {image_id} not found on Flickr')
            except OSError:
                LOGGER.warn(f'Image {image_id} is already on disk')
