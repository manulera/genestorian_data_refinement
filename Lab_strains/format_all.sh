for lab in *_lab
do
	cd $lab
	if test -f "format.py"; then
    	echo "running in $lab"
		python format.py
	fi
	cd ..
done