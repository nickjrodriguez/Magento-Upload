import sys
import csv
import pyinputplus as pyip
from datetime import datetime
import pandas


fieldnames = ["sku","store_view_code","attribute_set_code","product_type","categories","product_websites","name","description","short_description","weight","product_online","tax_class_name", 
			  "visibility","price","special_price","special_price_from_date","special_price_to_date","url_key","meta_title","meta_keywords","meta_description","base_image","base_image_label",
			  "small_image","small_image_label","thumbnail_image","thumbnail_image_label","swatch_image","swatch_image_label","created_at","updated_at","new_from_date","new_to_date",
			  "display_product_options_in","map_price","msrp_price","map_enabled","gift_message_available","custom_design","custom_design_from","custom_design_to","custom_layout_update",
			  "page_layout","product_options_container","msrp_display_actual_price_type","country_of_manufacture","additional_attributes","qty","out_of_stock_qty","use_config_min_qty",
			  "is_qty_decimal","allow_backorders","use_config_backorders","min_cart_qty","use_config_min_sale_qty","max_cart_qty","use_config_max_sale_qty","is_in_stock","notify_on_stock_below",
			  "use_config_notify_stock_qty","manage_stock","use_config_manage_stock","use_config_qty_increments","qty_increments","use_config_enable_qty_inc","enable_qty_increments","is_decimal_divided",
			  "website_id","related_skus","related_position","crosssell_skus","crosssell_position",	"upsell_skus","upsell_position","additional_images","additional_image_labels","hide_from_product_page",
			  "custom_options","bundle_price_type","bundle_sku_type","bundle_price_view","bundle_weight_type","bundle_values","bundle_shipment_type","configurable_variations","configurable_variation_labels",
			  "associated_skus"]

row = { "sku": "","store_view_code" : "","attribute_set_code" : "","product_type" : "simple",
		"categories" : "","product_websites" : "base","name" : "","description" : "","short_description" : "",
		"weight" : .2,"product_online": 1,"tax_class_name": "Taxable Goods", "visibility" : "Catalog, Search",
		"price": 0,"special_price": "","special_price_from_date": "","special_price_to_date": "",
		"url_key": "","meta_title": "","meta_keywords": "","meta_description": "","base_image":"","base_image_label":"",
		"small_image":"","small_image_label":"","thumbnail_image":"","thumbnail_image_label":"","swatch_image":"",
		"swatch_image_label":"","created_at":"","updated_at":"","new_from_date":"","new_to_date":"",
		"display_product_options_in":"Block after Info Column","map_price":"","msrp_price":"","map_enabled":"",
		"gift_message_available":"Use config","custom_design":"","custom_design_from":"","custom_design_to":"",
		"custom_layout_update":"","page_layout":"","product_options_container":"","msrp_display_actual_price_type":"",
		"country_of_manufacture":"","additional_attributes":"","qty":0,"out_of_stock_qty":0,"use_config_min_qty":1,
		"is_qty_decimal":0,"allow_backorders":0,"use_config_backorders":1,"min_cart_qty":1,"use_config_min_sale_qty":1,
		"max_cart_qty":10000,"use_config_max_sale_qty":1,"is_in_stock":1,"notify_on_stock_below":1,
		"use_config_notify_stock_qty":1,"manage_stock":0,"use_config_manage_stock":0,"use_config_qty_increments":1,
		"qty_increments":1,"use_config_enable_qty_inc":1,"enable_qty_increments":0,"is_decimal_divided":0,
		"website_id":0,"related_skus":"","related_position":"","crosssell_skus":"","crosssell_position":"","upsell_skus":"",
		"upsell_position":"","additional_images":"","additional_image_labels":"","hide_from_product_page":"",
		"custom_options":"","bundle_price_type":"","bundle_sku_type":"","bundle_price_view":"","bundle_weight_type":"",
		"bundle_values":"","bundle_shipment_type":"","configurable_variations":"","configurable_variation_labels":"",
		"associated_skus":""}

### Variables ###
attr_master = pandas.read_csv("attribute_master.csv")

attribute_set = {"switch" : ["manufacturer","mfg_no","upc","action","actuator_type","contact_form","illumination","illumination_color", 
							 "illumination_voltage", "lamp_type", "mounting_hole", "switch_current_rating", "switch_voltage_rating", 
							 "termination_style", "type"]
				}
sub_category = {"switch" : ["Toggle", "Specialty", "Snap Action", "Rocker", "Push Button", "Auto-Marine"]}
category = {"switch" : "Default Category/Parts/Electronic Components/Switches/"}
descriptions = {"switch" : ""}
names = {"switch" : ["manufacturer","mfg_no"]}
short_descs = {"switch" : ["type", "action", "switch_current_rating","switch_voltage_rating","contact_form"]}
tags = {"<p>":"</p>", "<ul>":"</ul>","<li>":"</li>"}


manufacturers = ['Cole Hersee','Littelfuse','Philmore']
needed_values = ["weight", "price"]

def assemble_category(attr_set):
	curr_cat = category[attr_set]
	if attr_set in sub_category:
		value = pyip.inputMenu(sub_category[attr_set], blank=False, numbered=True)
		curr_cat+=value
	return curr_cat

def gather_attributes(attr_set, mfr, mfg_no):
	attrs = {}
	for attr in attribute_set[attr_set]:
		print("\n*** %s ***\n" % attr)
		if attr == "manufacturer":
			attrs["manufacturer"] = mfr
		elif attr == "mfg_no":
			attrs["mfg_no"] = mfg_no
		elif attr == "upc":
			prompt = "Enter the %s for item %s:\n" % (attr, curr_sku)
			value = pyip.inputStr(prompt=prompt, blank=True,strip=True)
			if value:
				attrs[attr] = value
			else:
				attrs[attr] = ""
		else:
			prompt = "Enter the %s for item %s:\n" % (attr, curr_sku)
			values = attr_master[attr][0].split(',')
 
			print(values)
			print("\n")
			value = pyip.inputChoice(values, prompt=prompt, blank=True,strip=True)
			if value:
				attrs[attr] = value
			else:
				attrs[attr] = ""
	return attrs

def assemble_attributes(attr_d):
	return ",".join(f'{k}={v}' for k,v in attr_d.items())

def assemble_name(attrs, attr_set):
	name = ""
	for key in names[attr_set]:
		value = attrs[key]
		if value != "":
			name = name + value + " "
	name+=assemble_short_description(attrs, attr_set)
	return name

def assemble_description(attrs, attr_set):
	print("\n*** Assembling Description ***\n")
	base = "<p>Item # %s</p>"
	desc = base + "<p>" + assemble_short_description(attrs, attr_set) + "</p>"
	bullets = ""
	initial_response = 0
	initial_response_string = pyip.inputYesNo("Would you like to add bullet points?\n")
	if initial_response_string == "yes":
		initial_response = 1
	if initial_response:
		bullets += "<ul>"
	response = initial_response
	while response:
		bullets = bullets + "<li>" + pyip.inputStr(prompt="Enter additional description:\n", blank=True) + "</li>"
		response_str = pyip.inputYesNo("Would you like to add another bullet point?\n")
		if response_str == "no":
			response = 0
	if initial_response:
		bullets += "</ul>"

	return desc + bullets
	

def assemble_short_description(attrs, attr_set):
	short_desc = ""
	for key in short_descs[attr_set]:
		value = attrs[key]
		if value != "":
			short_desc = short_desc + value + " "
	return short_desc

def assemble_upsell_skus():
	skus = ""
	initial_response_string = pyip.inputYesNo("Would you like to add upsell skus?\n")
	initial_response = 0
	if initial_response_string == "yes":
		initial_response = 1
	response = initial_response
	while response:
		skus += pyip.inputStr(prompt="Enter upsell sku:\n", blank=True)
		response_str = pyip.inputYesNo("Would you like to add another sku?\n")
		if response_str == "no":
			response = 0
	return skus

def assemble_associated_skus():
	skus = ""
	initial_response_string = pyip.inputYesNo("Would you like to add associated skus?\n")
	initial_response = 0
	if initial_response_string == "yes":
		initial_response = 1
	response = initial_response
	while response:
		skus += pyip.inputStr(prompt="Enter associated sku:\n", blank=True)
		response_str = pyip.inputYesNo("Would you like to add another sku?\n")
		if response_str == "no":
			response = 0
	return skus

def manage_stock(row, sku):
	initial_response_string = pyip.inputYesNo("Would you like to manage_stock?\n")
	if initial_response_string == 'yes':
		row["manage_stock"] = 1
		qty = pyip.inputNum("Enter the Quantity for item: %s\n" % sku)
		row["qty"] = qty
		print("Stock Updated")
	return


def fill_row(row, sku, mfr, mfg_no, category, attr_set, needed_values):
	row["sku"] = sku
	row["attribute_set_code"] = attr_set
	row["categories"] = category
	for value in needed_values:
		prompt = "Enter the %s for item %s:\n" % (value, sku)
		user_input = pyip.inputNum(prompt=prompt, blank=False, greaterThan=0.01, strip=True)
		row[value] = user_input
	image_prompt = "Select image type: "
	print("\n***Entering Attributes for item: %s***\n" % sku)
	attrs = gather_attributes(attr_set, mfr, mfg_no)
	row["additional_attributes"] = assemble_attributes(attrs)
	row["name"] = assemble_name(attrs, attr_set)
	row["description"] = assemble_description(attrs, attr_set)
	print("Select the image extension type you are using: \n")
	image_ext = pyip.inputMenu([".jpg", ".jpeg", ".png",".svg"], numbered=True)
	row["base_image"] = mfg_no + image_ext
	row["thumbnail_image"] = mfg_no + image_ext
	row["swatch_image"] = mfg_no + image_ext
	row["small_image"] = mfg_no + image_ext
	a_skus = assemble_associated_skus()
	u_skus = assemble_upsell_skus()
	row["associated_skus"] = a_skus
	row["upsell_skus"] = u_skus
	manage_stock(row, sku)
	

def is_csv(file):
	try:
		with open(file, newline='') as csvfile:
			start = csvfile.read(4096)
			if not all([c in string.printable or c.isprintable() for c in start]):
				return False
			dialect = csv.Sniffer().sniff(start)
			return True
	except csv.Error:
		print("The file you specified is not in CSV format.\n")
		return False

def process_arguments(args):
	if len(args) >= 2:
		if is_csv(args[1]):
			return pyip.inputYesNo(prompt="Would you like to append to %s?\n" % args[1], yesVal=1, noVal=0)
		return 0
	return 0

### Parse Command Line Arguments ###
append = 0
append = process_arguments(sys.argv)

### Higher Order Values ###
choice = pyip.inputMenu(["switch","fuse"], numbered=True)
mfr = pyip.inputMenu(["Littelfuse","Philmore"], numbered=True)


### Format File ###
datetimeObj = datetime.now()
timestampstr = datetimeObj.strftime("%d-%b_%H-%M-%S")
file = sys.argv[1] if append else "%s" % mfr + choice + timestampstr + ".csv"


open_value = "a" if append else "w+"
with open(file, open_value, newline='') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	if open_value == "w+":
		writer.writeheader()

	curr_category = assemble_category(choice)
	response = 1
	while response:
		curr_row = row.copy()
		curr_sku = pyip.inputStr(prompt="Enter the Sku:\n", blank=False)
		curr_mfg_no = pyip.inputStr(prompt="Enter the Mfr No:\n", blank=False)
		fill_row(curr_row, curr_sku, mfr, curr_mfg_no, curr_category, choice, needed_values)
		writer.writerow(curr_row)
		print("You have added %s to the file.\n" % curr_sku)
		response_from_user = pyip.inputYesNo(prompt="Would you like to continue?\n")
		if response_from_user == 'no':
			response = 0

	print("File saved as: %s " % file)


### Improvements ###
# have a spreadsheet with all the existing attributes

