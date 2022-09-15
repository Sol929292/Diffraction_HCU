import csv
import re

filepath = "ugiecia.csv"

class Diffraction:
    def __init__(self):
        self.M = 0
        self.l = 0
        self.type = 0
        self.name = []

    def get_moment(self):
        t = True
        while t == True:
            moment = input("Podaj moment zginajacy: M [kNm] = \t")
            if re.search(",", moment):
                t = False
                self.M = float(re.sub(",", ".", moment))
                return self.M


            elif moment.isdigit() == False:
                print("Podaj wartosc momentu w prawidlowy sposob: (134.6)")
            elif float(moment) <= 0:
                print("Podaj wartosc wieksza od zera.")
            else:
                t = False
                self.M = float(moment)
                return self.M

    def get_length(self):
        t = True
        while t == True:
            length = input("Podaj dlugosc plyty: l [m] = \t")
            if re.search(",", length):
                t = False
                self.l = float(re.sub(",", ".", length))
                return self.l
            elif length.isdigit() == False:
                print("Podaj dlugosc w prawidlowy sposob: (12.64)")
            elif float(length) <= 0:
                print("Podaj wartosc wieksza od zera.")
            else:
                t = False
                self.l = float(length)
                return self.l

    def welcome_and_get_type(self):
        print("UGIECIA PLYT HCU")
        print("Dla jakich plyt sprawdzic ugiecie:\n")
        print("\t1. REI60\n" +
              "\t2. REI60 >13m\n" +
              "\t3. REI120\n" +
              "\t4. REI120 >13m\n")
        case=0
        t = True
        while t == True:
            numer = input("Wybierz numer od 1 do 4:\t")
            if numer.isdigit() == False:
                print("Podaj prawidlowy numer")
            elif numer.isdigit() == True:
                case = int(numer)
                if case in [1, 2, 3, 4]:
                    t = False
                else:
                    print("Podaj prawidlowy numer")
        self.type = case

    def slab_type(self):
        if self.type ==1:
            x = r"REI60$"
        elif self.type ==2:
            x = r"REI60 >13m"
        elif self.type == 3:
            x = r"REI120$"
        elif self.type == 4:
            x = r"REI120 >13m"
        return x

    def calculate_diffraction(self):
        results = []
        data = get_data(filepath)

        for row in data:
            if re.search(self.slab_type(), row[0]):
                name, E1, E2, g, I, P, z = get_parameters_from_row(row)
                a = diffraction_formula(self.M, self.l, E1, E2, g, I, P, z)
                results.append(a)
                self.name.append(name)
        return results

    def analize_results(self):
        results = self.calculate_diffraction()
        l_dop = (round(self.l * 1000, 1) / 250)
        print(f"M={self.M} kNm, l={self.l}m, {self.slab_type()}\n")
        for i in range(len(results)):
            u = results[i]
            if u <= l_dop:
                print(f"OK - {self.name[i]} - a/a_dop = {u}/{l_dop}[mm] - ({int((u / l_dop) * 100)}%) - OK")
            elif u <= 1.35*l_dop:
                print(f"ZLE - {self.name[i]} - a/a_dop = {u}/{l_dop}[mm] - ({int((u / l_dop) * 100)}%) - ZLE")
            else:
                pass
        if results[0] >= 1.35*l_dop: print("Zadna plyta nie spelnia wymagan.\n")

        print(f"\nWyniki dla: M={self.M} kNm, l={self.l}m, {self.slab_type()}")
        print("Opracowano na podstawie dokumentacji: maj 2020.\n")


def get_data(file_path):
    rows = []

    # reading csv file
    with open(file_path, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)

        # extracting field names through first row
        fields = next(csvreader)

        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)

    data = rows[:]
    data.reverse()
    return data


def diffraction_formula(M, l, E1, E2, g, I, P, z):

    a = (
            (5.0 / 48) * (M * (10 ** 3) * (l ** 2)) / (E2 * (10 ** 9) * I * (10 ** (-8)))
            + (1.0 / 64) * (g * (10 ** 3) * (l ** 4)) / (E1 * (10 ** 9) * I * (10 ** (-8)))
            - (1.0 / 8) * (0.9 * P * (10 ** 3) * z * (10 ** (-2)) * (l ** 2)) / (E1 * (10 ** 9) * I * (10 ** (-8)))
    )
    w=round(a*1000,1)
    return w


def get_parameters_from_row(row):
    name = row[0]
    E1 = float(row[1])
    E2 = float(row[2])
    g = float(row[3])
    I = float(row[4])
    P = float(row[5])
    z = float(row[6])
    return [name, E1, E2, g, I, P, z]





