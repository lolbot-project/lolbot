# lolbot setup script
# Setup the website with just a simple script run.
# (c) 2017 S Stewart
# MIT License.
space() {
	echo ""
	echo ""
}
if [ $1 == "--help" ]; then
	echo "lolbot web setup script v1.0"
	echo "(c) 2017 S Stewart, MIT License"
	echo "Arguments:"
	echo "--full    Download unminified CSS and JS (unrecommended)"
	exit 0
else
	echo "Welcome!"
	echo "This script downloads CSS and JS files"
	echo "not included with the website."
	echo "Starting in a second."
	sleep 1
	cd site
	mkdir css
	mkdir js
	space
	echo "-------------------------"
	echo "| Downloading CSS files |"
	echo "-------------------------"
	space
	if [ $1 == "--full" ]; then
		echo "Downloading uikit.css"
		wget -O css/uikit.css "https://cdn.jsdelivr.net/npm/uikit@3.0.0-beta.30/dist/css/uikit.css"
	else
		echo "Downloading uikit.min.css"
		wget -O css/uikit.css "https://cdn.jsdelivr.net/npm/uikit@3.0.0-beta.30/dist/css/uikit.min.css"
	fi
	echo "-------------------------"
	echo "| CSS download finished |"
	echo "-------------------------"
	space
	echo "------------------------"
	echo "| Downloading JS files |"
	echo "------------------------"
	if [ $1 == "--full" ]; then
		echo "Downloading uikit.js"
		wget -O js/uikit.js "https://cdn.jsdelivr.net/npm/uikit@3.0.0-beta.30/dist/js/uikit.js"
	else
		echo "Downloading uikit.min.js"
		wget -O js/uikit.js "https://cdn.jsdelivr.net/npm/uikit@3.0.0-beta.30/dist/js/uikit.min.js"
	fi
	echo "------------------------"
	echo "| JS download finished |"
	echo "------------------------"
fi
