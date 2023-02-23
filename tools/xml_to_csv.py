#import relevant libraries
import xml.dom.minidom
import csv

#initialize dictionaries
dict = {} #dictionary containing data values from xml
index_dict = {} #dictionary mapping values from dict to data tags as per semantic standard (MTConnect) - used to write headers in the CSV output

#recursive method to traverse XML file and retrieve pertinent data values
#Uses xml.dom.minidom to traverse XML document as a node tree
def output(node, num):
	children = node.childNodes #create list of children nodes of node
	if children.length == 0: #if node has no children
		return 1,node.nodeValue #return 1 and the value at the node to indicate node is a leaf node
	for child in children: #if node has children then traverse through all the children
		a, val = output(child, 0) #recursive function to look at each child node
		if val == None: #if  the child node has no value then  skip it
			pass
		elif '\n  ' in str(val): #if the child nodes value is null then skip it
			pass
		elif a == 1: #if the child node is a leaf node then publish the node
			publish(node, str(val))
		else: #any other conditions then skip it
			pass
	return 0,0 #return 0,0 to signifiy that node has allready been traverse and because the node is not a leaf node and

#method to update dictionary with value of specific leaf node
def publish(node, val):
	timestamp = node.getAttribute("timestamp") #retrieve timestamp
	dataItemId = node.getAttribute("dataItemId") #retrieve data tag
	val = val.replace(' ',',') #in cases such as coordinates where entry is two or more values separated by spaces, replace spaces with commas
	#the above is done to deal with issues writing dictionary to csv
	if dataItemId not in index_dict.keys(): #if a new data attribute is found then update index_dict
		index_dict.update({dataItemId:len(index_dict)})
	if timestamp not in dict.keys(): #if a new timestamp is found, then create a entry with the key being the timestamp in dict
		entry = {timestamp: {dataItemId: str(val)}}
		dict.update(entry) #update entry
	else: #if it is an existing timestamp or data attribute then update dict
		if dataItemId not in dict[timestamp].keys():
			entry = {dataItemId: str(val)}
			dict[timestamp].update(entry)
		else:
			pass

doc = xml.dom.minidom.parse("data_ur.xml") #create node tree to represent xml file
x,y = output(doc, 0) #parse through xml tree and populate dictionaries
w = csv.writer(open("output.csv", "w")) #write to csv output
header = ["timestamp"] #header for csv file
for key in index_dict.keys():
	header.append(key)
w.writerow(header) #write header to csv file

for key in dict.keys(): #write values from dict to csv using index_dict to map values to header
	temp_dict = dict[key]
	csv_output = [None]*(len(index_dict)+1)
	csv_output[0] = key
	for nested_key in temp_dict:
		csv_output[index_dict[nested_key]+1] = temp_dict[nested_key]
	w.writerow(csv_output)
