import * as React from 'react';

import './codeTable.less';

export interface Props {
  lines: string[];
}

function CodeTable({lines}: Props) {
  return (
    <div className="code-table">
      <table className="table table-hover table-responsive">
        <tbody>
        {lines && lines.map((line, idx) =>
          <tr key={`${idx}-${line}`}>
            <th className="line-number">
              {idx + 1}
            </th>
            <td className="line-code">
              {line}
            </td>
          </tr>
        )}
        </tbody>
      </table>
    </div>
  );
}

export default CodeTable;
