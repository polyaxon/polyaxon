import { connect } from 'react-redux';

import FilterCreate from '../../components/filters/filterCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { getErrorsGlobal } from '../../utils/errors';

export interface Params {
  onCreate: (form: { name: string, query: string, sort: string }) => void;
  query: string;
  sort: string;
}

export function mapStateToProps(state: AppState, params: Params) {

  const isLoading = isTrue(state.loadingIndicators.searches.global.create);
  return {
    onCreate: params.onCreate,
    query: params.query,
    sort: params.sort,
    isLoading,
    errors: getErrorsGlobal(state.alerts.searches.global, isLoading, ACTIONS.CREATE),
  };
}

export default connect(mapStateToProps, {})(FilterCreate);
