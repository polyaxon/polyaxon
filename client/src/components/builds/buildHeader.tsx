import * as React from 'react';

function BuildHeader() {
  return (
    <tr className="list-header">
      <th className="block">
        Status
      </th>
      <th className="block">
        Name
      </th>
      <th className="block">
        Run
      </th>
      <th className="block pull-right">
        Actions
      </th>
    </tr>
  );
}

export default BuildHeader;
