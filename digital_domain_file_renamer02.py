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
	hash_regxed_files = flaten_to_hash(ex_filelist)
	print_results(hash_regxed_files, ex_filelist[1])

def print_results(hash_regxed_files, numbers):
	for key in hash_regxed_files:
		count = len(hash_regxed_files[key][1])
		if count == 0:
			count = 1
		file_range = hash_regxed_files[key][1]
		if count >1:
			file_range = files_range(file_range)
		else:
			file_range = ""
		print("%s  %s                  %s" % (count, key, file_range))

def files_range(numbers):
	rangelist = ""
	for k, g in itertools.groupby(enumerate(numbers), lambda (i,x):int(i)-int(x)):
		result = map(operator.itemgetter(1), g)
		rangelist += ("%s - %s   " % (result[0], result[len(result)-1]) )
	return rangelist

def flaten_to_hash(lists):
	#flaten lists
	hash_regxed_files = {}
	flatlist = lists[:] 
	flatlist = flatlist
	for thelist in flatlist:
		exset = set(thelist[0])
		for key in exset:
			hash_regxed_files[key] = [[item for item in flatlist if item == key], thelist[1]]
	return hash_regxed_files


def regex_filename(filelist):
	numbers =[]
	#copy the array first
	copy_array = filelist[:] 
	for index, filename in enumerate(copy_array):
		length = len(copy_array)
		if index < length -1 and len(copy_array) > 1:
			current_file = regex_filename_results(filename)
			after_file = regex_filename_results(copy_array[index+1])
			
			for ind, regexdnumberlist in enumerate(current_file):
				replaced_current = copy_array[index].replace(str(regexdnumberlist[0]), replace_printf(regexdnumberlist[1]))
				replaced_before = copy_array[index+1].replace(str(after_file[ind][0]), replace_printf(after_file[ind][1]))
				
				if replaced_before == replaced_current: 
					filelist[index] = replaced_current
					numbers.append(regexdnumberlist[0])
					if index == length -2:
						filelist[index+1] = replaced_current

	return [filelist, numbers]


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

def customize_index(index, length):
	if index > 0:
		return index -1 
	elif index == 0 and length > 1:
		return index +1 

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


