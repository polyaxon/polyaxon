import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../../actions/access';
import * as k8sResourcesActions from '../../../actions/k8sResources';
import AccessFrom from '../../../components/settings/catalogs/accesses/accessFrom';
import { ACTIONS } from '../../../constants/actions';
import { AppState } from '../../../constants/types';
import { isTrue } from '../../../constants/utils';
import { AccessModel } from '../../../models/access';
import { getErrorsByIds, getErrorsGlobal } from '../../../utils/errors';
import { getIsLoading } from '../../../utils/isLoading';
import { getLastFetchedK8SResources } from '../../../utils/states';
import { getSuccessByIds, getSuccessGlobal } from '../../../utils/success';

interface Props extends RouteComponentProps<any> {
  resource: string;
  access?: AccessModel;
  onCancel: () => void;
}

export function mapStateToProps(state: AppState, props: Props) {
  let isLoading = false;
  let errors = null;
  let success: boolean | null = false;
  if (props.access) {
    const name = props.access.name;
    isLoading = getIsLoading(state.loadingIndicators.accesses.byIds, name, ACTIONS.UPDATE);
    errors = getErrorsByIds(state.alerts.accesses.byIds, isLoading, name, ACTIONS.UPDATE);
    success = getSuccessByIds(state.alerts.accesses.byIds, isLoading, name, ACTIONS.UPDATE);
  } else {
    isLoading = isTrue(state.loadingIndicators.accesses.global.create);
    errors = getErrorsGlobal(state.alerts.accesses.global, isLoading, ACTIONS.CREATE);
    success = getSuccessGlobal(state.alerts.accesses.global, isLoading, ACTIONS.CREATE);
  }
  const secrets = getLastFetchedK8SResources(state.k8sResources).k8sResources;
  return {
    resource: props.resource,
    access: props.access,
    isLoading,
    errors,
    success,
    secrets,
  };
}

export interface DispatchProps {
  onUpdate: (name: string, access: AccessModel) => actions.AccessAction;
  onCreate: (access: AccessModel) => actions.AccessAction;
  initState: (name: string) => actions.AccessAction;
  fetchSecrets: () => k8sResourcesActions.K8SResourceAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.AccessAction>, props: Props): DispatchProps {
  return {
    onUpdate: (name: string, access: AccessModel) => dispatch(actions.updateAccess(
      props.resource, '', name, access)),
    onCreate: (access: AccessModel) => dispatch(actions.createAccess(
      props.resource, access, '', false)),
    initState: (name: string) => dispatch(actions.initAccessState(props.resource, name)),
    fetchSecrets: () => dispatch(k8sResourcesActions.fetchK8SResourcesNames('k8s_secrets', ''))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(AccessFrom));
