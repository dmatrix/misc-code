import uuid
from faker import Faker
from faker.providers import internet, BaseProvider


class UUIDProvider(BaseProvider):

    def uid(self):
        return uuid.uuid1()


if __name__ == '__main__':

    fake = Faker()
    fake.add_provider(internet)
    fake.add_provider(UUIDProvider)
    for _ in range(5):
        fmt = "{}|{}|{}|{}|{}"
        print(fmt.format(fake.uid(), fake.name(), fake.address(), fake.ssn(), fake.ipv4_private()))
        print(fake.simple_profile())
