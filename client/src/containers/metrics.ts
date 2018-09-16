import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import { AppState } from '../constants/types';
import { MetricModel } from '../models/metric';

import * as actions from '../actions/metrics';
import Metrics from '../components/experiments/metrics';
import { ChartViewModel } from '../models/chartView';

export function mapStateToProps(state: AppState, params: any) {
  const useLastFetched = () => {
    const metricIds = state.metrics.lastFetched.ids;
    const count = state.metrics.lastFetched.count;
    const metrics: MetricModel[] = [];
    metricIds.forEach(
      (metricId: number, idx: number) => {
        metrics.push(state.metrics.byIds[metricId]);
      });
    return {metrics, count};
  };
  const results = useLastFetched();

  return {
    metrics: results.metrics,
    count: results.count
  };
}

export interface DispatchProps {
  fetchData?: () => actions.MetricsAction;
  fetchViews?: () => actions.MetricsAction;
  createView?: (data: ChartViewModel) => actions.MetricsAction;
  deleteView?: (viewId: number) => actions.MetricsAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.MetricsAction>, params: any): DispatchProps {
  return {
    fetchData: () => {
      return dispatch(actions.fetchMetrics(params.project, params.resource, params.id));
    },
    fetchViews: () => {
      return dispatch(actions.fetchChartViews(params.project, params.resource, params.id));
    },
    createView: (data: ChartViewModel) => {
      return dispatch(actions.createChartView(params.project, params.resource, params.id, data));
    },
    deleteView: (viewId: number) => {
      return dispatch(actions.deleteChartView(params.project, params.resource, params.id, viewId));
    },
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Metrics);
