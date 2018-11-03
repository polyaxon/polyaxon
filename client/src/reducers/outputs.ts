import { Reducer } from 'redux';

import { actionTypes, OutputsAction } from '../actions/outputs';
import { OutputsEmptyState, OutputsModel, OutputsNode } from '../models/outputs';

export const outputsReducer: Reducer<OutputsModel> =
  (state: OutputsModel = OutputsEmptyState, action: OutputsAction) => {
    switch (action.type) {

      case actionTypes.RECEIVE_OUTPUTS_TREE:
        let outputsNode: OutputsNode;
        if (!action.path) {
          outputsNode = new OutputsNode(true, '', true, '', {});
          outputsNode.setChildren(action.path, action.outputsTree.files, action.outputsTree.dirs);
        } else {
          outputsNode = state.outputsTree.root.deepCopy();
        }
        if (action.path) {
          const pathParts = action.path.split('/');
          let curoutputsNode = outputsNode;
          let currentPath = '';
          pathParts.forEach((part) => {
            currentPath = currentPath ? `${currentPath}/${part}` : part;
            if (curoutputsNode.children) {
              curoutputsNode = curoutputsNode.children[currentPath];
            }
          });
          curoutputsNode.setChildren(action.path, action.outputsTree.files, action.outputsTree.dirs);
        }

        return {
          ...state,
          outputsTree: {root : outputsNode},
        };
      default:
        return state;
    }
  };
