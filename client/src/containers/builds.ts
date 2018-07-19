import { connect } from 'react-redux';
import { Dispatch } from 'redux';
import * as _ from 'lodash';

import { AppState } from '../constants/types';
import Builds from '../components/builds';
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

  let useLastFetched = () => {
    let buildNames = state.builds.lastFetched.names;
    let count = state.builds.lastFetched.count;
    let builds: BuildModel[] = [];
    buildNames.forEach(
      function (build: string, idx: number) {
        builds.push(state.builds.byUniqueNames[build]);
      });
    return {builds: builds, count: count};
  };
  let results = useLastFetched();

  return {
    isCurrentUser: state.auth.user === ownProps.user,
    builds: results.builds,
    count: results.count,
    useFilters: !_.isNil(ownProps.useFilters) && ownProps.useFilters,
    bookmarks: !_.isNil(ownProps.bookmarks) && ownProps.bookmarks,
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
      let filters: {[key: string]: number|boolean|string} = {};
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
