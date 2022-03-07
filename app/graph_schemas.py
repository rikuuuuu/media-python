import graphene

from . import models

# class UserGrapheneInputModel(PydanticInputObjectType):
#     class Meta:
#         model = schemas.UserBase
# exclude_fields = ('id', 'posts', 'comments')

# class UserGrapheneModel(PydanticObjectType):
#     class Meta:
#         model = schemas.UserBase

# GraphQl
class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return "Hello " + name


class CreateUser(graphene.Mutation):
    # class Arguments:
    #     user = schemas.UserCreate

    # Output = schemas.User

    # @staticmethod
    def mutate(parent, info, db, user):
        # user = User()
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = models.User(
            email=user.email,
            hashed_password=fake_hashed_password,
            name="",
            refresh_token="",
        )
        # user.email = user_details.name
        # user.address = user_details.address
        # user.phone_number = user_details.phone_number
        # user.sex = user_details.sex
        # user.save()
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
