import {ProjectModel} from "../models/project";
import {ExperimentModel} from "../models/experiment";

export interface AppState {
    projects: {byIds: {[id: number]: ProjectModel}, ids: number[]},
    experiments: {byIds: {[id: number]: ExperimentModel}, ids: number[]},
}
