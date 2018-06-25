import { connect, Dispatch } from 'react-redux';
import * as _ from 'lodash';

import { AppState } from '../constants/types';
import * as actions from '../actions/build';
import { splitUniqueName } from '../constants/utils';
import EntityBuild from '../components/EntityBuild';

export function mapStateToProps(state: AppState, params: any) {
  return _.includes(state.builds.uniqueNames, params.buildName) ?
  {build: state.builds.byUniqueNames[params.buildName]} :
  {build: null};
}

export interface DispatchProps {
  fetchData: () => actions.BuildAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.BuildAction>, params: any): DispatchProps {
  return {
    fetchData: () => {
      if (params.buildName) {
        let buildValues = splitUniqueName(params.buildName);
        return dispatch(actions.fetchBuild(
          buildValues[0],
          buildValues[1],
          buildValues[3]));
      }
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(EntityBuild);
