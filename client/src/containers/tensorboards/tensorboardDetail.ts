import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import { AppState } from '../../constants/types';

import * as actions from '../../actions/tensorboard';
import TensorboardDetail from '../../components/tensorboards/tensorboardDetail';
import { getTensorboardUniqueName } from '../../constants/utils';

export function mapStateToProps(state: AppState, params: any) {
  const tensorboardUniqueName = getTensorboardUniqueName(
    params.match.params.user,
    params.match.params.projectName,
    params.match.params.tensorboardId);
  return _.includes(state.tensorboards.uniqueNames, tensorboardUniqueName) ?
    {tensorboard: state.tensorboards.byUniqueNames[tensorboardUniqueName]} :
    {tensorboard: null};
}

export interface DispatchProps {
  onUpdate: (updateDict: { [key: string]: any }) => actions.TensorboardAction;
  onDelete: () => actions.TensorboardAction;
  onStop: () => actions.TensorboardAction;
  onArchive: () => actions.TensorboardAction;
  onRestore: () => actions.TensorboardAction;
  fetchData?: () => actions.TensorboardAction;
  bookmark: () => actions.TensorboardAction;
  unbookmark: () => actions.TensorboardAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.TensorboardAction>, params: any): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchTensorboard(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.tensorboardId)),
    onUpdate: (updateDict: { [key: string]: any }) => dispatch(
      actions.updateTensorboard(
        getTensorboardUniqueName(
          params.match.params.user,
          params.match.params.projectName,
          params.match.params.tensorboardId),
        updateDict)),
    onDelete: () => dispatch(actions.deleteTensorboard(
      getTensorboardUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.tensorboardId),
      true)),
    onStop: () => dispatch(actions.stopTensorboard(getTensorboardUniqueName(
      params.match.params.user,
      params.match.params.projectName,
      params.match.params.tensorboardId))),
    onArchive: () => dispatch(actions.archiveTensorboard(getTensorboardUniqueName(
      params.match.params.user,
      params.match.params.projectName,
      params.match.params.tensorboardId),
      true)),
    onRestore: () => dispatch(actions.restoreTensorboard(getTensorboardUniqueName(
      params.match.params.user,
      params.match.params.projectName,
      params.match.params.tensorboardId))),
    bookmark: () => dispatch(
      actions.bookmark(getTensorboardUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.tensorboardId))),
    unbookmark: () => dispatch(
      actions.unbookmark(getTensorboardUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.tensorboardId))),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(TensorboardDetail));
