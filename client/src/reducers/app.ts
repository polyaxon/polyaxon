import {Action, combineReducers} from "redux";
import {projectsReducer, ProjectExperiments} from "./projects";
import {experimentsReducer} from "./experiments";
import {AppState} from "../constants/types";


const combinedReducer = combineReducers<AppState>({
  projects: projectsReducer,
  experiments: experimentsReducer,
});

function ProjectSliceReducer(state: AppState, action: Action) {
  return {
    projects: state.projects,
    experiments : ProjectExperiments(state.experiments, action)
  }
}

function appReducer(state: AppState, action: Action) {
    let _state = combinedReducer(state, action);
    _state = ProjectSliceReducer(_state, action);
    return _state;
}

export default appReducer;
