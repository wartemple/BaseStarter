from django.http import HttpResponse
from io import BytesIO
import pandas as pd
import openpyxl


class ViewUtils:
    @classmethod
    def get_excel_response(cls, data, file_name):
        file_ = BytesIO()
        writer = pd.ExcelWriter(file_, engine="xlsxwriter")
        df = pd.DataFrame(data)
        df.to_excel(writer, index=False)
        writer.save()
        writer.close()
        file_.seek(0)
        response = HttpResponse(file_.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f'attachment; filename={file_name}.xlsx'
        return response

    @classmethod
    def read_excel(cls, file_, fields):
        workbook = openpyxl.load_workbook(file_)
        worksheet = workbook.active
        results = []
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            results.append({field: value for field, value in zip(fields, row)})
        return results
