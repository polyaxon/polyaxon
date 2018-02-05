import { connect, Dispatch } from "react-redux";
import {withRouter} from "react-router-dom";

import { AppState } from "../constants/types";

import JobDetail from "../components/jobDetail";
import * as actions from "../actions/job";


export function mapStateToProps(state: AppState, params: any)  {
  let jobSequence = parseInt(params.match.params.jobSequence);
  let ret;

  state.jobs.uniqueNames.forEach(function (uniqueName: string, idx: number) {
    if (state.jobs.ByUniqueNames[uniqueName].sequence === jobSequence) {
      ret = {job: state.jobs.ByUniqueNames[uniqueName]};
    }
  });

  if (!ret) {
    ret = {job: null};
  }
  return ret;
}

export interface DispatchProps {
  onDelete?: () => any;
  fetchData?: (jobSequence: number) => any;
}


export function mapDispatchToProps(dispatch: Dispatch<actions.JobAction>, params: any): DispatchProps {
  // TODO: We are probably using the wrong user here
  return {
    onDelete: () => dispatch(() => {}),
    fetchData: () => dispatch(actions.fetchJob(params.match.params.user, params.match.params.projectName, params.match.params.experimentSequence, params.match.params.jobSequence))
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(JobDetail));
