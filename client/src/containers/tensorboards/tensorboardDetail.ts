import * as _ from 'lodash';
import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import { AppState } from '../../constants/types';

import * as actions from '../../actions/tensorboards';
import TensorboardDetail from '../../components/tensorboards/tensorboardDetail';
import { getTensorboardUniqueName } from '../../constants/utils';

interface Props extends RouteComponentProps<any> {}

export function mapStateToProps(state: AppState, props: Props) {
  const tensorboardUniqueName = getTensorboardUniqueName(
    props.match.params.user,
    props.match.params.projectName,
    props.match.params.tensorboardId);
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

export function mapDispatchToProps(dispatch: Dispatch<actions.TensorboardAction>, props: Props): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchTensorboard(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.tensorboardId)),
    onUpdate: (updateDict: { [key: string]: any }) => dispatch(
      actions.updateTensorboard(
        getTensorboardUniqueName(
          props.match.params.user,
          props.match.params.projectName,
          props.match.params.tensorboardId),
        updateDict)),
    onDelete: () => dispatch(actions.deleteTensorboard(
      getTensorboardUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.tensorboardId),
      true)),
    onStop: () => dispatch(actions.stopTensorboard(getTensorboardUniqueName(
      props.match.params.user,
      props.match.params.projectName,
      props.match.params.tensorboardId))),
    onArchive: () => dispatch(actions.archiveTensorboard(getTensorboardUniqueName(
      props.match.params.user,
      props.match.params.projectName,
      props.match.params.tensorboardId),
      true)),
    onRestore: () => dispatch(actions.restoreTensorboard(getTensorboardUniqueName(
      props.match.params.user,
      props.match.params.projectName,
      props.match.params.tensorboardId))),
    bookmark: () => dispatch(
      actions.bookmark(getTensorboardUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.tensorboardId))),
    unbookmark: () => dispatch(
      actions.unbookmark(getTensorboardUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.tensorboardId))),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(TensorboardDetail));
