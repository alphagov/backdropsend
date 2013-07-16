[![Build Status](https://travis-ci.org/alphagov/backdropsend.png)](https://travis-ci.org/alphagov/backdropsend)

backdropsend
=============

CLI tool for sending data to Backdrop

## Example

`backdrop-send --url http://location/of/backdrop/bucket --token TOPSECRET123456 myfile.json`

or

`cat myfile.json | backdrop-send --url http://location/of/backdrop/bucket --token TOPSECRET123456`
