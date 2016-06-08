# playweka
Gathers application permissions data from the Google Play Store and formats it for analysis by Weka.

```
playweka.py
Copyright (C) 2015 Thomas Valadez (@tvldz)
License: MIT
Requires: googleplay-api (https://github.com/egirault/googleplay-api)

This script searches the Google Play Store with a given query,
enumerates all of the "ANDROID." permissions for each app, and 
creates an ARFF file for Weka machine learning applications. It
also prints out an index, correlating each application with the 
integer the app is represented by within the file output.

Usage:
python playweka.py <search term>
```
