#!/usr/bin/python
from labelImage import label
from similaritySearch import find_similar

def get_label(file_name):
	label_name = label(file_name)
	similar_images = find_similar(file_name, label_name)
	print(similar_images)
	print("label name in service" + label_name)
	return similar_images, label_name