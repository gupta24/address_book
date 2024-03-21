# Readme for setup the app and call the api


***local linux machine setup***

* install the virtual environment and setup inside address_book if not avaiables
```
$ pip3 install virtualenv
$ virtualenv venv
```

* got inside the address_book folder
```
$ cd /<path_name>/<folder_name>
```

* activate the virtual environment inside address_book folder
```
$ source venv/bin/activate
``` 

***install basic app requirements***

* install the requirements
```
$ pip3 install -r requirements.txt
```

***run app***
* run the local machine server
```
$ python3 main.py
```

* Note: user the following address path and call the api on browser after setup the body param then excute.
   API's

   POST :   http://127.0.0.1:8080/docs#/geolocation/create_address

   PUT  :   http://127.0.0.1:8080/docs#/geolocation/update_address/{address_id}

   GET  :   http://127.0.0.1:8080/docs#/geolocation/get_address
   
   DELETE : http://127.0.0.1:8080/docs#/geolocation/delete_address/{address_id}

   POST :   http://127.0.0.1:8080/docs#/geolocation/search_address

   And address_id can be 1 or 2 or 3 or 4 or .... 100