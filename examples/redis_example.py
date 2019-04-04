import redis
kwargs = dict(
    host='redis-16382.c2.eu-west-1-3.ec2.cloud.redislabs.com', # 'redis-15365.c2.eu-west-1-3.ec2.cloud.redislabs.com',
    port=16382,
    password='jWIDB8PzhNBze5F8dNoeYsMOT7Po4LeX'
)

r = redis.Redis(**kwargs)


r.set('aa', 1)
res = r.get('aa')
res


import walrus
db = walrus.Database(**kwargs)
stream = db.Stream('stream-a')
msgid = stream.add({'message': 'hello streams'})

db['walrus'] = 'tusk'
db['not-here']