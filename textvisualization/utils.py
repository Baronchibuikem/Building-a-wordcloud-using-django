# # used for suppressing pandas warning that will populate on the terminal
# import warnings

# warnings.simplefilter(action='ignore', category=FutureWarning)

import base64
import io
import urllib
from typing import Any, Dict, List, Optional, Union
from django.core.files.uploadedfile import UploadedFile
import os

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
from nltk import FreqDist, ngrams, word_tokenize
from PIL import Image
from wordcloud import WordCloud


def create_text(
    condition: bool, dataframe: pd.DataFrame, *args: Any
) -> Union[List[str], str]:
    """Create nltk.Text(word_tokenize(narration)) based on categories (or without any categories)."""
    subset = []
    if dataframe is not None:
        if not any(args):
            subset = dataframe
        elif args[0] == 0:
            subset = dataframe[
                (dataframe["week"] == args[1]) & (dataframe["day"] == args[2])
            ]
        elif args[1] == 0:
            subset = dataframe[
                (dataframe["month"] == args[0]) & (dataframe["day"] == args[2])
            ]
        elif args[2] == 0:
            subset = dataframe[
                (dataframe["month"] == args[0]) & (dataframe["week"] == args[1])
            ]
        elif all(args):
            subset = dataframe[
                (dataframe["month"] == args[0])
                & (dataframe["week"] == args[1])
                & (dataframe["day"] == args[2])
            ]
        subset_narration = " ".join(subset["narration"].tolist())  # type: ignore
        # tokens to text for using nltk
        if condition:
            # create tokens
            tokens = word_tokenize(subset_narration)
            # tokens to text for using nltk
            text = nltk.Text(tokens)
            return text
        return subset_narration
    return subset


def show_wordcloud(data: Optional[Union[List[str], str]]) -> Optional[Image.Image]:
    """Convert matplotlib data to image."""
    try:
        wordcloud = WordCloud(
            background_color="white",
            max_words=200,
            max_font_size=40,
            scale=3,
            random_state=0,
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
