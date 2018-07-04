import { Reducer } from 'redux';
import { normalize } from 'normalizr';

import * as _ from 'lodash';

import { MetricsAction, actionTypes } from '../actions/metrics';
import { MetricStateSchema, MetricEmptyState, MetricModel } from '../models/metric';
import { MetricSchema } from '../constants/schemas';
import { LastFetchedIds } from '../models/utils';

export const MetricsReducer: Reducer<MetricStateSchema> =
  (state: MetricStateSchema = MetricEmptyState, action: MetricsAction) => {
    let newState = {...state};

    let processMetric = function (metric: MetricModel) {
      let id = metric.id;
      newState.lastFetched.ids.push(id);
      if (!_.includes(newState.ids, id)) {
        newState.ids.push(id);
      }
      let normalizedMetrics = normalize(metric, MetricSchema).entities.metrics;
      newState.byIds[id] = {
        ...newState.byIds[id], ...normalizedMetrics[id]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.REQUEST_METRICS:
        newState.lastFetched = new LastFetchedIds();
        return newState;
      case actionTypes.RECEIVE_METRICS:
        newState.lastFetched = new LastFetchedIds();
        newState.lastFetched.count = action.count;
        for (let build of action.metrics) {
          newState = processMetric(build);
        }
        return newState;
      default:
        return state;
    }
  };
