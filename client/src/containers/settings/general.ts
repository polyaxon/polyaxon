import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/options';
import GeneralSettings from '../../components/settings/general';
import { AppState } from '../../constants/types';
import { OptionModel } from '../../models/option';

interface Props extends RouteComponentProps<any> {
  section: string;
  options: string[];
}

export function mapStateToProps(state: AppState, props: Props) {
  const options: OptionModel[] = [];
  props.options.forEach(
    (key: string, idx: number) => {
      if (key in state.options.byUniqueNames) {
        options.push(state.options.byUniqueNames[key]);
      }
    });
  return {section: props.section, options};
}

export interface DispatchProps {
  onFetch: () => actions.OptionAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.OptionAction>, props: Props): DispatchProps {
  return {
    onFetch: () => dispatch(actions.fetchOptions(props.section, props.options))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(GeneralSettings));
