import * as _ from 'lodash';
import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as actions from '../../actions/builds';
import EntityBuild from '../../components/builds/entityBuild';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { splitUniqueName } from '../../constants/utils';
import { getErrorsByIds } from '../../utils/errors';
import { getIsLoading } from '../../utils/isLoading';

export function mapStateToProps(state: AppState, params: any) {
  const isLoading = getIsLoading(state.loadingIndicators.builds.byIds, params.buildName, ACTIONS.GET);
  const errors = getErrorsByIds(state.alerts.builds.byIds, isLoading, params.buildName, ACTIONS.GET);
  return _.includes(state.builds.uniqueNames, params.buildName) ?
    {
      build: state.builds.byUniqueNames[params.buildName],
      showBookmarks: false,
      isLoading,
      errors,
    } :
    {
      build: null,
      showBookmarks: false,
      isLoading,
      errors,
    };
}

export interface DispatchProps {
  onDelete: (buildName: string) => actions.BuildAction;
  onStop: (buildName: string) => actions.BuildAction;
  onArchive: (buildName: string) => actions.BuildAction;
  onRestore: (buildName: string) => actions.BuildAction;
  bookmark: (buildName: string) => actions.BuildAction;
  unbookmark: (buildName: string) => actions.BuildAction;
  fetchData: () => actions.BuildAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.BuildAction>, params: any): DispatchProps {
  return {
    onDelete: (buildName: string) => dispatch(actions.deleteBuild(buildName)),
    onStop: (buildName: string) => dispatch(actions.stopBuild(buildName)),
    onArchive: (buildName: string) => dispatch(actions.archiveBuild(buildName, true)),
    onRestore: (buildName: string) => dispatch(actions.restoreBuild(buildName)),
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
