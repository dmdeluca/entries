import datetime
import calendar
import os
import sys
import string


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


helpful_tips = '\n--TIPS-- try "--has keyword keyword2" or "july 8" or "jul --has dog"\n'


def date_to_path(year, month, day):
    return f'entries/{year}/{month}_({calendar.month_name[month].lower()})/entry-{datetime.datetime(year, month, day).date().isoformat()}'


def read_loop():
    while (True):
        input_string = input("which entries would you like to read? ")
        if (input_string == ""):
            os.system("CLS")
            print("closed journal")
            break
        arguments = input_string.split(' ')
        default_year = datetime.datetime.now().year

        if ("--h" in arguments):
            print(helpful_tips)
            continue

        # Because the only years we care about are from 2000 to 2100, and even that is generous.
        include_years = list(filter(lambda i: (str(i) in arguments and i != default_year),
                                    range(2000, 2100)))

        # Months in the calendar API are 1-indexed.
        include_months = list(filter(lambda x: (input_string.lower().find(
            calendar.month_abbr[x].lower()) != -1), range(1, 13)))
        include_days = list(
            filter(lambda i: (str(i) in arguments), range(1, 32)))

        # By default we include the current year because it just makes sense.
        if (len(include_years) < 1):
            include_years.append(default_year)
        if (include_months == []):
            include_months = [datetime.datetime.now().month]
        include_words = []
        entries_to_print = []
        if ("--has" in arguments):
            include_words = arguments[arguments.index("--has")+1:]
            print(f'looking for entries containing:', *include_words)
        none_found = True
        for year in include_years:
            for month in include_months:
                if (include_days == []):
                    include_days = range(
                        1, calendar.monthrange(year, month)[1]+1)
                for day in include_days:
                    formatted_date = datetime.datetime(
                        year, month, day).date().isoformat()
                    path = date_to_path(year, month, day)
                    if (os.path.isfile(path)):
                        f = open(path, 'r')
                        all_entries = f.read()
                        f.close()
                        # In this scenario we have no search terms.
                        if (include_words == []):
                            print(f'-- entry-{formatted_date} --')
                            print(all_entries)
                            none_found = False
                        # In this scenario we're looking for stuff.
                        else:
                            entries_containing_words = list(filter(lambda x: hits(
                                x, include_words) != 0, all_entries.split('\n')))
                            if (entries_containing_words != []):
                                additions = list(map(lambda x: f'<{year}-{calendar.month_abbr[month].lower()}-{day}>' +
                                                     x + f' ({hits(x,include_words)})', entries_containing_words))
                                entries_to_print += additions
                                none_found = False
        if none_found:
            print("no entries found. (type --h for help.)")
        elif (include_words != []):
            print('-- entries containing {', *include_words, '} --')
            print(*entries_to_print, sep='\n')


def hits(string_to_search, search_terms):
    hits = 0
    list_to_search = string_to_search.translate(
        str.maketrans('', '', string.punctuation)).lower().split(' ')
    for term in search_terms:
        hits += list_to_search.count(term.lower())
    return hits


def main():
    if (len(sys.argv) < 2 or sys.argv[1] == 'w'):
        write_loop()
    else:
        read_loop()


# Run the program
if __name__ == "__main__":
    main()
