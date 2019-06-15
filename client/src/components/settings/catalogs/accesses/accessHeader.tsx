import * as React from 'react';

function AccessHeader() {
  return (
    <tr className="list-header">
      <th className="block">
        Info
      </th>
      <th className="block">
        Host info
      </th>
      <th className="block pull-right">
        Actions
      </th>
    </tr>
  );
}

export default AccessHeader;
