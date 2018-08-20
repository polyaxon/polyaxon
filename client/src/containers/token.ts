import { connect } from 'react-redux';

import Token from '../components/token';
import { AppState } from '../constants/types';

export function mapStateToProps(state: AppState, ownProps: any)  {
  return {token: state.auth.token};
}

export default connect(mapStateToProps)(Token);
