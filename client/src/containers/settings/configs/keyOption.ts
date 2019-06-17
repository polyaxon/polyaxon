import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../../actions/options';
import KeyOption from '../../../components/settings/configs/keyOption';
import { ACTIONS } from '../../../constants/actions';
import { AppState } from '../../../constants/types';
import { getErrorsByIds } from '../../../utils/errors';
import { getIsLoading } from '../../../utils/isLoading';
import { getSuccessByIds } from '../../../utils/success';

interface Props extends RouteComponentProps<any> {
}

export function mapStateToProps(state: AppState, props: Props) {
  const isLoading = getIsLoading(state.loadingIndicators.options.byIds, 'keyOption', ACTIONS.UPDATE);
  const errors = getErrorsByIds(state.alerts.options.byIds, isLoading, 'keyOption', ACTIONS.UPDATE);
  const success = getSuccessByIds(state.alerts.options.byIds, isLoading, 'keyOption', ACTIONS.UPDATE);
  return {
    isLoading,
    errors,
    success,
  };
}

export interface DispatchProps {
  onSave: (option: { [key: string]: any }) => actions.OptionAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.OptionAction>, props: Props): DispatchProps {
  return {
    onSave: (option: { [key: string]: any }) => dispatch(actions.postOptions('keyOption', option))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(KeyOption));
