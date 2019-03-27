import { connect } from 'react-redux';

import ViewsCreate from '../../components/metrics/viewsCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { getErrorsGlobal } from '../../utils/errors';
import { getSuccessGlobal } from '../../utils/success';

export interface Params {
  onCreate: (form: { name: string }) => void;
  onClose: () => void;
  name: string;
}

export function mapStateToProps(state: AppState, params: Params) {

  const isLoading = isTrue(state.loadingIndicators.chartViews.global.create);
  return {
    onCreate: params.onCreate,
    name: params.name,
    isLoading,
    errors: getErrorsGlobal(state.alerts.chartViews.global, isLoading, ACTIONS.CREATE),
    success: getSuccessGlobal(state.alerts.chartViews.global, isLoading, ACTIONS.CREATE),
  };
}

export default connect(mapStateToProps, {})(ViewsCreate);
