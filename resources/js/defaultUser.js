var db = connect('127.0.0.1:27017/unificaterFlowsDEV');
db.users.deleteMany({});
db.users.insertMany([{
  "userId": 1,
  "name": "ADMIN",
  "password":"Admin123",
  "emailId":"admin@unificater.com",
  "isLocked": false,
  "createdBy": "Admin",
  "createdOn": new Date()
},
{
  "userId": 2,
  "name": "SUNDAR",
  "password":"Sundar123",
  "emailId":"sundararajan@unificater.com",
  "isLocked": false,
  "createdBy": "Admin",
  "createdOn": new Date()
},
{
  "userId": 3,
  "name": "CHANDRU",
  "password":"Chandru123",
  "emailId":"chandrasekaran@unificater.com",
  "isLocked": false,
  "createdBy": "Admin",
  "createdOn": new Date()
},
{
  "userId": 4,
  "name": "PRADEEP",
  "password":"Pradeep123",
  "emailId":"pradeep@unificater.com",
  "isLocked": false,
  "createdBy": "Admin",
  "createdOn": new Date()
},
{
  "userId": 5,
  "name": "LATHISH",
  "password":"Lathish123",
  "emailId":"lathish.kumar@unificater.com",
  "isLocked": false,
  "createdBy": "Admin",
  "createdOn": new Date()
},
{
  "userId": 6,
  "name": "SREENATH",
  "password":"Sreenath123",
  "emailId":"sreenath.reddy@unificater.com",
  "isLocked": false,
  "createdBy": "Admin",
  "createdOn": new Date()
}])

users = db.users.find();

while (users.hasNext()) {
   printjson(users.next());
}