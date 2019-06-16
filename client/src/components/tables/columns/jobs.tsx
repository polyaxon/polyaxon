import * as React from 'react';
import { Link } from 'react-router-dom';

import { ColumnInterface } from '../../../interfaces/tableColumns';
import { JobModel } from '../../../models/job';
import { getJobUrl, splitUniqueName } from '../../../urls/utils';
import { getBaseGlobalRunColumnOptions, getBaseRunColumnOptions } from './base';
import { FILTER_EXAMPLES } from './examples';

const getExtraColumns = (): { [key: string]: ColumnInterface } => {
  return {
    name: {
      name: 'Name',
      field: 'name',
      type: 'value',
      desc: FILTER_EXAMPLES.str('name'),
      sort: true,
      icon: 'fas fa-tasks',
      render: (text: any, experiment: JobModel) => {
        const values = splitUniqueName(experiment.project);
        return (
          <Link className="title" to={getJobUrl(values[0], values[1], experiment.id)}>
            <i className="fas fa-tasks icon" aria-hidden="true"/> {experiment.name || experiment.unique_name}
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
    buildId: {
      field: 'build.id',
      type: 'value',
      sort: true,
      desc: FILTER_EXAMPLES.id('build.id'),
      icon: 'fas fa-gavel',
    },
    buildName: {
      name: 'Build',
      field: 'build.name',
      type: 'value',
      sort: true,
      desc: FILTER_EXAMPLES.name('build.name'),
      icon: 'fas fa-gavel',
      dataIndex: 'build_job',
    },
  };
};

export const getJobColumnOptions = (): { [key: string]: ColumnInterface } => {
  return {
    ...getBaseRunColumnOptions(),
    ...getExtraColumns()
  };
};

export const getJobGlobalColumnOptions = (): { [key: string]: ColumnInterface } => {
  return {
    ...getBaseGlobalRunColumnOptions(),
    ...getExtraColumns()
  };
};
