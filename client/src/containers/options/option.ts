import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/options';
import Option from '../../components/options/option';
import { AppState } from '../../constants/types';
import { OptionModel } from '../../models/option';

interface Props extends RouteComponentProps<any> {
  option: OptionModel;
}

export function mapStateToProps(state: AppState, props: Props) {
  return {option: props.option};
}

export interface DispatchProps {
  onSave: (option: { [key: string]: any }) => actions.OptionAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.OptionAction>, props: Props): DispatchProps {
  return {
    onSave: (option: { [key: string]: any }) => dispatch(actions.postOptions(option.key, option))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Option));
