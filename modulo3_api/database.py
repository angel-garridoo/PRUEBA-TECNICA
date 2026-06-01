tasks_db: dict = {}
current_id: int = 0


def get_next_id() -> int:

    global current_id
    current_id += 1
    return current_id

def get_all_tasks() -> list:

    return list(tasks_db.values())

def get_task_by_id(task_id: int) -> dict | None:

    return tasks_db.get(task_id)

def create_task(titulo: str, descripcion: str, estado: str) -> dict:

    task_id = get_next_id()
    task = {
        "id": task_id,
        "titulo": titulo,
        "descripcion": descripcion,
        "estado": estado,
    }

    tasks_db[task_id] = task
    return task

def update_task(task_id: int, estado: str) -> dict | None:

    task = tasks_db.get(task_id)
    if task is None:
        return None

    task["estado"] = estado
    return task

def delete_task(task_id: int) -> bool:

    if task_id in tasks_db:
        del tasks_db[task_id]
        return True
    return False