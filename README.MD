# Django_Test

This Directory django project that contains the following apps:
- django_test
- rental_reservation


### Launching the django project

To quickly launch the web app you can create a virtual environment using:
```shell
python3 -m venv <virtual_env_name>
```
After creating a virtualenv. You will need to install the necessary libraries to run the app. To do so simply activate 
your new virtual environment by typing On Mac or Linux:
```shell
source <virtual_env_name>/bin/activate
```
and On Windows: 
```shell
 .\<virtual_env_name>\scripts\activate
```
Once your virtual environment is running your can go ahead and install the requirements using 
```shell
 pip install -r requirements.txt
``` 
With that done you can now launch the api by running:
```shell
 python manage.py runserver --host 0.0.0.0
```

You can make GET request to the url http://localhost:<Desired_Port>/reservation/reservations
 





