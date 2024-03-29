from fastapi_study.models.todo import ToDo as ToDoModel
from fastapi_study.schemas.todo import ToDoCreate as ToDoCreateSchema
from fastapi_study.schemas.todo import ToDoUpdate as ToDoUpdateSchema


from sqlalchemy import select
from sqlalchemy.orm import Session


def get_all_todos(db: Session) -> list[ToDoModel]:
    """
    모든 ToDo를 조회합니다.
    
    Parameters
    ----------
    db : Session
        DB 세션
        
    Returns
    -------
    list[ToDoModel]
        모든 ToDo
    """
    
    stmt = select(ToDoModel)
    return db.scalars(stmt).all()


def create_new_todo(
    new_todo: ToDoCreateSchema,
    db: Session
) -> ToDoModel:
    """
    새로운 ToDo를 생성합니다.
    
    Parameters
    ----------
    new_todo : ToDoCreate
        새로운 ToDo
    db : Session
        DB 세션
        
    Returns
    -------
    ToDoModel
        새로 생성된 ToDo
    """
    todo = ToDoModel(**new_todo.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def update_todo(
    todo_id: int,
    update_todo_data: ToDoUpdateSchema,
    db: Session
) -> ToDoModel:
    """
    기존의 ToDo를 수정합니다.
    
    Parameters
    ----------
    todo_id : int
        수정할 ToDo의 ID
    update_todo_data : ToDoUpdate
        수정할 ToDo
    db : Session
        DB 세션
        
    Returns
    -------
    ToDoModel
        수정된 ToDo
    """
    
    get_exist_todo_query = select(ToDoModel).where(ToDoModel.id == todo_id)
    
    # 수정할 ToDo가 존재하는지 확인
    todo = db.scalar(get_exist_todo_query)
    if todo is None:
        raise ValueError(f"Todo {todo_id} is not exists")
    
    # 수정할 내용을 반영
    for key, value in update_todo_data.model_dump(exclude_unset=True).items():
        setattr(todo, key, value)
    
    db.commit()
    db.refresh(todo)
    return todo