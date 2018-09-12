import * as _ from 'lodash';
import * as React from 'react';

import './paginatedTable.less';

export interface Props {
  values: { [key: string]: string | number | boolean; };
}

function VerticalTable({values}: Props) {
  const columnValues: string[] = [];
  Object.keys(values).sort()
    .filter((v: string) => columnValues.indexOf(v) === -1)
    .map((v: string) => columnValues.push(v));
  return (
    <div className="vertical-table">
      <table className="table table-hover table-responsive">
        <tbody>
        {columnValues && columnValues.map((col) =>
          <tr key={col}>
            <th className="list-header block">
              {col}
            </th>
            <td className="list-item block">
              {!_.isNil(values[col])  && values[col] + ''}
            </td>
          </tr>
        )}
        </tbody>
      </table>
    </div>
  );
}

export default VerticalTable;
