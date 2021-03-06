#!/usr/bin/env python
# -*- coding:utf-8 -*-

from functools import wraps
import pickle

def push(func):
    @wraps(func)
    def dec(redis, key, objects):
        if not (isinstance(objects, tuple) or isinstance(objects, list)):
            objects = [objects]
        serialization = list()
        for obj in objects:
            serialization.append(pickle.dumps(obj))
        pipe = redis.pipeline()
        func(pipe, key, serialization)
        pipe.execute()
    return dec

# list operation 列表操作
@push
def redis_push(redis, key, objects):
    for obj in objects:
        redis.rpush(key, obj)
    
def redis_pop(redis, key, timeout=10):
    serialization = redis.blpop(key, timeout=timeout)
    if serialization:
        return pickle.loads(serialization[1])

def redis_rpoplpush(redis, r_key, l_key):
    serialization = redis.rpoplpush(r_key, l_key)
    if serialization:
        return pickle.loads(serialization)

# set operation 集合操作
@push
def redis_sadd(redis, key, objects):
    for obj in objects:
        redis.sadd(key, obj)

def redis_srandmember(redis, key):
    serialization = redis.srandmember(key)
    if serialization:
        return pickle.loads(serialization)
