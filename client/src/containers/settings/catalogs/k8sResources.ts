import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../../actions/k8sResources';
import K8SResources from '../../../components/settings/catalogs/k8sResources/k8sResources';
import { ACTIONS } from '../../../constants/actions';
import { AppState } from '../../../constants/types';
import { isTrue } from '../../../constants/utils';
import { K8SResourceModel } from '../../../models/k8sResource';
import { getErrorsGlobal } from '../../../utils/errors';
import { getLastFetchedK8SResources } from '../../../utils/states';

interface Props extends RouteComponentProps<any> {
  resource: string;
  showDeleted: boolean;
}

export function mapStateToProps(state: AppState, props: Props) {
  const results = getLastFetchedK8SResources(state.k8sResources);
  const isLoading = isTrue(state.loadingIndicators.k8sResources.global.fetch);
  const errors = getErrorsGlobal(state.alerts.k8sResources.global, isLoading, ACTIONS.FETCH);
  return {
    resource: props.resource,
    showDeleted: props.showDeleted,
    k8sResources: results.k8sResources,
    count: results.count,
    isLoading,
    errors,
  };
}

export interface DispatchProps {
  onFetch: () => actions.K8SResourceAction;
  onDelete: (name: string) => actions.K8SResourceAction;
  onUpdate: (name: string, k8sResource: K8SResourceModel) => actions.K8SResourceAction;
  onCreate: (k8sResource: K8SResourceModel) => actions.K8SResourceAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.K8SResourceAction>, props: Props): DispatchProps {
  return {
    onFetch: () => dispatch(actions.fetchK8SResources(props.resource, '')),
    onDelete: (name: string) => dispatch(actions.deleteK8SResource(props.resource, '', name, false)),
    onUpdate: (name: string, k8sResource: K8SResourceModel) => dispatch(actions.updateK8SResource(
      props.resource, '', name, k8sResource)),
    onCreate: (k8sResource: K8SResourceModel) => dispatch(actions.createK8SResource(
      props.resource, k8sResource, '', false)),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(K8SResources));
