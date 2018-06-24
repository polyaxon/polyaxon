import * as React from 'react';

import * as ReactDataGrid from 'react-data-grid';

import './gridList.less';

export interface Props {
  columns?: { key: string; name: string; }[];
  rows: { [key: string]: any; }[];
}

function GridList({columns, rows}: Props) {
  if (!columns) {
    let columnValues: string[] = [];
    for (let row of rows) {
      Object.keys(row)
        .filter(v => columnValues.indexOf(v) === -1)
        .map(v => columnValues.push(v));
    }
    columns = columnValues.map(v => ({key: v, name: v}));
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
