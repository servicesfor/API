from redis import Redis

rd = Redis(host='localhost',
           port=6375, db=1)

if __name__ == '__main__':
    print(rd.keys("*"))
    rd.flushall()