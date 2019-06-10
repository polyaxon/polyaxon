import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/options';
import KeyOption from '../../components/settings/keyOption';
import { AppState } from '../../constants/types';

interface Props extends RouteComponentProps<any> {
}

export function mapStateToProps(state: AppState, props: Props) {
  return {};
}

export interface DispatchProps {
  onSave: (option: { [key: string]: any }) => actions.OptionAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.OptionAction>, props: Props): DispatchProps {
  return {
    onSave: (option: { [key: string]: any }) => dispatch(actions.postOptions(option.key, option))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(KeyOption));
