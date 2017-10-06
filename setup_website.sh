#!/bin/bash
# lolbot setup script
# Setup the website with just a simple script run.
# (c) 2017 S Stewart
# MIT License.
space() {
	echo ""
}
if [ "$1" = "--help" ]; then
	echo "lolbot web setup script v1.0"
	echo "(c) 2017 S Stewart, MIT License"
	echo "Arguments:"
	echo "    --help    Shows this help message"
	exit 0
else
	echo "Welcome!"
	echo "This script downloads CSS and JS files"
	echo "not included with the website."
	echo "Starting in a second."
	sleep 1
	cd site
	mkdir css > /dev/null 2>&1
	if [ "$?" -eq 1 ]; then
		echo "CSS folder already exists, skipping"
	else
		echo "CSS folder created"
	fi
	mkdir js > /dev/null 2>&1
	if [ "$?" -eq 1 ]; then
		echo "JS folder already exists, skipping"
	else
		echo "JS folder created"
	fi
	space
	echo "| Downloading CSS files |"
	space
	echo "Downloading uikit.min.css"
	wget -O css/uikit.css "https://cdn.jsdelivr.net/npm/uikit@3.0.0-beta.30/dist/css/uikit.min.css" > /dev/null 2>&1
	if [ "$?" -eq 1 ]; then
	    echo "| CSS download error. |"
	else
	    echo "| CSS download finished. |"
	fi
	space
	echo "| Downloading JS files |"
	echo "Downloading uikit.min.js"
	wget -O js/uikit.js "https://cdn.jsdelivr.net/npm/uikit@3.0.0-beta.30/dist/js/uikit.min.js" > /dev/null 2>&1
	if [ "$?" -eq 1 ]; then
	    echo "| UIKit JS download error. |"
	else
	    echo "| UIKit JS download finished. |"
	fi
	echo "Downloading uikit-icons.min.js"
	wget -O js/uikit-icons.js "https://cdn.jsdelivr.net/npm/uikit@3.0.0-beta.30/dist/js/uikit-icons.min.js" > /dev/null 2>&1
	if [ "$?" -eq 1 ]; then
	    echo "| Icons download error. |"
	else
	    echo "| Icons download finished. |"
	fi
	echo "Downloading jquery.min.js"
	wget -O js/jquery.js "https://cdn.jsdelivr.net/npm/jquery@3.2.1/dist/jquery.min.js" > /dev/null 2>&1
	if [ "$?" -eq 1 ]; then
	    echo "| JQuery download error. |"
	else
	    echo "| JQuery download finished. |"
	fi
fi
