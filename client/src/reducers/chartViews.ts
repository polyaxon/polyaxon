import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, ChartViewsAction } from '../actions/chartViews';
import { ACTIONS } from '../constants/actions';
import { chartViewSchema } from '../constants/schemas';
import { AlertEmptyState, AlertSchema, processErrorById, processErrorGlobal } from '../models/alerts';
import { ChartViewEmptyState, ChartViewModel, ChartViewStateSchema } from '../models/chartView';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
import { LastFetchedIds } from '../models/utils';

export const chartViewsReducer: Reducer<ChartViewStateSchema> =
  (state: ChartViewStateSchema = ChartViewEmptyState, action: ChartViewsAction) => {
    let newState = {...state};

    const processChartView = (chartView: ChartViewModel) => {
      newState.lastFetched.ids.push(chartView.id);
      if (!_.includes(newState.ids, chartView.id)) {
        newState.ids.push(chartView.id);
      }
      const normalizedBuilds = normalize(chartView, chartViewSchema).entities.chartViews;
      newState.byIds[chartView.id] = {
        ...newState.byIds[chartView.id], ...normalizedBuilds[chartView.id]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.FETCH_CHART_VIEWS_REQUEST:
        newState.lastFetched = new LastFetchedIds();
        return newState;
      case actionTypes.GET_CHART_VIEW_SUCCESS:
        return processChartView(action.chartView);
      case actionTypes.DELETE_CHART_VIEW_SUCCESS:
        return {
          ...state,
          ids: state.ids.filter(
            (id) => id !== action.viewId),
          lastFetched: {
            ...state.lastFetched,
            ids: state.lastFetched.ids.filter(
              (id) => id !== action.viewId)
          },
        };
      case actionTypes.FETCH_CHART_VIEWS_SUCCESS:
        newState.lastFetched = new LastFetchedIds();
        newState.lastFetched.count = action.count;
        for (const search of action.chartViews) {
          newState = processChartView(search);
        }
        return newState;
      default:
        return state;
    }
  };

export const LoadingIndicatorChartViewReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: ChartViewsAction) => {
    switch (action.type) {
      case actionTypes.GET_CHART_VIEW_REQUEST:
        return {
          ...state,
          chartViews: processLoadingIndicatorGlobal(
            processLoadingIndicatorById(state.chartViews, action.viewId, true, ACTIONS.GET),
            false,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_CHART_VIEW_ERROR:
      case actionTypes.GET_CHART_VIEW_SUCCESS:
        return {
          ...state,
          chartViews: processLoadingIndicatorById(state.chartViews, action.viewId, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_CHART_VIEW_REQUEST:
        return {
          ...state,
          chartViews: processLoadingIndicatorById(state.chartViews, action.viewId, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_CHART_VIEW_ERROR:
      case actionTypes.DELETE_CHART_VIEW_SUCCESS:
        return {
          ...state,
          chartViews: processLoadingIndicatorById(state.chartViews, action.viewId, false, ACTIONS.DELETE)
        };

      case actionTypes.FETCH_CHART_VIEWS_REQUEST:
        return {
          ...state,
          chartViews: processLoadingIndicatorGlobal(state.chartViews, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_CHART_VIEWS_ERROR:
      case actionTypes.FETCH_CHART_VIEWS_SUCCESS:
        return {
          ...state,
          chartViews: processLoadingIndicatorGlobal(state.chartViews, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_CHART_VIEW_REQUEST:
        return {
          ...state,
          chartViews: processLoadingIndicatorGlobal(state.chartViews, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_CHART_VIEW_ERROR:
      case actionTypes.CREATE_CHART_VIEW_SUCCESS:
        return {
          ...state,
          chartViews: processLoadingIndicatorGlobal(state.chartViews, false, ACTIONS.CREATE)
        };
      default:
        return state;
    }
  };

export const AlertChartViewReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: ChartViewsAction) => {
    switch (action.type) {
      case actionTypes.GET_CHART_VIEW_REQUEST:
        return {
          ...state,
          chartViews: processErrorGlobal(
            processErrorById(state.chartViews, action.viewId, null, null, ACTIONS.GET),
            null,
            null,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_CHART_VIEW_SUCCESS:
        return {
          ...state,
          chartViews: processErrorById(state.chartViews, action.viewId, null, true, ACTIONS.GET)
        };
      case actionTypes.GET_CHART_VIEW_ERROR:
        return {
          ...state,
          chartViews: processErrorById(state.chartViews, action.viewId, action.error, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_CHART_VIEW_REQUEST:
        return {
          ...state,
          chartViews: processErrorById(state.chartViews, action.viewId, null, null, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_CHART_VIEW_SUCCESS:
        return {
          ...state,
          chartViews: processErrorById(state.chartViews, action.viewId, null, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_CHART_VIEW_ERROR:
        return {
          ...state,
          chartViews: processErrorById(state.chartViews, action.viewId, action.error, false, ACTIONS.DELETE)
        };

      case actionTypes.FETCH_CHART_VIEWS_REQUEST:
        return {
          ...state,
          chartViews: processErrorGlobal(state.chartViews, null, false, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_CHART_VIEWS_SUCCESS:
        return {
          ...state,
          chartViews: processErrorGlobal(state.chartViews, null, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_CHART_VIEWS_ERROR:
        return {
          ...state,
          chartViews: processErrorGlobal(state.chartViews, action.error, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_CHART_VIEW_REQUEST:
        return {
          ...state,
          chartViews: processErrorGlobal(state.chartViews, null, null, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_CHART_VIEW_SUCCESS:
        return {
          ...state,
          chartViews: processErrorGlobal(state.chartViews, null, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_CHART_VIEW_ERROR:
        return {
          ...state,
          chartViews: processErrorGlobal(state.chartViews, action.error, false, ACTIONS.CREATE)
        };
      default:
        return state;
    }
  };
