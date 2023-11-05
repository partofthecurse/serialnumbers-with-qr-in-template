python qr-code-generator.py
REM inkscape ./Laser/typenschilder.svg --export-area-drawing --batch-process --export-type=pdf -T --export-filename=./Laser/typenschilder.pdf
"C:\Program Files\Inkscape\bin\inkscapecom.com" ./Laser/typenschilder.svg --export-area-drawing --batch-process --export-type=pdf -T --export-filename=./Laser/typenschilder.pdf
python rename.py
