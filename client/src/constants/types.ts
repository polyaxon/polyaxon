import {ProjectStateSchema, ProjectsEmptyState} from "../models/project";
import {ExperimentStateSchema, ExperimentsEmptyState} from "../models/experiment";

import {JobStateSchema, JobsEmptyState} from "../models/job";
import {GroupStateSchema, GroupsEmptyState} from "../models/group";

import {ModalStateSchema} from "../models/modal";
import {FormReducer} from "redux-form";

export interface AppState {
    projects: ProjectStateSchema,
    experiments: ExperimentStateSchema,
    groups: GroupStateSchema,
    jobs: JobStateSchema,
    modal: ModalStateSchema,
    form: FormReducer
}


export const AppEmptyState = {
    projects: ProjectsEmptyState,
    experiments: ExperimentsEmptyState,
    groups: GroupsEmptyState,
    jobs: JobsEmptyState
};
