import { connect, Dispatch } from 'react-redux';

import { AppState } from '../constants/types';
import Builds from '../components/builds';
import { BuildModel } from '../models/build';

import * as actions from '../actions/build';
import { getPaginatedSlice } from '../constants/paginate';

export function mapStateToProps(state: AppState, params: any) {
  let builds: BuildModel[] = [];
  let project = state.projects.byUniqueNames[params.projectName];
  let BuildNames = project.builds;
  BuildNames = getPaginatedSlice(BuildNames, state.pagination.buildCurrentPage);
  BuildNames.forEach(
    function (build: string, idx: number) {
      builds.push(state.builds.byUniqueNames[build]);
    });

  return {
    isCurrentUser: state.auth.user === params.user,
    builds: builds,
    count: project.num_builds
  };
}

export interface DispatchProps {
  onCreate?: (build: BuildModel) => actions.BuildAction;
  onDelete?: (build: BuildModel) => actions.BuildAction;
  onUpdate?: (build: BuildModel) => actions.BuildAction;
  fetchData?: (currentPage?: number) => actions.BuildAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.BuildAction>, params: any): DispatchProps {
  return {
    onCreate: (build: BuildModel) => dispatch(actions.createBuildActionCreator(build)),
    onDelete: (build: BuildModel) => dispatch(actions.deleteBuildActionCreator(build)),
    onUpdate: (build: BuildModel) => dispatch(actions.updateBuildActionCreator(build)),
    fetchData: (currentPage?: number) => dispatch(
      actions.fetchBuilds(params.projectName, currentPage))
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Builds);
