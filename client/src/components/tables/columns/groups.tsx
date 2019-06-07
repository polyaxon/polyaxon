import * as React from 'react';
import { Link } from 'react-router-dom';

import { getGroupUrl, splitUniqueName } from '../../../constants/utils';
import { ColumnInterface } from '../../../interfaces/tableColumns';
import { GroupModel } from '../../../models/group';
import { getBaseGlobalRunColumnOptions, getBaseRunColumnOptions } from './base';
import { FILTER_EXAMPLES } from './examples';

const getExtraColumns =  (): { [key: string]: ColumnInterface } => {
  return {
    name: {
      name: 'Name',
      field: 'name',
      type: 'value',
      desc: FILTER_EXAMPLES.name('name'),
      sort: true,
      icon: 'fas fa-cubes',
      dataIndex: 'unique_name',
      render: (text: any, experiment: GroupModel) => {
        const values = splitUniqueName(experiment.project);
        return (
          <Link className="title" to={getGroupUrl(values[0], values[1], experiment.id)}>
            <i className="fas fa-cubes icon" aria-hidden="true"/> {experiment.name || experiment.unique_name}
          </Link>);
      }
    },
    searchAlgorithm: {
      name: 'Algorithm',
      field: 'search_algorithm',
      type: 'value',
      desc: 'search_algorithm: bo or search_algorithm: random|hyperband',
      sort: true,
      icon: 'fas fa-asterisk',
      dataIndex: 'search_algorithm',
    },
    concurrency: {
      name: 'Concurrency',
      field: 'concurrency',
      type: 'scalar',
      desc: FILTER_EXAMPLES.int('concurrency'),
      sort: true,
      icon: 'fas fa-grip-lines-vertical',
      dataIndex: 'concurrency',
    },
    groupType: {
      name: 'Type',
      field: 'group_type',
      type: 'value',
      desc: 'group_type: study or group_type: selection',
      sort: true,
      icon: 'fas fa-grip-lines-vertical',
      dataIndex: 'group_type',
    }
  };
};

export const getGroupColumnOptions = (): { [key: string]: ColumnInterface } => {
  return {
    ...getBaseRunColumnOptions(),
    ...getExtraColumns()
  };
};

export const getGroupGlobalColumnOptions = (): { [key: string]: ColumnInterface } => {
  return {
    ...getBaseGlobalRunColumnOptions(),
    ...getExtraColumns()
  };
};
