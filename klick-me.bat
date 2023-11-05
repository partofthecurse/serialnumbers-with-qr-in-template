python qr-code-generator.py
REM inkscape ./Laser/typenschilder.svg --export-area-drawing --batch-process --export-type=pdf -T --export-filename=./Laser/typenschilder.pdf
"C:\Program Files\Inkscape\bin\inkscapecom.com" invoice-temp.svg --export-area-drawing --batch-process --export-type=pdf -T --export-filename=./invoice/invoice-temp.pdf
python rename.py
