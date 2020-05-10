import { make } from "vuex-pathify";
import http from "@/utils/http";
import { apiURL } from "@/api/user";
import jwt from "@/utils/jwt.js";

const state = {
  isAuthenticated: false,
  userId: 0,
  username: "",
  nickname: "",
  avatar: "",
  isAdmin: false,
  email: "",
  emailIsActive: false,
  accessToken: "",
  saveToken: false
};

const mutations = make.mutations(state);

mutations.SET_ACCESS_TOKEN = function(state, token) {
  state.accessToken = token;
  http.defaults.headers.common["Authorization"] = "Bearer " + token;
};

mutations.SIGN_IN = function(state, payload) {
  state.isAuthenticated = true;
  state.userId = payload.userId;
  state.username = payload.username || "";
  state.isAdmin = payload.isAdmin || false;
  state.email = payload.email || "";
  state.emailIsActive = payload.emailIsActive || false;
};

mutations.SIGN_OUT = function(state, payload) {
  state.isAuthenticated = false;
  state.userId = 0;
  state.username = "";
  state.avatar = "";
  state.isAdmin = false;
  state.email = "";
  state.emailIsActive = false;
  state.accessToken = "";
  state.saveToken = false;
  localStorage.removeItem("token:refresh");
};

const actions = {
  signIn({ commit }, { refresh, access, saveToken }) {
    this.set("auth/isAuthenticated", true);
    this.set("auth/accessToken", access);
    if (saveToken) {
      this.set("auth/saveToken", true);
      console.log(refresh);

      if (refresh) localStorage.setItem("token:refresh", refresh);
    }
    http.get(apiURL + "users/me/").then(
      res => {
        commit("SIGN_IN", {
          userId: res.data.id,
          username: res.data.username,
          email: res.data.email,
          emailIsActive: res.data.email_is_active,
          isAdmin: res.data.is_staff,
          avatar: res.data.avatar
        });
      },
      err => {
        this.set("app/snackbar", {
          icon: "warning",
          msg: "身份信息获取失败, 请重新登录",
          color: "warning"
        });
        commit("SIGN_OUT");
      }
    );
  },
  signOut({ commit }) {
    commit("SIGN_OUT");
  }
};

const getters = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};
