import {combineReducers} from "redux";
import {projectsReducer} from "./projects";
import {experimentsReducer} from "./experiments";
import {AppState} from "../types/index";


const appReducer = combineReducers<AppState>({
  projects: projectsReducer,
  experiments: experimentsReducer,
});

export default appReducer;
