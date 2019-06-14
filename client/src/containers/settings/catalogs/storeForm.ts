import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as k8sResourcesActions from '../../../actions/k8sResources';
import * as actions from '../../../actions/stores';
import StoreFrom from '../../../components/settings/catalogs/stores/storeFrom';
import { ACTIONS } from '../../../constants/actions';
import { AppState } from '../../../constants/types';
import { isTrue } from '../../../constants/utils';
import { StoreModel } from '../../../models/store';
import { getErrorsByIds, getErrorsGlobal } from '../../../utils/errors';
import { getIsLoading } from '../../../utils/isLoading';
import { getLastFetchedK8SResources } from '../../../utils/states';
import { getSuccessByIds, getSuccessGlobal } from '../../../utils/success';

interface Props extends RouteComponentProps<any> {
  resource: string;
  cstore?: StoreModel;
  onCancel: () => void;
}

export function mapStateToProps(state: AppState, props: Props) {
  let isLoading = false;
  let errors = null;
  let success: boolean | null = false;
  if (props.cstore) {
    const name = props.cstore.name;
    isLoading = getIsLoading(state.loadingIndicators.stores.byIds, name, ACTIONS.UPDATE);
    errors = getErrorsByIds(state.alerts.stores.byIds, isLoading, name, ACTIONS.UPDATE);
    success = getSuccessByIds(state.alerts.stores.byIds, isLoading, name, ACTIONS.UPDATE);
  } else {
    isLoading = isTrue(state.loadingIndicators.stores.global.create);
    errors = getErrorsGlobal(state.alerts.stores.global, isLoading, ACTIONS.CREATE);
    success = getSuccessGlobal(state.alerts.stores.global, isLoading, ACTIONS.CREATE);
  }
  const secrets = getLastFetchedK8SResources(state.k8sResources).k8sResources;
  return {
    resource: props.resource,
    cstore: props.cstore,
    isLoading,
    errors,
    success,
    secrets,
  };
}

export interface DispatchProps {
  onUpdate: (name: string, store: StoreModel) => actions.StoreAction;
  onCreate: (store: StoreModel) => actions.StoreAction;
  initState: (name: string) => actions.StoreAction;
  fetchSecrets: () => k8sResourcesActions.K8SResourceAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.StoreAction>, props: Props): DispatchProps {
  return {
    onUpdate: (name: string, store: StoreModel) => dispatch(actions.updateStore(
      props.resource, '', name, store)),
    onCreate: (store: StoreModel) => dispatch(actions.createStore(
      props.resource, store, '', false)),
    initState: (name: string) => dispatch(actions.initStoreState(props.resource, name)),
    fetchSecrets: () => dispatch(k8sResourcesActions.fetchK8SResourcesNames('k8s_secrets', ''))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(StoreFrom));
