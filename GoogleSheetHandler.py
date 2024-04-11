from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gspread

class GoogleSheetHandler:
    def __init__(self, credentials_file='credentials.json'):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.credentials_file = credentials_file
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, self.scope)
        self.gc = gspread.authorize(self.credentials)

    def get_sheet_data(self, spreadsheet_name, worksheet_index=0):
        spreadsheet = self.gc.open(spreadsheet_name)
        worksheet = spreadsheet.get_worksheet(worksheet_index)
        data = worksheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        return df

    def overwrite_sheet_with_data(self, dataframe, spreadsheet_name, worksheet_index=0):
        spreadsheet = self.gc.open(spreadsheet_name)
        worksheet = spreadsheet.get_worksheet(worksheet_index)
        data = dataframe.values.tolist()
        worksheet.clear()
        worksheet.append_row(dataframe.columns.tolist())
        worksheet.append_rows(data)
