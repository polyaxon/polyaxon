import * as React from 'react';
import * as _ from 'lodash';

import { ExperimentModel } from '../models/experiment';
import ExperimentJobs from '../containers/experimentJobs';
import Logs from '../containers/logs';
import {
  getExperimentUrl,
  getGroupUrl,
  getProjectUrl,
  getUserUrl,
  splitGroupName,
  splitProjectName,
} from '../constants/utils';
import Breadcrumb from './breadcrumb';
import LinkedTab from './linkedTab';
import ExperimentOverview from './experimentOverview';

export interface Props {
  experiment: ExperimentModel;
  onDelete: () => any;
  fetchData: () => any;
}

export default class ExperimentDetail extends React.Component<Props, Object> {
  componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const experiment = this.props.experiment;

    if (_.isNil(experiment)) {
      return (<div>Nothing</div>);
    }
    let values = splitProjectName(experiment.project_name);
    let exerimentUrl = getExperimentUrl(values[0], values[1], this.props.experiment.id);
    let group = null;
    if (!_.isNil(experiment.experiment_group_name)) {
      group = parseInt(splitGroupName(experiment.experiment_group_name)[2], 10);
    }
    let breadcrumbLinks = [
      {name: values[0], value: getUserUrl(values[0])},
      {name: values[1], value: getProjectUrl(values[0], values[1])},
      {name: `Experiment ${experiment.id}`}];
    if (group) {
      breadcrumbLinks.splice(
        2,
        0,
        {name: `Group ${group}`, value: getGroupUrl(values[0], values[1], group)});
    }
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb icon="fa-cube" links={breadcrumbLinks}/>
            <LinkedTab
              baseUrl={exerimentUrl}
              tabs={[
                {
                  title: 'Overview',
                  component: <ExperimentOverview experiment={experiment}/>,
                  relUrl: ''
                }, {
                  title: 'Logs',
                  component: <Logs fetchData={() => null} logs={''} user={experiment.user} experiment={experiment}/>,
                  relUrl: 'groups'
                }, {
                  title: 'Jobs',
                  component: <ExperimentJobs fetchData={() => null} user={experiment.user} experiment={experiment}/>,
                  relUrl: 'jobs'
                }
              ]}
            />
          </div>
        </div>
      </div>
    );
  }
}
