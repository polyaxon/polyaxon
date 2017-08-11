import {ProjectStateSchema, ProjectsEmptyState} from "../models/project";
import {ExperimentStateSchema, ExperimentsEmptyState} from "../models/experiment";
import {ModalStateSchema} from "../models/modal";
import {FormReducer} from "redux-form";

export interface AppState {
    projects: ProjectStateSchema,
    experiments: ExperimentStateSchema,
    modal: ModalStateSchema,
    form: FormReducer
}


export const AppEmptyState = {projects: ProjectsEmptyState, experiments: ExperimentsEmptyState};
