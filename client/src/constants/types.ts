import {ProjectStateSchema, ProjectsEmptyState} from "../models/project";
import {ExperimentStateSchema, ExperimentsEmptyState} from "../models/experiment";
import {ModalStateSchema} from "../models/modal";

export interface AppState {
    projects: ProjectStateSchema,
    experiments: ExperimentStateSchema,
    modal: ModalStateSchema
}


export const AppEmptyState = {projects: ProjectsEmptyState, experiments: ExperimentsEmptyState};
