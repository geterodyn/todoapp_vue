<template>
  <div class="container">
    <div class="col-sm-10">
      <h1>Задачи</h1>
      <confirmation :message="confirmationMessage"
      v-if="showConfirmation">
      </confirmation>
      <button type="button" id="task-add" class="btn btn-success btn-sm align-left d-block"
      v-b-modal.todo-modal>
          Добавить задачу</button>

<b-modal
    ref="addTodoModal"
    id="todo-modal"
    title="Завести задачу"
    hide-footer>
  <b-form @submit="onSubmit" @reset="onReset" class="w-100">
    <b-form-group id="form-description-group"
                label="Описание:"
                label-for="form-description-input">
        <b-form-input id="form-description-input"
                  type="text"
                  v-model="TodoForm.description"
                  required
                  placeholder="Завести задачу">
        </b-form-input>
    </b-form-group>

    <b-form-select v-model="TodoForm.priority" :options="options"></b-form-select>

    <b-form-checkbox
      id="form-checks"
      v-model="TodoForm.is_completed"
      name="form-checks"
      unchecked-value="false"
    >
      Задача выполнена?
    </b-form-checkbox>
    <b-button type="submit" variant="primary">Добавить</b-button>
    <b-button type="reset" variant="danger">Сброс</b-button>
  </b-form>
</b-modal>

<b-modal ref="updateTodoModal"
    id="todo-update-modal"
    title="Update"
    hide-footer>
  <b-form @submit="onUpdateSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-update-desccription-group"
          label="Описание"
          label-for="form-update-description-input">
          <b-form-input id="form-update-description-input"
                type="text"
                v-model="TodoForm.description"
                required>
          </b-form-input>
      </b-form-group>

      <b-form-select v-model="TodoForm.priority" :options="options" required></b-form-select>

      <b-form-group id="form-update-complete-group">
            <b-form-checkbox-group v-model="TodoForm.is_completed" id="form-update-checks">
                <b-form-checkbox
>Задача выполнена?</b-form-checkbox>
            </b-form-checkbox-group>
      </b-form-group>
      <b-button-group>
          <b-button type="submit" variant="primary">Обновить</b-button>
          <b-button type="reset" variant="danger">Сброс</b-button>
      </b-button-group>
  </b-form>
</b-modal>

      <table class="table table-dark table-stripped table-hover">
        <thead class="thead-light">
          <tr>
            <th>Uid</th>
            <th>Приоритет</th>
            <th>Описание</th>
            <th>Выполнена?</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(todo, index) in todos" :key="index">
            <td class="right-align">{{ todo.uid }}</td>
            <td class="center-align">
              <span v-if="todo.priority == 2">Средний</span>
              <span v-else-if="todo.priority == 1">Высокий</span>
              <span v-else-if="todo.priority == 3">Низкий</span>
              <span v-else>Не указано</span>
                </td>
            <td v-bind:class="{completed: todo.is_completed}">{{ todo.description }}</td>
            <td class="center-align">
              <span v-if="todo.is_completed">Выполнено</span>
              <span v-else>Не выполнено</span>
            </td>
            <td>
              <div class="btn-group" role="group">
                <button type="button" class="btn btn-secondary btn-sm"
                v-b-modal.todo-update-modal
                @click="updateTodo(todo)">
                Обновить</button>
                &nbsp;
                <button type="button" class="btn btn-danger btn-sm"
                @click="deleteTodo(todo)">X</button>
              </div>
            </td>
          </tr>
        </tbody>

      </table>
<section v-if="errored">
        <b-alert show variant="danger" class="w-100">
            Сервер временно не доступен, попробуйте позже...</b-alert>
</section>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Confirmation from './Confirmation.vue';

const dataURL = 'http://127.0.0.1:5000/api/tasks/';
export default {
  name: 'Todo',
  data() {
    return {
      todos: [],
      TodoForm: {
        description: '',
        is_completed: [],
        priority: null,
      },
      options: [
        { value: null, text: 'Приоритет', disabled: true },
        { value: 1, text: 'Высокий' },
        { value: 2, text: 'Средний' },
        { value: 3, text: 'Низкий' },
      ],
      confirmationMessage: '',
      showConfirmation: false,
      errored: false,
    };
  },
  methods: {
    getTodos() {
      axios
        .get(dataURL)
        .then((response) => {
          this.todos = response.data.tasks;
        })
        .catch(() => {
          this.errored = true;
        });
    },
    resetForm() {
      this.TodoForm.description = '';
      this.TodoForm.is_completed = [];
      this.TodoForm.priority = null;
    },
    onSubmit(event) {
      event.preventDefault();
      this.$refs.addTodoModal.hide();
      const requestData = {
        description: this.TodoForm.description,
        priority: this.TodoForm.priority,
        is_completed: this.TodoForm.is_completed[0],
      };
      axios
        .post(dataURL, requestData)
        .then(() => {
          this.getTodos();
          this.confirmationMessage = `Задача "${requestData.description}" добавлена`;
          this.showConfirmation = true;
        })
        .catch(() => {
          this.errored = true;
        });
      this.resetForm();
    },
    onReset(event) {
      event.preventDefault();
      this.resetForm();
    },
    updateTodo(todo) {
      this.TodoForm = todo;
    },
    onUpdateSubmit(event) {
      event.preventDefault();
      this.$refs.updateTodoModal.hide();
      const todoURL = dataURL + this.TodoForm.uid;
      const requestData = {
        description: this.TodoForm.description,
        priority: this.TodoForm.priority,
        is_completed: this.TodoForm.is_completed[0],
      };
      axios
        .put(todoURL, requestData)
        .then(() => {
          this.getTodos();
          this.confirmationMessage = 'Задача обновлена';
          this.showConfirmation = true;
        })
        .catch(() => {
          this.errored = true;
        });
    },
    deleteTodo(todo) {
      const todoURL = dataURL + todo.uid;
      axios
        .delete(todoURL)
        .then(() => {
          this.getTodos();
          this.confirmationMessage = 'Задача удалена из списка';
          this.showConfirmation = true;
        })
        .catch(() => {
          this.errored = true;
        });
    },
  },
  components: {
    confirmation: Confirmation,
  },
  created() {
    this.getTodos();
  },
};
</script>

<style>
button#task-add {
  margin-top: 20px;
  margin-bottom: 20px;
}
h1, td {
  text-align: left;
}
.right-align {
  text-align: right;
}
.center-align {
    text-align: center;
}
.completed {
    text-decoration: line-through;
    text-decoration-color: red;
    text-decoration-style: solid;
}
</style>
