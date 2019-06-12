import * as _ from 'lodash';
import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import { AppState } from '../../constants/types';

import * as actions from '../../actions/jobs';
import JobDetail from '../../components/jobs/jobDetail';
import { getJobUniqueName } from '../../urls/utils';

interface Props extends RouteComponentProps<any> {}

export function mapStateToProps(state: AppState, props: Props) {
  const jobUniqueName = getJobUniqueName(
    props.match.params.user,
    props.match.params.projectName,
    props.match.params.jobId);
  return _.includes(state.jobs.uniqueNames, jobUniqueName) ?
    {job: state.jobs.byUniqueNames[jobUniqueName]} :
    {job: null};
}

export interface DispatchProps {
  onDelete: () => actions.JobAction;
  onUpdate: (updateDict: { [key: string]: any }) => actions.JobAction;
  onStop: () => actions.JobAction;
  onRestart: () => actions.JobAction;
  onRestore: () => actions.JobAction;
  onArchive: () => actions.JobAction;
  fetchData?: () => actions.JobAction;
  bookmark: () => actions.JobAction;
  unbookmark: () => actions.JobAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.JobAction>, props: Props): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchJob(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.jobId)),
    onUpdate: (updateDict: { [key: string]: any }) => dispatch(
      actions.updateJob(
        getJobUniqueName(
          props.match.params.user,
          props.match.params.projectName,
          props.match.params.jobId),
        updateDict
      )),
    onDelete: () => dispatch(actions.deleteJob(
      getJobUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.jobId),
      true
    )),
    onStop: () => dispatch(actions.stopJob(
      getJobUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.jobId)
    )),
    onRestart: () => dispatch(actions.restartJob(
      getJobUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.jobId),
      true
    )),
    onArchive: () => dispatch(actions.archiveJob(
      getJobUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.jobId),
      true)),
    onRestore: () => dispatch(actions.restoreJob(
      getJobUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.jobId)
    )),
    bookmark: () => dispatch(
      actions.bookmark(getJobUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.jobId))),
    unbookmark: () => dispatch(
      actions.unbookmark(getJobUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.jobId)))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(JobDetail));
