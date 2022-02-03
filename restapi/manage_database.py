class Database:
    def __init__(self, UserAccount):
        self.UserAccount = UserAccount

    def createSuperUser(self, c_addr, email, password=None):
        print("Creating new superuser '{c_addr}, {email}'..")
        superuser = self.UserAccount.objects.create_superuser(
            c_addr=c_addr,
            email=email,
            password=password
        )
        superuser.save()
        print("Done")

    def createUser(self, c_addr):
        print(f"Creating user '{c_addr}..")
        user = UserAccount.objects.create_user(
            c_addr=c_addr,
            role_id=2,
        )
        user.save()
        print("Done")


from accounts.models import UserAccount


# SuperUser Load. Create a single superuser
def suLoad(c_addr):
    db = Database(UserAccount)
    db.createSuperUser(
        c_addr=c_addr.lower(),
        email="info@metabrainz.io",
        password=None
    )

# User Load. Create a single user
def uLoad(c_addr):
    db = Database(UserAccount)
    db.createUser(c_addr=c_addr.lower())