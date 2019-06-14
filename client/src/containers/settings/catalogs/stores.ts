import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../../actions/stores';
import Stores from '../../../components/settings/catalogs/stores/stores';
import { ACTIONS } from '../../../constants/actions';
import { AppState } from '../../../constants/types';
import { isTrue } from '../../../constants/utils';
import { StoreModel } from '../../../models/store';
import { getErrorsGlobal } from '../../../utils/errors';
import { getLastFetchedStores } from '../../../utils/states';

interface Props extends RouteComponentProps<any> {
  resource: string;
  showDeleted: boolean;
}

export function mapStateToProps(state: AppState, props: Props) {
  const results = getLastFetchedStores(state.stores);
  const isLoading = isTrue(state.loadingIndicators.stores.global.fetch);
  const errors = getErrorsGlobal(state.alerts.stores.global, isLoading, ACTIONS.FETCH);
  return {
    resource: props.resource,
    showDeleted: props.showDeleted,
    stores: results.stores,
    count: results.count,
    isLoading,
    errors,
  };
}

export interface DispatchProps {
  onFetch: () => actions.StoreAction;
  onDelete: (name: string) => actions.StoreAction;
  onUpdate: (name: string, k8sResource: StoreModel) => actions.StoreAction;
  onCreate: (k8sResource: StoreModel) => actions.StoreAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.StoreAction>, props: Props): DispatchProps {
  return {
    onFetch: () => dispatch(actions.fetchStores(props.resource, '')),
    onDelete: (name: string) => dispatch(actions.deleteStore(props.resource, '', name, false)),
    onUpdate: (name: string, store: StoreModel) => dispatch(actions.updateStore(
      props.resource, '', name, store)),
    onCreate: (store: StoreModel) => dispatch(actions.createStore(
      props.resource, store, '', false)),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Stores));
