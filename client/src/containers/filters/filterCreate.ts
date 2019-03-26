import { connect } from 'react-redux';

import FilterCreate from '../../components/filters/filterCreate';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';

export interface Params {
  onCreate: (form: { name: string, query: string, sort: string }) => void;
  onClose: () => void;
  query: string;
  sort: string;
}

export function mapStateToProps(state: AppState, params: Params) {

  return {
    onCreate: params.onCreate,
    query: params.query,
    sort: params.sort,
    isLoading: isTrue(state.loadingIndicators.searches.global.create),
    errors: state.errors.searches.global.create,
  };
}

export default connect(mapStateToProps, {})(FilterCreate);
