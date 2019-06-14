import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../../actions/k8sResources';
import K8SResourceFrom from '../../../components/settings/catalogs/k8sResources/k8sResourceFrom';
import { ACTIONS } from '../../../constants/actions';
import { AppState } from '../../../constants/types';
import { isTrue } from '../../../constants/utils';
import { K8SResourceModel } from '../../../models/k8sResource';
import { getErrorsByIds, getErrorsGlobal } from '../../../utils/errors';
import { getIsLoading } from '../../../utils/isLoading';
import { getSuccessByIds, getSuccessGlobal } from '../../../utils/success';

interface Props extends RouteComponentProps<any> {
  resource: string;
  k8sResource?: K8SResourceModel;
  onCancel: () => void;
}

export function mapStateToProps(state: AppState, props: Props) {
  let isLoading = false;
  let errors = null;
  let success: boolean | null = false;
  if (props.k8sResource) {
    const name = props.k8sResource.name;
    isLoading = getIsLoading(state.loadingIndicators.k8sResources.byIds, name, ACTIONS.UPDATE);
    errors = getErrorsByIds(state.alerts.k8sResources.byIds, isLoading, name, ACTIONS.UPDATE);
    success = getSuccessByIds(state.alerts.k8sResources.byIds, isLoading, name, ACTIONS.UPDATE);
  } else {
    isLoading = isTrue(state.loadingIndicators.k8sResources.global.create);
    errors = getErrorsGlobal(state.alerts.k8sResources.global, isLoading, ACTIONS.CREATE);
    success = getSuccessGlobal(state.alerts.k8sResources.global, isLoading, ACTIONS.CREATE);
  }
  return {
    resource: props.resource,
    k8sResource: props.k8sResource,
    isLoading,
    errors,
    success,
  };
}

export interface DispatchProps {
  onUpdate: (name: string, k8sResource: K8SResourceModel) => actions.K8SResourceAction;
  onCreate: (k8sResource: K8SResourceModel) => actions.K8SResourceAction;
  initState: (name: string) => actions.K8SResourceAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.K8SResourceAction>, props: Props): DispatchProps {
  return {
    onUpdate: (name: string, k8sResource: K8SResourceModel) => dispatch(actions.updateK8SResource(
      props.resource, '', name, k8sResource)),
    onCreate: (k8sResource: K8SResourceModel) => dispatch(actions.createK8SResource(
      props.resource, k8sResource, '', false)),
    initState: (name: string) => dispatch(actions.initK8SResourceState(props.resource, name)),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(K8SResourceFrom));
