import * as React from 'react';

import * as ReactDataGrid from 'react-data-grid';

import './gridList.less';

export interface Props {
  columns?: { key: string; name: string; }[];
  rows: { [key: string]: any; }[];
}

function GridList({columns, rows}: Props) {
  if (!columns) {
    columns = [];
    for (let row of rows) {
      let rowColumns = Object.keys(row).map(v => ({key: v, name: v}));
      columns.push(...rowColumns);
    }
  }
  return (
    <div className="grid-list">
      <ReactDataGrid
        columns={columns}
        rowGetter={i => rows[i]}
        rowsCount={rows.length}
        minHeight={35 * rows.length + 35}
      />
    </div>
  );
}

export default GridList;
