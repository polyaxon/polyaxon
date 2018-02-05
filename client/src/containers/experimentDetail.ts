import { connect, Dispatch } from "react-redux";
import {withRouter} from "react-router-dom";

import { AppState } from "../constants/types";
import ExperimentDetail from "../components/experimentDetail";
import * as actions from "../actions/experiment";


export function mapStateToProps(state: AppState, params: any)  {
  let experimentSequence = parseInt(params.match.params.experimentSequence);
  let ret;
  
  state.experiments.uniqueNames.forEach(function (uniqueName: string, idx: number) {
    if (state.experiments.ByUniqueNames[uniqueName].sequence === experimentSequence) {
      ret = {experiment: state.experiments.ByUniqueNames[uniqueName]};
    }
  });

  if (!ret) {
    ret = {experiment: null};
  }
  return ret;
}

export interface DispatchProps {
  onDelete?: () => any;
  fetchData?: () => any;
}


export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentAction>, params: any): DispatchProps {
  return {
    onDelete: () => dispatch(() => {}),
    fetchData: () => dispatch(actions.fetchExperiment(params.match.params.user, params.match.params.projectName, params.match.params.experimentSequence))
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ExperimentDetail));
