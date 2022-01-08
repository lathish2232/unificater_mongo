#load("defaultUser.js")
pretyPrinter() {
  echo
  echo "##########################################################################################"
  echo $1
  echo "##########################################################################################"
}

pretyPrinter "Pre-Installation step started... at $(date)"
sudo apt install python3-pip -y
sudo apt-get install python3-dev libmysqlclient-dev -y
python3 -m pip install mysql-connector -y
python3 -m pip install django-cors-headers -y
sudo apt-get install libmemcached-dev zlib1g-dev -y

sudo apt install unixodbc-dev -y

pretyPrinter "Inserting dataSource..."
mongo localhost:27017/test js/dataSource.js

pretyPrinter "Inserting outputType..."
mongo localhost:27017/test js/outputType.js

pretyPrinter "Inserting default User..."
mongo localhost:27017/test js/defaultUser.js

pretyPrinter "Pre-Installation step Completed successfully. at $(date)"
