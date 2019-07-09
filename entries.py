import datetime
import calendar
import os
import sys


def write_loop():
    year = str(datetime.datetime.now().year)
    month = datetime.datetime.now().month
    month_name = str(calendar.month_name[month]).lower()
    dirname = 'entries/'+year + "/" + str(month) + '_(' + month_name + ')'

    create_directory('entries')
    create_directory('entries/'+year)
    create_directory(dirname)

    try:
        filename = dirname+'/entry-' + datetime.datetime.now().date().isoformat()
        entry_file = open(filename, 'a')
    except:
        print('could not open journal.')
        exit

    print("(press enter twice to close journal)")
    while (True):
        user_input = input("~ ")
        if (user_input != ""):
            store_input(entry_file, user_input)
        else:
            break
    os.system("CLS")
    entry_file.close()
    print('(closed journal)')


def create_directory(name):
    if (not os.path.isdir(name)):
        try:
            os.mkdir(name)
            print('created a folder for '+name)
        except:
            print('failed to create folder for ' + name)
            exit


def store_input(entry_file, user_input):
    entry_file.write('['+datetime.datetime.now().time().isoformat().replace(
        ":", "-").replace(".", "-") + '] ' + user_input + '\n')


def read_loop():
    while (True):
        input_string = input("which entries would you like to read? ")
        if (input_string == ""):
            os.system("CLS")
            print("closed journal")
            break
        default_year = datetime.datetime.now().year
        include_years = list(
            filter(lambda i: (str(i) in input_string.split(' ') and i != default_year),
                   range(40, 3000)))
        if (len(include_years) < 1):
            include_years.append(default_year)
        include_days = list(
            filter(lambda i: (str(i) in input_string.split(' ')), range(1, 32)))
        include_months = list(filter(lambda x: (input_string.lower().find(
            calendar.month_abbr[x].lower()) != -1), range(1, 13)))
        none_found = True
        for year in include_years:
            for month in include_months:
                if (include_days == []):
                    include_days = range(1, calendar.monthrange(year,month)[1]+1)
                for day in include_days:
                    formatted_date = datetime.datetime(
                        year, month, day).date().isoformat()
                    path = f'entries/{year}/{month}_({calendar.month_name[month].lower()})/entry-{formatted_date}'
                    if (os.path.isfile(path)):
                        print(f'-- entry-{formatted_date} --')
                        f = open(path, 'r')
                        print(f.read())
                        f.close()
                        none_found = False
        if none_found:
            print("no entries found")


def main():
    if (len(sys.argv) < 2 or sys.argv[1] == 'w'):
        write_loop()
    else:
        read_loop()


# Run the program
if __name__ == "__main__":
    main()
