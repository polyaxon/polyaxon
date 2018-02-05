import { connect } from 'react-redux';

import { AppState } from '../constants/types';
import Token from '../components/token';

export function mapStateToProps(state: AppState, ownProps: any)  {
  return {token: state.auth.token};
}

export default connect(mapStateToProps)(Token);
