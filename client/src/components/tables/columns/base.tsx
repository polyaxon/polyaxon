import * as React from 'react';

import { ColumnInterface } from '../../../interfaces/tableColumns';
import DateMetaInfo from '../../metaInfo/dateMetaInfo';
import TaskRunMetaInfo from '../../metaInfo/taskRunMetaInfo';
import Status from '../../statuses/status';
import { FILTER_EXAMPLES } from './examples';

export const getBaseColumnOptions = (): { [key: string]: ColumnInterface } => {
  return {
    id: {
      name: 'Id',
      field: 'id',
      type: 'value',
      desc: FILTER_EXAMPLES.id('id'),
      sort: true,
      icon: 'fas fa-circle',
      dataIndex: 'id',
    },
    createdAt: {
      name: 'Create At',
      field: 'created_at',
      type: 'datetime',
      desc: FILTER_EXAMPLES.datetime('created_at'),
      sort: true,
      icon: 'far fa-clock',
      dataIndex: 'created_at',
      render: (datetime: Date | string) => <DateMetaInfo datetime={datetime}/>,
    },
    updatedAt: {
      name: 'Update At',
      field: 'updated_at',
      type: 'datetime',
      desc: FILTER_EXAMPLES.datetime('updated_at'),
      sort: true,
      icon: 'far fa-clock',
      dataIndex: 'updated_at',
      render: (datetime: Date | string) => <DateMetaInfo datetime={datetime}/>,
    },
    startedAt: {
      name: 'Started At',
      field: 'started_at',
      type: 'datetime',
      desc: FILTER_EXAMPLES.datetime('started_at'),
      sort: true,
      icon: 'far fa-clock',
      dataIndex: 'started_at',
      render: (datetime: Date | string) => <DateMetaInfo datetime={datetime}/>,
    },
    finishedAt: {
      name: 'Finished At',
      field: 'finished_at',
      type: 'datetime',
      desc: FILTER_EXAMPLES.datetime('finished_at'),
      sort: true,
      icon: 'far fa-clock',
      dataIndex: 'finished_at',
      render: (datetime: Date | string) => <DateMetaInfo datetime={datetime}/>,
    },
    tags: {
      name: 'Tags',
      field: 'tags',
      type: 'value',
      desc: 'tags: value1 or tags: value1|value2|value3 or tags: ~value1|value2',
      sort: false,
      icon: 'fas fa-tags',
      dataIndex: 'tags',
    },
    userId: {
      field: 'user.id',
      type: 'value',
      desc: FILTER_EXAMPLES.id('user.id'),
      sort: false,
      icon: 'far fa-user',
    },
    username: {
      name: 'User',
      field: 'user.username',
      type: 'value',
      desc: FILTER_EXAMPLES.name('user.username'),
      sort: true,
      icon: 'far fa-user',
      dataIndex: 'user',
    }
  };
};

export const getBaseRunColumnOptions = (): { [key: string]: ColumnInterface } => {
  return {
    ...getBaseColumnOptions(),
    ...{
      status: {
        name: 'Status',
        field: 'status',
        type: 'value',
        desc: 'status: running or status: succeeded|failed or status: ~started|building',
        sort: true,
        icon: 'fas fa-minus',
        dataIndex: 'last_status',
        render: (status: string) => <Status status={status}/>,
        fixed: true,
        width: 10
      },
      backend: {
        name: 'Backend',
        field: 'backend',
        type: 'value',
        desc: 'backend: native or backend: ~native or status: native|other',
        sort: true,
        icon: 'fas fa-brush',
        dataIndex: 'backend',
      },
      // run: {
      //   name: 'Run',
      //   field: 'run',
      //   type: 'value',
      //   desc: '',
      //   sort: false,
      //   icon: 'far fa-clock',
      //   render: (entity: any) => <TaskRunMetaInfo startedAt={entity.started_at} finishedAt={entity.finished_at}/>,
      // }
    }
  };
};

export const getBaseGlobalRunColumnOptions = (): { [key: string]: ColumnInterface } => {
  return {
    ...getBaseRunColumnOptions(),
    ...{
      projectId: {
        field: 'project.id',
        type: 'value',
        desc: FILTER_EXAMPLES.datetime('created_at'),
        sort: false,
        icon: 'fas fa-server',
        width: 10,
      },
      projectName: {
        name: 'Project',
        field: 'project.name',
        type: 'value',
        desc: FILTER_EXAMPLES.name('project.name'),
        sort: true,
        icon: 'fas fa-server',
        dataIndex: 'project',
      }
    }
  };
};

export const getColumnFilters = (columnOptions: { [key: string]: ColumnInterface }): ColumnInterface[] => {
  return Object.keys(columnOptions).map((colName: string) => columnOptions[colName]);
};

export const getColumnSorters = (columnOptions: { [key: string]: ColumnInterface }): string[] => {
  return Object.keys(columnOptions).map((colName: string) => columnOptions[colName].field);
};

export const getTableColumns = (columnOptions: { [key: string]: ColumnInterface }, columnNames: string[]) => {
  return columnNames.filter((colName: string) => columnOptions[colName].name).map((colName: string) => {
    const col = columnOptions[colName];
    return {
      title: col.name,
      dataIndex: col.dataIndex,
      render: col.render,
      width: col.width,
      fixed: col.fixed
    };
  });
};
