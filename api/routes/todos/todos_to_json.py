from api.extensions import ma
from api.models import Todo
from pkg.query_params.select import split_select


class TodoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todo
        include_fk = True


def todo_json(table, is_many, field_list):
    
    no_class_context = ()
    unnecessary_class_context = ()
    field_list = split_select(field_list, Todo, no_class_context, unnecessary_class_context)

    schema = TodoSchema(many=is_many, only=field_list)
 
    return schema.dump(table)