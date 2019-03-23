import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import Builds from '../../components/builds/builds';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { BuildModel } from '../../models/build';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';

import * as actions from '../../actions/builds';
import * as search_actions from '../../actions/search';
import { SearchModel } from '../../models/search';

interface OwnProps {
  user: string;
  projectName?: string;
  endpointList?: string;
  useFilters?: boolean;
  showBookmarks?: boolean;
  showDeleted?: boolean;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: OwnProps) {
  // let useFilter = () => {
  //   let builds: BuildModel[] = [];
  //   let project = state.projects.byUniqueNames[ownProps.projectName];
  //   let BuildNames = project.builds;
  //   BuildNames.forEach(
  //     function (build: string, idx: number) {
  //       builds.push(state.builds.byUniqueNames[build]);
  //     });
  //   return {builds: builds, count: project.num_builds};
  // };

  const useLastFetched = () => {
    const buildNames = state.builds.lastFetched.names;
    const count = state.builds.lastFetched.count;
    const builds: BuildModel[] = [];
    buildNames.forEach(
      (build: string, idx: number) => {
        builds.push(state.builds.byUniqueNames[build]);
      });
    return {builds, count};
  };
  const results = useLastFetched();

  return {
    isCurrentUser: state.auth.user === ownProps.user,
    builds: results.builds,
    count: results.count,
    useFilters: isTrue(ownProps.useFilters),
    showBookmarks: isTrue(ownProps.showBookmarks),
    showDeleted: isTrue(ownProps.showDeleted),
    endpointList: ownProps.endpointList,
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

export function mapDispatchToProps(dispatch: Dispatch<actions.BuildAction>, params: any): DispatchProps {
  return {
    onCreate: (build: BuildModel) => dispatch(actions.createBuild(
      params.match.params.user,
      params.match.params.projectName,
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
      if (params.projectName) {
        return dispatch(search_actions.fetchBuildSearches(params.projectName));
      } else {
        throw new Error('Builds container does not have project.');
      }
    },
    createSearch: (data: SearchModel) => {
      if (params.projectName) {
        return dispatch(search_actions.createBuildSearch(params.projectName, data));
      } else {
        throw new Error('Builds container does not have project.');
      }
    },
    deleteSearch: (searchId: number) => {
      if (params.projectName) {
        return dispatch(search_actions.deleteBuildSearch(params.projectName, searchId));
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
      if (_.isNil(params.projectName) && params.endpointList === BOOKMARKS) {
        return dispatch(actions.fetchBookmarkedBuilds(params.user, filters));
      } else if (_.isNil(params.projectName) && params.endpointList === ARCHIVES) {
        return dispatch(actions.fetchArchivedBuilds(params.user, filters));
      } else if (params.projectName) {
        return dispatch(actions.fetchBuilds(params.projectName, filters));
      } else {
        throw new Error('Builds container expects either a project name or bookmarks or archives.');
      }
    }
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Builds));
