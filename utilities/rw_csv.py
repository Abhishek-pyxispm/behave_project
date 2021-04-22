import csv


# read csv file as dictionary
def read_csv(testcase_name, key):
    with open('data/API_Test Case 1.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = ""
        for row in csv_reader:
            if testcase_name == row["Test Id"]:
                # print(f'Test ID: {row["Test Id"]}****************')
                data = row[key]
        if data == "":
            raise Exception("testcase name not found or no data present for the selected key.")
    return data


if __name__ == '__main__':
    print(read_csv("po_01"))
