import * as React from 'react';

function K8SResourceHeader() {
  return (
    <tr className="list-header">
      <th className="block">
        Info
      </th>
      <th className="block">
        K8S Ref
      </th>
      <th className="block pull-right">
        Actions
      </th>
    </tr>
  );
}

export default K8SResourceHeader;
