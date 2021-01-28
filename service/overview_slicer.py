import csv
import os


class OverviewSlicer:
    def __init__(self):
        self.__search_file_name()
        self.__read_csv()    # 2017, 2018, 2019, 2020
        self.__delete_file()

    def __search_file_name(self):
        for file in os.listdir():
            if ".csv" in file:
                self.__file_name = file
                break

    def __read_csv(self):
        print("Reading csv with peaks...")
        with open(os.path.join(os.getcwd(), self.__file_name), newline='') as file:
            reader = csv.reader(file)
            date = next(reader)
            peaks = next(reader)
        index = 65
        self.peaks_list = []
        for year in range(2017, 2021):
            peak = 0
            while str(year) in date[index]:
                peak = int(peaks[index]) if int(peaks[index]) > peak else peak
                index += 1
            self.peaks_list.append(peak)
        print("Peaks successfully extracted")

    def __delete_file(self):
        os.remove(os.path.join(os.getcwd(), self.__file_name))
        print("Deleted csv file")



