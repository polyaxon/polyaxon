import {ProjectStateSchema, ProjectsEmptyState} from "../models/project";
import {ExperimentStateSchema, ExperimentsEmptyState} from "../models/experiment";

import {JobStateSchema, JobsEmptyState} from "../models/job";
import {GroupStateSchema, GroupsEmptyState} from "../models/group";
import {TokenStateSchema, TokenEmptyState} from "../models/token";

import {ModalStateSchema} from "../models/modal";
import {FormReducer} from "redux-form";

export interface AppState {
    projects: ProjectStateSchema,
    experiments: ExperimentStateSchema,
    groups: GroupStateSchema,
    jobs: JobStateSchema,
    modal: ModalStateSchema,
    auth: TokenStateSchema,
    form: FormReducer
}


export const AppEmptyState = {
    projects: ProjectsEmptyState,
    experiments: ExperimentsEmptyState,
    groups: GroupsEmptyState,
    jobs: JobsEmptyState,
    auth: TokenEmptyState,
};
