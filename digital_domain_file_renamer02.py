#!usr/bin/python
import sys, os
import re, itertools, difflib, operator


def open_directory(path):
	#open the file and get all the file names
	filelist = [os.path.normcase(f) for f in os.listdir(path)]
	return filelist


def regex_filename(filelist):
	# print filelist
	result = {}
	#copy the array first
	for index, filename in enumerate(filelist):
		if index < len(filelist) -1 :
			#run a regex on filenames, return an array of [number, len, start, end] 
			current_file = regex_filename_results(filename)
			after_file = regex_filename_results(filelist[index+1])
			if current_file == []: result[filename] = [[filename]]
			result = add_replaced(current_file, after_file, index, result, filelist, filename)
	return result


def add_replaced(current_file, after_file, index, result, filelist, filename):
	if len(after_file) > 0 and len(current_file) > 0:
		# print current_file
		for ind, regexdnumberlist in enumerate(current_file):
				#replace the file name the c style fprint formatting 
			replaced_current = replace_filename(filelist[index], regexdnumberlist[0], regexdnumberlist[1])
			replaced_after = replace_filename(filelist[index+1], after_file[ind][0], after_file[ind][1])
			
			#if the current element and the one after equal, add current to result
			if replaced_after == replaced_current: 
				result = match(result, replaced_current, replaced_after, regexdnumberlist, after_file, ind, filelist, index)
			else: 
				result = no_matches(result, index, ind, filelist, replaced_current, regexdnumberlist)
				if len(current_file) == 1 and not (result.has_key(replaced_current)) : result[filename] = [filename]
			#what if they are == ? Compare it to the one before it. 
	return result


def replace_filename(filename, numbers, replacewith):
	cformatreplace = replace_printf(replacewith)
	return filename.replace(str(numbers), cformatreplace)


def no_matches(result, index, ind, filelist, replaced_current, regexdnumberlist):
	if index-1 > -1: 
		before_file = regex_filename_results(filelist[index-1])
		if len(before_file) >0: 
			replaced_before = replace_filename(filelist[index-1], before_file[ind][0], before_file[ind][1])
			if replaced_current == replaced_before: result[replaced_current].append([replaced_current, regexdnumberlist])
	return result


def match(result, replaced_current, replaced_after, regexdnumberlist, after_file, ind, filelist, index):
	if not result.has_key(replaced_current): result[replaced_current] = []
	result[replaced_current].append([replaced_current, regexdnumberlist])
	#only for the last element: 
	#if this is the last item, we know already that it's equal lets add it then. 
	if index == len(filelist) -2: 
		if not result.has_key(replaced_after): result[replaced_after] = []
		result[replaced_after].append([replaced_after, after_file[ind]])
	return result


def print_results(hash_regxed_files):
	#print the results!
	for key in hash_regxed_files:
		filerange = []
		count = 0 
		for eachgroup in hash_regxed_files[key]:
			if len(eachgroup) >1: filerange.append(eachgroup[1][0])
			count = count + 1 
		if count >1:
			file_range = files_range(filerange)
		else:
			file_range = ""
		print("%s  %s                  %s" % (count, key, file_range))


def files_range(numbers):
	rangelist = ""
	for k, g in itertools.groupby(enumerate(numbers), lambda (i,x):int(i)-int(x)):
		result = map(operator.itemgetter(1), g)
		rangelist += ("%s - %s   " % (result[0], result[len(result)-1]) )
	return rangelist


def replace_printf(number): 
	if number > 2:
		return "%0"+str(number)+"d"
	else:
		return "%d"


def regex_filename_results(filename):
	#let's get all the numbers
	result =[]
	for m in re.finditer(r"\d+", filename):
		numberlength = m.end() - m.start()
		result.append([m.group(0), numberlength, m.start(), m.end()])
	return result


def run():
	#Where all the magic happens
	if len(sys.argv) > 1 :
		filepath = str(sys.argv[1])
	else :
		filepath = './'
	filelist = open_directory(filepath)
	result = regex_filename(filelist)
	print_results(result)


#now run the code, 
run()


