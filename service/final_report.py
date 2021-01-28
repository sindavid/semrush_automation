import csv


class FinalReport:
    def __init__(self):
        self.__create_header()

    def __create_header(self):
        with open('DOMAIN-report.xlsx', 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['', 'ref domains', 2020, 2019, 2018, 2017, 'anchor1', 'anchor2', 'anchor3', 'Google cache'])

    def new_line(self, domain, ref_domain, peak_2020, peak_2019, peak_2018, peak_2017, anchor1, anchor2, anchor3):
        with open('DOMAIN-report.xlsx', "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([domain, ref_domain, peak_2020, peak_2019, peak_2018, peak_2017, anchor1, anchor2, anchor3, 'No', 'Fail'])
