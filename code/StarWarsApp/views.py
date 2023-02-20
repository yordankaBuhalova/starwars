from django.shortcuts import render
from django.views.generic import TemplateView
from StarWarsApp.collect_data import collect
from StarWarsApp.models import DatasetCSV
import petl as etl
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)


class ListView(TemplateView):
    '''
        List of csv files collection
    '''
    template_home = 'list.html'

    def get(self, request, *args, **kwargs):

        files = DatasetCSV.objects.all().order_by('-created_date')

        return render(
            request,
            self.template_home,
            {'files': files}
        )

    def post(self, request, *args, **kwargs):

        old_files = DatasetCSV.objects.all()
        files = collect()

        if len(old_files) < len(files):
            messages.success(request, 'Your file has been created and saved successfully!')
            logging.info('Your file has been created and saved successfully!')
        else:
            messages.error(request, 'Something went wrong!')
            logging.info('Something went wrong!')

        return render(
            request,
            self.template_home,
            {'files': files}
        )


class DetailView(TemplateView):
    '''
        Details for one csv file
    '''
    template_detail = 'detail.html'

    def get(self, request, pk):

        csv_file = DatasetCSV.objects.get(pk=pk)
        # load data from current csv
        data = etl.fromcsv(csv_file.path)
        # take headers
        header_keys = etl.header(data)
        # take only 10 rows
        data = etl.data(data, 10)

        return render(
            request,
            self.template_detail,
            {
                'csv_file': csv_file,
                'head': header_keys,
                'table': data,
            }
        )

    def post(self, request, pk):
        # num of rows to load in table
        entries = 0

        # count criteria
        criteria = []

        # get current csv obj from db
        csv_file = DatasetCSV.objects.get(pk=pk)

        # load data from file
        data = etl.fromcsv(csv_file.path)

        # take headers
        header_keys = etl.header(data)

        # collect criteria choice from request
        for title in header_keys:
            if request.POST.get(title):
                criteria.append(title)

        req_data = {
            'csv_file': csv_file,
            'head': header_keys,
            'criteria': criteria
        }

        if request.POST.get('load_entries'):
            # if request contains load_entries - load 10 more rows from data
            entries = int(request.POST.get('load_entries'))
            (data, table_end) = self.__load_additional_entries(data, entries)
            req_data['table_end'] = table_end

        elif criteria:
            data = self.__count_data_by_criteria(data, criteria)

            # counter headers
            count_header = etl.header(data)

            # load rows
            data = etl.data(data)

            req_data['count_header'] = count_header

        else:
            data = etl.data(data, entries + 10)

        req_data['table'] = data

        return render(
            request,
            self.template_detail,
            req_data
        )

    def __load_additional_entries(self, data, entries):
        len_all_data = len(data)
        new_entries = entries + 10
        data = etl.data(data, new_entries)

        return (data, len_all_data <= new_entries)

    def __count_data_by_criteria(self, data, criteria):
        # if counter criteria are chosen
        data = etl.valuecounts(data, *criteria)
        # remove frequency
        data = etl.cutout(data, 'frequency')

        return data
