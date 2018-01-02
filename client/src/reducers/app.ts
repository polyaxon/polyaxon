import {Action, combineReducers} from "redux";
import { reducer as formReducer } from "redux-form";


import {projectsReducer, ProjectExperiments} from "./projects";
import {experimentsReducer} from "./experiments";
import {groupsReducer} from "./groups";
import {jobsReducer} from "./jobs";

import {tokenReducer} from "./token";
import {AppState} from "../constants/types";
import {modalReducer} from "../reducers/modal";


const combinedReducer = combineReducers<AppState>({
  projects: projectsReducer,
  experiments: experimentsReducer,
  groups: groupsReducer,
  jobs: jobsReducer,
  modal: modalReducer,
  auth: tokenReducer,
  form: formReducer
});

function ProjectSliceReducer(state: AppState, action: Action) {
  return {
    projects: state.projects,
    experiments : ProjectExperiments(state.experiments, action),
    groups: state.groups,
    jobs: state.jobs,
    modal: state.modal,
    auth: state.auth,
    form: state.form
  }
}

function appReducer(state: AppState, action: Action) {
    let _state = combinedReducer(state, action);
    _state = ProjectSliceReducer(_state, action);
    return _state;
}

export default appReducer;
