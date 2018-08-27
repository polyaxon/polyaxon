import * as React from 'react';

import './paginatedTable.less';

export interface Props {
  values: { [key: string]: string | number; };
}

function GridTable({values}: Props) {
  const columnValues: string[] = [];
  Object.keys(values)
    .filter((v: string) => columnValues.indexOf(v) === -1)
    .map((v: string) => columnValues.push(v));
  return (
    <div className="grid-table">
      <table className="table table-hover table-responsive">
        <tbody>
        <tr className="list-header">
          {columnValues && columnValues.map((col) =>
            <th className="block" key={col}>
              {col}
            </th>
          )}
        </tr>
        <tr className="list-item">
          {columnValues && columnValues.map((col: string) =>
            <td className="block" key={col}>
              {values[col]}
            </td>
          )}
        </tr>
        </tbody>
      </table>
    </div>
  );
}

export default GridTable;
