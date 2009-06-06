
import hashlib

def concat(strs):
    return ''.join(sorted(['='.join(x) for x in strs]))

def dict_concat(d):
    return concat([(k, v) for k, v in d.items() if k != 'signature'])

def gen_signature(d, secret):
    return hashlib.md5(dict_concat(d) + secret).hexdigest()

def check_signature(d, secret):
    return d['signature'] == gen_signature(d, secret)