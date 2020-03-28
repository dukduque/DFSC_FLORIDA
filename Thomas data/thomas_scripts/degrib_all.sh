# This shell script degribs all the grb files in the given directory

# INPUTS:
# 	$1 -> $dgpath - full path to your degrib program (example: "/c/ndfd/degrib/bin/degrib.exe")
# 	$2 -> $pts - full path to pntFile (example: "/c/ndfd/pntsFL.txt" with format: label,lat,lon)
# 	$3 -> $grbpath - full path to the directory for the .grb files (example: "/c/ndfd/degrib/data/grbfilesB/")
# OUTPUTS:
#	$grbpath/out - a directory with a "degribbed" txt file for each grb file that was in the given directory

# function call example: /.degrib_all.sh "/c/ndfd/degrib/bin/degrib.exe" "/c/ndfd/pntsFL.txt" "/c/ndfd/degrib/data/grbfilesB/"

dgpath=$1
pts=$2
grbpath="$3"
outputpath="$4"

# check to see if grb output directory already exists
if [ -e "$grbpath""grbout" ]; then
	exists=true
fi
# make an output directory if it doesn't already
mkdir -p "$grbpath""grbout"

# degrib each file in the directory and return the output in "grbout"
for folder in `ls $grbpath`; do

	for entry in `ls "$grbpath""$folder"`; do
		# degrib the file
	    $dgpath "$grbpath""$folder/$entry" -P -pntFile $pts >> "$outputpath""grbout/$entry.txt" 
	done
done
