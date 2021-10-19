<template>
  <!-- Rooms Table -->
  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Rooms</h6>
      <button
        class="btn btn-primary"
        data-bs-toggle="modal"
        data-bs-target="#modal"
        @click="addModal"
      >
        Add
      </button>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table
          class="table table-borderless"
          id="dataTable"
          width="100%"
          cellspacing="0"
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="room in allRooms" :key="room.id">
              <td>{{ room.id }}</td>
              <td>{{ room.name }}</td>
              <td>
                <button
                  type="button"
                  class="btn btn-primary"
                  data-bs-toggle="modal"
                  data-bs-target="#modal"
                  @click="editModal(room.id)"
                >
                  Edit
                </button>
                <button class="btn btn-danger" @click="deleteRoom(room.id)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Edit Room Modal -->
  <div
    class="modal fade"
    id="modal"
    tabindex="-1"
    aria-labelledby="modal"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modalTitle">
            Edit Room {{ this.modalId }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="onSubmit">
            <!-- ID -->
            <div class="mb-3">
              <label for="inputIdLabel" class="form-label">ID</label>
              <input
                type="text"
                class="form-control"
                id="inputId"
                v-model="modalId"
              />
            </div>
            <!-- Name -->
            <div class="mb-3">
              <label for="inputNameLabel" class="form-label">Name</label>
              <input
                type="text"
                class="form-control"
                id="inputName"
                v-model="modalName"
              />
            </div>
            <button
              type="submit"
              data-bs-dismiss="modal"
              class="btn btn-primary"
            >
              Save
            </button>
          </form>
        </div>
        <!-- <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-primary">Save changes</button>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  name: "RoomsTable",
  data() {
    return {
      modalId: "",
      modalName: "",
    };
  },
  methods: {
    ...mapActions(["retrieveRooms", "addRoom", "editRoom", "deleteRoom"]),
    addModal: function() {},
    editModal: function(id) {
      let room = this.getRoom(id);
      this.modalId = room.id;
      this.modalName = room.name;
    },
    onSubmit: function() {
      let newRoom = { id: Number(this.modalId), name: this.modalName };
      this.editRoom(newRoom);
      this.modalId = "";
      this.modalName = "";
    },
  },
  computed: {
    ...mapGetters(["allRooms", "getRoom"]),
  },
  created() {
    this.retrieveRooms();
  },
};
</script>
