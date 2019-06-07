import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import Jobs from '../../components/jobs/jobs';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { JobModel } from '../../models/job';

import * as actions from '../../actions/jobs';
import * as search_actions from '../../actions/search';
import { ACTIONS } from '../../constants/actions';
import { SearchModel } from '../../models/search';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { getErrorsGlobal } from '../../utils/errors';
import { getLastFetchedJobs } from '../../utils/states';

interface Props extends RouteComponentProps<any> {
  user?: string;
  projectName?: string;
  groupId?: string;
  useFilters?: boolean;
  showBookmarks?: boolean;
  showDeleted?: boolean;
  endpointList?: string;
  fetchData?: () => actions.JobAction;
}

export function mapStateToProps(state: AppState, props: Props) {
  const cUser = props.user || props.match.params.user;
  const results = getLastFetchedJobs(state.jobs);
  const isLoading = isTrue(state.loadingIndicators.jobs.global.fetch);
  return {
    isCurrentUser: state.auth.user === cUser,
    jobs: results.jobs,
    count: results.count,
    useFilters: isTrue(props.useFilters),
    showBookmarks: isTrue(props.showBookmarks),
    showDeleted: isTrue(props.showDeleted),
    endpointList: props.endpointList,
    isLoading,
    errors: getErrorsGlobal(state.alerts.jobs.global, isLoading, ACTIONS.FETCH),
  };
}

export interface DispatchProps {
  onCreate?: (job: JobModel) => actions.JobAction;
  onDelete: (jobName: string) => actions.JobAction;
  onStop: (jobName: string) => actions.JobAction;
  onRestart: (jobName: string) => actions.JobAction;
  onArchive: (jobName: string) => actions.JobAction;
  onRestore: (jobName: string) => actions.JobAction;
  bookmark: (jobName: string) => actions.JobAction;
  unbookmark: (jobName: string) => actions.JobAction;
  onUpdate?: (job: JobModel) => actions.JobAction;
  fetchData?: (offset?: number, query?: string, sort?: string) => actions.JobAction;
  fetchSearches?: () => search_actions.SearchAction;
  createSearch?: (data: SearchModel) => search_actions.SearchAction;
  deleteSearch?: (searchId: number) => search_actions.SearchAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.JobAction>, props: Props): DispatchProps {
  const cUser = props.user || props.match.params.user;
  const cProjectName = props.projectName || `${cUser}.${props.match.params.projectName}`;

  return {
    onCreate: (job: JobModel) => dispatch(actions.createJob(
      props.match.params.user,
      props.match.params.projectName,
      job,
      true)),
    onDelete: (jobName: string) => dispatch(actions.deleteJob(jobName)),
    onStop: (jobName: string) => dispatch(actions.stopJob(jobName)),
    onRestart: (jobName: string) => dispatch(actions.restartJob(jobName, true)),
    onArchive: (jobName: string) => dispatch(actions.archiveJob(jobName)),
    onRestore: (jobName: string) => dispatch(actions.restoreJob(jobName)),
    bookmark: (jobName: string) => dispatch(actions.bookmark(jobName)),
    unbookmark: (jobName: string) => dispatch(actions.unbookmark(jobName)),
    onUpdate: (job: JobModel) => dispatch(actions.updateJobSuccessActionCreator(job)),
    fetchSearches: () => {
      if (cProjectName) {
        return dispatch(search_actions.fetchJobSearches(cProjectName));
      } else {
        throw new Error('Jobs container does not have project.');
      }
    },
    createSearch: (data: SearchModel) => {
      if (cProjectName) {
        return dispatch(search_actions.createJobSearch(cProjectName, data));
      } else {
        throw new Error('Builds container does not have project.');
      }
    },
    deleteSearch: (searchId: number) => {
      if (cProjectName) {
        return dispatch(search_actions.deleteJobSearch(cProjectName, searchId));
      } else {
        throw new Error('Builds container does not have project.');
      }
    },
    fetchData: (offset?: number, query?: string, sort?: string) => {
      const filters: { [key: string]: number | boolean | string } = {};
      if (query) {
        filters.query = query;
      }
      if (sort) {
        filters.sort = sort;
      }
      if (offset) {
        filters.offset = offset;
      }
      if (props.endpointList === BOOKMARKS) {
        return dispatch(actions.fetchBookmarkedJobs(cUser, filters));
      } else if (props.endpointList === ARCHIVES) {
        return dispatch(actions.fetchArchivedJobs(cUser, filters));
      } else if (cProjectName) {
        return dispatch(actions.fetchJobs(cProjectName, filters));
      } else {
        throw new Error('Jobs container expects either a project name or bookmarks or archives.');
      }
    }
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Jobs));
