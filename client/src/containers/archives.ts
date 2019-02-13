import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';

import Archives from '../components/archives';
import { AppState } from '../constants/types';

export function mapStateToProps(state: AppState, params: any) {
  return {user: params.match.params.user};
}

export default withRouter(connect(mapStateToProps, {})(Archives));
