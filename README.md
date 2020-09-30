# Account Creation Page
This repository is not very polished. Like many of my repos this one requires Python 3.7 and Python flask installed. It reads a configuration file `config.json` where you should populate your Okta org url and an API key made by a super administrator. 

## Important things to note
* If running it you need to navigate to the `/register` endpoint to actually begin registration
* This application sets a generic value for firstName and lastName in Okta. These are required attributes and you will have to add this to the page if you want to create a user with a custom first/last name.
* The root route `/` doesn't do anything but post "Hej!"
* Users will be activated and able to login to Okta after account creation.
