# Eddy
The marker localization mapper and mask merger of the quantification folder (MCMICRO)


python eddy.py -h

usage: eddy.py [-h] [--decimal_points DECIMAL_POINTS] [--remove REMOVE] directory

Process quantification files to create an eddy object with categorized localizations.

positional arguments: directory Path to the directory containing the CSV files.

options: -h, --help show this help message and exit

--decimal_points DECIMAL_POINTS Number of decimal points to round to (default is 3, maximum is 7).

--remove REMOVE Whether to remove other files in the directory after processing (default is True).
