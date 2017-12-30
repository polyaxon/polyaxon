import { connect, Dispatch } from "react-redux";
import {withRouter} from "react-router-dom";
import * as _ from "lodash";

import { AppState } from "../constants/types";
import { JobModel } from "../models/job";

import JobDetail from "../components/jobDetail";
import * as actions from "../actions/job";


export function mapStateToProps(state: AppState, params: any)  {
  let jobUuid = params.match.params.jobUuid;
  if (state.jobs) {
    return {
      job: state.jobs.byUuids[jobUuid]
    }
  }
  return {
    job: null
  }
}

export interface DispatchProps {
  onDelete?: () => any;
  fetchData?: (jobUuid: string) => any;
}


export function mapDispatchToProps(dispatch: Dispatch<actions.JobAction>, params: any): DispatchProps {
  // TODO: We are probably using the wrong user here
  return {
    onDelete: () => dispatch(() => {}),
    fetchData: () => dispatch(actions.fetchJob(params.match.params.user, params.match.params.projectName, params.match.params.experimentSequence, params.match.params.jobUuid))
  }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(JobDetail));