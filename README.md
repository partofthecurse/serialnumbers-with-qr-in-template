# serialnumbers-with-qr-in-template
python script to put serial numbers from a csv into a template and create qr codes to scan this number

the Serialnumber can consist of 4 blocks - for example product family, product number, production unit, date or something
the serial number is inside a .csv file
the python script takes the columns - puts them together and replaces the placeholder in the template file.
it is creating a qr code and replacing a placeholder box with it
the offset calculation for positioning is not correct, but for me it was ok at this point.

the batch file is just starting the python scripts.
the rename script is opening the template again and renames it to the last serial number, so if you need to do this again, files do not get lost.
