import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../actions/healthStatus';

import './healthStatus.less';

export interface Props {
  healthStatus: { [key: string]: any };
  fetchData: () => actions.HealthStatusAction;
}

export default class HealthStatus extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const services = [
      'Scheduler',
      'Crons',
      'Events',
      'Logs',
      'HPSearch',
      'Streams',
      'Postgres',
      'Rabbitmq',
      'Redis'
    ];
    const status: {[key: string]: boolean | null} = {
      Scheduler: null,
      Crons: null,
      Events: null,
      Logs: null,
      HPSearch: null,
      Streams: null,
      Postgres: null,
      Rabbitmq: null,
      Redis: null,
    };
    if (!_.isEmpty(this.props.healthStatus)) {
      status.Scheduler = this.props.healthStatus.SCHEDULER.is_healthy;
      status.Crons = this.props.healthStatus.CRONS.is_healthy;
      status.Events = this.props.healthStatus.EVENTS.is_healthy;
      status.Logs = this.props.healthStatus.LOGS.is_healthy;
      status.HPSearch = this.props.healthStatus.HPSEARCH.is_healthy;
      status.Streams = this.props.healthStatus.STREAMS.is_healthy;
      status.Postgres = this.props.healthStatus.POSTGRES.is_healthy;
      status.Rabbitmq = this.props.healthStatus.RABBITMQ.is_healthy;
      status.Redis = this.props.healthStatus.REDIS.is_healthy;
    }
    const getClassName = (isHealthy: boolean | null) => {
      if (isHealthy === null) {
        return 'status-unknown';
      } else if (isHealthy) {
        return 'status-healthy';
      } else {
        return 'status-unhealthy';
      }
    };
    return (
      <div className="jumbotron jumbotron-action health-status">
        {services.map((service) => (
          <div className={getClassName(status[service])}>
            <i className="fa fa-circle icon" aria-hidden="true"/> {service}
          </div>
        ))}
      </div>
    );
  }
}
