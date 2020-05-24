from mongoengine import *
from datetime import datetime
import hashlib

import types


def count_hash(obj) -> str:
    data = str(obj.number) + str(obj.name) + str(obj.amount) + str(obj.to_whom) \
           + str(obj.date) + str(obj.prev_hash)
    return hashlib.sha512(data.encode('UTF-8')).hexdigest()


class Block(Document):
    number = IntField()
    name = StringField(required=True, max_length=150)
    amount = IntField(required=True)
    to_whom = StringField(required=True, max_length=150)
    date = DateTimeField(default=datetime.now())
    prev_hash = StringField()

    def __init__(self, *args, **kwargs):
        super(Block, self).__init__(*args, **kwargs)

        if not self.number:
            self.number = Block.objects.all().count() + 1
        if not self.prev_hash:
            self.prev_hash = count_hash(Block.objects.get(number=self.number - 1))

    def check_integrity(self) -> str:
        try:
            prev_obj = Block.objects.get(number=self.number - 1)
            data = str(prev_obj.number) + str(prev_obj.name) + str(prev_obj.amount) + str(prev_obj.to_whom) \
                   + str(prev_obj.date) + str(prev_obj.prev_hash)
            if hashlib.sha512(data.encode('UTF-8')).hexdigest() == self.prev_hash:
                return '    Block {} is OK'.format(prev_obj.number)
            else:
                return '    Block {} is CORRUPTED'.format(prev_obj.number)
        except Exception:
            return 'GenesisBlock'

