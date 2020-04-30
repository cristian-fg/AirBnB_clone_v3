#!/usr/bin/python3
""" Test link
"""
from models.owner import Owner
from models.pet import Pet
from models import storage

# creation of a Owner
owner1 = Owner(first_name="owner1", last_name="test1")
owner1.save()
owner2 = Owner(first_name="owner2", last_name="test2")
owner2.save()

# creation of a Pet
pet1 = Pet(owner_id=owner1.id, name="firu1", age=2, color="black")
pet1.save()

pet2 = Pet(owner_id=owner1.id, name="firu2", age=3, color="white")
pet2.save()

pet1 = Pet(owner_id=owner2.id, name="dog1", age=2, color="black")
pet1.save()

pet2 = Pet(owner_id=owner2.id, name="cat2", age=3, color="white")
pet2.save()


storage.save()

print("OK")
