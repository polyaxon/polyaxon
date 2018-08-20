import * as _ from 'lodash';
import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import Builds from '../components/builds';
import { AppState } from '../constants/types';
import { isTrue } from '../constants/utils';
import { BuildModel } from '../models/build';

import * as actions from '../actions/build';

interface OwnProps {
  user: string;
  projectName?: string;
  bookmarks?: boolean;
  useFilters?: boolean;
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
    bookmarks: isTrue(ownProps.bookmarks),
  };
}

export interface DispatchProps {
  onCreate?: (build: BuildModel) => actions.BuildAction;
  onDelete?: (build: BuildModel) => actions.BuildAction;
  onUpdate?: (build: BuildModel) => actions.BuildAction;
  fetchData?: (offset?: number, query?: string, sort?: string) => actions.BuildAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.BuildAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (build: BuildModel) => dispatch(actions.createBuildActionCreator(build)),
    onDelete: (build: BuildModel) => dispatch(actions.deleteBuildActionCreator(build)),
    onUpdate: (build: BuildModel) => dispatch(actions.updateBuildActionCreator(build)),
    fetchData: (offset?: number, query?: string, sort?: string) => {
      const filters: {[key: string]: number|boolean|string} = {};
      if (query) {
        filters.query = query;
      }
      if (sort) {
        filters.sort = sort;
      }
      if (offset) {
        filters.offset = offset;
      }
      if (_.isNil(ownProps.projectName) && ownProps.bookmarks) {
        return dispatch(actions.fetchBookmarkedBuilds(ownProps.user, filters));
      } else if (ownProps.projectName) {
        return dispatch(actions.fetchBuilds(ownProps.projectName, filters));
      } else {
        throw new Error('Builds container expects either a project name or bookmarks.');
      }
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Builds);
