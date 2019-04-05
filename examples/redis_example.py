import redis
import json
kwargs = dict(
    host='redis-12727.c52.us-east-1-4.ec2.cloud.redislabs.com', #'redis-16382.c2.eu-west-1-3.ec2.cloud.redislabs.com',
    port=12727, #16382,
    password='JtC9UX0rrqWi4pLniiRNeGHCEbGPaAKQ', #'jWIDB8PzhNBze5F8dNoeYsMOT7Po4LeX'
    charset="utf-8",
    decode_responses=True,
)

kwargs = dict(
    host='redis-16382.c2.eu-west-1-3.ec2.cloud.redislabs.com', #'redis-16382.c2.eu-west-1-3.ec2.cloud.redislabs.com',
    port=16382, #16382,
    password='jWIDB8PzhNBze5F8dNoeYsMOT7Po4LeX', #'jWIDB8PzhNBze5F8dNoeYsMOT7Po4LeX'
    charset="utf-8",
    decode_responses=True,
)

r = redis.Redis(**kwargs)
r = redis.StrictRedis(**kwargs)


r.set('aa', 1)
r.get('aa')
latest= r.get('latest')
res = r.get(latest)
json.loads(res)

r.dbsize()
r.flushall()

import walrus
db = walrus.Database(**kwargs)
stream = db.Stream('stream-a')
msgid = stream.add({'message':1})
stream.get(msgid)


)
    {'message': {
    'dfdsf': 'hello streams'
}})

db['walrus'] = {'tusk': 1}
db['not-here']

db.Hash('abc').update(**{
    'asdasd': 1,
})
h = db.Hash('abc')


db.set('dsfdsf', 1)
db.get('dsfdsf')

db['fff'] = 'dgfsdf'
print(db['fff'])

walrus.__version__

db['aaa'] = h

i = db.Hash('abc2', )
i