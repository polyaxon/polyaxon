import {combineReducers} from "redux";
import {projectReducer} from "./project";
import {experimentReducer} from "./experiment";
import {AppState} from "../types/index";


const appReducer = combineReducers<AppState>({
  projects: projectReducer,
  experiments: experimentReducer
});

export default appReducer;
