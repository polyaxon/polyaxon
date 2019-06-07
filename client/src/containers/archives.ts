import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';

import Archives from '../components/archives';
import { AppState } from '../constants/types';

interface Props extends RouteComponentProps<any> {}

export function mapStateToProps(state: AppState, props: Props) {
  return {user: props.match.params.user};
}

export default withRouter(connect(mapStateToProps, {})(Archives));
