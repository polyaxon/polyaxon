import {connect} from "react-redux";

import RootModal from "../components/modal";
import {AppState} from "../constants/types";


export function mapStateToProps(state: AppState, ownProps: any) {
  return {modalProps: state.modal};
}

export default connect(mapStateToProps)(RootModal);
