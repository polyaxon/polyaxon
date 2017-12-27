import { connect, Dispatch } from "react-redux";
import * as _ from "lodash";

import { AppState } from "../constants/types";
import Experiments from "../components/experiments";
import {ExperimentModel} from "../models/experiment";
import {ProjectModel} from "../models/project";

import * as experimentActions from "../actions/experiment";
import * as projectActions from "../actions/project";

interface OwnProps {
  projectName?: string;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: any) {
  let experiments : ExperimentModel[] = [];
  let project : ProjectModel = new ProjectModel();
  if (state.experiments) {
    state.experiments.uuids.forEach(function (uuid: string, idx: number) {
      let experiment = state.experiments.byUuids[uuid];
      let projectName = experiment.project_name.substr(experiment.project_name.indexOf('.') + 1);
      if (projectName === ownProps.match.params.projectName) {
        experiments.push(experiment);
      }
    });
  }
  if (state.projects) {
    state.projects.uuids.forEach(function (uuid: string, idx: number) {
      if (state.projects.byUuids[uuid].name === ownProps.match.params.projectName) {
        project = state.projects.byUuids[uuid]
      }
    });
  }

  return {experiments: experiments, project: project}
}

export interface DispatchProps {
  onCreate?: (experiment: ExperimentModel) => any;
  onDelete?: (experimentName: string) => any;
  onUpdate?: (experiment: ExperimentModel) => any;
  fetchProjectsData?: () => any;
  fetchExperimentsData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<experimentActions.ExperimentAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (experiment: ExperimentModel) => dispatch(experimentActions.createExperimentActionCreator(experiment)),
    onDelete: (experimentName: string) => dispatch(experimentActions.deleteExperimentActionCreator(experimentName)),
    onUpdate: (experiment: ExperimentModel) => dispatch(experimentActions.updateExperimentActionCreator(experiment)),
    fetchProjectsData: () => dispatch(projectActions.fetchProjects()),
    fetchExperimentsData: () => dispatch(experimentActions.fetchExperiments())
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Experiments);
