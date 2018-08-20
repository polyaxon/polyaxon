import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, MetricsAction } from '../actions/metrics';
import { MetricSchema } from '../constants/schemas';
import { MetricEmptyState, MetricModel, MetricStateSchema } from '../models/metric';
import { LastFetchedIds } from '../models/utils';

export const MetricsReducer: Reducer<MetricStateSchema> =
  (state: MetricStateSchema = MetricEmptyState, action: MetricsAction) => {
    let newState = {...state};

    const processMetric = function(metric: MetricModel) {
      const id = metric.id;
      newState.lastFetched.ids.push(id);
      if (!_.includes(newState.ids, id)) {
        newState.ids.push(id);
      }
      const normalizedMetrics = normalize(metric, MetricSchema).entities.metrics;
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
        for (const build of action.metrics) {
          newState = processMetric(build);
        }
        return newState;
      default:
        return state;
    }
  };
