from PIL import Image
import os
import random
from probabilities import PROBABILITIES
import itertools
import config
import argparse

output_image_size = config.OUTPUT_SIZE
layer_image_size = output_image_size

REUSE_BASE = False
background_color = ()
args = ()

# Creates an image
def create_image():
	image = Image.new("RGBA", (output_image_size, output_image_size), background_color)
	return image


# Sets the background color
def set_background_color(color):
	global background_color
	background_color = color
	return 0
	

def	get_feature_variations(feature_type):
	feature_dir = [d for d in sorted(os.listdir(config.LAYERS_BASE_PATH)) if d.endswith(f"{feature_type}")]
	# print(feature_dir)
	feature_variations = [f for f in os.listdir(config.LAYERS_BASE_PATH + feature_dir[0]) if f.endswith(".png")]
	return sorted(feature_variations)


def apply_feature_to_image(image, feature_path, feature_label):
	# Open the image with the feature
	feature_img = Image.open(config.LAYERS_BASE_PATH + feature_label + "/" + feature_path)
	# Take into account the set probability (from the probabilities.py files)
	probability = PROBABILITIES.get(config.LAYERS_BASE_PATH + feature_label + "/" + feature_path, 1)
	if probability == 1:
		probability = PROBABILITIES.get(os.path.basename(feature_path), 1)
		
	if (random.randint(0, 100)/100 <= probability):
		image.paste(feature_img, mask=feature_img)
	feature_img.close()
	return 0


def get_feature_directories():
	directories = sorted([name for name in os.listdir(config.LAYERS_BASE_PATH) if os.path.isdir(os.path.join(config.LAYERS_BASE_PATH, name))])
	return directories


# Get ths layer size
def get_layer_size():
	directories = get_feature_directories()
	list_of_features = []
	for d in directories:
		features = get_feature_variations(d)
		for f in features:
			list_of_features.append(f)
	# print (list_of_features)
	image_size = get_image_size(config.LAYERS_BASE_PATH + directories[0] + "/" + list_of_features[0])
	return min(image_size)


# Gets the image size
def get_image_size(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Get the size of the image
        width, height = img.size
    return width, height

# Generates [count] x random images 
def generate_random_image(count):
	i = 0
	while (i < count):
		filename = ""
		random_image_result = create_image()
		directories = get_feature_directories()
		for dir in directories:
			variations = get_feature_variations(dir)
			random_feature = random.choice(variations)
			apply_feature_to_image(random_image_result, random_feature, dir)
			filename += str.split(os.path.basename(random_feature), ".png")[0]
			if (directories.index(dir) < len(directories) - 1):
				filename += "_"
		random_image_filepath = f"./results/random_{filename}.png"
		random_image_result.save(random_image_filepath, size=100)		
		# image2 = random_image_result.resize(random_image_filepath, random_image_filepath, 1000)
		print(random_image_filepath)
		i += 1


def resize_image(image_path, output_path, size):
    # Open the original image
    with Image.open(image_path) as img:
        # Resize the image
        resized_img = img.resize(size, Image.Resampling.NEAREST)
        # Save the resized image
        resized_img.save(output_path)


def get_name_from_feature_set(features):
	feature_names_without_extensions = []
	for f in features:
		feature_names_without_extensions.append(str.split(f, ".png")[0])
	return (config.RESULTS_BASE_PATH + config.FILENAME_SPLIT_ELEMENT.join(feature_names_without_extensions) + ".png")


def	generate_image_from_feature_set(features, directories, reuse_base = True):
	if reuse_base == True:
		future_name = get_name_from_feature_set(features)
		if get_closest_base_image(future_name):
			starting_image = Image.open(get_closest_base_image(future_name))
		else:
			starting_image = create_image()
	else:
		starting_image = create_image()
	resulting_image_name = ""
	
	for f in features:
		f_path = config.LAYERS_BASE_PATH + directories[features.index(f)] + "/" + f
		apply_feature_to_image(starting_image, feature_path=f, feature_label=directories[features.index(f)])
		resulting_image_name += str.split(f, ".")[0]
		if features.index(f) != len(features) - 1:
			resulting_image_name += config.FILENAME_SPLIT_ELEMENT

		if (features.index(f) < len(features) - 1 and reuse_base):
			base_image_prefix = "base"
		else:
			base_image_prefix = ""

		if (image_exists(config.RESULTS_BASE_PATH + base_image_prefix + resulting_image_name) == False):
			if reuse_base:
				starting_image.save(config.RESULTS_BASE_PATH + base_image_prefix + resulting_image_name + ".png")

	if not reuse_base:
		starting_image.save(config.RESULTS_BASE_PATH + base_image_prefix + resulting_image_name + ".png")
	print(config.RESULTS_BASE_PATH + resulting_image_name + ".png")
	print("-----------------------------------------------------------------------------")
	return 0


# Checks if an image with the given name or image_path exists
def image_exists(image_name=None, image_path=None):
	# print(f"image_exists: {image_path}")
	if not image_name and not image_path:
		return False
	if image_path == None:
		image_path = config.RESULTS_BASE_PATH + image_name
	if (os.path.exists(image_path)):
		# print("IMAGE EXISTS!")
		return True
	# print("IMAGE DOES NOT EXIST!")
	return False


# Returns the number of possible image combinations
def	get_all_possible_image_count():
	directories = get_feature_directories()
	total_images_count = 1
	for dir in directories:
		features_list = list(get_feature_variations(dir))
		total_images_count *= len(features_list)
	return (total_images_count)
	

# Generates all possible combinations of features
def generate_all_possible_images():
	directories = get_feature_directories()
	features = []
	total_images_count = get_all_possible_image_count()

	for dir in directories:
		features_list = list(get_feature_variations(dir))
		features.append(features_list)

	combinations = list(itertools.product(*features))
	i = 1
	for combination in combinations:
		print(f"{i}/{total_images_count}: {combination}")
		generate_image_from_feature_set(combination, directories, reuse_base=REUSE_BASE)
		i += 1
	return total_images_count


# Gets the closest parent image for the image given as the parameter
def get_closest_base_image(filepath):
	while (len(os.path.basename(filepath)) > 4):
		if (image_exists(image_path=filepath)):
			return filepath
		filepath = get_image_parent(filepath)
	return None


def	get_image_parent(filepath, split_element=config.FILENAME_SPLIT_ELEMENT):
	filename = os.path.basename(filepath)
	# print(filename)
	all_filename_parts = str.split(filename, split_element)
	# print(all_filename_parts)
	return (os.path.dirname(filepath) + "/" + split_element.join(all_filename_parts[:len(all_filename_parts) - 1]) + ".png")


def delete_all_files_in_folder(folder_path):
	[os.remove(os.path.join(folder_path, f)) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]


def delete_all_results():
	delete_all_files_in_folder(config.RESULTS_BASE_PATH)
	return 0


def parse_args():
	global args
	global layer_image_size
	global output_image_size

	try:
		layer_image_size = output_image_size
	except Exception as e:
		print(e)
		print("I GUESS YOUR LAYERS FOLDER IS EMPTY? PLEASE CHECK IT...")

	parser = argparse.ArgumentParser(description="A script to generate combined layer PNG files from separate PNG layers.")

	parser.add_argument('-t', '--transparent', action='store_true', help='Output PNG image will have transparent background.')
	parser.add_argument('-w', '--white', action='store_true', help='Output PNG image will have white background.')
	parser.add_argument('-b', '--black', action='store_true', help='Output PNG image will have black background.')
	parser.add_argument('--all', action='store_true', help='Generate all possible combinations.')
	parser.add_argument('-r', '--random', type=int, help='Generate a number of random combinations.')
	parser.add_argument('-s', '--size', type=int, help='Set output image size.')

	# Parse arguments
	args = parser.parse_args()

	# Print arguments (for demonstration purposes)
	if args.black:
		set_background_color(config.BLACK)
	elif args.white:
		set_background_color(config.WHITE)
	else:
		set_background_color(config.TRANSPARENT)
	if args.size:
		output_image_size = args.size
	else:
		output_image_size = config.OUTPUT_SIZE


if __name__ == "__main__":
	parse_args()

	try:
		if args.all:
			print("ESTIMATING THE TOTAL VARIATION COUNT...")
			print(f"Possible variations: {get_all_possible_image_count()}")
			user_response = input("Continue? y/n ")
			if user_response == "y":
				generate_all_possible_images()
	except AttributeError as e:
		print("Seems that you've forgotten the --all flag?")
	try:
		if args.random:
			generate_random_image(args.random)
	except AttributeError as e:
		print("Seems that you've forgotten the --random flag?")
	
	