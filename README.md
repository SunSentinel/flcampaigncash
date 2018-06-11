# Florida Campaign Cash

Scrapes and parses campaign finance data from the Florida Secretary of State's website.

## How it works
The Florida Secretary of State's campaign finance portal is somewhat of a nightmare to work with or glean anything meaningful from. This tool aims to make it easier to grab campaign finance data in bulk in a usable, machine-readable format rather than the fixed-width data normally returned when using the state's site. 

The main script grabs results, cleans up the fields and then saves the data as CSV and JSON.

## Installing
#### Requirements
+ Python 3
+ PostgreSQL
+ Some type of virtual environment recommended

Start up your virtual environment and run
`pip install -r requirements.txt`
or
`pipenv install` for pipenv users.


## Usage
Run `python flcampaigncash/main.py`

#### Configuration
By default, this grabs campaign contributions to candidates in the 2018 gubernatorial race. But the variables can be changed in the main script to specify different races or election years. That'll be more of a built out configuration feature eventually.


## License
[MIT]()
