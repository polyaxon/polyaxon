import * as React from 'react';

function ProjectHeader() {
  return (
    <tr className="list-header">
      <th className="block">
        Name
      </th>
      <th className="block">
        Info
      </th>
      <th className="block pull-right">
        Actions
      </th>
    </tr>
  );
}

export default ProjectHeader;
