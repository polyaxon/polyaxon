import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/options';
import Option from '../../components/options/option';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { OptionModel } from '../../models/option';
import { getErrorsByIds } from '../../utils/errors';
import { getIsLoading } from '../../utils/isLoading';
import { getSuccessByIds } from '../../utils/success';

interface Props extends RouteComponentProps<any> {
  option: OptionModel;
}

export function mapStateToProps(state: AppState, props: Props) {
  const isLoading = getIsLoading(state.loadingIndicators.options.byIds, props.option.key, ACTIONS.UPDATE);
  const errors = getErrorsByIds(state.alerts.options.byIds, isLoading, props.option.key, ACTIONS.UPDATE);
  const success = getSuccessByIds(state.alerts.options.byIds, isLoading, props.option.key, ACTIONS.UPDATE);
  return {option: props.option, isLoading, errors, success};
}

export interface DispatchProps {
  onSave: (option: { [key: string]: any }) => actions.OptionAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.OptionAction>, props: Props): DispatchProps {
  return {
    onSave: (option: { [key: string]: any }) => dispatch(actions.postOptions(props.option.key, option))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Option));
