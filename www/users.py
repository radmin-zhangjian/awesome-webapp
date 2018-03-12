import orm,asyncio
from models import User,Blog,Comment

# @asyncio.coroutine
async def test(loop):
    # yield from orm.create_pool(host='127.0.0.1',port=3306,user='root', password='', db='awesome',loop=loop)
    await orm.create_pool(user='www-data', password='www-data', db='awesome',loop=loop)
    u = User(name='小鱼儿',email='test3@test.com',passwd='test',image='about:blank')
    await u.save()
    await orm.destroy_pool() #销毁连接池

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()


#创建 mysql 用户 
#grant select, insert, update, delete on awesome.* to 'www-data'@'localhost' identified by 'www-data';
#flush privileages;



