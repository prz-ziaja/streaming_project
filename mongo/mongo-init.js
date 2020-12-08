print('Starting configuration')
db = db.getSiblingDB('api_dev_db')
db.createUser(
    {
        user: 'api_user',
        pwd: 'pass',
        roles: [{role: 'readWrite',db:'api_dev_db'}]
    }
)