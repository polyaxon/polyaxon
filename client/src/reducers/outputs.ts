import { Reducer } from 'redux';

import { actionTypes, OutputsAction } from '../actions/outputs';
import { ACTIONS } from '../constants/actions';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById
} from '../models/loadingIndicator';
import { OutputsEmptyState, OutputsModel, OutputsNode } from '../models/outputs';

export const outputsReducer: Reducer<OutputsModel> =
  (state: OutputsModel = OutputsEmptyState, action: OutputsAction) => {
    switch (action.type) {

      case actionTypes.FETCH_OUTPUTS_TREE_REQUEST:
        let reqOutputsNode: OutputsNode;
        let reqOutputsFiles: { [key: string]: string };
        if (!action.path) {
          reqOutputsNode = new OutputsNode(true, '', true, '', {});
          reqOutputsFiles = {};
          reqOutputsNode.setChildren(action.path, [], []);
          return {
            ...state,
            outputsTree: {root: reqOutputsNode},
            reqOutputsFiles
          };
        } else {
          return state;
        }
      case actionTypes.FETCH_OUTPUTS_FILE_SUCCESS:
        const newFiles: { [key: string]: string } = {};
        newFiles[action.path] = action.outputsFile;
        return {
          ...state,
          outputsFiles: {...state.outputsFiles, ...newFiles}
        };
      case actionTypes.FETCH_OUTPUTS_TREE_SUCCESS:
        let outputsNode: OutputsNode;
        let outputsFiles: { [key: string]: string };
        if (!action.path) {
          outputsNode = new OutputsNode(true, '', true, '', {});
          outputsFiles = {};
          outputsNode.setChildren(action.path, action.outputsTree.files, action.outputsTree.dirs);
        } else {
          outputsNode = state.outputsTree.root.deepCopy();
          outputsFiles = state.outputsFiles;
        }
        if (action.path) {
          const node = OutputsNode.findChild(outputsNode, action.path);
          if (node) {
            const _node = node as OutputsNode;
            _node.setChildren(action.path, action.outputsTree.files, action.outputsTree.dirs);
          }
        }

        return {
          ...state,
          outputsTree: {root: outputsNode},
          outputsFiles
        };
      default:
        return state;
    }
  };

export const LoadingIndicatorOutputsReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: OutputsAction) => {
    switch (action.type) {
      case actionTypes.FETCH_OUTPUTS_FILE_REQUEST:
        return {
          ...state,
          chartViews: processLoadingIndicatorById(state.chartViews, action.path, true, ACTIONS.GET)
        };
      case actionTypes.FETCH_OUTPUTS_FILE_ERROR:
      case actionTypes.FETCH_OUTPUTS_FILE_SUCCESS:
        return {
          ...state,
          chartViews: processLoadingIndicatorById(state.chartViews, action.path, false, ACTIONS.GET)
        };

      case actionTypes.FETCH_OUTPUTS_TREE_REQUEST:
        return {
          ...state,
          chartViews: processLoadingIndicatorById(state.chartViews, action.path, true, ACTIONS.GET)
        };
      case actionTypes.FETCH_OUTPUTS_TREE_ERROR:
      case actionTypes.FETCH_OUTPUTS_TREE_SUCCESS:
        return {
          ...state,
          chartViews: processLoadingIndicatorById(state.chartViews, action.path, false, ACTIONS.GET)
        };

      default:
        return state;
    }
  };
