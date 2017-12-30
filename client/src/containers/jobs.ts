import { connect, Dispatch } from "react-redux";
import * as _ from "lodash";

import {urlifyProjectName, sortByCreatedAt} from "../constants/utils"
import { AppState } from "../constants/types";
import Jobs from "../components/jobs";
import {JobModel} from "../models/job";
import {ExperimentModel} from "../models/experiment";

import {ProjectModel} from "../models/project";

import * as actions from "../actions/job";


export function mapStateToProps(state: AppState, params: any) {
  let jobs : JobModel[] = [];
  
  if (state.jobs) {
    state.jobs.uuids.forEach(function (uuid: string, idx: number) {
      let job = state.jobs.byUuids[uuid];
      if (job.experiment_name === params.experiment.unique_name) {
        jobs.push(job);
      }
    });
  }

  return {jobs: jobs.sort(sortByCreatedAt)}
}

export interface DispatchProps {
  onCreate?: (job: JobModel) => any;
  onDelete?: (jobName: string) => any;
  onUpdate?: (job: JobModel) => any;
  fetchData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.JobAction>, params: any): DispatchProps {
  return {
    onCreate: (job: JobModel) => dispatch(actions.createJobActionCreator(job)),
    onDelete: (jobName: string) => dispatch(actions.deleteJobActionCreator(jobName)),
    onUpdate: (job: JobModel) => dispatch(actions.updateJobActionCreator(job)),
    fetchData: () => dispatch(actions.fetchJobs(params.experiment.project_name, params.experiment.sequence))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Jobs);
