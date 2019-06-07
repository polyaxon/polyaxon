import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import Builds from '../../components/builds/builds';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { BuildModel } from '../../models/build';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';

import * as actions from '../../actions/builds';
import * as search_actions from '../../actions/search';
import { ACTIONS } from '../../constants/actions';
import { SearchModel } from '../../models/search';
import { getErrorsGlobal } from '../../utils/errors';
import { getLastFetchedBuilds } from '../../utils/states';

interface Props extends RouteComponentProps<any> {
  user?: string;
  projectName?: string;
  endpointList?: string;
  useFilters?: boolean;
  showBookmarks?: boolean;
  showDeleted?: boolean;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, props: Props) {
  const cUser = props.user || props.match.params.user;
  const results = getLastFetchedBuilds(state.builds);
  const isLoading = isTrue(state.loadingIndicators.builds.global.fetch);
  return {
    isCurrentUser: state.auth.user === cUser,
    builds: results.builds,
    count: results.count,
    useFilters: isTrue(props.useFilters),
    showBookmarks: isTrue(props.showBookmarks),
    showDeleted: isTrue(props.showDeleted),
    endpointList: props.endpointList,
    isLoading,
    errors: getErrorsGlobal(state.alerts.builds.global, isLoading, ACTIONS.FETCH),
  };
}

export interface DispatchProps {
  onCreate?: (build: BuildModel) => actions.BuildAction;
  onDelete: (buildName: string) => actions.BuildAction;
  onStop: (buildName: string) => actions.BuildAction;
  onArchive: (buildName: string) => actions.BuildAction;
  onRestore: (buildName: string) => actions.BuildAction;
  onUpdate?: (buildName: string, build: BuildModel) => actions.BuildAction;
  bookmark?: (buildName: string) => actions.BuildAction;
  unbookmark?: (buildName: string) => actions.BuildAction;
  fetchData?: (offset?: number, query?: string, sort?: string) => actions.BuildAction;
  fetchSearches?: () => search_actions.SearchAction;
  createSearch?: (data: SearchModel) => search_actions.SearchAction;
  deleteSearch?: (searchId: number) => search_actions.SearchAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.BuildAction>, props: Props): DispatchProps {
  const cUser = props.user || props.match.params.user;
  const cProjectName = props.projectName || `${cUser}.${props.match.params.projectName}`;

  return {
    onCreate: (build: BuildModel) => dispatch(actions.createBuild(
      props.match.params.user,
      props.match.params.projectName,
      build,
      true)),
    onDelete: (buildName: string) => dispatch(actions.deleteBuild(buildName)),
    onStop: (buildName: string) => dispatch(actions.stopBuild(buildName)),
    onArchive: (buildName: string) => dispatch(actions.archiveBuild(buildName)),
    onRestore: (buildName: string) => dispatch(actions.restoreBuild(buildName)),
    bookmark: (buildName: string) => dispatch(actions.bookmark(buildName)),
    unbookmark: (buildName: string) => dispatch(actions.unbookmark(buildName)),
    onUpdate: (buildName: string, build: BuildModel) => dispatch(actions.updateBuild(buildName, build)),
    fetchSearches: () => {
      if (cProjectName) {
        return dispatch(search_actions.fetchBuildSearches(cProjectName));
      } else {
        throw new Error('Builds container does not have project.');
      }
    },
    createSearch: (data: SearchModel) => {
      if (cProjectName) {
        return dispatch(search_actions.createBuildSearch(cProjectName, data));
      } else {
        throw new Error('Builds container does not have project.');
      }
    },
    deleteSearch: (searchId: number) => {
      if (cProjectName) {
        return dispatch(search_actions.deleteBuildSearch(cProjectName, searchId));
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
        return dispatch(actions.fetchBookmarkedBuilds(cUser, filters));
      } else if (props.endpointList === ARCHIVES) {
        return dispatch(actions.fetchArchivedBuilds(cUser, filters));
      } else if (cProjectName) {
        return dispatch(actions.fetchBuilds(cProjectName, filters));
      } else {
        throw new Error('Builds container expects either a project name or bookmarks or archives.');
      }
    }
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Builds));
