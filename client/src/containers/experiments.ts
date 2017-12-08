import { connect, Dispatch } from "react-redux";
import * as _ from "lodash";

import { AppState } from "../constants/types";
import Experiments from "../components/experiments";
import {ExperimentModel} from "../models/experiment";
import * as actions from "../actions/experiment";

interface OwnProps {
  projectUuid?: string;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: OwnProps) {
  let experimentUuids: any = [];
  if (!_.isNil(ownProps.projectUuid) && !_.isEmpty(state.projects.byUuids)){
    experimentUuids = state.projects.byUuids[ownProps.projectUuid].experiments
  }

  if (state.experiments) {
    if (_.isEmpty(experimentUuids)) {
      return {experiments: (<any>Object).values(state.experiments.byUuids)};
    } else {
      return {experiments: state.experiments.uuids.filter(
        (k: string) => _.includes(experimentUuids, k)).map((k: string) => state.experiments.byUuids[k])};
    }
  }
  return [];
}

export interface DispatchProps {
  onCreate?: (experiment: ExperimentModel) => any;
  onDelete?: (experimentUuid: string) => any;
  onUpdate?: (experiment: ExperimentModel) => any;
  fetchData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (experiment: ExperimentModel) => dispatch(actions.createExperimentActionCreator(experiment)),
    onDelete: (experimentUuid: string) => dispatch(actions.deleteExperimentActionCreator(experimentUuid)),
    onUpdate: (experiment: ExperimentModel) => dispatch(actions.updateExperimentActionCreator(experiment)),
    fetchData: () => dispatch(ownProps.fetchData? ownProps.fetchData : actions.fetchExperiments())
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Experiments);
