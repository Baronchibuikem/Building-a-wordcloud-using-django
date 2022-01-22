from uuid import UUID
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views import View
from django.contrib import messages

from textvisualization.forms import DataForm
from textvisualization.utils import (
    show_wordcloud,
    create_text,
    read_file_by_file_extension,
)

from typing import Any, Optional
import pandas as pd

# Create your views here.


class WordCloudView(View):
    template_name = "textvisualization/wordcloudvisualization.html"

    def get_context_data(
        self,
    ) -> dict[str, Any]:
        context: dict[str, Any] = {}
        context["DataForm"] = DataForm()
        return context

    def narration_chart_data(
        self, request: HttpRequest, data: Optional[pd.DataFrame]
    ) -> HttpResponse:
        """Use to display narration wordcloud and other charts."""
        context = self.get_context_data()

        # read data from an excel sheet

        # get wordcloud image
        wordcloud = show_wordcloud(data)
        print("printiing wordcloud", wordcloud)
        context["wordcloud"] = wordcloud
        return render(request, self.template_name)

    def get(self, request: HttpRequest) -> HttpResponse:

        return render(
            request,
            self.template_name,
            self.get_context_data(),
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        context = self.get_context_data()
        form = DataForm(request.POST, request.FILES)
        values = []
        if form.is_valid():
            user_file = form.cleaned_data["file"]
            read_file = read_file_by_file_extension(user_file)
            for _, row in read_file.iterrows():
                print(row["access-to-basic-amenities-total-responses-2018-census-csv"])
                values.append(
                    row["access-to-basic-amenities-total-responses-2018-census-csv"]
                )
            return self.narration_chart_data(
                request,
                values,
            )
        else:
            form = DataForm(request.POST, request.FILES)
        return render(request, self.template_name, context)
