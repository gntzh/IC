import { make } from "vuex-pathify";

const defaultSnackbar = {
  color: "success",
  href: false,
  icon: "info",
  msg: "",
  text: "Close",
  to: false,
  timeout: 3000,
  close: true
};

const state = {
  showDrawer: false,
  snackbar: defaultSnackbar,
  showSnackbar: false,
  showSignIn: false,
  showSignUp: false
};
const mutations = make.mutations(state);

state.snackbar = defaultSnackbar;

mutations.SET_SNACKBAR = (state, payload) => {
  state.snackbar = { ...defaultSnackbar, ...payload };
  state.showSnackbar = true;
};

const actions = {};

const getters = {};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};
