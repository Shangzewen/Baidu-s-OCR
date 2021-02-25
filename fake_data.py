from faker import Faker
fake2 = Faker('en_US')
for i in range(10):
    print(fake2.address())