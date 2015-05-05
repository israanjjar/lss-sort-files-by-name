#!usr/bin/python
import sys
import os
import re
import itertools
import operator


def open_directory(path):
    # 
    """
    open the file from the given path retrun a list of all the files names
    :rtype : list
    """
    file_list = [os.path.normcase(f) for f in os.listdir(path)]
    return file_list


def regex_filename(file_list):
    result = {}
    # copy the array first
    for index, filename in enumerate(file_list):
        if index < len(file_list) - 1:
            # run a regex on file names, return an array of [number, len, start, end]
            current_file = regex_filename_results(filename)
            after_file = regex_filename_results(file_list[index + 1])
            if not current_file:
                result[filename] = [[filename]]
            result = add_replaced(current_file, after_file, index, result, file_list, filename)
    return result


def add_replaced(current_file, after_file, index, result, file_list, filename):
    if len(after_file) > 0 and len(current_file) > 0:
        # print current_file
        for ind, regexd_number_list in enumerate(current_file):
            # replace the file name the c style f print formatting
            replaced_current = replace_filename(file_list[index], regexd_number_list[0], regexd_number_list[1])
            replaced_after = replace_filename(file_list[index + 1], after_file[ind][0], after_file[ind][1])

            # if the current element and the one after equal, add current to result
            if replaced_after == replaced_current:
                result = match(result, replaced_current, replaced_after, regexd_number_list, after_file, ind, file_list,
                               index)
            else:
                result = no_matches(result, index, ind, file_list, replaced_current, regexd_number_list)
                if 1 == len(current_file) and replaced_current not in result:
                    # what if they are == ? Compare it to the one before it.
                    result[filename] = [filename]
    return result


def replace_filename(filename, numbers, replace_with):
    """
    replace the numbers in filename with a c style formatting 
    example: file01_0040.rgb => file01_%04d.rgb 

    :param filename: str File name before formatting 
    :param numbers: str numbers in the string
    :param replace_with: str c style formatting string
    :rtype : str
    """
    cformatreplace = replace_printf(replace_with)
    return filename.replace(str(numbers), cformatreplace)


def no_matches(result, index, ind, file_list, replaced_current, regexdnumberlist):
    """
    replace the numbers in filename with a c style formatting
    example: file01_0040.rgb => file01_%04d.rgb

    :param result: dict File name before formatting
    :param index: int numbers in the string
    :param file_list: list c style formatting string
    :param replaced_current: str c style formatting string
    :param regexdnumberlist: list c style formatting string
    :rtype : dict
    """
    if index - 1 > -1:
        before_file = regex_filename_results(file_list[index - 1])
        if len(before_file) > 0:
            replaced_before = replace_filename(file_list[index - 1], before_file[ind][0], before_file[ind][1])
            if replaced_current == replaced_before:
                result[replaced_current].append([replaced_current, regexdnumberlist])
    assert isinstance(result, dict)
    return result


def match(result, replaced_current, replaced_after, regexdnumberlist, after_file, ind, filelist, index):
    if replaced_current not in result:
        result[replaced_current] = []
    result[replaced_current].append([replaced_current, regexdnumberlist])
    # only for the last element:
    # if this is the last item, we know already that it's equal lets add it then.
    if index == len(filelist) - 2:
        if replaced_after not in result:
            result[replaced_after] = []
        result[replaced_after].append([replaced_after, after_file[ind]])
    return result


def print_results(hash_regxed_files):
    # print the results!
    for key in hash_regxed_files:
        file_range = []
        count = 0
        for each_group in hash_regxed_files[key]:
            if len(each_group) > 1:
                file_range.append(each_group[1][0])
            count += 1
        if count > 1:
            file_range = files_range(file_range)
        else:
            file_range = ""
        # print("%s\t%s%s" % (count, key, file_range))
        print '{0:<2} {1:>35} {2:>30}'.format(count, key, file_range)


def files_range(numbers):
    range_list = ""
    for k, g in itertools.groupby(enumerate(numbers), lambda (i, x): int(i) - int(x)):
        result = map(operator.itemgetter(1), g)
        range_list += ("%s - %s   " % (result[0], result[len(result) - 1]))
    return range_list


def replace_printf(number):
    if number > 2:
        return "%0" + str(number) + "d"
    else:
        return "%d"


def regex_filename_results(filename):
    # let's get all the numbers
    """

    :rtype : list
    """
    result = []
    for m in re.finditer(r"\d+", filename):
        number_length = m.end() - m.start()
        result.append([m.group(0), number_length, m.start(), m.end()])
    return result


def run():
    # Where all the magic happens
    if len(sys.argv) > 1:
        file_path = str(sys.argv[1])
    else:
        file_path = './'
    file_list = open_directory(file_path)
    result = regex_filename(file_list)
    print_results(result)


# now run the code,
run()


