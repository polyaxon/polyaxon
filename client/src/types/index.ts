import {ProjectStateSchema} from "../models/project";
import {ExperimentStateSchema} from "../models/experiment";

export interface AppState {
    projects: ProjectStateSchema,
    experiments: ExperimentStateSchema,
}
