import * as React from 'react';

function JobHeader() {
  return (
    <tr className="list-header">
      <th className="block">
        Status
      </th>
      <th className="block">
        Name
      </th>
      <th className="block">
        Info
      </th>
      <th className="block">
        Run
      </th>
      <th className="block">
        Actions
      </th>
    </tr>
  );
}

export default JobHeader;
