import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as actions from '../actions/outputs';
import Outputs from '../components/outputs/outputs';
import { AppState } from '../constants/types';
import { downloadName, outputsDownloadUrl } from '../utils/downloads';

export function mapStateToProps(state: AppState, params: any) {
  return {
    outputsTree: state.outputs.outputsTree,
    outputsFiles: state.outputs.outputsFiles,
    downloadOutputsUrl: outputsDownloadUrl(params.project, params.resource, params.id),
    downloadOutputsName: downloadName(params.project, params.resource, params.id),
  };
}

export interface DispatchProps {
  fetchOutputsTree: (path: string) => actions.OutputsAction;
  fetchOutputsFiles: (path: string, filetype: string) => actions.OutputsAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.OutputsAction>, params: any): DispatchProps {
  return {
    fetchOutputsTree: (path: string) => dispatch(
      actions.fetchOutputsTree(params.project, params.resource, params.id, path)),
    fetchOutputsFiles: (path: string, filetype: string) => dispatch(
      actions.fetchOutputsFile(params.project, params.resource, params.id, path, filetype))
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Outputs);
