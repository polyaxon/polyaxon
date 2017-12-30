import { connect, Dispatch } from "react-redux";
import * as _ from "lodash";

import {urlifyProjectName, sortByUpdatedAt} from "../constants/utils"
import { AppState } from "../constants/types";
import Experiments from "../components/experiments";
import {ExperimentModel} from "../models/experiment";
import {ProjectModel} from "../models/project";

import * as actions from "../actions/experiment";

interface OwnProps {
  user: string;
  projectName: string;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: any) {
  let experiments : ExperimentModel[] = [];
  if (state.experiments) {
    state.experiments.uuids.forEach(function (uuid: string, idx: number) {
      let experiment = state.experiments.byUuids[uuid];
      if (experiment.project_name === ownProps.projectName) {
        experiments.push(experiment);
      }
    });
  }

  return {experiments: experiments.sort(sortByUpdatedAt)}
}

export interface DispatchProps {
  onCreate?: (experiment: ExperimentModel) => any;
  onDelete?: (experiment: ExperimentModel) => any;
  onUpdate?: (experiment: ExperimentModel) => any;
  fetchData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (experiment: ExperimentModel) => dispatch(actions.createExperimentActionCreator(experiment)),
    onDelete: (experiment: ExperimentModel) => dispatch(actions.deleteExperimentActionCreator(experiment)),
    onUpdate: (experiment: ExperimentModel) => dispatch(actions.updateExperimentActionCreator(experiment)),
    fetchData: () => dispatch(actions.fetchExperiments(ownProps.projectName))
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Experiments);
