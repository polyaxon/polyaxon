import * as React from 'react';
import { Link } from 'react-router-dom';

import { ColumnInterface } from '../../../interfaces/tableColumns';
import { ExperimentModel } from '../../../models/experiment';
import { getExperimentUrl, splitUniqueName } from '../../../urls/utils';
import { getBaseGlobalRunColumnOptions, getBaseRunColumnOptions } from './base';
import { FILTER_EXAMPLES } from './examples';

export const getParamColumn = (field: string) => {
  return {
    name: field,
    field: `params.${field}`,
    type: 'value',
    desc: 'params.activation: sigmoid or params.activation: sigmoid|relu',
    sort: true,
    icon: 'fas fa-cog',
    dataIndex: `params.${field}`,
  };
};

export const getMetricColumn = (field: string) => {
  return {
    name: field,
    field: `metrics.${field}`,
    type: 'scalar',
    desc: FILTER_EXAMPLES.scalar('metrics.loss'),
    sort: true,
    icon: 'fas fa-chart-area',
    dataIndex: `last_metric.${field}`,
  };
};

const getExtraColumnOptions = (): { [key: string]: ColumnInterface } => {
  return {
    name: {
      name: 'Name',
      field: 'name',
      type: 'value',
      desc: FILTER_EXAMPLES.str('name'),
      sort: true,
      icon: 'fas fa-cube',
      render: (text: any, experiment: ExperimentModel) => {
        const values = splitUniqueName(experiment.project);
        return (
          <Link className="title" to={getExperimentUrl(values[0], values[1], experiment.id)}>
            <i className="fas fa-cube icon" aria-hidden="true"/> {experiment.name || experiment.unique_name}
          </Link>);
      }
    },
    description: {
      name: 'Description',
      field: 'description',
      type: 'value',
      desc: FILTER_EXAMPLES.str('description'),
      sort: false,
      icon: 'fas fa-info',
    },
    params: {
      name: 'Params',
      field: `params.*`,
      type: 'scalar',
      desc: 'params.activation: sigmoid or params.activation: sigmoid|relu',
      sort: true,
      icon: 'fas fa-cog',
      dataIndex: `params.*`,
    },
    metrics: {
      name: 'Metrics',
      field: `metrics.*`,
      type: 'scalar',
      desc: FILTER_EXAMPLES.scalar('metrics.loss'),
      sort: true,
      icon: 'fas fa-chart-area',
      dataIndex: `metrics.*`,
    },
    groupId: {
      field: 'group.id',
      type: 'value',
      desc: FILTER_EXAMPLES.id('group.id'),
      sort: false,
      icon: 'fas fa-cubes',
    },
    groupName: {
      name: 'Group',
      field: 'group.name',
      type: 'value',
      desc: FILTER_EXAMPLES.name('group.name'),
      sort: true,
      icon: 'fas fa-cubes',
      dataIndex: 'experiment_group',
    }
  };
};

export const getExperimentColumnOptions = (): { [key: string]: ColumnInterface } => {
  return {
    ...getBaseRunColumnOptions(),
    ...getExtraColumnOptions()
  };
};

export const getGlobalExperimentColumnOptions = (): { [key: string]: ColumnInterface } => {
  return {
    ...getBaseGlobalRunColumnOptions(),
    ...getExtraColumnOptions()
  };
};

const getAllExtraColumnOptions = (): { [key: string]: ColumnInterface } => {
  return {
    independent: {
      field: 'independent',
      type: 'bool',
      desc: 'independent: true, default is false',
      sort: true,
      icon: 'fas fa-minus'
    }
  };
};

export const getExperimentAllColumnOptions = (): { [key: string]: ColumnInterface } => {
  return {
    ...getExperimentColumnOptions(),
    ...getAllExtraColumnOptions()
  };
};

export const getGlobalExperimentAllColumnOptions = (): { [key: string]: ColumnInterface } => {
  return {
    ...getGlobalExperimentColumnOptions(),
    ...getAllExtraColumnOptions()
  };
};
