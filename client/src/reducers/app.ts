import {Action, combineReducers} from "redux";
import {projectsReducer, ProjectExperiments} from "./projects";
import {experimentsReducer} from "./experiments";
import {AppState} from "../constants/types";
import {modalReducer} from "../reducers/modal";


const combinedReducer = combineReducers<AppState>({
  projects: projectsReducer,
  experiments: experimentsReducer,
  modal: modalReducer,
});

function ProjectSliceReducer(state: AppState, action: Action) {
  return {
    projects: state.projects,
    experiments : ProjectExperiments(state.experiments, action),
    modal: state.modal,
  }
}

function appReducer(state: AppState, action: Action) {
    let _state = combinedReducer(state, action);
    _state = ProjectSliceReducer(_state, action);
    return _state;
}

export default appReducer;
