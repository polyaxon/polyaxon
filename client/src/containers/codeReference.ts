import * as _ from 'lodash';
import { connect } from 'react-redux';

import * as actions from '../actions/codeReference';
import CodeReference from '../components/codeReference';
import { AppState } from '../constants/types';

export interface Params {
  fetchData: () => actions.CodeReferenceAction;
  codeReferenceId: number;
}

export function mapStateToProps(state: AppState, params: Params) {
  return _.includes(state.codeReferences.ids, params.codeReferenceId) ?
  {
    codeReference: state.codeReferences.byIds[params.codeReferenceId],
    fetchData: params.fetchData
  } :
  {
    codeReference: null,
    fetchData: params.fetchData
  };
}

export default connect(mapStateToProps, {})(CodeReference);
