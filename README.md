# Nursery Management -  3 in 1 business solution

It's a 3 in 1 complete business management tool for nursery owners, <br>
1. A complete E-commerce website for owners to list their nursery products and sell them. <br>
2. A tool to provide statistical analysis on nursery profit and employee performance. <br>
3. A one stop shop to manage all the employees working in the nursery, plants sown, inventory available, etc..

## Setup:
Please Use UBUNTU/MAC and not windows if you want your life to be any good.
### create a virtual environment in the base folder
`python3 -m venv venv`

### activate the virtual environment
`source venv/bin/activate`

### Install the requirements
`pip3 install -r requirements.txt`

### Link to database, create a new database on your mysql from the root user
#### Log on to mysql as root user, 
`mysql -u root -p`
<br/>
write you password, then create database:
<br/>
`create database nursery_management;`

### Grant priveleges to user(idk if you made the user or not but figure it out userself you have dbms afterall)
#### my username is noisymime so for me:
`GRANT ALL PRIVILEGES ON nursery_management.* TO 'noisymime'@'localhost';`

## Congo on making it till here, now let's set up flask, create a file secret.py in the base directory
`touch secret.py`
### Now inside the file, add the username and password of your mysql user, we do this so we don't have to share the password on github.
e.g: the 2 lines could be
<br/>
`name = 'YOUR USER NAME'`
<br/>
`password = 'YOUR PASSWORD'`

### Now let's run the APP, WOHOO!!
`python3 run.py`

### Now open any browser and go to [0.0.0.0:8080/](0.0.0.0:8080/)
