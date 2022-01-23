import base64
import io
import urllib
from typing import Any, Dict, List, Optional, Union
from django.core.files.uploadedfile import UploadedFile
import os


import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

stopwords = set(STOPWORDS)


def show_wordcloud(data: Optional[Union[List[str], str]]) -> Optional[Image.Image]:
    """Convert matplotlib data to image."""
    try:
        wordcloud = WordCloud(
            background_color="white",
            max_words=200,
            max_font_size=40,
            scale=3,
            random_state=0,
            stopwords=stopwords,
        )
        wordcloud.generate(str(data))

        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")

        image = io.BytesIO()
        plt.savefig(image, format="png")
        image.seek(0)  # rewind the data
        string = base64.b64encode(image.read())

        image_64 = "data:image/png;base64," + urllib.parse.quote(string)
        return image_64

        # return wordcloud.to_file("first_review.png")
    except ValueError:
        return None


def check_file_type(file: Union[UploadedFile, Any]) -> str:
    """Check the extension of the file."""
    extension = os.path.splitext(file.name)[1]
    return extension


def read_file_by_file_extension(
    file: Union[UploadedFile, Any]
) -> Optional[pd.DataFrame]:
    """Read the content of the file if it's .xlsx or .csv ."""
    file_type = check_file_type(file)
    read_file: Optional[pd.DataFrame] = None

    if file_type == ".xlsx":
        read_file = pd.read_excel(file)
    elif file_type == ".csv":
        read_file = pd.read_csv(file)
    return read_file
