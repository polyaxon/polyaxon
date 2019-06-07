import * as _ from 'lodash';
import { connect } from 'react-redux';

import * as actions from '../actions/codeReference';
import CodeReference from '../components/codeReference';
import { AppState } from '../constants/types';

export interface Props {
  fetchData: () => actions.CodeReferenceAction;
  codeReferenceId: number;
}

export function mapStateToProps(state: AppState, props: Props) {
  return _.includes(state.codeReferences.ids, props.codeReferenceId) ?
  {
    codeReference: state.codeReferences.byIds[props.codeReferenceId],
    fetchData: props.fetchData
  } :
  {
    codeReference: null,
    fetchData: props.fetchData
  };
}

export default connect(mapStateToProps, {})(CodeReference);
