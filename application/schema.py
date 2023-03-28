import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Person, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
session = Session()


class PersonObject(SQLAlchemyObjectType):
    class Meta:
        model = Person
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="World"))
    person = graphene.Field(PersonObject, id=graphene.Int(required=True))

    def resolve_hello(self, info, name):
        return f'Hello {name}!'

    def resolve_person(self, info, id):
        # base64 encoded globally unique id instead of Person.id
        return session.query(Person).filter_by(id=id).first()


schema = graphene.Schema(query=Query, types=[PersonObject])
