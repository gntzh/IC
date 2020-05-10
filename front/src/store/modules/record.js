import { make } from "vuex-pathify";

const state = {
    addForm: {
        operation: 1,
        component: '',
        num: '0',
        money: '0',
        time: ''
    },
};
const addForm = state.addForm

const mutations = make.mutations(state);
mutations.RESET_ADD_Form = (state) => {
    state.addForm = addForm
}
const actions = {};

const getters = {};

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters
};
