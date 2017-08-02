import {ProjectModel} from "../models/project";
import {ExperimentModel} from "../models/experiment";

export interface AppState {
    projects: ProjectModel[],
    experiments: ExperimentModel[]
}
