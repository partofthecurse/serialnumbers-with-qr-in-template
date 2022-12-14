#!/usr/bin/env python
# coding: utf8

################################################################################
# Programm zum Einsetzen von Seriennummern in ein Template.
# Autor: Daniel Strohbach
# Datum: 02.12.2021
# Infos:
# 1. Das Script wird mit durch die KLICK-ME.bat ausgeführt
# 2. Es werden eine Datei mit "template.svg" und "Seriennummern.csv" erwartet.
################################################################################

# import libs
import csv
from ensurepip import version
from pickle import TRUE
import qrcode
import qrcode.image.svg
import re

# instances
templateFile = "template.svg"
inputCSV = "Seriennummern.csv"

Serial = "%SERIAL%"
QRCode = "%QR%"

SVGNS = {"svg":"http://www.w3.org/2000/svg"}

qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=5
)

# read csv file with serial numbers
with open(inputCSV) as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)

    f = open(templateFile,'r')
    filedata = f.read()
    f.close()

    f = open("Laser/typenschilder.svg",'w')
    f.write(filedata)
    f.close()

    n=0

    #get element tree from template file
    from lxml import etree
    tree = etree.parse(templateFile)
    root = tree.getroot()
    # print("root: ")
    # print(root)
    # print()

    #find placeholder elements    
    placeholder = tree.xpath('//*[local-name()="svg"]//*[local-name()="rect"]/@id', namespaces=SVGNS)
    print("Placeholder List: " + str(placeholder))

    #find placeholder size
    placeholder_width = tree.xpath('//*[local-name()="svg"]//*[local-name()="rect"]/@width', namespaces=SVGNS)
    placeholder_height = tree.xpath('//*[local-name()="svg"]//*[local-name()="rect"]/@height', namespaces=SVGNS) 
    print("Width List: " + str(placeholder_width))
    print("Height List: " + str(placeholder_height)) 
    
  # do stuff for each row from csv
    for row in reader:
        #parse newly saved file with data to replace
        tree = etree.parse("Laser/typenschilder.svg")
        root = tree.getroot()

        # where are we?
        Serial = "%SERIAL" + str(n) + "%"
        print("Current ROW in CSV: " + str(n))
        print("Current Serial Placeholder: " + Serial)

        #which qr code?
        QRCode = "%QR" + str(n) + "%"
        print("Current QR Code: " + str(n))
        print("Current QR Code Placeholder: " + QRCode)

        #build serial from csv
        SerialString = row[0]+"-"+row[1]+"-"+row[2]+"-"+row[3]
        print("Serial-Number from CSV: "+ row[0]+ "-" + row[1] + "-" + row[2] + "-" + row[3])

        # print for checking
        print("SerialString-Check: "+ SerialString)
        print()

        #make qr code and save 
        qr.clear() 
        qr.add_data(SerialString)
        #qr.add_data('www.heavn-lights.com')
        qr.make(fit=True)

        #qr_img = qrcode.make(SerialString, image_factory=qrcode.image.svg.SvgImage)
        qr_img = qr.make_image(image_factory=qrcode.image.svg.SvgImage)
        qr_img.save("test/qr" + str(n) + ".svg") 

        #parse saved qr image
        qrtree = etree.parse("test/qr" + str(n) + ".svg")
        # print("QR Tree: ")
        # etree.indent(qrtree)
        # print(etree.tostring(qrtree, pretty_print=True))
        # print()

        #get qr code from img
        QRC = qrtree.xpath('//*[local-name()="svg"]//*[local-name()="rect"]', namespaces=SVGNS)
        QR_Element = etree.Element('g')
        #etree.indent(QR_Element)

        # print("QRC " + str(n) + ": ")
        # #print(etree.tostring(QRC, pretty_print=True))
        # print(QRC)
        # print() 
        
        i=0
        for element in tree.xpath('//*[attribute::id]', namespaces=SVGNS):
            # print("Position " + str(n) +": ")
            # print("Element " + str(i) + ": ")
            # print(element)
            # print("with ID: " + element.attrib['id']) 
            # print()
            # print("looking for: " + placeholder[n])
            # print()

            i = i + 1
            if element.attrib['id'] == placeholder[n]:

                #get size of qr code
                qr_height = qrtree.xpath('//*[local-name()="svg"]/@height', namespaces=SVGNS)[0]
                qr_width = qrtree.xpath('//*[local-name()="svg"]/@width', namespaces=SVGNS)[0]
                # print("QR Code Height: ")
                # print(qr_height)
                # print("QR Code Width: ")
                # print(qr_width)
                # print()

                #get placeholder size
                placeholder_height=element.attrib['height']
                placeholder_width=element.attrib['width']
                #placeholder_height = tree.xpath('//*[local-name()="svg"]//*[local-name()="rect"]/@width', namespaces=SVGNS)[0]
                #placeholder_width = tree.xpath('//*[local-name()="svg"]//*[local-name()="rect"]/@height', namespaces=SVGNS)[0]
                # print("Placeholder Height: ")
                # print(placeholder_height)
                # print("Placeholder Width: ")
                # print(placeholder_width)
                # print()

                #values might have units, we need to cut off
                qr_height = [float(re.sub("[^0-9.\-]","",qr_height))]
                qr_width = [float(re.sub("[^0-9.\-]","",qr_width))]
                
                # print("QR Height after Transform: ")
                # print(qr_height)
                # print("QR Width after Transform: ")
                # print(qr_width)
                # print()

                placeholder_height = [float(re.sub("[^0-9.\-]","",placeholder_height))]
                placeholder_width = [float(re.sub("[^0-9.\-]","",placeholder_width))]
                # print("Placeholder Height after Transform: ")
                # print(placeholder_height)
                # print("Placeholder Width after Transform: ")
                # print(placeholder_width)
                # print()

                #make sure its a square
                assert(placeholder_height == placeholder_width)
                assert(qr_height == qr_width)

                #calculate offset 
                offset = (placeholder_height[0] - qr_height[0]*0.865) / 2
                # print("Offset: " + str(offset))
                # print()

                #Add it to QR Code
                #qrtree.xpath('//*[local-name()="svg"]', namespaces=SVGNS)[0].attrib['transform'] = 'translate({0},{0})'.format(offset)

                #find placeholder coordinates and modify with offset value
                placeholder_y = float(element.attrib['y']) - offset
                placeholder_x = float(element.attrib['x']) - offset
                print("Placeholder Y-Koordinate: " + str(placeholder_y))
                print("Placeholder X-Koordinate: " + str(placeholder_x))

                #qrtree.xpath('//*[local-name()="svg"]', namespaces=SVGNS)[0].attrib['x'] = '{0}'.format(placeholder_x)
                #qrtree.xpath('//*[local-name()="svg"]', namespaces=SVGNS)[0].attrib['y'] = '{0}'.format(placeholder_y)

                #add Group element and attributes
                element.addnext(QR_Element)
                QR_Element.attrib['width'] = str(placeholder_width[0])
                QR_Element.attrib['height'] = str(placeholder_height[0])
                QR_Element.attrib['id'] = 'insertedQR' + str(n)
                QR_Element.attrib['transform'] = 'matrix(0.62,0,0,0.62,{0},{1})'.format(placeholder_x, placeholder_y)         

                #add the qr code rectangle by rectangle to group (maybe not elegant, but it works)
                for rectangle in QRC:
                   QR_Element.append(rectangle)

                #remove placeholder
                parent=element.getparent()
                print("found parent with ID: " + parent.attrib['id'])
                print()
                parent.remove(element)
                print("removed element: " + element.attrib['id'])
                print()
                
   
        # open file to replace serial numbers in plain text
        f = open("Laser/typenschilder.svg",'r')
        filedata = f.read()
        f.close()

        # replace file data with modified tree data
        newqrdata = etree.tostring( tree, pretty_print=True, xml_declaration=True, encoding='UTF-8', standalone="yes").decode()

        #replace string placeholders
        newdata = newqrdata.replace(Serial, SerialString)     
                 
        # write and save - file will be opened again on next loop
        f = open("Laser/typenschilder.svg",'w')
        f.write(newdata)
        f.close()

        n = n + 1  

          

