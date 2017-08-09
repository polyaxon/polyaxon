import {ProjectStateSchema, ProjectsEmptyState} from "../models/project";
import {ExperimentStateSchema, ExperimentsEmptyState} from "../models/experiment";

export interface AppState {
    projects: ProjectStateSchema,
    experiments: ExperimentStateSchema,
}


export const AppEmptyState = {projects: ProjectsEmptyState, experiments: ExperimentsEmptyState};
