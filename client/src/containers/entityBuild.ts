import * as _ from 'lodash';
import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as actions from '../actions/build';
import EntityBuild from '../components/builds/entityBuild';
import { AppState } from '../constants/types';
import { splitUniqueName } from '../constants/utils';

export function mapStateToProps(state: AppState, params: any) {
  return _.includes(state.builds.uniqueNames, params.buildName) ?
    {build: state.builds.byUniqueNames[params.buildName], showBookmarks: false} :
    {build: null, showBookmarks: false};
}

export interface DispatchProps {
  onDelete: (buildName: string) => actions.BuildAction;
  onStop: (buildName: string) => actions.BuildAction;
  bookmark: (buildName: string) => actions.BuildAction;
  unbookmark: (buildName: string) => actions.BuildAction;
  fetchData: () => actions.BuildAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.BuildAction>, params: any): DispatchProps {
  return {
    onDelete: (buildName: string) => dispatch(actions.deleteBuild(buildName)),
    onStop: (buildName: string) => dispatch(actions.stopBuild(buildName)),
    bookmark: (buildName: string) => dispatch(actions.bookmark(buildName)),
    unbookmark: (buildName: string) => dispatch(actions.unbookmark(buildName)),
    fetchData: () => {
      if (params.buildName) {
        const buildValues = splitUniqueName(params.buildName);
        return dispatch(actions.fetchBuild(
          buildValues[0],
          buildValues[1],
          buildValues[3]));
      }
    },
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(EntityBuild);
