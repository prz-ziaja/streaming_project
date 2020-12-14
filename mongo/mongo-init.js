print('Starting configuration');
db = new Mongo().getDB("api_dev_db");
db.createUser(
    {
        user: 'api_user',
        pwd: 'raspberry',
        roles: [{role: 'read',db:'api_dev_db'}]
    }
);
db.createUser(
    {
        user: 'backend_user',
        pwd: 'papay',
        roles: [{role: 'readWrite',db:'api_dev_db'}]
    }
);
db.createUser(
    {
        user: 'analyser',
        pwd: 'banana',
        roles: [{role: 'readWrite',db:'api_dev_db'}]
    }
);

db.createCollection( 'photos',
    {
      autoIndexId: true,
      size: 1024,
      capped: true
    }
 );
 db.photos.insert([{'test':1}])