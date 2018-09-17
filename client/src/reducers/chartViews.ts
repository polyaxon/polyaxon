import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, MetricsAction } from '../actions/metrics';
import { chartViewSchema } from '../constants/schemas';
import {
  ChartViewEmptyState,
  ChartViewModel,
  ChartViewStateSchema
} from '../models/chartView';
import { LastFetchedIds } from '../models/utils';

export const chartViewsReducer: Reducer<ChartViewStateSchema> =
  (state: ChartViewStateSchema = ChartViewEmptyState, action: MetricsAction) => {
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
      case actionTypes.REQUEST_CHART_VIEWS:
        newState.lastFetched = new LastFetchedIds();
        return newState;
      case actionTypes.RECEIVE_CHART_VIEW:
        return processChartView(action.chartView);
      case actionTypes.DELETE_CHART_VIEW:
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
      case actionTypes.RECEIVE_CHART_VIEWS:
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
