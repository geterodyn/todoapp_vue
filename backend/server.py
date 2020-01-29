import bottle
import q
from truckpad.bottle.cors import CorsPlugin, enable_cors

app = bottle.Bottle()

class TodoItem:
    def __init__(self, description, unique_id):
        self.description = description
        self.priority = 2
        self.is_completed = False
        self.uid = unique_id

    def __str__(self):
        return self.description.lower()

    def to_dict(self):
        return {
            'description': self.description,
            'priority': self.priority,
            'is_completed': self.is_completed,
            'uid': self.uid
        }

tasks_db = {
    uid: TodoItem(desc, uid)
    for uid, desc in enumerate(
        start=1,
        iterable=[
            'test_1','test_2','test_3','test_4'
        ],
    )
}

@enable_cors
@app.route('/api/tasks/', method=['GET', 'POST'])
def add_task():
    if bottle.request.method == 'GET':
        tasks = [task.to_dict() for task in tasks_db.values()]
        return {'tasks': tasks}
    elif bottle.request.method == 'POST':
        desc = bottle.request.json['description']
        priority = bottle.request.json['priority']
        is_completed = 'is_completed' in bottle.request.json
        if len(desc) > 0:
            if len(tasks_db):
                max_uid = max(tasks_db.keys())
            else:
                max_uid = 0
            new_uid = max_uid + 1
            t = TodoItem(desc, new_uid)
            t.is_completed = is_completed
            t.priority = priority
            tasks_db[new_uid] = t
        return 'OK'

@enable_cors
@app.route('/api/tasks/<uid:int>', method=['GET', 'PUT', 'DELETE'])
def show_or_modify_task(uid):
    if bottle.request.method == 'GET':
        return tasks_db[uid].to_dict()
    elif bottle.request.method == 'PUT':
        if 'description' in bottle.request.json:
            tasks_db[uid].description = bottle.request.json['description']
        if 'priority' in bottle.request.json:
            tasks_db[uid].priority = bottle.request.json['priority']
        tasks_db[uid].is_completed = 'is_completed' in bottle.request.json
        # q.d()
        return f"Modified task {uid}"
    elif bottle.request.method == 'DELETE':
        tasks_db.pop(uid)
        return f"Deleted task {uid}"

app.install(CorsPlugin(origins=['http://127.0.0.1:5000']))
bottle.run(app, host='127.0.0.1', port=5000)