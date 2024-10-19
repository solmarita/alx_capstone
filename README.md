# Film Opine

**Film Opine** is a Movie Review and Rating API developed for the **ALX Back-End Web Development Capstone Project**. This project allows users to review and rate movies, providing a platform where they can express their opinions. Users can also read reviews and ratings from others, fostering a community of movie enthusiasts. The project showcases the skills learned throughout the program, focusing on backend development and API design.

## Important Note

This API currently supports only films listed in the IMDB database. Future updates will allow for manual data entry for films not found in the database.

## License

This project is licensed under the MIT License (See the LICENSE file for more information).

## Deployment to Heroku

To deploy the Filmopine API to Heroku, follow these steps:

### Prerequisites

- Ensure you have the Heroku CLI installed.
- Create a Heroku account if you don’t already have one.
- Sign up for an OMDb API key to access movie data.

### Local Setup

1. **Create a `.env` File**  
Create a `.env` file in your project directory with the following contents to work locally:
 
```bash

# Django
SECRET_KEY=<your_secret_key>
DEBUG=<True/False>

# Database
DB_NAME=<db_name>
DB_HOST=localhost
DB_USER=<db_user>
DB_PASSWORD=<db_password>

# OMDb

OMDB_API_KEY=<omdb_api_key>

```

    
2. **Using `Pipfile` to Set Up Locally**  

Make sure you have `pipenv` installed. You can create a virtual environment and install dependencies using:
    
```bash
pipenv install
```
    
To activate your virtual environment:
    
```bash
pipenv shell
```

### Steps to Deploy

1. **Login to Heroku**
```bash
heroku login
```
    
2. **Create a New Heroku App**
 ```bash
heroku create <your-app-name>
```
3. **Set Up MySQL on Heroku**  
 Add a MySQL database to your Heroku app using the following command:
```bash
heroku addons:create jawsdb:kitefin
```
    
For detailed instructions on setting up a MySQL database in Heroku, refer to the [JawsDB MySQL documentation](https://devcenter.heroku.com/articles/jawsdb).
    
4. **Set Environment Variables**  
 Set the environment variables in Heroku using the values from your `.env` file. Run the following commands:
 
 ```bash
heroku config:set SECRET_KEY=<your_secret_key>
heroku config:set DEBUG=<True/False>
heroku config:set DB_NAME=<production db_name>
heroku config:set DB_USER=<production db_user>
heroku config:set DB_PASSWORD=<production db_password>
heroku config:set OMDB_API_KEY=<odb_api_key>
 
 ```
    
5. **Push Your Code to Heroku**
    
```bash
git push heroku main
```
    
6. **Run Migrations** After your code has been deployed, run the following command to apply migrations:
    
```bash
heroku run python filmopine/manage.py migrate
```
    
7. **Open Your App** You can open your app in the browser by running:
    
```bash
heroku open
```
    
8. **Access the API Documentation** The API documentation is accessible at:
    
```bash
https://<your-app-name>.herokuapp.com/swagger/
```
 
 ### Notes
 
 Monitor heroku logs for any errors:
 
 ```bash
 heroku logs --tail
 ```