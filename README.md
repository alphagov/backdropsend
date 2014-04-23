[![Build Status](https://travis-ci.org/alphagov/backdropsend.png)](https://travis-ci.org/alphagov/backdropsend)

backdropsend
=============

CLI tool for sending data to Backdrop

## Install

`pip install https://github.com/alphagov/backdropsend/tarball/0.0.1`

## Example

`backdrop-send --url https://location/of/backdrop/data_set --token TOPSECRET123456 myfile.json`

or

`cat myfile.json | backdrop-send --url https://location/of/backdrop/data_set --token TOPSECRET123456`
