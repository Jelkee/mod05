<template>
  <!-- Outer Row -->
  <div class="row justify-content-center">
    <div class="col-xl-6 col-lg-6 col-md-4">
      <div class="card o-hidden border-0 shadow-lg my-5">
        <div class="card-body p-0">
          <!-- Nested Row within Card Body -->
          <!-- <div class="row">
            <div class="col-lg-6"> -->
          <div class="p-5">
            <div class="text-center">
              <h1 class="h4 text-gray-900 mb-4">Raspberry Home</h1>
            </div>
            <form class="user" @submit.prevent="onSubmit">
              <div class="form-group">
                <input
                  type="text"
                  class="form-control form-control-user"
                  id="inputUsername"
                  aria-describedby="emailHelp"
                  placeholder="Username"
                  v-model="username"
                />
              </div>
              <div class="form-group">
                <input
                  type="password"
                  class="form-control form-control-user"
                  id="exampleInputPassword"
                  placeholder="Password"
                  v-model="password"
                />
              </div>
              <div class="form-group">
                <div class="custom-control custom-checkbox small">
                  <input
                    type="checkbox"
                    class="custom-control-input"
                    id="customCheck"
                  />
                  <label class="custom-control-label" for="customCheck"
                    >Remember Me</label
                  >
                </div>
              </div>
              <button type="submit" class="btn btn-primary btn-user btn-block">
                Login
              </button>
              <hr />
            </form>
            <hr />
            <!-- <div class="text-center">
                  <a class="small" href="#">Forgot Password?</a>
                </div> -->
            <!-- </div>
            </div> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions } from "vuex";

export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    ...mapActions(["login"]),
    onSubmit: function() {
      let credentials = { username: this.username, password: this.password };
      this.handleLogin(credentials);
    },
    async handleLogin(credentials) {
      let res = await axios.post("http://localhost:3000/login", {
        email: credentials.username,
        password: credentials.password,
      });
      if (res.status === 200) {
        localStorage.setItem("token", res.data.token);
        this.login();
        this.$router.push("/dashboard");
      }
    },
  },
};
</script>
