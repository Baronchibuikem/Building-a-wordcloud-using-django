import os

from django.core.exceptions import ValidationError
from django.forms import FileField, Form


class DataForm(Form):
    file = FileField()

    def clean_file(self) -> str:
        """Process the file data."""
        data = self.cleaned_data["file"]
        extension = os.path.splitext(data.name)[1]
        valid_extensions = [".xlsx", ".csv"]

        if extension not in valid_extensions:
            raise ValidationError("File type not supported")
        return data
