## PieOrg 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
### A python CLI app to organise every story you read on the internet!

### Get started:
This app has some components that conflict with some conda keywords. Therefore, it is necessary to use a virtual environment to install and use this app.

* **Now to get started, first create a folder on your system where you want the database to be created for storing your stories. You will be coming back here whenever you want to add another story to the database, edit a story or search for one.**
  - Make a new virtual environment - 
  
  ```
  pipenv shell
  ```
  
  - Then, install PieOrg simply by running,
  
  ```
  pip install pieorg
  ```

### Features:
* Insert a story with the following options:
  - Title
  - Author
  - Link(url)
  - Category/Folder to create
  - 2 different genres
  - Fandom ( if it's a fanfiction, enter the fandom, otherwise enter misc)
  - The type of story (a novel or a short story)
  - A Love meter for the story (on a scale of 1 to 5, 5 being the most loved story)
  - If the story is complete 

* View your stories from the database with the following options:
  - View all stories
  - View stories which are complete
  - View stories which belong to a particular category/folder
  - View stories which are written by a particular author
  - View stories of a particular genre
  - View all categories/folders you have
  - View stories with a specific minimum love metre
  - View stories of a particular type(novel or short story)
  - View stories of a genre and love metre
  - View stories of a description/keyword (upon search)
 
* Edit a story in the database:
  - Edit the description of an existing story
  - Edit the status(complete or not) of an existing story
 
 
 ### Using Pieorg
 Just go into your virtual env and run:
 ```
 pieorg
 ```
 
 1. Insertion Operation:
 **Some crucial things to note**:
 - If the name of the fandom is for example, Peaky Blinders, then type the fandom as *PB*
 - When inserting the url of the story, insert the url from *www.wattpad.com/something* and don't include *https://* in the url as it interferes with database functions. 
 - See the following example to get a hang of it:
 
 ![Insertion](https://github.com/yashprakash13/PieOrg/blob/master/screen/i.png)
 
 2. Edit Operation:
 
 ![Edit](https://github.com/yashprakash13/PieOrg/blob/master/screen/e.png)
 
 3. Display/Search operations:
 
 ![Search](https://github.com/yashprakash13/PieOrg/blob/master/screen/d.png)
 
 
 #### A big Thank you to:
 * [Click](https://pypi.org/project/click8/)
 * [Art](https://pypi.org/project/art/)
