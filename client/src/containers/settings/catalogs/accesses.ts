import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../../actions/access';
import * as optionActions from '../../../actions/options';
import Accesses from '../../../components/settings/catalogs/accesses/accesses';
import { ACTIONS } from '../../../constants/actions';
import { AppState } from '../../../constants/types';
import { isTrue } from '../../../constants/utils';
import { AccessModel } from '../../../models/access';
import { ACCESS_GIT, ACCESS_REGISTRY } from '../../../options/access';
import { getErrorsGlobal } from '../../../utils/errors';
import { getLastFetchedAccesses } from '../../../utils/states';

interface Props extends RouteComponentProps<any> {
  resource: string;
  showDeleted: boolean;
}

export function mapStateToProps(state: AppState, props: Props) {
  const results = getLastFetchedAccesses(state.accesses);
  const isLoading = isTrue(state.loadingIndicators.accesses.global.fetch);
  const errors = getErrorsGlobal(state.alerts.accesses.global, isLoading, ACTIONS.FETCH);
  return {
    resource: props.resource,
    showDeleted: props.showDeleted,
    accesses: results.accesses,
    count: results.count,
    isLoading,
    errors,
  };
}

export interface DispatchProps {
  onFetch: () => actions.AccessAction;
  onDelete: (name: string) => actions.AccessAction;
  onUpdate: (name: string, k8sResource: AccessModel) => actions.AccessAction;
  onCreate: (k8sResource: AccessModel) => actions.AccessAction;
  onMakeDefault: (id: string | number) => optionActions.OptionAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.AccessAction | optionActions.OptionAction>,
                                   props: Props): DispatchProps {
  return {
    onFetch: () => dispatch(actions.fetchAccesses(props.resource, '')),
    onDelete: (name: string) => dispatch(actions.deleteAccess(props.resource, '', name, false)),
    onUpdate: (name: string, access: AccessModel) => dispatch(actions.updateAccess(
      props.resource, '', name, access)),
    onCreate: (access: AccessModel) => dispatch(actions.createAccess(
      props.resource, access, '', false)),
    onMakeDefault: (id: string | number) => {
      const optionKey = props.resource === 'git_access' ? ACCESS_GIT : ACCESS_REGISTRY;
      const options: { [key: string]: any } = {};
      options[optionKey] = id;
      return dispatch(optionActions.postOptions('access', options));
    }
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Accesses));
