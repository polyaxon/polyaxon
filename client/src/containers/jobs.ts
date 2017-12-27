import { connect, Dispatch } from "react-redux";
import * as _ from "lodash";

import { AppState } from "../constants/types";
import Jobs from "../components/jobs";
import {JobModel} from "../models/job";
import {ExperimentModel} from "../models/experiment";

import {ProjectModel} from "../models/project";

import * as experimentActions from "../actions/experiment";
import * as jobActions from "../actions/job";

interface OwnProps {
  projectName?: string;
  experimentSequence?: number;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: any) {
  let jobs : JobModel[] = [];
  let experiment : ExperimentModel = new ExperimentModel();
  if (state.experiments) {
    state.experiments.uuids.forEach(function (uuid: string, idx: number) {
      if (state.experiments.byUuids[uuid].sequence === parseInt(ownProps.match.params.experimentSequence)) {
        experiment = state.experiments.byUuids[uuid]
      }
    });
  }
  
  if (state.jobs) {
    state.jobs.uuids.forEach(function (uuid: string, idx: number) {
      let job = state.jobs.byUuids[uuid];
      if (job.experiment_name === experiment.unique_name) {
        jobs.push(job);
      }
    });
  }

  return {jobs: jobs, experiment: experiment}
}

export interface DispatchProps {
  onCreate?: (job: JobModel) => any;
  onDelete?: (jobName: string) => any;
  onUpdate?: (job: JobModel) => any;
  fetchExperimentsData?: () => any;
  fetchJobsData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<jobActions.JobAction>, ownProps: any): DispatchProps {
  return {
    onCreate: (job: JobModel) => dispatch(jobActions.createJobActionCreator(job)),
    onDelete: (jobName: string) => dispatch(jobActions.deleteJobActionCreator(jobName)),
    onUpdate: (job: JobModel) => dispatch(jobActions.updateJobActionCreator(job)),
    fetchExperimentsData: () => dispatch(experimentActions.fetchExperiments()),
    fetchJobsData: () => dispatch(jobActions.fetchJobs(ownProps.match.params.projectName, ownProps.match.params.experimentSequence))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Jobs);
