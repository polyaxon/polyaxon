import * as React from 'react';

export interface Props {
  pullRight: boolean;
  url: string;
  name: string;
}

function Download({url, name, pullRight}: Props) {
  const download = (
    <span>
      <a
        className="btn btn-sm btn-default"
        href={url}
        download={name}
      >
        <i className="fa fa-cloud-download icon" aria-hidden="true"/> Download
      </a>
    </span>
  );

  if (pullRight) {
    return (
    <div className="pull-right button-refresh">
      {download}
    </div>
    );
  }
  return download;
}

export default Download;
