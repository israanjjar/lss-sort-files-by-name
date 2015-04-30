#!usr/bin/python
import sys, os
import re, itertools, difflib, operator

def open_directory(path):
	#open the file and get all the file names
	filelist = [os.path.normcase(f) for f in os.listdir(path)]
	return filelist

def find_length(filelist): 
	# I picked a set to ensure no duplicates in lengthsetVariables occurs
	lengthset = set()
	for filename in filelist:
		lengthset.add(len(filename))
	return lengthset

def split_into_hashes(filelist, lengthset): 
	resulthash = {}
	for le in lengthset:
		#split the files into arrays depeding of thier length
		resulthash[le] = [i for i in filelist if len(i) == le] 
	return resulthash

def get_results(hashes):
	resullist = []
	for key in hashes:
		filelist = hashes[key]
		#load a set at the time, the apply the regex for each set
		resullist.append(regex_filename(filelist))
	return resullist

def group_results(ex_filelist):
	for eachhash in ex_filelist:
		# ex_filelist[key] = [i for i in filelist if len(i) == le] 
		print_results(eachhash)

def print_results(hash_regxed_files):
	#print the results!
	filerange = []
	for key in hash_regxed_files:
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

def regex_filename(filelist):
	numbers =[]
	result = {}
	#copy the array first
	for index, filename in enumerate(filelist):
		length = len(filelist)
		if index < length -1 and len(filelist) > 1:
			#run a regex on filenames, return an array of [number, len, start, end] 
			current_file = regex_filename_results(filename)
			after_file = regex_filename_results(filelist[index+1])

			for ind, regexdnumberlist in enumerate(current_file):
				#replace the file name the c style fprint formatting 
				replaced_current = replace_filename(filelist[index], regexdnumberlist[0], regexdnumberlist[1])
				replaced_after = replace_filename(filelist[index+1], after_file[ind][0], after_file[ind][1])
				
				#if the current element and the one after equal, add current to result
				if replaced_after == replaced_current: 
					if result.has_key(replaced_current) == False: result[replaced_current] = []
					result[replaced_current].append([replaced_current, regexdnumberlist])

					#only for the last element: 
					#if this is the last item, we know already that it's equal lets add it then. 
					if index == length -2: 
						if result.has_key(replaced_after) == False: result[replaced_after] = []
						result[replaced_after].append([replaced_after, after_file[ind]])

		elif len(filelist) == 1: result[filename] = [[filename]]
	return result

def replace_filename(filename, numbers, replacewith):
	cformatreplace = replace_printf(replacewith)
	return filename.replace(str(numbers), cformatreplace)

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
	lengthset = find_length(filelist)
	hashes = split_into_hashes(filelist, lengthset)
	filelist = get_results(hashes)
	group_results(filelist)


#touch files for testing 
# ruby -e '107.upto(122) { |n| %x( touch "sd_fx29.0#{n}.txt" ) }'
# ruby -e '124.upto(147) { |n| %x( touch "sd_fx29.0#{n}.txt" ) }'
# ruby -e '40.upto(43) { |n| %x( touch "file01_00#{n}.rgb" ) }'
# ruby -e '44.upto(47) { |n| %x( touch "file02_00#{n}.rgb" ) }'
# ruby -e '1.upto(4) { |n| %x( touch "file1.03.rgb" ) }'
# touch file.info.03.rgb
# touch alpha.txt

#now run the code, 
run()


