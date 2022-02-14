# WM393 Assessment 2 - Creating the resource board  

## About The Project  
The WMG Teaching Support system (WMGTSS) has been developed for a post-pandemic environment as the pandemic highlighted inadequacies in the previous system.  
This repository contains the software solution to create a resource board based upon the requirements set out in part 3.  
The code is written using python, html, css and SQL.  

## Built With:  
* Python 3.7.6  
* Flask 2.0.2  
* Werkzeug 2.0.2  
* BootStrap 4.5.2  
* os  
* datetime  
* sys  
* sqlite3  

## Usage  
This application is designed to be used to:  
* Register a user  
* Login as that user  
* Add a new resource  
* Edit the information about the uploaded resource  
* Add a comment (as a student)  
* Reply to a comment (as a tutor)  
* Set priority level and module of comment  
* Filter all resources by module  

## Getting Started  
1. Source Code can be downloaded from the Tabula submission or cloned from the Version Control Repository:  https://github.com/u1914181/WM393_U1914181.git  
2. Save the flaskr folder inside another folder called 'resource_board_code'  
3. Run this project folder ('resource_board_code') in the local IDE (e.g. Visual Studio Code)  
4. Add an instance folder inside 'resource_board_code' if not already present.  
5. Initialise the database by typing: `flask init-db` in the terminal.  
6. Run the following commands in the terminal:  
* `set FLASK_APP=flaskr`  
* `set FLASK_ENV=development`  
* `flask run`  
7. This will start a development server containing the address for the server which is: http://127.0.0.1:5000/  

## How to use the web application  
1. Press register in the top right corner.  
2. Login as the admin user by inputting:  
* Username: admin  
* Password: adminpassword  
3. Add yourself as a user by registering. The username and password can be chosen by you. To set the user role enter either: `Student` or  `Tutor`. Steps 4-9 are for a tutor view.  
4. Log in with the username and password that you registered previously.  
5. Navigate to top right of screen and press 'New' button to upload a resource. The resources that can be uploaded are in the /uploads folder. Please fill in all fields shown on the screen.  
6. Once pressing upload, you will be directed back to the resource board where you will see the resource that you uploaded.  
7. Add more resources by pressing the 'New' button again.  
8. Filter resources using the module dropdown in the right top corner. Edit and delete uploads by pressing edit.  
9. Logout using the logout button.  
10. Click register again and register a student.  
11. Login using these student username and password.  
12. Student view means the student can see the uploaded resources and add comments.  
13. Click add comment.  
14. Add a comment and fill in all the fields on the screen.  
15. Download a resource by clicking the filename that is shown in white on the resource board.  
16. Log in again as the tutor to reply to the comment.  

### Prerequisites:  
* All libraries previously listed are installed on your machine - use 'pip' install to install libraries as required.  
* Project must be run on a windows machine.  
* Machine must have internet connection.  


### Installation  
1.  Clone the repository on to local machine using:  
`git clone https://github.com/u1914181/WM393_U1914181.git`  
2. Launch Project Folder and Run in local IDE (e.g. Microsoft Visual Studio Code)  

## GIT  
To download the latest release of this source code please visit:  
https://github.com/u1914181/WM393_U1914181.git
 