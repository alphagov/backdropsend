[![Build Status](https://travis-ci.org/alphagov/backdrop-send.png)](https://travis-ci.org/alphagov/backdrop-send)

backdrop-send
=============

CLI tool for sending data to Backdrop

## Example

`backdrop-send --url http://location/of/backdrop/bucket --token TOPSECRET123456 myfile.json`

or

`cat myfile.json | backdrop-send --url http://location/of/backdrop/bucket --token TOPSECRET123456`
