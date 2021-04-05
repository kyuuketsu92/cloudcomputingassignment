# cloudcomputingassignment
This is an assignment work for cloud computing application that has to incorporate databases, REST API and optionally user authentication and load balancing. We are no professionals and the website in this repository might not be secure enough. After submission, this project is not going to be updated.

Plase note that this repo is a school project and not a proper production server. Never share real information on this website as the key file is included in the repository!!!

Group: 21
Members: 
	Fuad Ahmed Mohamedhaji - ex20506
	Gabor Bozser - ex20034


The task was to create a system that generated a dynamically generated REST API what uses CRUD operations over a cloud MYSQL database. The API provided by us should also make use of an external third party REST API.

We created a website that allows for adding, modifying and removing reminders both over the browser GUI and command line interface.
On the website and the API we made use of two exernal APIs, one being a weather forecast API which takes geographical coordinates in, and returns a 5-day weather forecast, and the other being getting the coordinates through the ip address with the help of ip-api.com

In order to be able to use the CLI api for the website, one has to register. After registration the new user will be generated a new authorisation key. If the user is freshly registered, for added compexity we ask a few personal information from the user as well as a display "nickname" that will be used to welcome the user in the header. 

The dashboard is the logged in index page where the user will see the reminders that are in the future still as well as the 5 day weather forecast. Here the user have links to add new entries as well as modify entries.

To use the CLI API, first the user have to note the personal authorisation key. The tab where one can access to the personal key there are documentations on how to use the CLI. Most of these API calls are designed in a way, that a GET request if that's not the only possible method returns a short example on how to use the command. 

The user can: 
 - Access all of the entries that's tied to the authorisation key. This is a GET operation and returns:
	- Date, Description, enrty id
 - Create new entry. This is a POST operation that also has the GET method for examples.
 - Modify an entry. This is a POST operation that also has the GET method for examples.
 - Deleting an entry. This is a DELETE operation that also have the GET method for examples.
 - Getting the weather forecast as a JSON table. This is a simple get operation and can be tested in the browser.
 
Website was developed on Python3.6. Please make sure when running flask it uses python3. For further information please refer to how to run locally text file.
